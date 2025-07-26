#!/usr/bin/env python3
"""
Integrate the extracted US Teacher Guide content into lesson files
"""

import json
import os
import glob
from bs4 import BeautifulSoup

def integrate_us_content():
    """Integrate US teacher guide content into relevant lesson files"""
    
    print('🇺🇸 INTEGRATING US TEACHER GUIDE CONTENT')
    print('=' * 50)
    
    # Load the extracted content
    with open('us_teacher_guide_extracted_content.json', 'r') as f:
        us_data = json.load(f)
    
    if not us_data.get('success') or not us_data.get('lessons'):
        print('❌ No valid lesson content found in extraction')
        return False
    
    print(f'📚 Found {len(us_data["lessons"])} lessons to integrate')
    
    # Process each lesson
    integrated_files = []
    
    for lesson in us_data['lessons']:
        title = lesson['title']
        content = lesson['content']
        
        print(f'\\n🎯 Processing: {title[:50]}...')
        
        # Find relevant lesson files based on content
        target_files = find_relevant_files(title, content)
        
        if target_files:
            for file_path in target_files:
                try:
                    if integrate_content_into_file(file_path, lesson):
                        integrated_files.append(file_path)
                        print(f'   ✅ Updated: {os.path.basename(file_path)}')
                except Exception as e:
                    print(f'   ❌ Failed to update {os.path.basename(file_path)}: {str(e)}')
        else:
            print(f'   ⚠️  No matching lesson files found')
    
    print(f'\\n📊 INTEGRATION SUMMARY:')
    print(f'   📚 Lessons processed: {len(us_data["lessons"])}')
    print(f'   📄 Files updated: {len(set(integrated_files))}')
    
    if integrated_files:
        print(f'\\n✅ Successfully integrated US Teacher Guide content!')
        print(f'Updated files: {len(set(integrated_files))}')
        for file_path in sorted(set(integrated_files)):
            print(f'   • {os.path.basename(file_path)}')
        return True
    else:
        print(f'\\n⚠️  No files were updated')
        return False

def find_relevant_files(title, content):
    """Find lesson files that match the content topic"""
    
    # Look for US-related lesson files
    us_patterns = [
        'units/lessons/*united-states*',
        'units/lessons/*us-*',
        'units/lessons/*america*',
        'units/lessons/unit6-*',  # Module 6 from the content
        'units/lessons/unit33-*', # US Geography units
        'units/lessons/unit34-*',
        'units/lessons/unit35-*',
        'units/lessons/unit36-*'
    ]
    
    matching_files = []
    
    for pattern in us_patterns:
        files = glob.glob(pattern)
        matching_files.extend(files)
    
    # If no specific US files, look in later units (30+) which might cover North America
    if not matching_files:
        for unit_num in range(30, 38):  # Units 30-37 might cover North America
            pattern = f'units/lessons/unit{unit_num}-lesson*'
            files = glob.glob(pattern)
            matching_files.extend(files[:2])  # Just take first 2 lessons per unit
    
    return list(set(matching_files))  # Remove duplicates

def integrate_content_into_file(file_path, lesson):
    """Integrate lesson content into a specific HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main content area
    main_content = soup.find('main') or soup.find('div', class_='lesson-content') or soup.find('body')
    
    if not main_content:
        return False
    
    # Clean and prepare the content
    lesson_content = lesson['content']
    title = lesson['title']
    
    # Create enhanced content sections
    content_html = f'''
    <div class="us-teacher-guide-content" style="background: #f8f9fa; padding: 20px; margin: 20px 0; border-left: 4px solid #007bff; border-radius: 5px;">
        <h3 style="color: #007bff; margin-bottom: 15px;">🇺🇸 US Teacher Guide Content</h3>
        <h4 style="color: #333; margin-bottom: 10px;">{clean_title(title)}</h4>
        <div class="guide-content" style="line-height: 1.6;">
            {format_teacher_content(lesson_content)}
        </div>
        <div class="content-meta" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6; font-size: 0.9em; color: #6c757d;">
            <strong>Source:</strong> US Teacher Guide • <strong>Quality Score:</strong> {lesson['quality_score']} • <strong>Confidence:</strong> {lesson['extraction_confidence']}
        </div>
    </div>
    '''
    
    # Find a good insertion point
    insertion_point = None
    
    # Try to find an existing content section
    existing_content = main_content.find('div', class_='lesson-body') or main_content.find('section')
    
    if existing_content:
        # Insert after existing content
        insertion_point = existing_content
    else:
        # Insert at the beginning of main content
        insertion_point = main_content
    
    # Insert the new content
    if insertion_point:
        new_content = BeautifulSoup(content_html, 'html.parser')
        if insertion_point == main_content:
            # Insert at beginning
            insertion_point.insert(0, new_content)
        else:
            # Insert after
            insertion_point.insert_after(new_content)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    
    return False

def clean_title(title):
    """Clean up the title text"""
    # Remove dots and page references
    title = title.split('\\n')[0]  # Take first line
    title = title.replace(' . ', ' ')
    title = title.replace('.', '')
    title = title.strip()
    
    # Remove page numbers and artifacts
    import re
    title = re.sub(r'\\d{3,}', '', title)  # Remove 3+ digit numbers (page refs)
    title = re.sub(r'\\s+', ' ', title)    # Normalize whitespace
    
    return title.strip()

def format_teacher_content(content):
    """Format the teacher guide content for HTML display"""
    
    # Split into paragraphs
    paragraphs = content.split('\\n\\n')
    
    formatted_content = ""
    
    for para in paragraphs:
        if para.strip():
            # Clean up the paragraph
            para = para.replace('\\n', ' ')
            para = para.strip()
            
            # Skip page markers and technical notes
            if 'DO NOT EDIT' in para or 'CorrectionKey' in para or 'Page ---' in para:
                continue
            
            # Format as different elements based on content
            if para.startswith('The Big Idea'):
                formatted_content += f'<div class="big-idea" style="background: #e7f3ff; padding: 15px; margin: 10px 0; border-radius: 5px;"><strong>🎯 {para}</strong></div>'
            elif para.startswith('Culture') or para.startswith('Geography') or para.startswith('History'):
                formatted_content += f'<div class="teaching-note" style="background: #fff3cd; padding: 10px; margin: 8px 0; border-radius: 3px;"><strong>{para}</strong></div>'
            elif 'Analyze Visuals' in para or 'questions:' in para:
                formatted_content += f'<div class="activity" style="background: #d4edda; padding: 10px; margin: 8px 0; border-radius: 3px;">{para}</div>'
            else:
                formatted_content += f'<p style="margin: 8px 0;">{para}</p>'
    
    return formatted_content

if __name__ == '__main__':
    success = integrate_us_content()
    exit(0 if success else 1)
