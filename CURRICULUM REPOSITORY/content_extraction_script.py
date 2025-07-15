#!/usr/bin/env python3
"""
Content Extraction Script for Geography Teacher Guides

This script extracts region-specific content from PDF teacher guides and
organizes it into structured JSON files for worksheet generation.
"""

import os
import re
import json
import PyPDF2
from collections import defaultdict

# Define directories
PDF_DIR = "/workspace"
OUTPUT_DIR = "content"

# Ensure output directory exists
def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

# Extract region name from filename
def extract_region_name(filename):
    """Extract region name from PDF filename."""
    # Remove 'compressed_' prefix and ' Teacher Guide PDF.pdf' suffix
    region_name = filename.replace('compressed_', '').replace(' Teacher Guide PDF.pdf', '')
    return region_name

# Extract vocabulary terms and definitions
def extract_vocabulary(text):
    """Extract vocabulary terms and definitions from text."""
    vocabulary = []
    
    # Look for glossary or vocabulary sections
    glossary_pattern = r'(?:Glossary|Vocabulary|Key Terms)[:\s]*(.*?)(?:(?:Chapter|Section|References)|$)'
    glossary_match = re.search(glossary_pattern, text, re.DOTALL | re.IGNORECASE)
    
    if glossary_match:
        glossary_text = glossary_match.group(1)
        
        # Extract term-definition pairs
        term_def_pattern = r'([A-Za-z\s-]+)(?::|–|-)\s*([^:–-]+?)(?:\n|$)'
        term_defs = re.findall(term_def_pattern, glossary_text)
        
        for term, definition in term_defs:
            term = term.strip()
            definition = definition.strip()
            if term and definition:
                vocabulary.append({"term": term, "definition": definition})
    
    # If no glossary found, look for defined terms in the text
    if not vocabulary:
        term_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|are|refers to|means)\s+([^.]+)\.'
        term_defs = re.findall(term_pattern, text)
        
        for term, definition in term_defs:
            term = term.strip()
            definition = definition.strip()
            if term and definition:
                vocabulary.append({"term": term, "definition": definition})
    
    return vocabulary

# Extract reading passages
def extract_reading_passages(text, region_name):
    """Extract reading passages about the region."""
    passages = []
    
    # Look for paragraphs that mention the region name
    region_terms = region_name.split()
    region_pattern = '|'.join([re.escape(term) for term in region_terms if len(term) > 3])
    
    if region_pattern:
        paragraph_pattern = r'([A-Z][^.!?]*(?:' + region_pattern + r')[^.!?]*[.!?](?:\s+[A-Z][^.!?]*[.!?]){0,3})'
        paragraphs = re.findall(paragraph_pattern, text)
        
        for i, paragraph in enumerate(paragraphs[:3]):  # Limit to 3 passages
            # Clean up the paragraph
            clean_paragraph = re.sub(r'\s+', ' ', paragraph).strip()
            
            # Extract potential main idea (first sentence)
            main_idea_match = re.match(r'([A-Z][^.!?]*[.!?])', clean_paragraph)
            main_idea = main_idea_match.group(1) if main_idea_match else ""
            
            # Extract supporting details (remaining sentences)
            supporting_details = []
            if main_idea:
                remaining_text = clean_paragraph[len(main_idea):].strip()
                detail_matches = re.findall(r'([A-Z][^.!?]*[.!?])', remaining_text)
                supporting_details = [detail.strip() for detail in detail_matches]
            
            passages.append({
                "title": f"About {region_name}",
                "text": clean_paragraph,
                "main_idea": main_idea,
                "supporting_details": supporting_details
            })
    
    # If no region-specific paragraphs found, extract general informative paragraphs
    if not passages:
        paragraph_pattern = r'([A-Z][^.!?]*(?:geography|region|area|country|continent|landform|climate)[^.!?]*[.!?](?:\s+[A-Z][^.!?]*[.!?]){0,3})'
        paragraphs = re.findall(paragraph_pattern, text)
        
        for i, paragraph in enumerate(paragraphs[:3]):  # Limit to 3 passages
            # Clean up the paragraph
            clean_paragraph = re.sub(r'\s+', ' ', paragraph).strip()
            
            # Extract potential main idea (first sentence)
            main_idea_match = re.match(r'([A-Z][^.!?]*[.!?])', clean_paragraph)
            main_idea = main_idea_match.group(1) if main_idea_match else ""
            
            # Extract supporting details (remaining sentences)
            supporting_details = []
            if main_idea:
                remaining_text = clean_paragraph[len(main_idea):].strip()
                detail_matches = re.findall(r'([A-Z][^.!?]*[.!?])', remaining_text)
                supporting_details = [detail.strip() for detail in detail_matches]
            
            passages.append({
                "title": f"Geographic Information",
                "text": clean_paragraph,
                "main_idea": main_idea,
                "supporting_details": supporting_details
            })
    
    return passages

# Extract scientific phenomena
def extract_scientific_phenomena(text, region_name):
    """Extract scientific phenomena related to the region."""
    phenomena = []
    
    # Look for scientific phenomena related to the region
    science_keywords = [
        "climate", "ecosystem", "landform", "river", "mountain", "ocean", 
        "weather", "environment", "geology", "water", "forest", "desert"
    ]
    
    for keyword in science_keywords:
        pattern = r'([A-Z][^.!?]*' + re.escape(keyword) + r'[^.!?]*[.!?](?:\s+[A-Z][^.!?]*[.!?]){0,2})'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        for match in matches[:2]:  # Limit to 2 matches per keyword
            clean_text = re.sub(r'\s+', ' ', match).strip()
            
            # Create observation prompts
            observation_prompts = [
                f"What features of {keyword} can you identify in {region_name}?",
                f"How might {keyword} affect people living in {region_name}?",
                f"What patterns do you notice about {keyword} in {region_name}?"
            ]
            
            phenomena.append({
                "title": f"{region_name} {keyword.title()}",
                "description": clean_text,
                "observation_prompts": observation_prompts
            })
    
    return phenomena

# Extract writing prompts
def extract_writing_prompts(region_name):
    """Generate writing prompts for the region."""
    return [
        f"Using information from the passage and your own knowledge, write an informative paragraph about {region_name}. Include at least three vocabulary terms from Part 1.",
        f"Describe an important geographic feature of {region_name} and explain its significance to the region.",
        f"Compare and contrast two aspects of {region_name} discussed in the reading passage."
    ]

# Extract reflection questions
def extract_reflection_questions(region_name):
    """Generate reflection questions for the region."""
    return [
        f"What new information did you learn about {region_name}?",
        f"What questions do you still have about {region_name}?",
        f"How does learning about {region_name} help you understand our world better?",
        f"How might life in {region_name} be similar to or different from your own?"
    ]

# Extract system identification items
def extract_system_identification(region_name):
    """Generate system identification items for the region."""
    # Generic system identification for physical geography
    physical_systems = [
        {"description": f"Major mountain ranges in {region_name}", "system": "Lithosphere"},
        {"description": f"Rivers and lakes in {region_name}", "system": "Hydrosphere"},
        {"description": f"Climate patterns affecting {region_name}", "system": "Atmosphere"},
        {"description": f"Plant and animal life in {region_name}", "system": "Biosphere"},
        {"description": f"Natural resources found in {region_name}", "system": "Lithosphere"},
        {"description": f"Ocean currents affecting {region_name}", "system": "Hydrosphere"},
        {"description": f"Weather patterns in {region_name}", "system": "Atmosphere"},
        {"description": f"Ecosystems unique to {region_name}", "system": "Biosphere"}
    ]
    
    # Human geography systems
    human_systems = [
        {"description": f"Major cities in {region_name}", "system": "Urban"},
        {"description": f"Languages spoken in {region_name}", "system": "Cultural"},
        {"description": f"Economic activities in {region_name}", "system": "Economic"},
        {"description": f"Political boundaries in {region_name}", "system": "Political"},
        {"description": f"Transportation networks in {region_name}", "system": "Infrastructure"},
        {"description": f"Religious practices in {region_name}", "system": "Cultural"},
        {"description": f"Agricultural patterns in {region_name}", "system": "Economic"},
        {"description": f"Historical settlements in {region_name}", "system": "Historical"}
    ]
    
    # Determine which set to use based on region name
    if any(term in region_name.lower() for term in ["physical", "world", "earth", "land"]):
        return {
            "title": "EARTH'S SYSTEMS IDENTIFICATION",
            "instructions": "Label each description with the correct Earth system: Lithosphere, Hydrosphere, Atmosphere, or Biosphere.",
            "items": physical_systems
        }
    else:
        return {
            "title": "HUMAN GEOGRAPHY SYSTEMS",
            "instructions": "Label each description with the correct human geography system: Urban, Cultural, Economic, Political, or Infrastructure.",
            "items": human_systems
        }

# Process PDF file
def process_pdf_file(pdf_path):
    """Process a PDF file to extract region-specific content."""
    print(f"Processing {pdf_path}...")
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return None
    
    # Extract region name from filename
    filename = os.path.basename(pdf_path)
    region_name = extract_region_name(filename)
    print(f"Extracted region name: {region_name}")
    
    # Extract content
    vocabulary = extract_vocabulary(text)
    reading_passages = extract_reading_passages(text, region_name)
    scientific_phenomena = extract_scientific_phenomena(text, region_name)
    writing_prompts = extract_writing_prompts(region_name)
    reflection_questions = extract_reflection_questions(region_name)
    system_identification = extract_system_identification(region_name)
    
    # Create content object
    content = {
        "region_name": region_name,
        "vocabulary": vocabulary,
        "reading_passages": reading_passages,
        "scientific_phenomena": scientific_phenomena,
        "writing_prompts": writing_prompts,
        "reflection_questions": reflection_questions,
        "system_identification": system_identification
    }
    
    return content

# Save content to JSON file
def save_content_to_json(content, region_name):
    """Save extracted content to a JSON file."""
    filename = region_name.lower().replace(' ', '_') + ".json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2)
    
    print(f"Saved content to {filepath}")
    return filepath

# Main function
def main():
    """Main function to extract content from PDFs."""
    ensure_output_directory()
    
    # Find all PDF files in the directory
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf') and os.path.isfile(os.path.join(PDF_DIR, f))]
    
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    
    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        content = process_pdf_file(pdf_path)
        
        if content:
            save_content_to_json(content, content["region_name"])
    
    print("Content extraction complete.")

if __name__ == "__main__":
    main()