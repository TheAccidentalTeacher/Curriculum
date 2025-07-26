#!/usr/bin/env python3

import json
import glob
from pathlib import Path

def summarize_extraction():
    """Summarize all PDF extraction progress"""
    print("📊 PDF Content Extraction Summary")
    print("=" * 50)
    
    # Find all progress files
    progress_files = sorted(glob.glob('progress_batch_*.json'))
    
    total_pdfs = 0
    total_characters = 0
    total_lessons = 0
    total_objectives = 0
    total_activities = 0
    
    geography_pdfs = []
    
    for progress_file in progress_files:
        with open(progress_file, 'r') as f:
            data = json.load(f)
        
        batch_num = progress_file.replace('progress_batch_', '').replace('.json', '')
        print(f"\n📄 Batch {batch_num} ({len(data)} PDFs):")
        
        for pdf_name, content in data.items():
            total_pdfs += 1
            
            # Count characters
            char_count = len(str(content))
            total_characters += char_count
            
            # Count lessons, objectives, activities
            lessons = content.get('lessons', {})
            objectives = content.get('objectives', {})
            activities = content.get('activities', {})
            
            lesson_count = len(lessons)
            objective_count = len(objectives)
            activity_count = len(activities)
            
            total_lessons += lesson_count
            total_objectives += objective_count
            total_activities += activity_count
            
            # Check if geography-related
            geography_keywords = ['geography', 'world', 'europe', 'asia', 'africa', 'america', 'civilizations', 'mediterranean', 'china', 'india', 'oceania']
            if any(keyword in pdf_name.lower() for keyword in geography_keywords):
                geography_pdfs.append(pdf_name)
            
            print(f"  • {pdf_name}")
            print(f"    📝 {char_count:,} chars | 📚 {lesson_count} lessons | 🎯 {objective_count} objectives | 🎲 {activity_count} activities")
    
    # Overall summary
    print(f"\n🎯 TOTAL EXTRACTION RESULTS:")
    print(f"📚 PDFs Processed: {total_pdfs}")
    print(f"📝 Total Characters: {total_characters:,}")
    print(f"📖 Total Lessons: {total_lessons}")
    print(f"🎯 Total Objectives: {total_objectives}")
    print(f"🎲 Total Activities: {total_activities}")
    
    # Geography-specific summary
    print(f"\n🌍 GEOGRAPHY-RELATED CONTENT:")
    print(f"📚 Geography PDFs: {len(geography_pdfs)}")
    for pdf in geography_pdfs:
        print(f"  • {pdf}")
    
    # File size summary
    print(f"\n💾 FILE SIZES:")
    for progress_file in progress_files:
        size = Path(progress_file).stat().st_size
        print(f"  • {progress_file}: {size:,} bytes ({size/1024/1024:.1f} MB)")
    
    print(f"\n✅ Mass lesson enhancement completed with {total_pdfs} PDFs worth of authentic curriculum content!")

if __name__ == "__main__":
    summarize_extraction()
