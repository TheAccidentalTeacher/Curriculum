#!/usr/bin/env python3
"""
Script to make unit references clickable links across all unit HTML files.
Converts text like "Unit 2", "Unit 3", etc. to clickable links to their respective unit pages.
"""

import os
import re
import glob

def make_unit_references_clickable(file_path):
    """Make unit references clickable in a single unit HTML file."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match "Unit X" where X is a number (but not in titles, URLs, or already linked)
    # Look for "Unit X" that's not already part of a link or in a title/header
    unit_pattern = r'(?<!href=")(?<!<title>)(?<!<h\d>)(?<!Back to )\bUnit (\d+)\b(?!</a>)(?! \w)'
    
    def replace_unit_reference(match):
        unit_num = match.group(1)
        unit_text = match.group(0)  # "Unit X"
        
        # Don't replace if it's already part of a link
        start_pos = match.start()
        before_text = content[max(0, start_pos-50):start_pos]
        after_text = content[start_pos:start_pos+100]
        
        # Skip if it's already in a link, title, or header
        if '<a ' in before_text and '</a>' not in before_text:
            return unit_text
        if 'title>' in before_text or '<h' in before_text:
            return unit_text
        if 'Back to' in before_text:
            return unit_text
            
        # Create clickable link
        link_href = f"unit{unit_num}.html"
        return f'<a href="{link_href}" style="color: #1976d2; text-decoration: none;">{unit_text}</a>'
    
    # Apply the replacement
    updated_content = re.sub(unit_pattern, replace_unit_reference, content)
    
    # Count changes
    changes = len(re.findall(unit_pattern, content))
    
    if changes > 0:
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"  ✅ Updated {changes} unit references in {os.path.basename(file_path)}")
        return True
    else:
        print(f"  ℹ️  No unit references found in {os.path.basename(file_path)}")
        return False

def main():
    """Main function to process all unit HTML files."""
    # Find all unit HTML files
    unit_files = glob.glob('/workspaces/Curriculum/units/unit*.html')
    unit_files = [f for f in unit_files if re.match(r'.*/unit\d+\.html$', f)]
    
    print(f"Found {len(unit_files)} unit files to process")
    print("Making unit references clickable...\n")
    
    total_processed = 0
    total_changes = 0
    
    for file_path in sorted(unit_files):
        try:
            if make_unit_references_clickable(file_path):
                total_processed += 1
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
    
    print(f"\n🎉 Successfully processed {total_processed} unit files!")
    print("All unit references (Unit 1, Unit 2, etc.) should now be clickable links!")

if __name__ == "__main__":
    main()
