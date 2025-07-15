#!/usr/bin/env python3
"""
Fix Cross-Curricular Links to Point to Actual Worksheets
Updates geography lessons to link to the actual awesome worksheets instead of non-existent day files.
"""

import os
import re
import glob
from typing import Dict, Tuple

# Enhanced mapping from geography units to actual worksheet regions
UNIT_WORKSHEET_MAPPING = {
    1: "a_geographer_s_world",  # Unit 1: Geographic Tools -> A Geographer's World
    2: "the_physical_world",    # Unit 2: Physical Geography -> The Physical World  
    3: "canada",                # Unit 3: Canada -> Canada
    4: "north_america",         # Unit 4: United States -> North America
    5: "central_america_and_the_caribbean",  # Unit 5: Mexico & Central America -> Central America and the Caribbean
    6: "south_america",         # Unit 6: South America -> South America
    7: "southern_europe",       # Unit 7: Western Europe -> Southern Europe
    8: "eastern_europe",        # Unit 8: Eastern Europe -> Eastern Europe
    9: "russia_and_the_caucasus",  # Unit 9: Russia & Central Asia -> Russia and the Caucasus
    10: "china,_mongolia,_and_taiwan",  # Unit 10: East Asia -> China, Mongolia, and Taiwan
    11: "southeast_asia",       # Unit 11: Southeast & South Asia -> Southeast Asia
    12: "the_arabian_peninsula_to_central_asia",  # Unit 12: Southwest Asia & North Africa -> The Arabian Peninsula to Central Asia
    13: "east_and_southern_africa",  # Unit 13: Sub-Saharan Africa -> East and Southern Africa
    14: "oceania_and_antarctica",     # Unit 14: Australia & Oceania -> Oceania and Antarctica
    15: "the_physical_world",   # Unit 15: Environmental Issues -> The Physical World (environmental focus)
    16: "economics",            # Unit 16: Economic Geography -> Economics
    17: "the_human_world",      # Unit 17: Cultural Geography -> The Human World
    18: "the_human_world",      # Unit 18: Future Geography -> The Human World (human impact focus)
    19: "early_civilizations_of_the_fertile_crescent_and_the_nile_valley",  # Ancient civilizations
    20: "early_civilizations_of_china",  # Ancient China
    21: "early_civilizations_of_latin_america",  # Ancient Americas
    22: "indian_early_civilizations,_empires,_and_world_religions",  # Ancient India
    23: "europe_before_the_1700s",  # Medieval Europe
    24: "history_of_modern_europe",  # Modern Europe
    25: "history_of_sub-saharan_africa",  # African history
    26: "japan_and_the_koreas",  # East Asian nations
    27: "the_indian_subcontinent",  # South Asia
    28: "the_eastern_mediterranean",  # Mediterranean region
    29: "north_africa",         # North Africa
    30: "mexico",               # Mexico specifically
    31: "government_and_citizenship",  # Civics
    32: "human_world"           # Human geography
}

def extract_unit_lesson_from_filename(filename: str) -> Tuple[int, int]:
    """Extract unit and lesson numbers from filename like 'unit1-lesson2-grade6.html'."""
    match = re.search(r'unit(\d+)-lesson(\d+)-grade\d+\.html', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 0, 0

def get_worksheet_region(unit_num: int) -> str:
    """Get the worksheet region name for a given unit."""
    return UNIT_WORKSHEET_MAPPING.get(unit_num, "a_geographer_s_world")

def create_cross_curricular_section(unit_num: int, lesson_num: int) -> str:
    """Create the cross-curricular HTML section with links to actual worksheets."""
    region = get_worksheet_region(unit_num)
    
    return f'''        <!-- Cross-Curricular Integration Links -->
        <section style="background: linear-gradient(135deg, #27ae60, #2ecc71); border-radius: 12px; padding: 1.5em; margin: 2em 0; color: white;">
            <h3 style="margin: 0 0 1em 0; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.5em;">🔗</span>
                Cross-Curricular Integration - Unit {unit_num}, Lesson {lesson_num}
            </h3>
            <p style="margin-bottom: 1.5em; opacity: 0.9;">Enhance this geography lesson with awesome aligned ELA and Science worksheets:</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; backdrop-filter: blur(10px);">
                    <h4 style="margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2em;">📝</span>
                        ELA Worksheet
                    </h4>
                    <p style="margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.8;">Comprehensive reading, writing, and communication activities based on this region</p>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <a href="../../CURRICULUM REPOSITORY/worksheets/{region}_ela_worksheet.html" 
                           style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block; transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.3);"
                           onmouseover="this.style.background='rgba(255,255,255,0.3)'; this.style.transform='translateY(-2px)';"
                           onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(0)';">
                            📖 View ELA Worksheet
                        </a>
                        <a href="../../CURRICULUM REPOSITORY/worksheets/{region}_ela_worksheet.pdf" 
                           style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block; transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.3);"
                           onmouseover="this.style.background='rgba(255,255,255,0.3)'; this.style.transform='translateY(-2px)';"
                           onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(0)';">
                            📄 Download PDF
                        </a>
                    </div>
                </div>
                
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; backdrop-filter: blur(10px);">
                    <h4 style="margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2em;">🔬</span>
                        Science Worksheet
                    </h4>
                    <p style="margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.8;">Investigate Earth systems and scientific processes for this geographic region</p>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <a href="../../CURRICULUM REPOSITORY/worksheets/{region}_science_worksheet.html" 
                           style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block; transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.3);"
                           onmouseover="this.style.background='rgba(255,255,255,0.3)'; this.style.transform='translateY(-2px)';"
                           onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(0)';">
                            🧪 View Science Worksheet
                        </a>
                        <a href="../../CURRICULUM REPOSITORY/worksheets/{region}_science_worksheet.pdf" 
                           style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block; transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.3);"
                           onmouseover="this.style.background='rgba(255,255,255,0.3)'; this.style.transform='translateY(-2px)';"
                           onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='translateY(0)';">
                            📄 Download PDF
                        </a>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2);">
                <p style="margin: 0; font-size: 0.85em; opacity: 0.8; text-align: center;">
                    💡 <strong>Teaching Tip:</strong> Use these worksheets before, during, or after your geography lesson to reinforce cross-curricular connections and deepen student understanding.
                </p>
            </div>
        </section>'''

def update_lesson_file(filepath: str) -> bool:
    """Update a lesson file with cross-curricular links to actual worksheets."""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract unit and lesson numbers
        filename = os.path.basename(filepath)
        unit_num, lesson_num = extract_unit_lesson_from_filename(filename)
        
        if unit_num == 0:
            print(f"⚠️  Could not extract unit/lesson from {filename}")
            return False
        
        # Remove existing cross-curricular section if it exists
        # Look for the section starting with <!-- Cross-Curricular Integration Links -->
        pattern = r'        <!-- Cross-Curricular Integration Links -->.*?</section>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Find the end of the first main section (typically after the first </section> tag)
        # Insert the new cross-curricular section after the first major section
        section_pattern = r'(        </section>\s*)'
        match = re.search(section_pattern, content)
        
        if match:
            # Create the new cross-curricular section
            new_section = create_cross_curricular_section(unit_num, lesson_num)
            
            # Insert after the first section
            insert_position = match.end()
            updated_content = (content[:insert_position] + 
                             '\n' + new_section + '\n' + 
                             content[insert_position:])
            
            # Write the updated content back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            region = get_worksheet_region(unit_num)
            print(f"✅ Updated {filename} -> {region} worksheets")
            return True
        else:
            print(f"⚠️  Could not find insertion point in {filename}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main function to update all geography lesson files."""
    print("🔗 Fixing Cross-Curricular Links to Point to Actual Awesome Worksheets")
    print("=" * 70)
    
    # Find all geography lesson files
    lesson_pattern = "/workspaces/Curriculum/units/lessons/unit*-lesson*-grade*.html"
    lesson_files = glob.glob(lesson_pattern)
    
    if not lesson_files:
        print("❌ No lesson files found!")
        return
    
    print(f"📁 Found {len(lesson_files)} lesson files to update")
    print()
    
    # Update each file
    success_count = 0
    for filepath in sorted(lesson_files):
        if update_lesson_file(filepath):
            success_count += 1
    
    print()
    print("=" * 70)
    print(f"🎉 Successfully updated {success_count}/{len(lesson_files)} geography lessons!")
    print("✨ Your awesome worksheets are now properly linked!")
    print()
    print("🔍 Each lesson now links to:")
    print("   📝 Region-specific ELA worksheet (HTML + PDF)")
    print("   🔬 Region-specific Science worksheet (HTML + PDF)")
    print("   💡 Teaching tips for cross-curricular integration")

if __name__ == "__main__":
    main()
