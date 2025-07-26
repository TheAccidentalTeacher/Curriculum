#!/usr/bin/env python3
"""
Advanced PDF Content Extractor for Geography Curriculum Enhancement
Properly extracts complete, structured teaching content from teacher guide PDFs
"""

import pdfplumber
import os
import json
import re
from pathlib import Path
from collections import defaultdict

def extract_structured_content(pdf_path):
    """Extract properly structured content from teacher guide PDFs"""
    
    content = {
        'title': '',
        'lessons': {},
        'teaching_materials': {},
        'full_text': '',
        'structured_sections': {}
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            
            # Extract all text with page boundaries preserved
            pages_text = []
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    pages_text.append(f"--- PAGE {page_num + 1} ---\n{page_text}")
                    full_text += page_text + "\n"
            
            content['full_text'] = full_text
            content['pages_text'] = pages_text
            
            # Extract title
            filename = os.path.basename(pdf_path)
            content['title'] = filename.replace('compressed_', '').replace(' Teacher Guide PDF.pdf', '')
            
            # Advanced lesson extraction
            content['lessons'] = extract_complete_lessons(full_text)
            
            # Extract teaching materials
            content['teaching_materials'] = extract_teaching_materials(full_text)
            
            # Extract structured sections
            content['structured_sections'] = extract_structured_sections(full_text)
            
            print(f"✅ Advanced extraction from {content['title']}")
            print(f"   📚 Complete lessons: {len(content['lessons'])}")
            print(f"   🎯 Teaching materials: {len(content['teaching_materials'])}")
            print(f"   📋 Structured sections: {len(content['structured_sections'])}")
            
    except Exception as e:
        print(f"❌ Error in advanced extraction from {pdf_path}: {e}")
    
    return content

def extract_complete_lessons(text):
    """Extract complete lesson plans with all components"""
    lessons = {}
    
    # More sophisticated lesson detection
    lesson_patterns = [
        r'Lesson\s+(\d+)[\:\s]+(.*?)\n(.*?)(?=Lesson\s+\d+|Module\s+\d+|$)',
        r'LESSON\s+(\d+)[\:\s]+(.*?)\n(.*?)(?=LESSON\s+\d+|MODULE\s+\d+|$)',
        r'Chapter\s+(\d+)[\:\s]+(.*?)\n(.*?)(?=Chapter\s+\d+|$)'
    ]
    
    for pattern in lesson_patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
        for match in matches:
            lesson_num = match.group(1)
            lesson_title = match.group(2).strip()
            lesson_content = match.group(3)
            
            # Extract detailed components from lesson content
            lesson_data = parse_lesson_components(lesson_content)
            lesson_data['title'] = lesson_title
            lesson_data['number'] = lesson_num
            
            lessons[f"lesson_{lesson_num}"] = lesson_data
    
    return lessons

def parse_lesson_components(lesson_text):
    """Parse individual lesson components"""
    components = {
        'objectives': [],
        'activities': [],
        'materials': [],
        'assessments': [],
        'procedures': [],
        'vocabulary': [],
        'big_ideas': []
    }
    
    # Extract Big Ideas
    big_idea_patterns = [
        r'Big Idea[:\s]+(.*?)(?=\n\n|\n[A-Z])',
        r'The Big Idea[:\s]+(.*?)(?=\n\n|\n[A-Z])',
        r'Essential Question[:\s]+(.*?)(?=\n\n|\n[A-Z])'
    ]
    
    for pattern in big_idea_patterns:
        matches = re.findall(pattern, lesson_text, re.IGNORECASE)
        components['big_ideas'].extend([match.strip() for match in matches])
    
    # Extract Objectives - look for "Students will" patterns
    objective_patterns = [
        r'Students will[:\s]+(.*?)(?=\n|\.|Students will)',
        r'Objective[s]?[:\s]+(.*?)(?=\n\n|Materials|Activities)',
        r'Learning Goals?[:\s]+(.*?)(?=\n\n|Materials|Activities)',
        r'Main Ideas?[:\s]+(.*?)(?=\n\n|Materials|Activities)'
    ]
    
    for pattern in objective_patterns:
        matches = re.findall(pattern, lesson_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            # Clean up the objective text
            objective = re.sub(r'\s+', ' ', match.strip())
            if len(objective) > 10:  # Filter out very short fragments
                components['objectives'].append(objective)
    
    # Extract Activities - look for structured activity descriptions
    activity_patterns = [
        r'Activity[:\s]+(.*?)(?=Activity|Assessment|Materials|\n\n[A-Z])',
        r'Explore[:\s]+(.*?)(?=Activity|Assessment|Materials|\n\n[A-Z])',
        r'Practice[:\s]+(.*?)(?=Activity|Assessment|Materials|\n\n[A-Z])',
        r'Have students[:\s]+(.*?)(?=\n\n|\d+\.)',
        r'Ask students[:\s]+(.*?)(?=\n\n|\d+\.)',
        r'\d+\.\s+(.*?)(?=\d+\.|$)'
    ]
    
    for pattern in activity_patterns:
        matches = re.findall(pattern, lesson_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            activity = re.sub(r'\s+', ' ', match.strip())
            if len(activity) > 20:  # Filter out short fragments
                components['activities'].append(activity)
    
    # Extract Materials
    materials_patterns = [
        r'Materials[:\s]+(.*?)(?=Activity|Assessment|Procedure|\n\n[A-Z])',
        r'Resources[:\s]+(.*?)(?=Activity|Assessment|Procedure|\n\n[A-Z])',
        r'Supplies[:\s]+(.*?)(?=Activity|Assessment|Procedure|\n\n[A-Z])'
    ]
    
    for pattern in materials_patterns:
        matches = re.findall(pattern, lesson_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            # Split materials into individual items
            material_items = re.split(r'\n|•|•|\*', match)
            for item in material_items:
                item = item.strip()
                if len(item) > 3:
                    components['materials'].append(item)
    
    # Extract Assessment information
    assessment_patterns = [
        r'Assessment[:\s]+(.*?)(?=Activity|Materials|Procedure|\n\n[A-Z])',
        r'Evaluate[:\s]+(.*?)(?=Activity|Materials|Procedure|\n\n[A-Z])',
        r'Quiz[:\s]+(.*?)(?=Activity|Materials|Procedure|\n\n[A-Z])'
    ]
    
    for pattern in assessment_patterns:
        matches = re.findall(pattern, lesson_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            assessment = re.sub(r'\s+', ' ', match.strip())
            if len(assessment) > 10:
                components['assessments'].append(assessment)
    
    return components

def extract_teaching_materials(text):
    """Extract broader teaching materials and resources"""
    materials = {
        'worksheets': [],
        'primary_sources': [],
        'multimedia': [],
        'assessments': [],
        'vocabulary_lists': []
    }
    
    # Extract worksheet references
    worksheet_patterns = [
        r'worksheet[:\s]+(.*?)(?=\n|\.|Activity)',
        r'handout[:\s]+(.*?)(?=\n|\.|Activity)',
        r'graphic organizer[:\s]+(.*?)(?=\n|\.|Activity)'
    ]
    
    for pattern in worksheet_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        materials['worksheets'].extend([match.strip() for match in matches])
    
    # Extract primary source references
    primary_source_patterns = [
        r'primary source[:\s]+(.*?)(?=\n|\.|Activity)',
        r'document[:\s]+(.*?)(?=\n|\.|Activity)',
        r'historical[:\s]+(.*?)(?=\n|\.|Activity)'
    ]
    
    for pattern in primary_source_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        materials['primary_sources'].extend([match.strip() for match in matches])
    
    return materials

def extract_structured_sections(text):
    """Extract major structured sections from the guide"""
    sections = {}
    
    # Look for major section headers
    section_patterns = [
        r'(Module\s+\d+.*?)\n(.*?)(?=Module\s+\d+|$)',
        r'(Chapter\s+\d+.*?)\n(.*?)(?=Chapter\s+\d+|$)',
        r'(Unit\s+\d+.*?)\n(.*?)(?=Unit\s+\d+|$)'
    ]
    
    for pattern in section_patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
        for match in matches:
            section_title = match.group(1).strip()
            section_content = match.group(2)
            
            sections[section_title] = {
                'content': section_content[:2000],  # First 2000 chars
                'lessons': extract_section_lessons(section_content)
            }
    
    return sections

def extract_section_lessons(section_text):
    """Extract lessons from a section"""
    lessons = []
    
    # Look for lesson references within sections
    lesson_refs = re.findall(r'Lesson\s+\d+[:\s]+(.*?)(?=\n|Lesson)', section_text, re.IGNORECASE)
    for ref in lesson_refs:
        if len(ref.strip()) > 10:
            lessons.append(ref.strip())
    
    return lessons

def analyze_content_quality(content):
    """Analyze the quality of extracted content"""
    quality_report = {
        'total_lessons': len(content['lessons']),
        'complete_lessons': 0,
        'has_objectives': 0,
        'has_activities': 0,
        'content_richness': 0
    }
    
    for lesson_key, lesson in content['lessons'].items():
        if lesson.get('objectives') and lesson.get('activities'):
            quality_report['complete_lessons'] += 1
        
        if lesson.get('objectives'):
            quality_report['has_objectives'] += 1
            
        if lesson.get('activities'):
            quality_report['has_activities'] += 1
    
    # Calculate content richness score
    total_content = sum([
        len(content['lessons']),
        len(content['teaching_materials'].get('worksheets', [])),
        len(content['structured_sections'])
    ])
    
    quality_report['content_richness'] = total_content
    
    return quality_report

def main():
    """Test advanced extraction on a PDF"""
    pdf_dir = Path("/workspaces/Curriculum/Compressed")
    
    # Test with A Geographer's World first
    test_pdf = pdf_dir / "compressed_A Geographer_s World Teacher Guide PDF.pdf"
    
    if test_pdf.exists():
        print(f"🔍 Advanced extraction from: {test_pdf.name}")
        content = extract_structured_content(test_pdf)
        
        # Analyze content quality
        quality = analyze_content_quality(content)
        print(f"\n📊 Content Quality Report:")
        print(f"   Total lessons found: {quality['total_lessons']}")
        print(f"   Complete lessons: {quality['complete_lessons']}")
        print(f"   Lessons with objectives: {quality['has_objectives']}")
        print(f"   Lessons with activities: {quality['has_activities']}")
        print(f"   Content richness score: {quality['content_richness']}")
        
        # Show sample lesson content
        if content['lessons']:
            sample_lesson = list(content['lessons'].values())[0]
            print(f"\n📚 Sample Lesson Content:")
            print(f"   Title: {sample_lesson.get('title', 'N/A')}")
            print(f"   Big Ideas: {len(sample_lesson.get('big_ideas', []))}")
            print(f"   Objectives: {len(sample_lesson.get('objectives', []))}")
            print(f"   Activities: {len(sample_lesson.get('activities', []))}")
            
            if sample_lesson.get('objectives'):
                print(f"   Sample Objective: {sample_lesson['objectives'][0][:100]}...")
        
        # Save advanced content for review
        output_file = Path("/workspaces/Curriculum/advanced_extracted_content.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Advanced content saved to: {output_file}")
        
    else:
        print(f"❌ PDF not found: {test_pdf}")

if __name__ == "__main__":
    main()
