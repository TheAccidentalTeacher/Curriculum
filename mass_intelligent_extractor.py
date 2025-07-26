#!/usr/bin/env python3
"""
Mass Intelligent PDF Content Extractor
Uses proven intelligent extraction to process all curriculum PDFs
"""

import os
import json
from pathlib import Path
from intelligent_pdf_extractor import IntelligentPDFExtractor
import sys

def mass_extract_all_pdfs():
    """Extract content from all PDFs using intelligent extraction"""
    extractor = IntelligentPDFExtractor()
    pdf_dir = Path("/workspaces/Curriculum/Compressed")
    
    # Get all PDFs
    pdfs = list(pdf_dir.glob("*.pdf"))
    
    print(f"🚀 Mass Intelligent PDF Extraction")
    print(f"=" * 60)
    print(f"📚 Processing {len(pdfs)} PDFs...")
    
    all_results = {}
    successful_extractions = 0
    total_lessons = 0
    
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"\n[{i}/{len(pdfs)}] 📖 Processing: {pdf_path.name}")
        
        # Suppress stderr for PDF warnings
        original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        try:
            content = extractor.process_pdf(pdf_path)
            
            if content and content['lessons']:
                all_results[content['title']] = content
                successful_extractions += 1
                total_lessons += content['lessons_found']
                
                # Analyze content quality
                total_sections = 0
                for lesson in content['lessons']:
                    total_sections += sum(len(lesson[key]) for key in 
                                        ['objectives', 'materials', 'procedures', 'assessment', 'vocabulary'])
                
                print(f"   ✅ Success: {content['lessons_found']} lessons, {total_sections} sections")
                
                # Show best lesson title
                if content['lessons']:
                    best_lesson = max(content['lessons'], key=lambda x: len(x['full_content']))
                    print(f"   📖 Best lesson: {best_lesson['title'][:70]}...")
            else:
                print(f"   ⚠️  No structured lessons found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        finally:
            sys.stderr.close()
            sys.stderr = original_stderr
    
    print(f"\n🎯 Mass Extraction Summary")
    print(f"=" * 40)
    print(f"📊 Successful extractions: {successful_extractions}/{len(pdfs)}")
    print(f"📚 Total lessons extracted: {total_lessons}")
    print(f"💾 Success rate: {successful_extractions/len(pdfs)*100:.1f}%")
    
    if all_results:
        # Save all results
        output_file = Path("/workspaces/Curriculum/mass_intelligent_extraction.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 All results saved to: {output_file}")
        
        # Show top content sources
        sorted_results = sorted(all_results.items(), 
                              key=lambda x: x[1]['lessons_found'], reverse=True)
        
        print(f"\n🏆 Top Content Sources:")
        for i, (title, content) in enumerate(sorted_results[:5], 1):
            print(f"   {i}. {title}: {content['lessons_found']} lessons ({content['total_pages']} pages)")
        
        # Calculate total content extracted
        total_content_lines = sum(
            sum(len(lesson['full_content']) for lesson in content['lessons'])
            for content in all_results.values()
        )
        
        print(f"\n📈 Content Statistics:")
        print(f"   Total content lines: {total_content_lines:,}")
        print(f"   Average lessons per PDF: {total_lessons/successful_extractions:.1f}")
        
        # Create summary for integration
        create_integration_summary(all_results)
        
    else:
        print("❌ No content successfully extracted")

def create_integration_summary(all_results):
    """Create a summary for lesson integration"""
    summary = {
        'extraction_date': str(Path(__file__).stat().st_mtime),
        'total_pdfs_processed': len(all_results),
        'curriculum_modules': {},
        'lesson_catalog': []
    }
    
    for title, content in all_results.items():
        # Categorize by curriculum module
        summary['curriculum_modules'][title] = {
            'lessons_count': content['lessons_found'],
            'pages': content['total_pages'],
            'lesson_titles': [lesson['title'] for lesson in content['lessons']]
        }
        
        # Create lesson catalog for integration
        for lesson in content['lessons']:
            lesson_entry = {
                'source_module': title,
                'title': lesson['title'],
                'page_start': lesson['page_start'],
                'content_lines': len(lesson['full_content']),
                'has_objectives': len(lesson['objectives']) > 0,
                'has_materials': len(lesson['materials']) > 0,
                'has_procedures': len(lesson['procedures']) > 0,
                'has_assessment': len(lesson['assessment']) > 0,
                'content_quality_score': (
                    len(lesson['objectives']) * 3 +
                    len(lesson['materials']) * 2 +
                    len(lesson['procedures']) * 5 +
                    len(lesson['assessment']) * 2 +
                    len(lesson['vocabulary']) * 1
                )
            }
            summary['lesson_catalog'].append(lesson_entry)
    
    # Sort lessons by quality
    summary['lesson_catalog'].sort(key=lambda x: x['content_quality_score'], reverse=True)
    
    # Save integration summary
    summary_file = Path("/workspaces/Curriculum/lesson_integration_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Integration summary saved to: {summary_file}")
    
    # Show top quality lessons
    print(f"\n⭐ Top Quality Lessons for Integration:")
    for i, lesson in enumerate(summary['lesson_catalog'][:5], 1):
        print(f"   {i}. {lesson['source_module']}: {lesson['title'][:50]}...")
        print(f"      Quality score: {lesson['content_quality_score']} | Lines: {lesson['content_lines']}")

if __name__ == "__main__":
    mass_extract_all_pdfs()
