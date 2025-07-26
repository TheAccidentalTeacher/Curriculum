#!/usr/bin/env python3
"""
Step 1: Systematic Mass PDF Extraction
Scale up intelligent extraction to process all 32 PDFs systematically
"""

import os
import json
from pathlib import Path
from intelligent_pdf_extractor import IntelligentPDFExtractor
import sys
import time

def systematic_mass_extraction():
    """Systematically extract content from all PDFs with progress tracking"""
    extractor = IntelligentPDFExtractor()
    pdf_dir = Path("/workspaces/Curriculum/Compressed")
    
    # Get all PDFs
    pdfs = list(pdf_dir.glob("*.pdf"))
    
    print(f"🚀 STEP 1: Systematic Mass PDF Extraction")
    print(f"=" * 60)
    print(f"📚 Found {len(pdfs)} PDFs to process")
    print(f"🎯 Goal: Extract structured lesson content from all teacher guides")
    
    results = {}
    extraction_log = []
    successful_count = 0
    failed_count = 0
    total_lessons = 0
    
    # Progress tracking
    start_time = time.time()
    
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"\n📖 [{i}/{len(pdfs)}] Processing: {pdf_path.name}")
        
        # Suppress stderr for PDF warnings
        original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        extraction_result = {
            'filename': pdf_path.name,
            'status': 'failed',
            'lessons_found': 0,
            'content_quality': 0,
            'error': None
        }
        
        try:
            content = extractor.process_pdf(pdf_path)
            
            if content and content['lessons']:
                # Calculate content quality score
                quality_score = calculate_content_quality(content)
                
                results[content['title']] = content
                extraction_result.update({
                    'status': 'success',
                    'lessons_found': content['lessons_found'],
                    'content_quality': quality_score,
                    'pages': content['total_pages']
                })
                
                successful_count += 1
                total_lessons += content['lessons_found']
                
                print(f"   ✅ SUCCESS: {content['lessons_found']} lessons, quality score: {quality_score}")
                
                # Show best lesson
                if content['lessons']:
                    best_lesson = max(content['lessons'], key=lambda x: len(x['full_content']))
                    print(f"   📖 Best: {best_lesson['title'][:70]}...")
            else:
                extraction_result['error'] = 'No structured content found'
                failed_count += 1
                print(f"   ⚠️  No structured lessons found")
                
        except Exception as e:
            extraction_result['error'] = str(e)
            failed_count += 1
            print(f"   ❌ Error: {e}")
        finally:
            sys.stderr.close()
            sys.stderr = original_stderr
            extraction_log.append(extraction_result)
    
    elapsed_time = time.time() - start_time
    
    # Save results and create summary
    print(f"\n🎯 STEP 1 COMPLETION SUMMARY")
    print(f"=" * 40)
    print(f"⏱️  Processing time: {elapsed_time:.1f} seconds")
    print(f"✅ Successful extractions: {successful_count}/{len(pdfs)} ({successful_count/len(pdfs)*100:.1f}%)")
    print(f"📚 Total lessons extracted: {total_lessons}")
    print(f"📊 Average lessons per successful PDF: {total_lessons/max(successful_count,1):.1f}")
    
    if results:
        # Save all extracted content
        output_file = Path("/workspaces/Curriculum/systematic_extraction_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save extraction log
        log_file = Path("/workspaces/Curriculum/extraction_log.json")
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_log, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_file}")
        print(f"📋 Extraction log saved to: {log_file}")
        
        # Show top content sources ranked by quality
        quality_ranked = sorted(results.items(), 
                              key=lambda x: calculate_content_quality(x[1]), reverse=True)
        
        print(f"\n🏆 Top 5 Content Sources (by quality):")
        for i, (title, content) in enumerate(quality_ranked[:5], 1):
            quality = calculate_content_quality(content)
            print(f"   {i}. {title}: {content['lessons_found']} lessons, quality {quality}")
        
        return True, results, extraction_log
    else:
        print("❌ No content successfully extracted")
        return False, {}, extraction_log

def calculate_content_quality(content):
    """Calculate a quality score for extracted content"""
    if not content or not content['lessons']:
        return 0
    
    total_score = 0
    for lesson in content['lessons']:
        # Score based on different content types
        lesson_score = (
            len(lesson['objectives']) * 5 +      # Objectives are highly valuable
            len(lesson['materials']) * 2 +       # Materials are valuable
            len(lesson['procedures']) * 10 +     # Procedures are most valuable
            len(lesson['assessment']) * 3 +      # Assessments are valuable
            len(lesson['vocabulary']) * 1 +      # Vocabulary is useful
            len(lesson['full_content']) * 0.1    # Raw content adds small value
        )
        total_score += lesson_score
    
    return int(total_score)

def preview_extraction_results():
    """Preview what we found in the extraction"""
    results_file = Path("/workspaces/Curriculum/systematic_extraction_results.json")
    log_file = Path("/workspaces/Curriculum/extraction_log.json")
    
    if not results_file.exists():
        print("❌ No extraction results found. Run extraction first.")
        return
    
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    with open(log_file, 'r', encoding='utf-8') as f:
        log = json.load(f)
    
    print(f"\n📊 EXTRACTION RESULTS PREVIEW")
    print(f"=" * 40)
    print(f"📚 Total curriculum modules extracted: {len(results)}")
    
    successful_extractions = [entry for entry in log if entry['status'] == 'success']
    total_lessons = sum(entry['lessons_found'] for entry in successful_extractions)
    
    print(f"✅ Successful PDFs: {len(successful_extractions)}")
    print(f"📖 Total lessons available: {total_lessons}")
    
    # Show sample of what we can work with
    print(f"\n📖 Sample Available Content:")
    for i, (title, content) in enumerate(list(results.items())[:3], 1):
        print(f"   {i}. {title}:")
        print(f"      - {content['lessons_found']} lessons")
        print(f"      - {content['total_pages']} pages")
        if content['lessons']:
            sample_lesson = content['lessons'][0]
            print(f"      - Sample: {sample_lesson['title'][:50]}...")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run systematic extraction")
    print("2. Preview existing results")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        success, results, log = systematic_mass_extraction()
        if success:
            print(f"\n🎉 Step 1 Complete! Ready for Step 2: Content Mapping")
    elif choice == "2":
        preview_extraction_results()
    else:
        print("Invalid choice")
