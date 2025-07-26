#!/usr/bin/env python3
"""
Extract content from the uncompressed US Teacher Guide PDF
"""

import sys
import json
import traceback
from intelligent_pdf_extractor import IntelligentPDFExtractor

def extract_us_pdf():
    """Extract content from US Teacher Guide PDF with detailed logging"""
    
    print('🇺🇸 EXTRACTING FROM UNCOMPRESSED US TEACHER GUIDE PDF')
    print('=' * 60)
    
    extractor = IntelligentPDFExtractor()
    pdf_path = 'The United States Teacher Guide PDF.pdf'
    
    print(f'📚 Processing: {pdf_path}')
    print('⏱️  Starting extraction...')
    
    try:
        # Check if file exists
        import os
        if not os.path.exists(pdf_path):
            print(f'❌ File not found: {pdf_path}')
            return False
            
        file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # MB
        print(f'📁 File size: {file_size:.1f} MB')
        
        # Extract with timeout protection
        result = extractor.process_pdf(pdf_path)
        
        if result and result.get('success'):
            print(f'   📄 Extracted {result["pages"]} pages')
            print(f'   🎯 Found {len(result["lessons"])} potential lessons')
            
            total_quality = 0
            for i, lesson in enumerate(result['lessons'], 1):
                title = lesson['title'][:70] + '...' if len(lesson['title']) > 70 else lesson['title']
                print(f'   ✅ Lesson {i}: {title}')
                print(f'      📊 Quality: {lesson["quality_score"]}, Length: {len(lesson["content"])} chars')
                total_quality += lesson['quality_score']
            
            print(f'   🏆 Total quality score: {total_quality}')
            
            # Save results
            output_file = 'us_teacher_guide_extracted_content.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f'   💾 Results saved to: {output_file}')
            print(f'   ✅ SUCCESS: US PDF extraction completed!')
            return True
            
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
            print(f'   ❌ Extraction failed: {error_msg}')
            return False
            
    except KeyboardInterrupt:
        print('\n🛑 Extraction interrupted by user')
        return False
    except Exception as e:
        print(f'   💥 Exception occurred: {str(e)}')
        print('🔍 Full traceback:')
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = extract_us_pdf()
    sys.exit(0 if success else 1)
