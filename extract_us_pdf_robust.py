#!/usr/bin/env python3
"""
Robust US PDF Extractor with memory management and error handling
"""

import sys
import json
import traceback
import gc
import os
from pathlib import Path

def extract_us_pdf_robust():
    """Extract content from US PDF with robust error handling"""
    
    print('🇺🇸 ROBUST US TEACHER GUIDE PDF EXTRACTION')
    print('=' * 60)
    
    pdf_path = 'The United States Teacher Guide PDF.pdf'
    
    if not os.path.exists(pdf_path):
        print(f'❌ File not found: {pdf_path}')
        return False
        
    file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # MB
    print(f'📁 File size: {file_size:.1f} MB')
    
    # Try PyPDF2 first (more memory efficient for large files)
    print('🔄 Attempting extraction with PyPDF2...')
    try:
        import PyPDF2
        
        extracted_text = ""
        page_count = 0
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            page_count = len(pdf_reader.pages)
            print(f'📄 Total pages: {page_count}')
            
            # Process in smaller chunks to avoid memory issues
            chunk_size = 10
            for start_page in range(0, min(page_count, 50), chunk_size):  # Limit to first 50 pages
                end_page = min(start_page + chunk_size, min(page_count, 50))
                print(f'📖 Processing pages {start_page + 1}-{end_page}...')
                
                chunk_text = ""
                for page_num in range(start_page, end_page):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            chunk_text += f"\\n\\n--- Page {page_num + 1} ---\\n{page_text}"
                    except Exception as e:
                        print(f'⚠️  Warning: Could not extract page {page_num + 1}: {str(e)}')
                        continue
                
                extracted_text += chunk_text
                
                # Force garbage collection after each chunk
                gc.collect()
        
        if extracted_text.strip():
            print('✅ Text extraction successful!')
            
            # Look for lesson patterns in the extracted text
            lessons = find_lesson_patterns(extracted_text)
            
            result = {
                'success': True,
                'pages': min(page_count, 50),
                'lessons': lessons,
                'total_text_length': len(extracted_text),
                'extraction_method': 'PyPDF2'
            }
            
            # Save results
            output_file = 'us_teacher_guide_extracted_content.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f'📊 Extracted {len(extracted_text)} characters from {min(page_count, 50)} pages')
            print(f'🎯 Found {len(lessons)} potential lessons')
            
            for i, lesson in enumerate(lessons, 1):
                title = lesson['title'][:70] + '...' if len(lesson['title']) > 70 else lesson['title']
                print(f'   ✅ Lesson {i}: {title}')
                print(f'      📊 Quality: {lesson["quality_score"]}, Length: {len(lesson["content"])} chars')
            
            print(f'💾 Results saved to: {output_file}')
            return True
        else:
            print('❌ No text could be extracted')
            return False
            
    except ImportError:
        print('❌ PyPDF2 not available, trying alternative method...')
    except Exception as e:
        print(f'❌ PyPDF2 extraction failed: {str(e)}')
    
    return False

def find_lesson_patterns(text):
    """Find lesson patterns in extracted text"""
    lessons = []
    
    # Patterns to identify lesson content
    import re
    lesson_patterns = [
        r'LESSON\s+(\d+)\s*[:\-]\s*(.+?)(?=LESSON\s+\d+|$)',
        r'Lesson\s+(\d+)\s*[:\-]\s*(.+?)(?=Lesson\s+\d+|$)',
        r'Unit\s+\d+\s+Lesson\s+(\d+)\s*[:\-]\s*(.+?)(?=Unit\s+\d+\s+Lesson\s+\d+|$)'
    ]
    
    for pattern in lesson_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            lesson_num = match.group(1)
            lesson_content = match.group(2).strip()
            
            if len(lesson_content) > 200:  # Only include substantial content
                # Extract title from first line
                lines = lesson_content.split('\\n')
                title = lines[0].strip() if lines else f"Lesson {lesson_num}"
                title = title[:100]  # Limit title length
                
                lessons.append({
                    'lesson_number': lesson_num,
                    'title': title,
                    'content': lesson_content[:5000],  # Limit content length
                    'quality_score': min(len(lesson_content), 5000),
                    'extraction_confidence': 'medium'
                })
    
    # If no formal lessons found, look for other structured content
    if not lessons:
        # Look for sections that might contain lesson content
        sections = re.split(r'\\n\\s*\\n', text)
        for i, section in enumerate(sections):
            if len(section) > 500:  # Substantial content
                lines = section.split('\\n')
                title = lines[0].strip() if lines else f"Section {i+1}"
                
                lessons.append({
                    'lesson_number': str(i+1),
                    'title': title[:100],
                    'content': section[:3000],
                    'quality_score': min(len(section), 3000),
                    'extraction_confidence': 'low'
                })
                
                if len(lessons) >= 10:  # Limit number of sections
                    break
    
    return lessons

if __name__ == '__main__':
    success = extract_us_pdf_robust()
    sys.exit(0 if success else 1)
