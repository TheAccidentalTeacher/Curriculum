#!/usr/bin/env python3
"""
Content Populator for Proper Curriculum
Fills the clean module structure with actual extracted content from PDFs
"""

import json
import os
import re
from pathlib import Path

def load_extracted_content():
    """Load all extracted content from chunk processing files"""
    
    all_content = {}
    
    # Load from chunk processing results which have PDF-specific content
    chunk_files = [
        "/workspaces/Curriculum/chunk1_complete_pipeline_results.json",
        "/workspaces/Curriculum/chunk2_complete_pipeline_results.json", 
        "/workspaces/Curriculum/chunk3_final_complete_pipeline_results.json"
    ]
    
    for file_path in chunk_files:
        if os.path.exists(file_path):
            try:
                print(f"📖 Loading content from {os.path.basename(file_path)}...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'extracted_content' in data:
                        extracted = data['extracted_content']
                        all_content.update(extracted)
                        print(f"✅ Loaded {len(extracted)} PDF content sections")
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
    
    # Also load US Teacher Guide content
    us_file = "/workspaces/Curriculum/us_teacher_guide_extracted_content.json"
    if os.path.exists(us_file):
        try:
            print(f"📖 Loading US Teacher Guide content...")
            with open(us_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'lessons' in data:
                    all_content['The United States'] = data
                    print(f"✅ Loaded US Teacher Guide content")
        except Exception as e:
            print(f"❌ Error loading US content: {e}")
    
    print(f"📚 Total content sections loaded: {len(all_content)}")
    return all_content

def normalize_title_for_matching(title):
    """Normalize title for matching between PDFs and content"""
    
    # Remove common prefixes/suffixes
    normalized = title.lower()
    normalized = re.sub(r'\s*teacher\s*guide\s*pdf?\s*', '', normalized)
    normalized = re.sub(r'\s*compressed[_\s]*', '', normalized)
    normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

def find_content_for_module(module_title, all_content):
    """Find extracted content that matches a module"""
    
    normalized_module = normalize_title_for_matching(module_title)
    
    # Try various matching strategies
    matching_content = []
    
    for content_key, content_data in all_content.items():
        normalized_key = normalize_title_for_matching(content_key)
        
        # Direct match
        if normalized_module in normalized_key or normalized_key in normalized_module:
            matching_content.append((content_key, content_data))
        
        # Word-based matching
        module_words = set(normalized_module.split())
        key_words = set(normalized_key.split())
        
        if len(module_words.intersection(key_words)) >= 2:  # At least 2 words match
            matching_content.append((content_key, content_data))
    
    return matching_content

def extract_lessons_from_content(content_data):
    """Extract individual lessons from content data"""
    
    lessons = []
    
    if isinstance(content_data, dict):
        # Check for direct lessons array
        if 'lessons' in content_data:
            lessons_data = content_data['lessons']
            if isinstance(lessons_data, list):
                for i, lesson in enumerate(lessons_data, 1):
                    if isinstance(lesson, dict):
                        lessons.append({
                            'lesson_number': i,
                            'title': lesson.get('title', f'Lesson {i}'),
                            'content': lesson.get('content', ''),
                            'objectives': lesson.get('objectives', []),
                            'activities': lesson.get('activities', []),
                            'materials': lesson.get('materials', []),
                            'duration': lesson.get('duration', '45 minutes')
                        })
        
        # Check for lesson content in other formats
        elif 'content' in content_data:
            content_text = content_data['content']
            if isinstance(content_text, str):
                # Try to split content into lessons
                lesson_chunks = split_content_into_lessons(content_text)
                for i, chunk in enumerate(lesson_chunks, 1):
                    lessons.append({
                        'lesson_number': i,
                        'title': extract_lesson_title(chunk, i),
                        'content': chunk,
                        'objectives': extract_objectives_from_text(chunk),
                        'activities': extract_activities_from_text(chunk),
                        'materials': [],
                        'duration': '45 minutes'
                    })
        
        # Check for extracted lessons in comprehensive format
        elif 'extracted_lessons' in content_data:
            extracted = content_data['extracted_lessons']
            if isinstance(extracted, list):
                for i, lesson in enumerate(extracted, 1):
                    lessons.append({
                        'lesson_number': i,
                        'title': lesson.get('lesson_title', f'Lesson {i}'),
                        'content': lesson.get('lesson_content', ''),
                        'objectives': lesson.get('objectives', []),
                        'activities': lesson.get('activities', []),
                        'materials': lesson.get('materials', []),
                        'duration': lesson.get('duration', '45 minutes')
                    })
    
    elif isinstance(content_data, str):
        # If content is just a string, split it into lessons
        lesson_chunks = split_content_into_lessons(content_data)
        for i, chunk in enumerate(lesson_chunks, 1):
            lessons.append({
                'lesson_number': i,
                'title': extract_lesson_title(chunk, i),
                'content': chunk,
                'objectives': extract_objectives_from_text(chunk),
                'activities': extract_activities_from_text(chunk),
                'materials': [],
                'duration': '45 minutes'
            })
    
    return lessons[:8]  # Limit to 8 lessons per module

def split_content_into_lessons(content_text):
    """Split content text into individual lessons"""
    
    # Try to find lesson boundaries
    lesson_patterns = [
        r'(?:^|\n)\s*(?:Lesson|LESSON)\s+(\d+)',
        r'(?:^|\n)\s*(\d+)\.\s*[A-Z]',
        r'(?:^|\n)\s*Chapter\s+(\d+)',
        r'(?:^|\n)\s*Section\s+(\d+)',
    ]
    
    chunks = []
    
    for pattern in lesson_patterns:
        matches = list(re.finditer(pattern, content_text, re.MULTILINE | re.IGNORECASE))
        if len(matches) >= 2:  # Found multiple lessons
            for i in range(len(matches)):
                start = matches[i].start()
                end = matches[i+1].start() if i+1 < len(matches) else len(content_text)
                chunk = content_text[start:end].strip()
                if len(chunk) > 100:  # Reasonable lesson length
                    chunks.append(chunk)
            break
    
    # If no lesson boundaries found, split by paragraphs
    if not chunks:
        paragraphs = content_text.split('\n\n')
        chunk_size = max(1, len(paragraphs) // 6)  # Aim for 6 lessons
        for i in range(0, len(paragraphs), chunk_size):
            chunk = '\n\n'.join(paragraphs[i:i+chunk_size])
            if len(chunk.strip()) > 50:
                chunks.append(chunk.strip())
    
    return chunks[:8]  # Limit chunks

def extract_lesson_title(content_chunk, default_number):
    """Extract lesson title from content chunk"""
    
    # Try to find title patterns
    title_patterns = [
        r'(?:^|\n)\s*(?:Lesson|LESSON)\s+\d+[:\s]*([^\n]+)',
        r'(?:^|\n)\s*\d+\.\s*([A-Z][^\n]+)',
        r'(?:^|\n)\s*([A-Z][A-Za-z\s]{10,50})\s*(?:\n|$)',
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, content_chunk[:200], re.MULTILINE)
        if match:
            title = match.group(1).strip()
            if 5 <= len(title) <= 60:  # Reasonable title length
                return title
    
    # Extract first meaningful sentence
    sentences = re.split(r'[.!?]\s+', content_chunk[:300])
    for sentence in sentences:
        sentence = sentence.strip()
        if 10 <= len(sentence) <= 80 and not sentence.lower().startswith('lesson'):
            return sentence
    
    return f"Lesson {default_number}"

def extract_objectives_from_text(text):
    """Extract learning objectives from text"""
    
    objectives = []
    
    # Look for objective patterns
    objective_patterns = [
        r'(?:objective|goal|aim)s?[:\s]*([^\n]+)',
        r'(?:students? will|learners? will)[:\s]*([^\n]+)',
        r'(?:by the end|after this lesson)[^\n]*students?[^\n]*([^\n]+)',
    ]
    
    for pattern in objective_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            obj = match.strip()
            if 10 <= len(obj) <= 200:
                objectives.append(obj)
    
    # If no objectives found, create generic ones
    if not objectives:
        objectives = [
            "Understand key concepts and vocabulary",
            "Analyze geographic patterns and relationships", 
            "Apply knowledge to real-world scenarios"
        ]
    
    return objectives[:5]  # Limit to 5 objectives

def extract_activities_from_text(text):
    """Extract activities from text"""
    
    activities = []
    
    # Look for activity patterns
    activity_patterns = [
        r'(?:activity|exercise|task|assignment)[:\s]*([^\n]+)',
        r'(?:have students|students will|class will)[:\s]*([^\n]+)',
        r'(?:discussion|debate|project|research)[:\s]*([^\n]+)',
    ]
    
    for pattern in activity_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            activity = match.strip()
            if 10 <= len(activity) <= 200:
                activities.append(activity)
    
    # If no activities found, create generic ones
    if not activities:
        activities = [
            "Class discussion on key concepts",
            "Map analysis activity",
            "Reading comprehension exercise",
            "Group research project"
        ]
    
    return activities[:6]  # Limit to 6 activities

def populate_modules_with_content():
    """Populate the clean modules with actual content"""
    
    print("🔍 Loading extracted content...")
    all_content = load_extracted_content()
    
    print("📝 Populating modules with content...")
    
    modules_dir = "/workspaces/Curriculum/modules"
    updated_count = 0
    
    for module_dir in sorted(os.listdir(modules_dir)):
        module_path = os.path.join(modules_dir, module_dir)
        if not os.path.isdir(module_path):
            continue
        
        # Load existing module info
        module_info_path = os.path.join(module_path, 'module_info.json')
        if not os.path.exists(module_info_path):
            continue
        
        with open(module_info_path, 'r', encoding='utf-8') as f:
            module_info = json.load(f)
        
        # Find matching content
        matching_content = find_content_for_module(module_info['title'], all_content)
        
        if matching_content:
            print(f"📚 Processing Module {module_info['module_number']:02d}: {module_info['title']}")
            
            # Combine content from all matches
            all_lessons = []
            for content_key, content_data in matching_content:
                lessons = extract_lessons_from_content(content_data)
                all_lessons.extend(lessons)
            
            # Update module info with lessons
            if all_lessons:
                module_info['lessons'] = all_lessons[:8]  # Limit to 8 lessons
                
                # Save updated module info
                with open(module_info_path, 'w', encoding='utf-8') as f:
                    json.dump(module_info, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Added {len(module_info['lessons'])} lessons to Module {module_info['module_number']:02d}")
                updated_count += 1
            else:
                print(f"⚠️  No lessons extracted for Module {module_info['module_number']:02d}")
        else:
            print(f"❌ No matching content found for Module {module_info['module_number']:02d}: {module_info['title']}")
    
    print(f"\n🎉 Updated {updated_count} modules with content!")
    return updated_count

if __name__ == "__main__":
    print("🚀 Starting Content Population...")
    print("=" * 60)
    
    updated_count = populate_modules_with_content()
    
    print("\n" + "=" * 60)
    print(f"✅ CONTENT POPULATION COMPLETE!")
    print(f"📚 {updated_count} modules populated with lessons")
    print("🎯 Ready to rebuild clean HTML lessons with actual content")
