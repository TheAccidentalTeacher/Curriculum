#!/usr/bin/env python3
"""
Add Cross-Curricular Links to Geography Lessons
Adds ELA and Science lesson links to all geography lesson files based on unit/lesson mapping to day numbers.
"""

import os
import re
import glob
from typing import Dict, Tuple

# Unit mapping - Geography units to day ranges (from enhance_all_lessons_detailed.py)
UNIT_DAY_MAPPING = {
    1: (1, 10),    # Unit 1: Geographic Tools -> Days 1-10
    2: (11, 20),   # Unit 2: Physical Geography -> Days 11-20  
    3: (21, 30),   # Unit 3: Canada -> Days 21-30
    4: (31, 44),   # Unit 4: United States -> Days 31-44
    5: (45, 54),   # Unit 5: Mexico & Central America -> Days 45-54
    6: (55, 64),   # Unit 6: South America -> Days 55-64
    7: (65, 74),   # Unit 7: Western Europe -> Days 65-74
    8: (75, 79),   # Unit 8: Eastern Europe -> Days 75-79
    9: (80, 89),   # Unit 9: Russia & Central Asia -> Days 80-89
    10: (90, 99),  # Unit 10: East Asia -> Days 90-99
    11: (100, 109), # Unit 11: Southeast & South Asia -> Days 100-109
    12: (110, 115), # Unit 12: Southwest Asia & North Africa -> Days 110-115
    13: (116, 125), # Unit 13: Sub-Saharan Africa -> Days 116-125
    14: (126, 135), # Unit 14: Australia & Oceania -> Days 126-135
    15: (136, 145), # Unit 15: Environmental Issues -> Days 136-145
    16: (146, 155), # Unit 16: Economic Geography -> Days 146-155
    17: (156, 165), # Unit 17: Cultural Geography -> Days 156-165
    18: (166, 175), # Unit 18: Future Geography -> Days 166-175
}

def get_day_from_unit_lesson(unit_num: int, lesson_num: int) -> int:
    """Convert unit and lesson number to day number."""
    if unit_num not in UNIT_DAY_MAPPING:
        return 1
    
    start_day, end_day = UNIT_DAY_MAPPING[unit_num]
    days_per_unit = end_day - start_day + 1
    
    # Calculate day within the range (lessons 1-5 typically map to evenly distributed days)
    if lesson_num <= days_per_unit:
        return start_day + lesson_num - 1
    else:
        # If more lessons than days, cycle through
        return start_day + ((lesson_num - 1) % days_per_unit)

def extract_unit_lesson_from_filename(filename: str) -> Tuple[int, int]:
    """Extract unit and lesson numbers from filename like 'unit1-lesson2-grade6.html'."""
    match = re.search(r'unit(\d+)-lesson(\d+)-grade\d+\.html', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 1, 1

def add_crosscut_links(file_path: str) -> bool:
    """Add cross-curricular links to a geography lesson file."""
    try:
        # Extract unit and lesson from filename
        filename = os.path.basename(file_path)
        unit_num, lesson_num = extract_unit_lesson_from_filename(filename)
        day_num = get_day_from_unit_lesson(unit_num, lesson_num)
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if links already exist
        if 'crosscut-lessons' in content:
            print(f"✓ Links already exist in {filename}")
            return True
        
        # Create the cross-curricular links section
        crosscut_section = f'''
        <!-- Cross-Curricular Integration Links -->
        <section style="background: linear-gradient(135deg, #27ae60, #2ecc71); border-radius: 12px; padding: 1.5em; margin: 2em 0; color: white;">
            <h3 style="margin: 0 0 1em 0; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.5em;">🔗</span>
                Cross-Curricular Integration - Day {day_num}
            </h3>
            <p style="margin-bottom: 1.5em; opacity: 0.9;">Enhance this geography lesson with aligned ELA and Science activities:</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; backdrop-filter: blur(10px);">
                    <h4 style="margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2em;">📝</span>
                        ELA Integration
                    </h4>
                    <p style="margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.8;">Practice reading, writing, and communication skills through geographic content</p>
                    <a href="../../crosscut-lessons/ela/day{day_num}.html" 
                       style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block; transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.3);"
                       onmouseover="this.style.background='rgba(255,255,255,0.3)'; this.style.transform='translateY(-2px)';"
                       onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(0)';">
                        📖 View ELA Day {day_num}
                    </a>
                </div>
                
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; backdrop-filter: blur(10px);">
                    <h4 style="margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2em;">🔬</span>
                        Science Integration
                    </h4>
                    <p style="margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.8;">Investigate Earth systems and scientific processes behind geographic phenomena</p>
                    <a href="../../crosscut-lessons/science/day{day_num}.html" 
                       style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block; transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.3);"
                       onmouseover="this.style.background='rgba(255,255,255,0.3)'; this.style.transform='translateY(-2px)';"
                       onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(0)';">
                        🧪 View Science Day {day_num}
                    </a>
                </div>
            </div>
            
            <div style="margin-top: 15px; padding: 12px; background: rgba(255,255,255,0.1); border-radius: 6px; border-left: 4px solid rgba(255,255,255,0.4);">
                <p style="margin: 0; font-size: 0.9em; opacity: 0.9;">
                    <strong>💡 Teaching Tip:</strong> Use these lessons together for maximum impact! Start with geography concepts, reinforce with ELA activities, and deepen understanding through science investigations.
                </p>
            </div>
        </section>'''
        
        # Find the best insertion point (after learning objectives but before lesson content)
        insertion_patterns = [
            (r'(<section[^>]*style="background: #e3f2fd[^"]*"[^>]*>.*?</section>)', 'after_objectives'),
            (r'(<section[^>]*margin-bottom: 2em[^"]*"[^>]*>.*?</section>)', 'after_first_section'),
            (r'(<main>)', 'after_main_open')
        ]
        
        inserted = False
        for pattern, location in insertion_patterns:
            if re.search(pattern, content, re.DOTALL):
                if location == 'after_objectives' or location == 'after_first_section':
                    content = re.sub(pattern, r'\1' + crosscut_section, content, count=1, flags=re.DOTALL)
                else:  # after_main_open
                    content = re.sub(pattern, r'\1' + crosscut_section, content, count=1)
                inserted = True
                break
        
        # Fallback: insert before the first section if no good spot found
        if not inserted:
            main_pattern = r'(<main>.*?)(<section)'
            if re.search(main_pattern, content, re.DOTALL):
                content = re.sub(main_pattern, r'\1' + crosscut_section + r'\2', content, count=1, flags=re.DOTALL)
                inserted = True
        
        if not inserted:
            print(f"⚠️  Could not find insertion point for {filename}")
            return False
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Added Day {day_num} links to {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Add cross-curricular links to all geography lesson files."""
    print("🔗 Adding Cross-Curricular Links to Geography Lessons")
    print("=" * 60)
    
    # Find all geography lesson files
    lesson_files = glob.glob("/workspaces/Curriculum/units/lessons/unit*-lesson*-grade*.html")
    
    if not lesson_files:
        print("❌ No geography lesson files found!")
        return
    
    print(f"📚 Found {len(lesson_files)} geography lesson files")
    print()
    
    success_count = 0
    total_count = len(lesson_files)
    
    for file_path in sorted(lesson_files):
        if add_crosscut_links(file_path):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"📊 Cross-Curricular Integration Complete!")
    print(f"✅ Successfully updated: {success_count}/{total_count} files")
    print(f"📈 Success rate: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print()
        print("🎉 ALL GEOGRAPHY LESSONS NOW HAVE CROSS-CURRICULAR LINKS!")
        print("🌟 Features added:")
        print("   • Direct links to corresponding ELA lessons")
        print("   • Direct links to corresponding Science lessons") 
        print("   • Day-based mapping for perfect alignment")
        print("   • Beautiful integrated design")
        print("   • Teaching tips for cross-curricular use")
    else:
        print(f"\n⚠️  {total_count - success_count} files need manual attention")

if __name__ == "__main__":
    main()
