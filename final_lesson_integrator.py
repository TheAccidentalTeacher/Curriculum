#!/usr/bin/env python3
"""
Final Lesson Integration System
Takes extracted PDF content and integrates it into existing lesson HTML files
"""

import json
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

def integrate_real_content():
    """Integrate real extracted content into lesson files"""
    
    # Use our best extracted content as the source
    content_file = Path("/workspaces/Curriculum/best_extracted_content.json")
    
    if not content_file.exists():
        print("❌ No extracted content found")
        return
    
    with open(content_file, 'r', encoding='utf-8') as f:
        pdf_content = json.load(f)
    
    print(f"🔗 Final Lesson Integration System")
    print(f"=" * 50)
    print(f"📚 Source: {pdf_content['title']}")
    print(f"📖 Lessons available: {pdf_content['lessons_found']}")
    
    # Find corresponding lesson files in our curriculum
    units_dir = Path("/workspaces/Curriculum/units")
    updated_files = 0
    
    for lesson_data in pdf_content['lessons']:
        print(f"\n🎯 Processing lesson: {lesson_data['title'][:60]}...")
        
        # Try to find matching lesson files
        matching_files = find_matching_lesson_files(units_dir, lesson_data)
        
        for lesson_file in matching_files:
            try:
                updated_content = enhance_lesson_with_real_content(lesson_file, lesson_data)
                if updated_content:
                    with open(lesson_file, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    updated_files += 1
                    print(f"   ✅ Updated: {lesson_file.name}")
            except Exception as e:
                print(f"   ❌ Error updating {lesson_file.name}: {e}")
    
    print(f"\n📊 Integration Summary:")
    print(f"   Files updated: {updated_files}")
    print(f"   Content source: Real teacher guide PDFs")
    print(f"   Integration method: Structured content insertion")

def find_matching_lesson_files(units_dir, lesson_data):
    """Find lesson files that might match this PDF content"""
    matching_files = []
    
    # Extract keywords from lesson title
    title = lesson_data['title'].lower()
    keywords = extract_keywords_from_title(title)
    
    # Search through all lesson files
    for lesson_file in units_dir.glob("**/lessons/*.html"):
        if matches_lesson_content(lesson_file, keywords):
            matching_files.append(lesson_file)
    
    return matching_files[:3]  # Limit to top 3 matches

def extract_keywords_from_title(title):
    """Extract meaningful keywords from lesson title"""
    # Remove common lesson formatting
    title = re.sub(r'lesson\s+\d+[:\-\s]*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\.{3,}', '', title)  # Remove ellipses
    title = re.sub(r'\d+', '', title)     # Remove numbers
    
    # Extract meaningful words
    keywords = [word.strip() for word in title.split() 
                if len(word.strip()) > 2 and word.strip().lower() not in 
                ['the', 'and', 'for', 'with', 'from', 'page']]
    
    return keywords[:5]  # Top 5 keywords

def matches_lesson_content(lesson_file, keywords):
    """Check if lesson file content matches keywords"""
    try:
        with open(lesson_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # Check for keyword matches in title, content, or filename
        filename = lesson_file.name.lower()
        matches = sum(1 for keyword in keywords 
                     if keyword.lower() in content or keyword.lower() in filename)
        
        return matches >= 2  # Require at least 2 keyword matches
    except:
        return False

def enhance_lesson_with_real_content(lesson_file, lesson_data):
    """Enhance a lesson file with real PDF content"""
    try:
        with open(lesson_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find or create main content area
        main_content = soup.find('main') or soup.find('div', class_='content')
        if not main_content:
            # Create main content area
            main_content = soup.new_tag('main')
            soup.body.append(main_content)
        
        # Add real teaching content
        add_real_teaching_content(soup, main_content, lesson_data)
        
        return str(soup)
        
    except Exception as e:
        print(f"      Error enhancing {lesson_file.name}: {e}")
        return None

def add_real_teaching_content(soup, main_content, lesson_data):
    """Add real teaching content from PDF to lesson"""
    
    # Create lesson header with real title
    lesson_header = soup.new_tag('div', class_='lesson-header')
    title_tag = soup.new_tag('h1')
    title_tag.string = clean_lesson_title(lesson_data['title'])
    lesson_header.append(title_tag)
    main_content.insert(0, lesson_header)
    
    # Add teaching materials if available
    if lesson_data['materials']:
        materials_section = create_content_section(soup, "Materials & Resources", lesson_data['materials'][:5])
        main_content.append(materials_section)
    
    # Add assessment content if available
    if lesson_data['assessment']:
        assessment_section = create_content_section(soup, "Assessment & Evaluation", lesson_data['assessment'][:5])
        main_content.append(assessment_section)
    
    # Add vocabulary if available
    if lesson_data['vocabulary']:
        vocab_section = create_content_section(soup, "Key Vocabulary", lesson_data['vocabulary'][:10])
        main_content.append(vocab_section)
    
    # Add sample content from full lesson
    if lesson_data['full_content']:
        sample_content = extract_sample_teaching_content(lesson_data['full_content'])
        if sample_content:
            content_section = create_content_section(soup, "Teaching Content", sample_content)
            main_content.append(content_section)

def clean_lesson_title(title):
    """Clean up lesson title for display"""
    # Remove page numbers and formatting
    title = re.sub(r'\.{3,}.*', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def create_content_section(soup, section_title, content_items):
    """Create a content section with real materials"""
    section = soup.new_tag('div', class_='content-section')
    
    # Section header
    header = soup.new_tag('h3')
    header.string = section_title
    section.append(header)
    
    # Content list
    content_list = soup.new_tag('ul', class_='content-list')
    
    for item in content_items:
        if isinstance(item, str) and len(item.strip()) > 10:
            li = soup.new_tag('li')
            li.string = item.strip()[:200] + ("..." if len(item.strip()) > 200 else "")
            content_list.append(li)
    
    section.append(content_list)
    return section

def extract_sample_teaching_content(full_content):
    """Extract meaningful teaching content from full lesson text"""
    teaching_lines = []
    
    for line in full_content:
        # Look for lines that contain teaching instructions or activities
        if any(keyword in line.lower() for keyword in 
               ['students', 'teach', 'activity', 'discuss', 'explain', 'review', 'practice']):
            if len(line.strip()) > 30:  # Substantial content
                teaching_lines.append(line.strip())
                if len(teaching_lines) >= 5:  # Limit to 5 items
                    break
    
    return teaching_lines

def test_integration():
    """Test the integration system"""
    print("🧪 Testing Real Content Integration")
    print("=" * 50)
    
    # Check if we have our best content
    content_file = Path("/workspaces/Curriculum/best_extracted_content.json")
    if content_file.exists():
        integrate_real_content()
    else:
        print("❌ Need to run PDF extraction first")
        print("📝 Run: python test_multiple_pdfs.py")

if __name__ == "__main__":
    test_integration()
