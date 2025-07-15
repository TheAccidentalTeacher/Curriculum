#!/usr/bin/env python3
"""
Worksheet Generator for Geography Lessons

This script generates ELA and Science worksheets for geography lessons
using extracted content from JSON files and HTML templates.
"""

import os
import json
import re
from jinja2 import Template
import pdfkit

# Define directories
CONTENT_DIR = "content"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "worksheets"

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist."""
    for directory in [CONTENT_DIR, TEMPLATE_DIR, OUTPUT_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

# Load region content
def load_region_content(region_name):
    """Load region-specific content from JSON file."""
    filename = region_name.lower().replace(' ', '_') + ".json"
    filepath = os.path.join(CONTENT_DIR, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Content file not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from: {filepath}")
        return None

# Load HTML template
def load_template(template_name):
    """Load HTML template from file."""
    filepath = os.path.join(TEMPLATE_DIR, template_name)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Template file not found: {filepath}")
        return None

# Save HTML to file
def save_html(html, filename):
    """Save HTML content to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath

# Convert HTML to PDF
def html_to_pdf(html_path, pdf_path):
    """Convert HTML file to PDF."""
    try:
        pdfkit.from_file(html_path, pdf_path)
        print(f"Created PDF: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error converting HTML to PDF: {e}")
        return None

# Generate ELA worksheet
def generate_ela_worksheet(region_name):
    """Generate ELA worksheet for the specified region."""
    # Load region content
    content = load_region_content(region_name)
    if not content:
        return None
    
    # Load HTML template
    template_str = load_template("ela_worksheet_template.html")
    if not template_str:
        return None
    
    # Create Jinja2 template
    template = Template(template_str)
    
    # Format vocabulary terms
    vocab_terms_html = ""
    for i, item in enumerate(content.get("vocabulary", [])[:5], 1):
        vocab_terms_html += f"<div class='vocabulary-item'>{i}. _____ {item['term']}</div>\n"
    
    # Format vocabulary definitions
    vocab_defs_html = ""
    for i, item in enumerate(content.get("vocabulary", [])[:5]):
        letter = chr(65 + i)  # A, B, C, D, E
        vocab_defs_html += f"<div class='vocabulary-item'>{letter}. {item['definition']}</div>\n"
    
    # Get reading passage
    reading_passage = ""
    if content.get("reading_passages") and len(content["reading_passages"]) > 0:
        reading_passage = content["reading_passages"][0]["text"]
    
    # Get writing prompt
    writing_prompt = "Using information from the passage and your own knowledge, write an informative paragraph about this region. Include at least three vocabulary terms from Part 1."
    if content.get("writing_prompts") and len(content["writing_prompts"]) > 0:
        writing_prompt = content["writing_prompts"][0]
    
    # Render template with content
    html = template.render(
        REGION_NAME=region_name,
        VOCABULARY_TERMS=vocab_terms_html,
        VOCABULARY_DEFINITIONS=vocab_defs_html,
        READING_PASSAGE=reading_passage,
        WRITING_PROMPT=writing_prompt
    )
    
    # Save HTML file
    filename = f"{region_name.lower().replace(' ', '_')}_ela_worksheet.html"
    html_path = save_html(html, filename)
    
    # Convert to PDF
    pdf_filename = f"{region_name.lower().replace(' ', '_')}_ela_worksheet.pdf"
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
    html_to_pdf(html_path, pdf_path)
    
    return pdf_path

# Generate Science worksheet
def generate_science_worksheet(region_name):
    """Generate Science worksheet for the specified region."""
    # Load region content
    content = load_region_content(region_name)
    if not content:
        return None
    
    # Load HTML template
    template_str = load_template("science_worksheet_template.html")
    if not template_str:
        return None
    
    # Create Jinja2 template
    template = Template(template_str)
    
    # Get phenomenon instructions
    phenomenon_instructions = "Observe the image/model of this region's geographic features and record your observations below."
    if content.get("scientific_phenomena") and len(content["scientific_phenomena"]) > 0:
        phenomenon = content["scientific_phenomena"][0]
        phenomenon_instructions = phenomenon["description"]
    
    # Get system identification
    system_id = content.get("system_identification", {})
    system_id_title = system_id.get("title", "GEOGRAPHIC SYSTEMS IDENTIFICATION")
    system_id_instructions = system_id.get("instructions", "Label each description with the correct geographic system.")
    
    # Format system identification items
    system_id_items_html = ""
    for i, item in enumerate(system_id.get("items", [])[:8], 1):
        system_id_items_html += f"<div class='system-item'>{i}. _________________ {item['description']}</div>\n"
    
    # Create data table
    data_table_html = """
    <table class='data-table'>
        <tr>
            <th>Feature</th>
            <th>Observations</th>
            <th>Significance</th>
        </tr>
        <tr>
            <td>Climate</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Landforms</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Water Features</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Vegetation</td>
            <td></td>
            <td></td>
        </tr>
    </table>
    """
    
    # Format analysis questions
    analysis_questions_html = """
    <div>1. What patterns do you notice in the data? _______________________________</div>
    <div class="response-line"></div>
    <div>2. How do these features interact with each other? _______________________</div>
    <div class="response-line"></div>
    <div>3. What might explain these geographic patterns? ________________________</div>
    <div class="response-line"></div>
    """
    
    # Get model instructions
    model_instructions = f"Create a model showing how the geographic features of {region_name} interact. Label each feature and draw arrows showing the interactions."
    
    # Get explanation prompt
    explanation_prompt = f"Using your model and what you've learned about {region_name}, explain how the geographic features of this region influence human settlement and activities."
    
    # Get reflection prompts
    reflection_prompt_1 = f"My model shows _________________ about {region_name} because:"
    reflection_prompt_2 = f"One way humans have adapted to the geography of {region_name} is:"
    
    # Render template with content
    html = template.render(
        REGION_NAME=region_name,
        PHENOMENON_INSTRUCTIONS=phenomenon_instructions,
        SYSTEM_IDENTIFICATION_TITLE=system_id_title,
        SYSTEM_IDENTIFICATION_INSTRUCTIONS=system_id_instructions,
        SYSTEM_IDENTIFICATION_ITEMS=system_id_items_html,
        DATA_ANALYSIS_INSTRUCTIONS=f"Collect data about the geographic features of {region_name} using the table below.",
        DATA_TABLE=data_table_html,
        ANALYSIS_QUESTIONS=analysis_questions_html,
        MODEL_INSTRUCTIONS=model_instructions,
        EXPLANATION_PROMPT=explanation_prompt,
        REFLECTION_PROMPT_1=reflection_prompt_1,
        REFLECTION_PROMPT_2=reflection_prompt_2
    )
    
    # Save HTML file
    filename = f"{region_name.lower().replace(' ', '_')}_science_worksheet.html"
    html_path = save_html(html, filename)
    
    # Convert to PDF
    pdf_filename = f"{region_name.lower().replace(' ', '_')}_science_worksheet.pdf"
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
    html_to_pdf(html_path, pdf_path)
    
    return pdf_path

# Create HTML templates
def create_html_templates():
    """Create HTML templates for worksheets."""
    # ELA worksheet template
    ela_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{REGION_NAME}}: Text Analysis Worksheet</title>
    <style>
        @page {
            size: letter portrait;
            margin: 1cm;
        }
        body {
            font-family: Arial, sans-serif;
            line-height: 1.5;
            margin: 0;
            padding: 0.5in;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #0057b7;
            padding-bottom: 10px;
        }
        .title {
            font-size: 18pt;
            font-weight: bold;
            color: #0057b7;
        }
        .student-info {
            margin-top: 15px;
            margin-bottom: 25px;
        }
        .section-title {
            font-size: 14pt;
            font-weight: bold;
            color: #0057b7;
            margin-top: 25px;
            margin-bottom: 15px;
            border-bottom: 1px solid #0057b7;
            padding-bottom: 5px;
        }
        .subsection-title {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        .instructions {
            margin-bottom: 15px;
        }
        .vocabulary-item {
            margin-bottom: 10px;
        }
        .reading-passage {
            background-color: #f5f5f5;
            padding: 15px;
            margin-bottom: 15px;
            font-style: italic;
        }
        .response-line {
            border-bottom: 1px solid #999;
            margin-bottom: 15px;
            height: 20px;
        }
        .writing-space {
            border: 1px solid #999;
            height: 200px;
            padding: 10px;
            margin-bottom: 15px;
        }
        .footer {
            text-align: center;
            font-size: 9pt;
            margin-top: 30px;
            border-top: 1px solid #999;
            padding-top: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">{{REGION_NAME}}: Text Analysis Worksheet</div>
    </div>
    
    <div class="student-info">
        Name: _________________________________ Date: _____________ Class: _____________
    </div>
    
    <div class="section-title">PART 1: VOCABULARY DEVELOPMENT</div>
    <div class="instructions">Match each term with its definition by writing the correct letter in the blank.</div>
    
    <div class="subsection-title">Terms:</div>
    {{VOCABULARY_TERMS}}
    
    <div class="subsection-title">Definitions:</div>
    {{VOCABULARY_DEFINITIONS}}
    
    <div class="section-title">PART 2: CLOSE READING</div>
    <div class="instructions">Read the passage below about {{REGION_NAME}}. Then answer the questions that follow.</div>
    
    <div class="reading-passage">
        {{READING_PASSAGE}}
    </div>
    
    <div class="subsection-title">Main Idea:</div>
    <div class="instructions">What is the main idea of this passage? Underline the sentence that best states it.</div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    
    <div class="subsection-title">Supporting Details:</div>
    <div class="instructions">List three supporting details from the passage:</div>
    <div>1. ________________________________________________________________________</div>
    <div class="response-line"></div>
    <div>2. ________________________________________________________________________</div>
    <div class="response-line"></div>
    <div>3. ________________________________________________________________________</div>
    <div class="response-line"></div>
    
    <div class="section-title">PART 3: INFORMATIVE WRITING</div>
    <div class="instructions">{{WRITING_PROMPT}}</div>
    <div class="writing-space"></div>
    
    <div class="section-title">PART 4: REFLECTION</div>
    <div class="instructions">Complete the following sentences:</div>
    
    <div class="subsection-title">One new thing I learned about {{REGION_NAME}} is...</div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    
    <div class="subsection-title">One question I still have about {{REGION_NAME}} is...</div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    
    <div class="footer">
        Cross-Curricular Geography Program | {{REGION_NAME}} Unit | ELA Worksheet
    </div>
</body>
</html>"""
    
    # Science worksheet template
    science_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{REGION_NAME}}: Scientific Investigation Worksheet</title>
    <style>
        @page {
            size: letter portrait;
            margin: 1cm;
        }
        body {
            font-family: Arial, sans-serif;
            line-height: 1.5;
            margin: 0;
            padding: 0.5in;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #28a745;
            padding-bottom: 10px;
        }
        .title {
            font-size: 18pt;
            font-weight: bold;
            color: #28a745;
        }
        .student-info {
            margin-top: 15px;
            margin-bottom: 25px;
        }
        .section-title {
            font-size: 14pt;
            font-weight: bold;
            color: #28a745;
            margin-top: 25px;
            margin-bottom: 15px;
            border-bottom: 1px solid #28a745;
            padding-bottom: 5px;
        }
        .subsection-title {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        .instructions {
            margin-bottom: 15px;
        }
        .system-item {
            margin-bottom: 10px;
        }
        .response-line {
            border-bottom: 1px solid #999;
            margin-bottom: 15px;
            height: 20px;
        }
        .model-space {
            border: 1px solid #999;
            height: 300px;
            margin-bottom: 15px;
            text-align: center;
            padding-top: 140px;
            color: #999;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .data-table th, .data-table td {
            border: 1px solid #999;
            padding: 8px;
            text-align: left;
        }
        .data-table th {
            background-color: #f2f2f2;
        }
        .footer {
            text-align: center;
            font-size: 9pt;
            margin-top: 30px;
            border-top: 1px solid #999;
            padding-top: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">{{REGION_NAME}}: Scientific Investigation Worksheet</div>
    </div>
    
    <div class="student-info">
        Name: _________________________________ Date: _____________ Class: _____________
    </div>
    
    <div class="section-title">PART 1: SCIENTIFIC PHENOMENON OBSERVATION</div>
    <div class="instructions">{{PHENOMENON_INSTRUCTIONS}}</div>
    
    <div class="subsection-title">I notice:</div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    
    <div class="subsection-title">I wonder:</div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    
    <div class="section-title">{{SYSTEM_IDENTIFICATION_TITLE}}</div>
    <div class="instructions">{{SYSTEM_IDENTIFICATION_INSTRUCTIONS}}</div>
    
    {{SYSTEM_IDENTIFICATION_ITEMS}}
    
    <div class="section-title">PART 3: DATA COLLECTION & ANALYSIS</div>
    <div class="instructions">{{DATA_ANALYSIS_INSTRUCTIONS}}</div>
    
    {{DATA_TABLE}}
    
    <div class="subsection-title">Analysis Questions:</div>
    {{ANALYSIS_QUESTIONS}}
    
    <div class="section-title">PART 4: MODEL DEVELOPMENT</div>
    <div class="instructions">{{MODEL_INSTRUCTIONS}}</div>
    
    <div class="model-space">Draw your model in this space</div>
    
    <div class="subsection-title">Model Key:</div>
    <div>Arrow direction shows: ___________________________________________________</div>
    <div class="response-line"></div>
    <div>Dotted lines represent: ___________________________________________________</div>
    <div class="response-line"></div>
    
    <div class="section-title">PART 5: SCIENTIFIC EXPLANATION</div>
    <div class="instructions">{{EXPLANATION_PROMPT}}</div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    
    <div class="section-title">PART 6: REFLECTION</div>
    <div class="instructions">Complete the following sentences:</div>
    
    <div class="subsection-title">{{REFLECTION_PROMPT_1}}</div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    
    <div class="subsection-title">{{REFLECTION_PROMPT_2}}</div>
    <div class="response-line"></div>
    <div class="response-line"></div>
    
    <div class="footer">
        Cross-Curricular Geography Program | {{REGION_NAME}} Unit | Science Worksheet
    </div>
</body>
</html>"""
    
    # Save templates
    ensure_directories()
    
    with open(os.path.join(TEMPLATE_DIR, "ela_worksheet_template.html"), 'w', encoding='utf-8') as f:
        f.write(ela_template)
    
    with open(os.path.join(TEMPLATE_DIR, "science_worksheet_template.html"), 'w', encoding='utf-8') as f:
        f.write(science_template)
    
    print("Created HTML templates.")

# Generate worksheets for all regions
def generate_all_worksheets():
    """Generate worksheets for all regions with available content."""
    # Ensure directories exist
    ensure_directories()
    
    # Create HTML templates if they don't exist
    if not os.path.exists(os.path.join(TEMPLATE_DIR, "ela_worksheet_template.html")):
        create_html_templates()
    
    # Get all content files
    if not os.path.exists(CONTENT_DIR):
        print(f"Content directory not found: {CONTENT_DIR}")
        return
    
    content_files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.json')]
    
    if not content_files:
        print(f"No content files found in {CONTENT_DIR}")
        return
    
    # Process each content file
    for content_file in content_files:
        # Extract region name from filename
        region_name = content_file.replace('.json', '').replace('_', ' ').title()
        
        print(f"Generating worksheets for {region_name}...")
        
        # Generate ELA worksheet
        ela_path = generate_ela_worksheet(region_name)
        
        # Generate Science worksheet
        science_path = generate_science_worksheet(region_name)
        
        if ela_path and science_path:
            print(f"Successfully generated worksheets for {region_name}")
        else:
            print(f"Failed to generate some worksheets for {region_name}")
    
    print("Worksheet generation complete.")

# Main function
def main():
    """Main function to generate worksheets."""
    generate_all_worksheets()

if __name__ == "__main__":
    main()