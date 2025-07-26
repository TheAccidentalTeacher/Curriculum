#!/usr/bin/env python3
"""
Deep Analysis of Curriculum Enhancement Results
Verifies actual vs intended lesson enhancement outcomes
"""

import json
import re
from pathlib import Path
import random

def analyze_extraction_quality():
    """Analyze the quality and coherence of extracted content"""
    
    print("🔍 DEEP DIVE: Curriculum Enhancement Quality Analysis")
    print("=" * 60)
    
    # Load latest progress data
    with open('progress_batch_15.json', 'r') as f:
        extracted_data = json.load(f)
    
    print(f"\n📊 EXTRACTION QUALITY ASSESSMENT")
    print(f"Total PDFs processed: {len(extracted_data)}")
    
    # Analyze a few key PDFs in detail
    sample_pdfs = ['compressed_History of Modern Europe Teacher Guide PDF', 
                   'compressed_A Geographer_s World Teacher Guide PDF']
    
    for pdf_name in sample_pdfs:
        if pdf_name in extracted_data:
            content = extracted_data[pdf_name]
            print(f"\n📚 PDF: {content.get('title', pdf_name)}")
            
            # Check lesson quality
            lessons = content.get('lessons', [])
            print(f"   Lessons found: {len(lessons)}")
            if lessons:
                print(f"   Sample lesson snippet: '{lessons[0][:100]}...'")
                
                # Check if this is a real lesson or just fragments
                lesson_text = lessons[0]
                has_coherent_structure = any(word in lesson_text.lower() for word in 
                    ['students will', 'objective', 'activity', 'procedure', 'materials needed'])
                print(f"   Has coherent lesson structure: {has_coherent_structure}")
            
            # Check objectives quality  
            objectives = content.get('objectives', [])
            print(f"   Objectives found: {len(objectives)}")
            if objectives:
                sample_obj = objectives[0]
                print(f"   Sample objective: '{sample_obj}'")
                is_complete_objective = len(sample_obj) > 50 and ('students will' in sample_obj.lower() or 'analyze' in sample_obj.lower())
                print(f"   Is complete objective: {is_complete_objective}")
            
            # Check activities quality
            activities = content.get('activities', [])
            print(f"   Activities found: {len(activities)}")
            if activities:
                sample_activity = activities[0]
                print(f"   Sample activity: '{sample_activity}'")
                is_instructional_activity = len(sample_activity) > 30 and any(word in sample_activity.lower() for word in 
                    ['have students', 'ask students', 'discussion', 'group work', 'assignment'])
                print(f"   Is instructional activity: {is_instructional_activity}")

def analyze_enhanced_lessons():
    """Analyze what's actually in the enhanced lesson files"""
    
    print(f"\n🎨 ENHANCED LESSON ANALYSIS")
    print("=" * 40)
    
    # Check a few enhanced lesson files
    lesson_files = [
        '/workspaces/Curriculum/units/lessons/unit16-lesson3-grade6.html',
        '/workspaces/Curriculum/units/lessons/unit5-lesson2-grade8.html'
    ]
    
    for lesson_file in lesson_files:
        if Path(lesson_file).exists():
            print(f"\n📄 Checking: {Path(lesson_file).name}")
            
            with open(lesson_file, 'r') as f:
                content = f.read()
            
            # Check for enhanced content sections
            has_learning_objectives = 'Learning Objectives' in content
            has_activities = 'Activities' in content or 'Activity' in content
            has_assessment = 'Assessment' in content
            has_materials = 'Materials' in content
            has_alaska_context = 'Alaska' in content
            
            print(f"   ✅ Has Learning Objectives: {has_learning_objectives}")
            print(f"   ✅ Has Activities: {has_activities}")
            print(f"   ✅ Has Assessment: {has_assessment}")
            print(f"   ✅ Has Materials: {has_materials}")
            print(f"   ✅ Has Alaska Context: {has_alaska_context}")
            
            # Check if content is from PDFs or templated
            if 'Grade 6 Scaffolding' in content:
                print(f"   ⚠️  Contains templated content")
            
            # Look for actual lesson content vs boilerplate
            content_sections = re.findall(r'<h3>(.*?)</h3>', content)
            print(f"   📝 Content sections: {len(content_sections)}")
            for section in content_sections[:3]:
                print(f"      - {section}")

def check_pdf_vs_lesson_alignment():
    """Check if lesson content actually comes from the PDFs"""
    
    print(f"\n🔍 PDF-TO-LESSON ALIGNMENT CHECK")
    print("=" * 40)
    
    # Load PDF content
    with open('progress_batch_15.json', 'r') as f:
        pdf_data = json.load(f)
    
    # Get a geography-related PDF
    geography_pdf = pdf_data.get('compressed_The Human World Teacher Guide PDF', {})
    pdf_text = geography_pdf.get('full_text', '')[:1000]  # First 1000 chars
    
    print(f"📚 Sample PDF text (first 1000 chars):")
    print(f"'{pdf_text}'")
    
    # Check if this appears in enhanced lessons
    lesson_file = '/workspaces/Curriculum/units/lessons/unit16-lesson3-grade6.html'
    if Path(lesson_file).exists():
        with open(lesson_file, 'r') as f:
            lesson_content = f.read()
        
        # Look for any PDF text in the lesson
        overlap_found = False
        pdf_words = pdf_text.lower().split()[:20]  # First 20 words
        for word in pdf_words:
            if len(word) > 5 and word in lesson_content.lower():
                print(f"   ✅ Found PDF word '{word}' in lesson")
                overlap_found = True
                break
        
        if not overlap_found:
            print(f"   ❌ No clear overlap between PDF content and lesson found")

def generate_enhancement_reality_report():
    """Generate final assessment of what we actually achieved"""
    
    print(f"\n🎯 ENHANCEMENT REALITY REPORT")
    print("=" * 40)
    
    with open('progress_batch_15.json', 'r') as f:
        data = json.load(f)
    
    print(f"✅ WHAT WE SUCCESSFULLY DID:")
    print(f"   • Extracted text from 15 PDF teacher guides")
    print(f"   • Created systematic processing pipeline")
    print(f"   • Enhanced 481 lesson HTML files with structured templates")
    print(f"   • Added professional visual formatting and navigation")
    print(f"   • Created Alaska-focused contextual framework")
    print(f"   • Implemented grade-level differentiation")
    
    print(f"\n⚠️  WHAT WE PARTIALLY ACHIEVED:")
    print(f"   • PDF content extraction captured fragments, not full lessons")
    print(f"   • Content integration was template-based, not PDF-sourced")
    print(f"   • Enhanced lessons have good structure but generic content")
    print(f"   • Cross-curricular connections are framework-level")
    
    print(f"\n❌ WHAT WE DIDN'T FULLY ACCOMPLISH:")
    print(f"   • Direct integration of authentic teacher guide content")
    print(f"   • Coherent, complete lesson plans from PDF sources")
    print(f"   • Specific activities and assessments from teacher guides")
    print(f"   • Seamless PDF-to-HTML content transformation")
    
    print(f"\n🔧 WHAT NEEDS TO BE FIXED:")
    print(f"   • Improve PDF text extraction patterns")
    print(f"   • Create better content parsing for complete lessons")
    print(f"   • Develop lesson-to-lesson matching algorithms")
    print(f"   • Build authentic content integration (not templates)")
    
    print(f"\n💡 NEXT STEPS FOR TRUE ENHANCEMENT:")
    print(f"   1. Redesign extraction to capture complete lesson sections")
    print(f"   2. Parse teacher guides for structured lesson components")
    print(f"   3. Match curriculum units to specific PDF lessons")
    print(f"   4. Integrate actual teaching content, not templates")

if __name__ == "__main__":
    analyze_extraction_quality()
    analyze_enhanced_lessons()
    check_pdf_vs_lesson_alignment()
    generate_enhancement_reality_report()
