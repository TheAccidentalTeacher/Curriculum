#!/usr/bin/env python3
"""
Intelligent PDF Content Extractor for Geography Curriculum
Extracts complete, coherent lesson content using advanced parsing techniques
"""

import pdfplumber
import os
import json
import re
from pathlib import Path
import warnings

# Suppress the PDF color warnings completely
warnings.filterwarnings("ignore", category=UserWarning)

class IntelligentPDFExtractor:
    def __init__(self):
        # Patterns to identify lesson starts
        self.lesson_start_patterns = [
            r'^(LESSON\s+\d+)\s*[:\-]\s*(.+?)$',
            r'^(Lesson\s+\d+)\s*[:\-]\s*(.+?)$',
            r'^\d+\.\d+\s+(.+?)$',  # 1.1 Some Title
            r'^Unit\s+\d+\s+Lesson\s+\d+\s*[:\-]\s*(.+?)$'
        ]
        
        # Patterns to identify section headers within lessons
        self.section_patterns = {
            'objectives': r'(?:Objectives?|Learning Goals?|Students will learn)[:\s]*',
            'materials': r'(?:Materials?|Resources?|You Will Need)[:\s]*',
            'procedures': r'(?:Procedures?|Instructions?|Teaching Steps?|Activities?)[:\s]*',
            'assessment': r'(?:Assessment|Evaluation|Check Understanding)[:\s]*',
            'vocabulary': r'(?:Vocabulary|Key Terms?|Important Words?)[:\s]*'
        }

    def extract_text_by_pages(self, pdf_path):
        """Extract text page by page to maintain structure"""
        pages = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append({
                        'page_num': i + 1,
                        'text': text,
                        'lines': [line.strip() for line in text.split('\n') if line.strip()]
                    })
        
        return pages

    def find_lesson_sections(self, pages):
        """Find lessons by looking for consistent patterns across pages"""
        all_lines = []
        line_to_page = {}
        
        # Collect all lines with page references
        for page in pages:
            for line in page['lines']:
                line_num = len(all_lines)
                all_lines.append(line)
                line_to_page[line_num] = page['page_num']
        
        lessons = []
        current_lesson = None
        
        for i, line in enumerate(all_lines):
            # Check if this line starts a new lesson
            for pattern in self.lesson_start_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # Save previous lesson if exists
                    if current_lesson:
                        lessons.append(current_lesson)
                    
                    # Start new lesson
                    current_lesson = {
                        'title': line,
                        'start_line': i,
                        'start_page': line_to_page[i],
                        'content_lines': [line],
                        'sections': {}
                    }
                    break
            else:
                # Add line to current lesson if we're in one
                if current_lesson:
                    current_lesson['content_lines'].append(line)
                    
                    # Check for section headers
                    for section_name, pattern in self.section_patterns.items():
                        if re.match(pattern, line, re.IGNORECASE):
                            current_lesson['sections'][section_name] = {
                                'start_line': i,
                                'header': line,
                                'content': []
                            }
        
        # Add final lesson
        if current_lesson:
            lessons.append(current_lesson)
        
        return lessons

    def extract_section_content(self, lesson, section_name):
        """Extract content for a specific section within a lesson"""
        if section_name not in lesson['sections']:
            return []
        
        section = lesson['sections'][section_name]
        section_start = section['start_line'] - lesson['start_line']
        
        # Find where this section ends (next section or lesson end)
        section_end = len(lesson['content_lines'])
        for other_section in lesson['sections'].values():
            other_start = other_section['start_line'] - lesson['start_line']
            if other_start > section_start and other_start < section_end:
                section_end = other_start
        
        # Extract content between section start and end
        content_lines = lesson['content_lines'][section_start + 1:section_end]
        
        # Clean and filter content
        clean_content = []
        for line in content_lines:
            # Skip very short lines, page numbers, headers
            if len(line) > 15 and not re.match(r'^\d+$', line):
                clean_content.append(line)
        
        return clean_content

    def process_pdf(self, pdf_path):
        """Main processing function"""
        print(f"📚 Processing: {os.path.basename(pdf_path)}")
        
        # Extract pages
        pages = self.extract_text_by_pages(pdf_path)
        if not pages:
            return None
        
        print(f"   📄 Extracted {len(pages)} pages")
        
        # Find lessons
        lessons = self.find_lesson_sections(pages)
        print(f"   🎯 Found {len(lessons)} potential lessons")
        
        # Process each lesson
        processed_lessons = []
        for lesson in lessons:
            processed_lesson = {
                'title': lesson['title'],
                'page_start': lesson['start_page'],
                'content_preview': ' '.join(lesson['content_lines'][:3]),
                'objectives': self.extract_section_content(lesson, 'objectives'),
                'materials': self.extract_section_content(lesson, 'materials'),
                'procedures': self.extract_section_content(lesson, 'procedures'),
                'assessment': self.extract_section_content(lesson, 'assessment'),
                'vocabulary': self.extract_section_content(lesson, 'vocabulary'),
                'full_content': lesson['content_lines']
            }
            
            # Only include lessons with substantial content
            total_content = sum(len(processed_lesson[key]) for key in 
                              ['objectives', 'materials', 'procedures', 'assessment', 'vocabulary'])
            
            if total_content > 0 or len(processed_lesson['full_content']) > 10:
                processed_lessons.append(processed_lesson)
                print(f"   ✅ Lesson: {processed_lesson['title'][:60]}...")
        
        # Extract title
        filename = os.path.basename(pdf_path)
        title = filename.replace('compressed_', '').replace(' Teacher Guide PDF.pdf', '')
        
        return {
            'title': title,
            'total_pages': len(pages),
            'lessons_found': len(processed_lessons),
            'lessons': processed_lessons
        }

def test_intelligent_extraction():
    """Test the intelligent extractor"""
    extractor = IntelligentPDFExtractor()
    
    pdf_dir = Path("/workspaces/Curriculum/Compressed")
    test_pdf = pdf_dir / "compressed_A Geographer_s World Teacher Guide PDF.pdf"
    
    if not test_pdf.exists():
        print(f"❌ Test PDF not found: {test_pdf}")
        return
    
    print("🧠 Testing Intelligent PDF Extraction")
    print("=" * 50)
    
    # Suppress stderr to hide PDF warnings
    import sys
    original_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    
    try:
        content = extractor.process_pdf(test_pdf)
    finally:
        sys.stderr.close()
        sys.stderr = original_stderr
    
    if content and content['lessons']:
        print(f"\n📊 Extraction Results:")
        print(f"   Title: {content['title']}")
        print(f"   Pages: {content['total_pages']}")
        print(f"   Lessons: {content['lessons_found']}")
        
        # Show first lesson details
        lesson = content['lessons'][0]
        print(f"\n📖 First Lesson Analysis:")
        print(f"   Title: {lesson['title']}")
        print(f"   Page: {lesson['page_start']}")
        print(f"   Objectives: {len(lesson['objectives'])}")
        print(f"   Materials: {len(lesson['materials'])}")
        print(f"   Procedures: {len(lesson['procedures'])}")
        print(f"   Assessment: {len(lesson['assessment'])}")
        print(f"   Vocabulary: {len(lesson['vocabulary'])}")
        print(f"   Total content lines: {len(lesson['full_content'])}")
        
        if lesson['objectives']:
            print(f"\n   📝 Sample Objective:")
            print(f"      {lesson['objectives'][0]}")
        
        if lesson['procedures']:
            print(f"\n   🔧 Sample Procedure:")
            print(f"      {lesson['procedures'][0]}")
        
        # Save results
        output_file = Path("/workspaces/Curriculum/intelligent_extracted_content.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Show a sample of raw content for verification
        print(f"\n📄 Sample Raw Content (first 5 lines):")
        for i, line in enumerate(lesson['full_content'][:5]):
            print(f"   {i+1}: {line}")
            
    else:
        print("❌ No coherent lessons found")

if __name__ == "__main__":
    test_intelligent_extraction()
