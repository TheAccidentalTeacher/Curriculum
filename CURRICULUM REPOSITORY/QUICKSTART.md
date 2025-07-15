# Geography Worksheet System Quick Start Guide

## Getting Started

1. **Install Dependencies**
   ```
   pip install PyPDF2 jinja2 pdfkit
   ```
   Also install wkhtmltopdf for your operating system.

2. **Run the System**
   ```
   python run_worksheet_system.py
   ```

3. **Access Worksheets**
   Open `final_output/index.html` in your web browser.

## Directory Structure

- `content/`: JSON files with extracted content
- `templates/`: HTML templates for worksheets
- `worksheets/`: Generated worksheet files
- `final_output/`: Organized worksheets by region

## Customization

- Edit HTML templates in `templates/` directory
- Modify content extraction in `content_extraction_script.py`
- Adjust worksheet generation in `worksheet_generator.py`

## Troubleshooting

- Check that PDFs contain extractable text
- Verify that wkhtmltopdf is installed correctly
- Ensure all directories exist and are writable
