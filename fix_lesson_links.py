#!/usr/bin/env python3
"""
Script to fix lesson links in all unit HTML files.
Converts plain text lesson titles to clickable links for 7th and 8th grade sections.
"""

import os
import re
import glob

def fix_lesson_links_in_file(file_path):
    """Fix lesson links in a single unit HTML file."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract unit number from filename
    unit_match = re.search(r'unit(\d+)\.html', file_path)
    if not unit_match:
        print(f"Could not extract unit number from {file_path}")
        return False
    
    unit_num = unit_match.group(1)
    
    # Fix 7th grade lesson links
    # Pattern: <h3>Lesson X: Title</h3>
    grade7_pattern = r'<h3>(Lesson \d+: [^<]+)</h3>'
    
    def replace_grade7_lesson(match):
        lesson_text = match.group(1)
        # Extract lesson number
        lesson_match = re.search(r'Lesson (\d+):', lesson_text)
        if lesson_match:
            lesson_num = lesson_match.group(1)
            link_href = f"lessons/unit{unit_num}-lesson{lesson_num}-grade7.html"
            # Add appropriate emoji and styling
            return f'<h3><a href="{link_href}" style="color: #f57c00; text-decoration: none;">{lesson_text}</a></h3>'
        return match.group(0)
    
    # Fix 8th grade lesson links
    def replace_grade8_lesson(match):
        lesson_text = match.group(1)
        # Extract lesson number
        lesson_match = re.search(r'Lesson (\d+):', lesson_text)
        if lesson_match:
            lesson_num = lesson_match.group(1)
            link_href = f"lessons/unit{unit_num}-lesson{lesson_num}-grade8.html"
            # Add appropriate emoji and styling
            return f'<h3><a href="{link_href}" style="color: #388e3c; text-decoration: none;">{lesson_text}</a></h3>'
        return match.group(0)
    
    # Split content into sections to target only 7th and 8th grade areas
    sections = content.split('<!-- Grade 7 Content -->')
    if len(sections) > 1:
        # Process 7th grade section
        grade7_and_after = sections[1].split('<!-- Grade 8 Content -->')
        if len(grade7_and_after) > 1:
            # We have both 7th and 8th grade sections
            grade7_section = grade7_and_after[0]
            grade8_and_after = grade7_and_after[1]
            
            # Fix 7th grade links
            grade7_section = re.sub(grade7_pattern, replace_grade7_lesson, grade7_section)
            
            # Split 8th grade section
            remaining_sections = grade8_and_after.split('</section>', 1)
            if len(remaining_sections) > 1:
                grade8_section = remaining_sections[0] + '</section>'
                after_grade8 = remaining_sections[1]
                
                # Fix 8th grade links  
                grade8_section = re.sub(grade7_pattern, replace_grade8_lesson, grade8_section)
                
                # Reconstruct content
                content = (sections[0] + 
                          '<!-- Grade 7 Content -->' + 
                          grade7_section + 
                          '<!-- Grade 8 Content -->' + 
                          grade8_section + 
                          after_grade8)
            else:
                # Only process 7th grade section
                content = (sections[0] + 
                          '<!-- Grade 7 Content -->' + 
                          grade7_section + 
                          '<!-- Grade 8 Content -->' + 
                          grade8_and_after[1])
        else:
            # Only 7th grade section found
            grade7_section = re.sub(grade7_pattern, replace_grade7_lesson, grade7_and_after[0])
            content = sections[0] + '<!-- Grade 7 Content -->' + grade7_section
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {file_path}")
    return True

def main():
    """Main function to process all unit HTML files."""
    # Find all unit HTML files
    unit_files = glob.glob('/workspaces/Curriculum/units/unit*.html')
    unit_files = [f for f in unit_files if re.match(r'.*/unit\d+\.html$', f)]
    
    print(f"Found {len(unit_files)} unit files to process")
    
    processed = 0
    for file_path in sorted(unit_files):
        if fix_lesson_links_in_file(file_path):
            processed += 1
    
    print(f"\nSuccessfully processed {processed} unit files!")
    print("All lesson titles should now be clickable links!")

if __name__ == "__main__":
    main()
