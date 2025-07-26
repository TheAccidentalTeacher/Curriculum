import pdfplumber
import json
import re
from pathlib import Path
import glob
import os

def extract_pdf_content(pdf_path):
    """Extract content from a PDF file."""
    content = {
        "title": "",
        "lessons": [],
        "objectives": [],
        "activities": [],
        "materials": [],
        "assessments": [],
        "primary_sources": [],
        "full_text": ""
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            content["full_text"] = full_text
            content["title"] = Path(pdf_path).stem.replace("compressed_", "").replace(" Teacher Guide PDF", "")
            
            # Extract lessons using patterns
            lesson_patterns = [
                r'Lesson \d+:.*?(?=Lesson \d+:|$)',
                r'Module \d+.*?(?=Module \d+:|$)', 
                r'Chapter \d+.*?(?=Chapter \d+:|$)',
                r'Unit \d+.*?(?=Unit \d+:|$)'
            ]
            
            for pattern in lesson_patterns:
                matches = re.findall(pattern, full_text, re.DOTALL | re.IGNORECASE)
                content["lessons"].extend([match[:500] for match in matches])
            
            # Extract objectives
            objective_patterns = [
                r'students will.*?(?=\n|\.|;)',
                r'objective[s]?:.*?(?=\n)',
                r'learning goal[s]?:.*?(?=\n)',
                r'by the end.*?(?=\n)',
                r'big idea[s]?:.*?(?=\n)',
                r'main idea[s]?:.*?(?=\n)'
            ]
            
            for pattern in objective_patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                content["objectives"].extend([match[:200] for match in matches])
            
            # Extract activities
            activity_patterns = [
                r'activity:.*?(?=\n)',
                r'exercise.*?(?=\n)',
                r'practice.*?(?=\n)',
                r'assignment.*?(?=\n)',
                r'explore.*?(?=\n)',
                r'analyze.*?(?=\n)',
                r'investigate.*?(?=\n)'
            ]
            
            for pattern in activity_patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                content["activities"].extend([match[:200] for match in matches])
            
            # Extract materials
            material_patterns = [
                r'materials:.*?(?=\n)',
                r'resources.*?(?=\n)',
                r'supplies.*?(?=\n)',
                r'tools.*?(?=\n)'
            ]
            
            for pattern in material_patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                content["materials"].extend([match[:200] for match in matches])
            
            # Extract assessments
            assessment_patterns = [
                r'assessment.*?(?=\n)',
                r'evaluation.*?(?=\n)',
                r'quiz.*?(?=\n)',
                r'test.*?(?=\n)',
                r'rubric.*?(?=\n)'
            ]
            
            for pattern in assessment_patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                content["assessments"].extend([match[:200] for match in matches])
            
            # Extract primary sources
            source_patterns = [
                r'primary source.*?(?=\n)',
                r'document.*?(?=\n)',
                r'artifact.*?(?=\n)',
                r'historical.*?(?=\n)'
            ]
            
            for pattern in source_patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                content["primary_sources"].extend([match[:200] for match in matches])
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    
    return content

def process_all_pdfs():
    """Process all PDF files in the Compressed directory."""
    pdf_directory = "/workspaces/Curriculum/Compressed"
    pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))
    
    all_extracted_content = {}
    
    print(f"Found {len(pdf_files)} PDF files to process...")
    
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\nProcessing {i}/{len(pdf_files)}: {os.path.basename(pdf_path)}")
        
        try:
            content = extract_pdf_content(pdf_path)
            filename = Path(pdf_path).stem
            all_extracted_content[filename] = content
            
            # Print summary
            print(f"  - Characters: {len(content['full_text'])}")
            print(f"  - Lessons: {len(content['lessons'])}")
            print(f"  - Objectives: {len(content['objectives'])}")
            print(f"  - Activities: {len(content['activities'])}")
            
        except Exception as e:
            print(f"  - ERROR: {e}")
    
    return all_extracted_content

# Process all PDFs
print("Starting mass PDF extraction...")
all_content = process_all_pdfs()

# Save all extracted content
output_file = "/workspaces/Curriculum/all_extracted_content.json"
with open(output_file, "w") as f:
    json.dump(all_content, f, indent=2)

print(f"\n=== EXTRACTION COMPLETE ===")
print(f"Processed {len(all_content)} PDF files")
print(f"All content saved to: {output_file}")

# Summary statistics
total_chars = sum(len(content['full_text']) for content in all_content.values())
total_lessons = sum(len(content['lessons']) for content in all_content.values())
total_objectives = sum(len(content['objectives']) for content in all_content.values())
total_activities = sum(len(content['activities']) for content in all_content.values())

print(f"\n=== SUMMARY STATISTICS ===")
print(f"Total characters extracted: {total_chars:,}")
print(f"Total lessons identified: {total_lessons}")
print(f"Total objectives identified: {total_objectives}")
print(f"Total activities identified: {total_activities}")

# List all processed files
print(f"\n=== PROCESSED FILES ===")
for filename in sorted(all_content.keys()):
    title = all_content[filename]['title']
    print(f"- {title}")

print("\nReady for lesson enhancement phase!")
