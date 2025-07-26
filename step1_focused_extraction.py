#!/usr/bin/env python3
"""
Step 1 - Quick Focused Extraction
Extract from the PDFs we know work well, then proceed to mapping
"""

import json
from pathlib import Path
from intelligent_pdf_extractor import IntelligentPDFExtractor
import sys
import os

def focused_extraction():
    """Extract from the top-performing PDFs we identified"""
    extractor = IntelligentPDFExtractor()
    pdf_dir = Path("/workspaces/Curriculum/Compressed")
    
    # Focus on PDFs we know have good content
    focus_pdfs = [
        "compressed_The Eastern Mediterranean Teacher Guide PDF.pdf",
        "compressed_Western Europe Teacher Guide PDF.pdf", 
        "compressed_Japan and the Koreas Teacher Guide PDF.pdf",
        "compressed_The Human World Teacher Guide PDF.pdf",
        "compressed_Eastern Europe Teacher Guide PDF.pdf",
        "compressed_Europe before the 1700s Teacher Guide PDF.pdf"
    ]
    
    print(f"🎯 STEP 1: Focused Extraction from Top PDFs")
    print(f"=" * 50)
    print(f"📚 Processing {len(focus_pdfs)} high-quality PDFs")
    
    results = {}
    successful_count = 0
    total_lessons = 0
    
    for i, pdf_name in enumerate(focus_pdfs, 1):
        pdf_path = pdf_dir / pdf_name
        if not pdf_path.exists():
            print(f"⚠️  [{i}/{len(focus_pdfs)}] {pdf_name} not found")
            continue
            
        print(f"\n📖 [{i}/{len(focus_pdfs)}] Processing: {pdf_name}")
        
        # Suppress PDF warnings
        original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        try:
            content = extractor.process_pdf(pdf_path)
            
            if content and content['lessons']:
                results[content['title']] = content
                successful_count += 1
                total_lessons += content['lessons_found']
                
                print(f"   ✅ SUCCESS: {content['lessons_found']} lessons")
                
                # Show lesson details
                for j, lesson in enumerate(content['lessons'][:2], 1):  # Show first 2 lessons
                    print(f"      {j}. {lesson['title'][:60]}...")
                    print(f"         Materials: {len(lesson['materials'])}, Assessment: {len(lesson['assessment'])}")
            else:
                print(f"   ⚠️  No structured content found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        finally:
            sys.stderr.close()
            sys.stderr = original_stderr
    
    if results:
        # Save results
        output_file = Path("/workspaces/Curriculum/focused_extraction_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 Step 1 Complete!")
        print(f"✅ Extracted content from {successful_count} PDFs")
        print(f"📚 Total lessons available: {total_lessons}")
        print(f"💾 Results saved to: {output_file}")
        
        return True, results
    else:
        print("❌ No content extracted")
        return False, {}

if __name__ == "__main__":
    success, results = focused_extraction()
    if success:
        print(f"\n➡️  Ready for Step 2: Content Mapping")
