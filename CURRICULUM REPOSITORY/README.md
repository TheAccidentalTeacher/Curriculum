# Geography Worksheet Generation System

This package contains a complete system for generating ELA and Science worksheets for 32 geography units.

## Contents

- `content/`: Extracted content from PDF teacher guides
- `templates/`: HTML templates for worksheets
- `worksheets/`: Generated worksheet files (HTML and PDF)
- `final_output/`: Organized worksheets by region with an index.html file
- `content_extraction_script.py`: Script to extract content from PDFs
- `worksheet_generator.py`: Script to generate worksheets
- `run_worksheet_system.py`: Main script to run the entire system
- `organize_output.py`: Script to organize the output files
- `README_worksheet_system.md`: System documentation
- `worksheet_development_plan.md`: Development plan
- `worksheet_generation_system.md`: Detailed system explanation
- `worksheet_template_html.md`: HTML templates documentation

## Usage

1. Place all 32 PDF teacher guides in the workspace directory
2. Run the main script: `python run_worksheet_system.py`
3. Access the worksheets in the `final_output` directory
4. Open `final_output/index.html` in a web browser to access all worksheets

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

## Support

For questions or issues with the worksheet generation system, please contact your curriculum coordinator or instructional technology specialist.
