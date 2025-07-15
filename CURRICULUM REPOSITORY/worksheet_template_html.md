# HTML Templates for Worksheet Generation

These HTML templates can be used to efficiently generate worksheets for all 32 geography units. The templates include placeholders that can be automatically populated with region-specific content.

## ELA Worksheet Template

```html
<!DOCTYPE html>
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
</html>
```

## Science Worksheet Template

```html
<!DOCTYPE html>
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
    
    <div class="section-title">PART 2: {{SYSTEM_IDENTIFICATION_TITLE}}</div>
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
</html>
```

## Python Script for Worksheet Generation

```python
import json
import os
from jinja2 import Template
import pdfkit

def load_region_content(region_name):
    """Load region-specific content from JSON file."""
    with open(f"content/{region_name.lower().replace(' ', '_')}.json", 'r') as f:
        return json.load(f)

def generate_ela_worksheet(region_name):
    """Generate ELA worksheet for the specified region."""
    # Load region content
    content = load_region_content(region_name)
    
    # Load HTML template
    with open("templates/ela_worksheet_template.html", 'r') as f:
        template_str = f.read()
    
    # Create Jinja2 template
    template = Template(template_str)
    
    # Format vocabulary terms
    vocab_terms_html = ""
    for i, item in enumerate(content["vocabulary"][:5], 1):
        vocab_terms_html += f"<div class='vocabulary-item'>{i}. _____ {item['term']}</div>\n"
    
    # Format vocabulary definitions
    vocab_defs_html = ""
    for i, item in enumerate(content["vocabulary"][:5]):
        letter = chr(65 + i)  # A, B, C, D, E
        vocab_defs_html += f"<div class='vocabulary-item'>{letter}. {item['definition']}</div>\n"
    
    # Render template with content
    html = template.render(
        REGION_NAME=region_name,
        VOCABULARY_TERMS=vocab_terms_html,
        VOCABULARY_DEFINITIONS=vocab_defs_html,
        READING_PASSAGE=content["reading_passages"][0]["text"],
        WRITING_PROMPT=content["writing_prompts"][0]
    )
    
    # Save HTML file
    os.makedirs("output", exist_ok=True)
    html_path = f"output/{region_name.lower().replace(' ', '_')}_ela_worksheet.html"
    with open(html_path, 'w') as f:
        f.write(html)
    
    # Convert to PDF
    pdf_path = f"output/{region_name.lower().replace(' ', '_')}_ela_worksheet.pdf"
    pdfkit.from_file(html_path, pdf_path)
    
    return pdf_path

def generate_science_worksheet(region_name):
    """Generate Science worksheet for the specified region."""
    # Similar implementation for science worksheet
    # ...

def generate_all_worksheets():
    """Generate worksheets for all regions."""
    regions = [
        "Physical World",
        "Human World",
        "North America",
        "South America",
        "Central America and Caribbean",
        "Europe",
        "Russia and Caucasus",
        "East Asia",
        "Oceania",
        "Sub-Saharan Africa"
        # Add all 32 regions here
    ]
    
    for region in regions:
        print(f"Generating worksheets for {region}...")
        ela_path = generate_ela_worksheet(region)
        science_path = generate_science_worksheet(region)
        print(f"Created: {ela_path}")
        print(f"Created: {science_path}")

if __name__ == "__main__":
    generate_all_worksheets()
```

This system allows for efficient generation of consistent worksheets across all 32 geography units while maintaining quality and customization for each region.