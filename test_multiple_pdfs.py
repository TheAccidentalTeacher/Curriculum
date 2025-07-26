#!/usr/bin/env python3
"""
Test multiple PDFs to find the best content extraction approach
"""

import os
from pathlib import Path
from intelligent_pdf_extractor import IntelligentPDFExtractor
import sys

def test_multiple_pdfs():
    """Test extraction on multiple PDFs to find best content"""
    extractor = IntelligentPDFExtractor()
    pdf_dir = Path("/workspaces/Curriculum/Compressed")
    
    # Get list of PDFs
    pdfs = list(pdf_dir.glob("*.pdf"))[:5]  # Test first 5
    
    results = []
    
    print("🔍 Testing Multiple PDFs for Best Content")
    print("=" * 60)
    
    for pdf_path in pdfs:
        print(f"\n📚 Testing: {pdf_path.name}")
        
        # Suppress stderr for PDF warnings
        original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        try:
            content = extractor.process_pdf(pdf_path)
            if content:
                results.append({
                    'file': pdf_path.name,
                    'title': content['title'],
                    'pages': content['total_pages'],
                    'lessons': content['lessons_found'],
                    'content': content
                })
                
                # Analyze content quality
                total_sections = 0
                has_objectives = False
                has_procedures = False
                
                for lesson in content['lessons']:
                    total_sections += sum(len(lesson[key]) for key in 
                                        ['objectives', 'materials', 'procedures', 'assessment', 'vocabulary'])
                    if lesson['objectives']:
                        has_objectives = True
                    if lesson['procedures']:
                        has_procedures = True
                
                print(f"   📊 Pages: {content['total_pages']}, Lessons: {content['lessons_found']}")
                print(f"   📝 Total sections: {total_sections}")
                print(f"   🎯 Has objectives: {has_objectives}")
                print(f"   🔧 Has procedures: {has_procedures}")
                
                # Show sample lesson title
                if content['lessons']:
                    print(f"   📖 Sample lesson: {content['lessons'][0]['title'][:60]}...")
            else:
                print("   ❌ No content extracted")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        finally:
            sys.stderr.close()
            sys.stderr = original_stderr
    
    # Find best results
    print(f"\n🏆 Analysis Summary:")
    print("=" * 40)
    
    if results:
        # Sort by content quality
        results.sort(key=lambda x: (
            x['lessons'] * 10 + 
            sum(len(lesson['full_content']) for lesson in x['content']['lessons'])
        ), reverse=True)
        
        print(f"📈 Best content found in:")
        for i, result in enumerate(results[:3]):
            print(f"   {i+1}. {result['title']} ({result['lessons']} lessons, {result['pages']} pages)")
        
        # Save best result
        best = results[0]
        output_file = Path("/workspaces/Curriculum/best_extracted_content.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(best['content'], f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Best content saved to: {output_file}")
        
        # Show detailed analysis of best content
        best_lesson = best['content']['lessons'][0]
        print(f"\n📖 Best Lesson Analysis:")
        print(f"   Title: {best_lesson['title']}")
        print(f"   Content lines: {len(best_lesson['full_content'])}")
        
        if best_lesson['objectives']:
            print(f"   📝 Objectives ({len(best_lesson['objectives'])}):")
            for obj in best_lesson['objectives'][:2]:
                print(f"      • {obj[:80]}...")
        
        if best_lesson['procedures']:
            print(f"   🔧 Procedures ({len(best_lesson['procedures'])}):")
            for proc in best_lesson['procedures'][:2]:
                print(f"      • {proc[:80]}...")
        
        if best_lesson['assessment']:
            print(f"   📊 Assessment ({len(best_lesson['assessment'])}):")
            for assess in best_lesson['assessment'][:2]:
                print(f"      • {assess[:80]}...")
    else:
        print("❌ No usable content found")

if __name__ == "__main__":
    test_multiple_pdfs()
