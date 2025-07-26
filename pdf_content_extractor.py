#!/usr/bin/env python3
"""
PDF Content Extractor for Geography Curriculum Enhancement
Extracts teaching content from teacher guide PDFs to enhance lesson files
"""

import pdfplumber
import os
import json
import re
from pathlib import Path

def extract_pdf_content(pdf_path):
    """Extract text content from a PDF file"""
    content = {
        'title': '',
        'lessons': [],
        'objectives': [],
        'activities': [],
        'materials': [],
        'assessments': [],
        'primary_sources': [],
        'full_text': ''
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
            
            content['full_text'] = full_text
            
            # Extract title from filename
            filename = os.path.basename(pdf_path)
            content['title'] = filename.replace('compressed_', '').replace(' Teacher Guide PDF.pdf', '')
            
            # Extract lessons (look for patterns like "Lesson 1:", "Activity:", etc.)
            lessons = re.findall(r'Lesson\s+\d+[:\.].*?(?=Lesson\s+\d+|$)', full_text, re.DOTALL | re.IGNORECASE)
            content['lessons'] = lessons[:10]  # Limit to first 10 lessons
            
            # Extract objectives (look for patterns)
            objectives = re.findall(r'(?:objective|goal|students will).*?(?:\n|\.)', full_text, re.IGNORECASE)
            content['objectives'] = objectives[:5]
            
            # Extract activities
            activities = re.findall(r'(?:activity|instruction|procedure).*?(?:\n\n|\d+\.)', full_text, re.IGNORECASE)
            content['activities'] = activities[:10]
            
            # Extract materials
            materials = re.findall(r'(?:materials|supplies|resources).*?(?:\n\n|[A-Z])', full_text, re.IGNORECASE)
            content['materials'] = materials[:5]
            
            print(f"✅ Extracted content from {content['title']}")
            print(f"   - Found {len(content['lessons'])} lessons")
            print(f"   - Found {len(content['objectives'])} objectives")
            print(f"   - Found {len(content['activities'])} activities")
            
    except Exception as e:
        print(f"❌ Error extracting from {pdf_path}: {e}")
    
    return content

def main():
    """Test extraction on the first PDF"""
    pdf_dir = Path("/workspaces/Curriculum/Compressed")
    
    # Test with A Geographer's World first
    test_pdf = pdf_dir / "compressed_A Geographer_s World Teacher Guide PDF.pdf"
    
    if test_pdf.exists():
        print(f"🔍 Extracting content from: {test_pdf.name}")
        content = extract_pdf_content(test_pdf)
        
        # Save sample content for review
        output_file = Path("/workspaces/Curriculum/sample_extracted_content.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Sample content saved to: {output_file}")
        print(f"📊 Full text length: {len(content['full_text'])} characters")
        
        # Show first few lines of extracted text
        lines = content['full_text'].split('\n')[:20]
        print("\n📖 First 20 lines of extracted text:")
        for i, line in enumerate(lines, 1):
            if line.strip():
                print(f"{i:2d}: {line.strip()[:80]}...")
    else:
        print(f"❌ PDF not found: {test_pdf}")

if __name__ == "__main__":
    main()
