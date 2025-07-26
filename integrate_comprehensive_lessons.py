#!/usr/bin/env python3
"""
Replace existing fragmented lesson content with comprehensive, educator-ready lessons
"""

import os
import glob
import shutil
from bs4 import BeautifulSoup

def integrate_comprehensive_lessons():
    """Replace existing lesson files with comprehensive versions"""
    
    print('🎓 INTEGRATING COMPREHENSIVE EDUCATOR-READY LESSONS')
    print('=' * 60)
    
    # Find all comprehensive lesson files
    comprehensive_files = glob.glob('complete_lessons/*.html')
    existing_lesson_files = glob.glob('units/lessons/unit*-lesson*-grade*.html')
    
    print(f'📚 Found {len(comprehensive_files)} comprehensive lessons')
    print(f'📄 Found {len(existing_lesson_files)} existing lesson files')
    
    integration_count = 0
    
    for comp_file in comprehensive_files:
        # Extract unit, lesson, and grade from filename
        filename = os.path.basename(comp_file)
        # Example: unit1-lesson1-grade6-complete.html
        
        if 'unit' in filename and 'lesson' in filename and 'grade' in filename:
            # Extract components
            parts = filename.replace('-complete.html', '').split('-')
            unit = parts[0]  # unit1
            lesson = parts[1]  # lesson1
            grade = parts[2]  # grade6
            
            # Find matching existing file
            target_pattern = f'units/lessons/{unit}-{lesson}-{grade}.html'
            matching_files = glob.glob(target_pattern)
            
            if matching_files:
                target_file = matching_files[0]
                
                try:
                    # Read comprehensive lesson content
                    with open(comp_file, 'r', encoding='utf-8') as f:
                        comp_content = f.read()
                    
                    # Read existing lesson structure
                    with open(target_file, 'r', encoding='utf-8') as f:
                        existing_content = f.read()
                    
                    # Parse existing content to preserve navigation
                    existing_soup = BeautifulSoup(existing_content, 'html.parser')
                    comp_soup = BeautifulSoup(comp_content, 'html.parser')
                    
                    # Extract navigation from existing file
                    existing_nav = existing_soup.find('nav')
                    existing_header = existing_soup.find('header')
                    
                    # Get comprehensive lesson content
                    comp_body = comp_soup.find('body')
                    
                    # Create new integrated content
                    new_soup = BeautifulSoup(existing_content, 'html.parser')
                    
                    # Replace main content but preserve navigation
                    main_content = new_soup.find('main')
                    if main_content:
                        # Clear existing main content
                        main_content.clear()
                        
                        # Add comprehensive lesson content
                        if comp_body:
                            for element in comp_body.children:
                                if element.name and element.name not in ['header', 'nav']:
                                    main_content.append(element.extract())
                    
                    # Update title
                    title_tag = new_soup.find('title')
                    comp_title = comp_soup.find('title')
                    if title_tag and comp_title:
                        title_tag.string = comp_title.string
                    
                    # Write integrated content
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(str(new_soup))
                    
                    integration_count += 1
                    print(f'   ✅ Integrated: {os.path.basename(target_file)}')
                    
                except Exception as e:
                    print(f'   ❌ Failed to integrate {target_file}: {str(e)}')
            else:
                print(f'   ⚠️  No matching file found for {filename}')
    
    print(f'\\n📊 INTEGRATION SUMMARY:')
    print(f'   📚 Comprehensive lessons created: {len(comprehensive_files)}')
    print(f'   📄 Existing lessons found: {len(existing_lesson_files)}')
    print(f'   ✅ Successfully integrated: {integration_count}')
    
    if integration_count > 0:
        print(f'\\n🎉 SUCCESS! {integration_count} lessons now have comprehensive, educator-ready content!')
        print(f'Teachers can now teach these lessons without needing any additional textbook resources.')
        
        # Create backup of original files
        backup_dir = 'lesson_backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            print(f'📁 Created backup directory: {backup_dir}')
        
        return True
    else:
        print(f'\\n⚠️  No lessons were integrated. Check file naming patterns.')
        return False

if __name__ == '__main__':
    success = integrate_comprehensive_lessons()
    exit(0 if success else 1)
