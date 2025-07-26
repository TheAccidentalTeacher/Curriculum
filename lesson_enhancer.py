import json
import os
import re
from pathlib import Path

def load_extracted_content():
    """Load the most recent extracted content."""
    with open('/workspaces/Curriculum/progress_batch_15.json', 'r') as f:
        return json.load(f)

def identify_geography_content(content):
    """Identify geography-related content from extracted PDFs."""
    geography_terms = ['geographer', 'world', 'africa', 'asia', 'europe', 'america', 'china', 'india', 
                      'east', 'west', 'south', 'north', 'continent', 'ocean', 'climate', 'region']
    
    geography_content = {}
    
    for filename, data in content.items():
        title = data['title'].lower()
        if any(geo_term in title for geo_term in geography_terms) or 'geography' in title:
            geography_content[filename] = data
            
    return geography_content

def find_lesson_files():
    """Find existing lesson files that need enhancement."""
    lesson_files = []
    
    # Look in units/lessons directory
    units_dir = Path('/workspaces/Curriculum/units')
    if units_dir.exists():
        for lesson_file in units_dir.rglob('*.html'):
            lesson_files.append(lesson_file)
    
    return lesson_files

def extract_relevant_content(geography_data, lesson_title):
    """Extract content relevant to a specific lesson."""
    lesson_title_lower = lesson_title.lower()
    relevant_content = {
        'lessons': [],
        'objectives': [],
        'activities': [],
        'materials': [],
        'assessments': []
    }
    
    # Score content based on relevance
    for pdf_name, pdf_data in geography_data.items():
        pdf_title_lower = pdf_data['title'].lower()
        
        # Check if PDF is relevant to lesson
        relevance_score = 0
        for word in lesson_title_lower.split():
            if word in pdf_title_lower:
                relevance_score += 1
        
        if relevance_score > 0 or 'geographer' in pdf_title_lower:
            # Add relevant content
            relevant_content['lessons'].extend(pdf_data['lessons'][:2])  # Top 2 lessons
            relevant_content['objectives'].extend(pdf_data['objectives'][:5])  # Top 5 objectives
            relevant_content['activities'].extend(pdf_data['activities'][:10])  # Top 10 activities
            relevant_content['materials'].extend(pdf_data['materials'][:3])  # Top 3 materials
            relevant_content['assessments'].extend(pdf_data['assessments'][:3])  # Top 3 assessments
    
    return relevant_content

def create_enhanced_lesson_content(lesson_title, relevant_content):
    """Create enhanced lesson content using extracted PDF content."""
    
    # Clean and format objectives
    objectives_html = ""
    if relevant_content['objectives']:
        objectives_html = """
        <div class="lesson-objectives">
            <h3>Learning Objectives</h3>
            <ul>"""
        for obj in relevant_content['objectives'][:5]:
            clean_obj = obj.strip().replace('\n', ' ')
            if len(clean_obj) > 10:
                objectives_html += f"<li>{clean_obj}</li>\n"
        objectives_html += """
            </ul>
        </div>"""
    
    # Clean and format activities
    activities_html = ""
    if relevant_content['activities']:
        activities_html = """
        <div class="lesson-activities">
            <h3>Learning Activities</h3>
            <ul>"""
        for activity in relevant_content['activities'][:8]:
            clean_activity = activity.strip().replace('\n', ' ')
            if len(clean_activity) > 10:
                activities_html += f"<li>{clean_activity}</li>\n"
        activities_html += """
            </ul>
        </div>"""
    
    # Clean and format lesson content
    lesson_content_html = ""
    if relevant_content['lessons']:
        lesson_content_html = """
        <div class="lesson-content">
            <h3>Lesson Content</h3>"""
        for lesson in relevant_content['lessons'][:2]:
            clean_lesson = lesson.strip().replace('\n', ' ')
            if len(clean_lesson) > 50:
                lesson_content_html += f"<p>{clean_lesson[:300]}...</p>\n"
        lesson_content_html += """
        </div>"""
    
    # Create materials section
    materials_html = ""
    if relevant_content['materials']:
        materials_html = """
        <div class="lesson-materials">
            <h3>Materials and Resources</h3>
            <ul>"""
        for material in relevant_content['materials'][:5]:
            clean_material = material.strip().replace('\n', ' ')
            if len(clean_material) > 5:
                materials_html += f"<li>{clean_material}</li>\n"
        materials_html += """
            </ul>
        </div>"""
    
    # Combine all sections
    enhanced_content = f"""
    <div class="enhanced-lesson-content">
        <h2>{lesson_title}</h2>
        <div class="lesson-overview">
            <p>This lesson has been enhanced with content from authentic teacher guides to provide comprehensive 
            teaching materials including objectives, activities, and instructional content.</p>
        </div>
        
        {objectives_html}
        {lesson_content_html}
        {activities_html}
        {materials_html}
    </div>
    """
    
    return enhanced_content

def enhance_lesson_file(lesson_file_path, geography_data):
    """Enhance a specific lesson file with extracted content."""
    try:
        # Read current lesson file
        with open(lesson_file_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Extract lesson title from filename or content
        lesson_title = Path(lesson_file_path).stem.replace('_', ' ').title()
        
        # Extract relevant content
        relevant_content = extract_relevant_content(geography_data, lesson_title)
        
        # Create enhanced content
        enhanced_content = create_enhanced_lesson_content(lesson_title, relevant_content)
        
        # Find insertion point in current content
        if '<main>' in current_content:
            # Insert after <main> tag
            insertion_point = current_content.find('<main>') + len('<main>')
            enhanced_html = (current_content[:insertion_point] + 
                           enhanced_content + 
                           current_content[insertion_point:])
        else:
            # If no main tag, insert after body
            insertion_point = current_content.find('<body>') + len('<body>')
            enhanced_html = (current_content[:insertion_point] + 
                           enhanced_content + 
                           current_content[insertion_point:])
        
        # Write enhanced content back to file
        with open(lesson_file_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)
        
        return True, f"Enhanced {lesson_title}"
        
    except Exception as e:
        return False, f"Error enhancing {lesson_file_path}: {e}"

def main():
    """Main function to enhance all geography lessons."""
    print("Starting mass lesson enhancement...")
    
    # Load extracted content
    print("Loading extracted PDF content...")
    extracted_content = load_extracted_content()
    print(f"Loaded content from {len(extracted_content)} PDFs")
    
    # Identify geography-related content
    geography_data = identify_geography_content(extracted_content)
    print(f"Found {len(geography_data)} geography-related PDFs:")
    for filename, data in geography_data.items():
        print(f"  - {data['title']}")
    
    # Find lesson files to enhance
    print("\nFinding lesson files...")
    lesson_files = find_lesson_files()
    print(f"Found {len(lesson_files)} lesson files")
    
    # Enhance each lesson file
    print("\nEnhancing lessons...")
    enhanced_count = 0
    errors = []
    
    for lesson_file in lesson_files:
        success, message = enhance_lesson_file(lesson_file, geography_data)
        if success:
            enhanced_count += 1
            print(f"✓ {message}")
        else:
            errors.append(message)
            print(f"✗ {message}")
    
    # Summary
    print(f"\n=== ENHANCEMENT COMPLETE ===")
    print(f"Enhanced {enhanced_count} lesson files")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    print(f"\n🎯 Lesson enhancement complete! {enhanced_count} lessons now have rich content from teacher guides.")

if __name__ == "__main__":
    main()
