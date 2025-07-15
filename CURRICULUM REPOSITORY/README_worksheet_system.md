# Geography Worksheet Generation System

This system automatically generates ELA and Science worksheets for 32 geography units based on teacher guide PDFs. The worksheets are designed to align with the geography curriculum, making it easy for teachers to implement cross-curricular lessons.

## System Overview

The worksheet generation system consists of three main components:

1. **Content Extraction**: Extracts region-specific content from PDF teacher guides
2. **Worksheet Generation**: Creates ELA and Science worksheets using the extracted content
3. **Output Organization**: Organizes the worksheets by region for easy access

## Files Included

- `run_worksheet_system.py`: Main script that orchestrates the entire process
- `content_extraction_script.py`: Extracts content from PDF teacher guides
- `worksheet_generator.py`: Generates ELA and Science worksheets
- `worksheet_template_html.md`: HTML templates for the worksheets
- `worksheet_generation_system.md`: Detailed explanation of the system
- `sample_physical_world_ela_worksheet.pdf`: Example ELA worksheet
- `sample_physical_world_science_worksheet.pdf`: Example Science worksheet

## Requirements

- Python 3.6 or higher
- PyPDF2 library
- Jinja2 library
- pdfkit library
- wkhtmltopdf (external dependency)

## Installation

1. Install Python dependencies:
   ```
   pip install PyPDF2 jinja2 pdfkit
   ```

2. Install wkhtmltopdf:
   - On Debian/Ubuntu: `sudo apt-get install wkhtmltopdf`
   - On macOS: `brew install wkhtmltopdf`
   - On Windows: Download from https://wkhtmltopdf.org/downloads.html

## Usage

1. Place all 32 PDF teacher guides in the workspace directory

2. Run the main script:
   ```
   python run_worksheet_system.py
   ```

3. The script will:
   - Check for required dependencies
   - Create necessary directories
   - Extract content from the PDFs
   - Generate ELA and Science worksheets
   - Organize the worksheets by region
   - Create an index.html file for easy access

4. Access the worksheets:
   - Open `final_output/index.html` in a web browser
   - Click on the links to view or print the worksheets

## Directory Structure

After running the system, you'll have the following directory structure:

```
/
├── content/                  # Extracted content from PDFs
│   ├── physical_world.json
│   ├── human_world.json
│   └── ...
├── templates/                # HTML templates for worksheets
│   ├── ela_worksheet_template.html
│   └── science_worksheet_template.html
├── worksheets/               # Generated worksheet files
│   ├── physical_world_ela_worksheet.html
│   ├── physical_world_ela_worksheet.pdf
│   ├── physical_world_science_worksheet.html
│   ├── physical_world_science_worksheet.pdf
│   └── ...
└── final_output/             # Organized output files
    ├── index.html            # Main access point
    ├── Physical_World/
    │   ├── physical_world_ela_worksheet.pdf
    │   └── physical_world_science_worksheet.pdf
    ├── Human_World/
    │   ├── human_world_ela_worksheet.pdf
    │   └── human_world_science_worksheet.pdf
    └── ...
```

## Customization

### Modifying Templates

To customize the worksheet templates:

1. Edit the HTML templates in `templates/`:
   - `ela_worksheet_template.html`
   - `science_worksheet_template.html`

2. Run the worksheet generator again:
   ```
   python worksheet_generator.py
   ```

### Adding New Regions

To add new regions:

1. Place the new PDF teacher guide in the workspace directory
2. Run the content extraction script:
   ```
   python content_extraction_script.py
   ```
3. Run the worksheet generator:
   ```
   python worksheet_generator.py
   ```

## Troubleshooting

### PDF Content Extraction Issues

If the system has trouble extracting content from PDFs:

1. Check that the PDFs are not scanned images (they must contain actual text)
2. Try converting problematic PDFs to text manually:
   ```
   pdftotext your_pdf_file.pdf output_text_file.txt
   ```
3. Create a JSON content file manually using the structure in `worksheet_generation_system.md`

### Worksheet Generation Issues

If worksheets aren't generating properly:

1. Check the content JSON files in the `content/` directory
2. Ensure the HTML templates are valid
3. Verify that wkhtmltopdf is installed correctly

## Support

For questions or issues with the worksheet generation system, please contact your curriculum coordinator or instructional technology specialist.