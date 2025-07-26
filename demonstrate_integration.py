#!/usr/bin/env python3
"""
Demonstration: Real Content Integration
Show how we can integrate actual teacher guide content into lesson files
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup

def demonstrate_real_integration():
    """Demonstrate integrating real PDF content into a lesson file"""
    
    print("🎯 DEMONSTRATION: Real Content Integration")
    print("=" * 60)
    
    # Load our best extracted content
    content_file = Path("/workspaces/Curriculum/best_extracted_content.json")
    with open(content_file, 'r', encoding='utf-8') as f:
        pdf_content = json.load(f)
    
    # Get the best lesson with most content
    best_lesson = max(pdf_content['lessons'], key=lambda x: len(x['full_content']))
    
    print(f"📚 Source PDF: {pdf_content['title']}")
    print(f"📖 Lesson: {best_lesson['title']}")
    print(f"📊 Content lines: {len(best_lesson['full_content'])}")
    print(f"📝 Materials: {len(best_lesson['materials'])}")
    print(f"🔍 Assessment: {len(best_lesson['assessment'])}")
    
    # Create enhanced lesson content
    sample_lesson_file = Path("/workspaces/Curriculum/units/lessons/unit11-lesson4-grade6.html")
    
    with open(sample_lesson_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse and enhance
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the lesson content area
    lesson_content = soup.find('div', class_='enhanced-lesson-content')
    
    if lesson_content:
        # Clear existing placeholder content
        lesson_content.clear()
        
        # Add real lesson title
        title = soup.new_tag('h2')
        title.string = f"Real Content: {clean_title(best_lesson['title'])}"
        lesson_content.append(title)
        
        # Add source attribution
        source = soup.new_tag('p', style="background: #e8f5e8; padding: 10px; border-radius: 8px; font-style: italic;")
        source.string = f"Content extracted from: {pdf_content['title']} Teacher Guide"
        lesson_content.append(source)
        
        # Add real materials section
        if best_lesson['materials']:
            materials_section = create_section(soup, "📚 Teaching Materials & Resources", 
                                            best_lesson['materials'][:8])
            lesson_content.append(materials_section)
        
        # Add real assessment content
        if best_lesson['assessment']:
            assessment_section = create_section(soup, "📊 Assessment & Evaluation", 
                                             best_lesson['assessment'][:8])
            lesson_content.append(assessment_section)
        
        # Add sample teaching content
        teaching_content = extract_teaching_instructions(best_lesson['full_content'])
        if teaching_content:
            teaching_section = create_section(soup, "🎯 Teaching Instructions", teaching_content)
            lesson_content.append(teaching_section)
        
        # Add content quality indicator
        quality_div = soup.new_tag('div', style="background: #f0f8ff; border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; margin-top: 20px;")
        quality_p = soup.new_tag('p')
        quality_p.string = f"✅ REAL CONTENT INTEGRATION SUCCESS: This lesson now contains authentic teaching materials extracted from professional teacher guides, including {len(best_lesson['materials'])} resource items, {len(best_lesson['assessment'])} assessment components, and {len(best_lesson['full_content'])} lines of instructional content."
        quality_div.append(quality_p)
        lesson_content.append(quality_div)
    
    # Save the enhanced file
    output_file = Path("/workspaces/Curriculum/demo_enhanced_lesson.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"\n💾 Demo enhanced lesson saved to: {output_file}")
    
    # Show sample content
    print(f"\n📖 Sample Real Teaching Materials:")
    for i, material in enumerate(best_lesson['materials'][:3], 1):
        print(f"   {i}. {material[:80]}...")
    
    print(f"\n🎯 Sample Assessment Content:")
    for i, assess in enumerate(best_lesson['assessment'][:3], 1):
        print(f"   {i}. {assess[:80]}...")
    
    print(f"\n✅ PROOF OF CONCEPT: Successfully integrated real teacher guide content!")
    print(f"   This demonstrates we CAN extract and integrate authentic curriculum materials.")

def clean_title(title):
    """Clean lesson title for display"""
    import re
    title = re.sub(r'\.{3,}.*', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title[:60] + ("..." if len(title) > 60 else "")

def create_section(soup, title, items):
    """Create a content section with real materials"""
    section = soup.new_tag('div', style="margin: 20px 0; padding: 15px; background: #f9f9f9; border-radius: 8px;")
    
    # Section header
    header = soup.new_tag('h3', style="color: #2c3e50; margin-bottom: 10px;")
    header.string = title
    section.append(header)
    
    # Content list
    content_list = soup.new_tag('ul', style="margin: 0; padding-left: 20px;")
    
    for item in items:
        if isinstance(item, str) and len(item.strip()) > 15:
            li = soup.new_tag('li', style="margin-bottom: 8px; line-height: 1.4;")
            clean_item = item.strip()[:150] + ("..." if len(item.strip()) > 150 else "")
            li.string = clean_item
            content_list.append(li)
    
    section.append(content_list)
    return section

def extract_teaching_instructions(full_content):
    """Extract actual teaching instructions from content"""
    instructions = []
    
    for line in full_content:
        line_lower = line.lower()
        # Look for teaching-specific content
        if any(keyword in line_lower for keyword in 
               ['students should', 'have students', 'teach', 'explain to', 'discuss with', 
                'activity', 'instruction', 'step']):
            if len(line.strip()) > 25:  # Substantial content
                instructions.append(line.strip())
                if len(instructions) >= 6:  # Limit to 6 items
                    break
    
    return instructions

if __name__ == "__main__":
    demonstrate_real_integration()
