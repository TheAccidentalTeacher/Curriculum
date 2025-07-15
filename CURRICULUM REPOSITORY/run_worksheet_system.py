#!/usr/bin/env python3
"""
Run Worksheet System

This script orchestrates the entire worksheet generation process:
1. Extract content from PDF teacher guides
2. Generate worksheets for all regions
3. Organize the output files
"""

import os
import sys
import subprocess
import shutil
import time

def print_header(message):
    """Print a formatted header message."""
    print("\n" + "=" * 80)
    print(f"  {message}")
    print("=" * 80)

def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(e.stderr)
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    print_header("Checking Dependencies")
    
    dependencies = [
        ("PyPDF2", "pip install PyPDF2"),
        ("jinja2", "pip install jinja2"),
        ("pdfkit", "pip install pdfkit")
    ]
    
    all_installed = True
    
    for package, install_cmd in dependencies:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is not installed. Installing...")
            if not run_command(install_cmd):
                all_installed = False
    
    # Check for wkhtmltopdf (required by pdfkit)
    try:
        result = subprocess.run(["which", "wkhtmltopdf"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ wkhtmltopdf is installed")
        else:
            print("✗ wkhtmltopdf is not installed. Please install it manually.")
            print("  On Debian/Ubuntu: sudo apt-get install wkhtmltopdf")
            print("  On macOS: brew install wkhtmltopdf")
            all_installed = False
    except Exception:
        print("✗ Could not check for wkhtmltopdf. Please ensure it's installed.")
        all_installed = False
    
    return all_installed

def create_directories():
    """Create necessary directories for the workflow."""
    print_header("Creating Directories")
    
    directories = [
        "content",
        "templates",
        "worksheets",
        "final_output"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")

def extract_content():
    """Run the content extraction script."""
    print_header("Extracting Content from PDFs")
    
    if not os.path.exists("content_extraction_script.py"):
        print("Error: content_extraction_script.py not found")
        return False
    
    return run_command("python content_extraction_script.py")

def generate_worksheets():
    """Run the worksheet generator script."""
    print_header("Generating Worksheets")
    
    if not os.path.exists("worksheet_generator.py"):
        print("Error: worksheet_generator.py not found")
        return False
    
    return run_command("python worksheet_generator.py")

def organize_output():
    """Organize the output files into a clean structure."""
    print_header("Organizing Output Files")
    
    # Create region directories in final_output
    if not os.path.exists("content"):
        print("Error: content directory not found")
        return False
    
    content_files = [f for f in os.listdir("content") if f.endswith('.json')]
    
    if not content_files:
        print("No content files found")
        return False
    
    for content_file in content_files:
        region_name = content_file.replace('.json', '').replace('_', ' ').title()
        region_dir = os.path.join("final_output", region_name.replace(' ', '_'))
        
        if not os.path.exists(region_dir):
            os.makedirs(region_dir)
            print(f"Created directory: {region_dir}")
        
        # Copy worksheets to region directory
        ela_worksheet = f"{region_name.lower().replace(' ', '_')}_ela_worksheet.pdf"
        science_worksheet = f"{region_name.lower().replace(' ', '_')}_science_worksheet.pdf"
        
        for worksheet in [ela_worksheet, science_worksheet]:
            src_path = os.path.join("worksheets", worksheet)
            if os.path.exists(src_path):
                dst_path = os.path.join(region_dir, worksheet)
                shutil.copy2(src_path, dst_path)
                print(f"Copied {worksheet} to {region_dir}")
    
    print("Output files organized successfully")
    return True

def create_index():
    """Create an index HTML file for easy access to all worksheets."""
    print_header("Creating Index File")
    
    if not os.path.exists("final_output"):
        print("Error: final_output directory not found")
        return False
    
    region_dirs = [d for d in os.listdir("final_output") if os.path.isdir(os.path.join("final_output", d))]
    
    if not region_dirs:
        print("No region directories found")
        return False
    
    # Create index HTML
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Geography Worksheets Index</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #0057b7;
            text-align: center;
            margin-bottom: 30px;
        }
        .region-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .region-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            background-color: #f9f9f9;
        }
        .region-card h2 {
            color: #0057b7;
            margin-top: 0;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        .worksheet-links {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .worksheet-link {
            display: inline-block;
            padding: 8px 15px;
            background-color: #0057b7;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            text-align: center;
        }
        .worksheet-link.ela {
            background-color: #0057b7;
        }
        .worksheet-link.science {
            background-color: #28a745;
        }
        .worksheet-link:hover {
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <h1>Geography Worksheets Index</h1>
    
    <div class="region-grid">
"""
    
    # Add region cards
    for region_dir in sorted(region_dirs):
        region_name = region_dir.replace('_', ' ').title()
        
        # Check for worksheets
        ela_worksheet = f"{region_dir.lower()}_ela_worksheet.pdf"
        science_worksheet = f"{region_dir.lower()}_science_worksheet.pdf"
        
        ela_path = os.path.join("final_output", region_dir, ela_worksheet)
        science_path = os.path.join("final_output", region_dir, science_worksheet)
        
        index_html += f"""
        <div class="region-card">
            <h2>{region_name}</h2>
            <div class="worksheet-links">
"""
        
        if os.path.exists(ela_path):
            rel_path = f"{region_dir}/{ela_worksheet}"
            index_html += f'                <a href="{rel_path}" class="worksheet-link ela">ELA Worksheet</a>\n'
        
        if os.path.exists(science_path):
            rel_path = f"{region_dir}/{science_worksheet}"
            index_html += f'                <a href="{rel_path}" class="worksheet-link science">Science Worksheet</a>\n'
        
        index_html += """
            </div>
        </div>
"""
    
    # Close HTML
    index_html += """
    </div>
</body>
</html>
"""
    
    # Save index HTML
    index_path = os.path.join("final_output", "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"Created index file: {index_path}")
    return True

def main():
    """Main function to run the worksheet system."""
    print_header("Geography Worksheet Generation System")
    
    # Check dependencies
    if not check_dependencies():
        print("Error: Missing dependencies. Please install them and try again.")
        return 1
    
    # Create directories
    create_directories()
    
    # Extract content from PDFs
    if not extract_content():
        print("Error: Content extraction failed.")
        return 1
    
    # Generate worksheets
    if not generate_worksheets():
        print("Error: Worksheet generation failed.")
        return 1
    
    # Organize output
    if not organize_output():
        print("Error: Failed to organize output files.")
        return 1
    
    # Create index
    if not create_index():
        print("Error: Failed to create index file.")
        return 1
    
    print_header("Worksheet Generation Complete")
    print(f"All worksheets have been generated and organized in the 'final_output' directory.")
    print(f"Open 'final_output/index.html' to access all worksheets.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())