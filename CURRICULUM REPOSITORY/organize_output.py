#!/usr/bin/env python3
"""
Organize Output Files

This script organizes the generated worksheets by region and creates an index.html file.
"""

import os
import shutil

# Define directories
WORKSHEETS_DIR = "worksheets"
OUTPUT_DIR = "final_output"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

# Get all worksheet files
worksheet_files = [f for f in os.listdir(WORKSHEETS_DIR) if f.endswith('.pdf')]

# Extract unique region names
regions = set()
for filename in worksheet_files:
    # Remove _ela_worksheet.pdf or _science_worksheet.pdf suffix
    if "_ela_worksheet.pdf" in filename:
        region_name = filename.replace("_ela_worksheet.pdf", "")
        regions.add(region_name)
    elif "_science_worksheet.pdf" in filename:
        region_name = filename.replace("_science_worksheet.pdf", "")
        regions.add(region_name)

# Create region directories and copy files
for region in regions:
    # Create region directory with title case name
    region_display = region.replace('_', ' ').title()
    region_dir = os.path.join(OUTPUT_DIR, region)
    
    if not os.path.exists(region_dir):
        os.makedirs(region_dir)
        print(f"Created directory: {region_dir}")
    
    # Copy worksheets to region directory
    ela_worksheet = f"{region}_ela_worksheet.pdf"
    science_worksheet = f"{region}_science_worksheet.pdf"
    
    for worksheet in [ela_worksheet, science_worksheet]:
        src_path = os.path.join(WORKSHEETS_DIR, worksheet)
        if os.path.exists(src_path):
            dst_path = os.path.join(region_dir, worksheet)
            shutil.copy2(src_path, dst_path)
            print(f"Copied {worksheet} to {region_dir}")

# Create index HTML
print("Creating index.html...")
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

# Add region cards to index.html
for region in sorted(regions):
    region_display = region.replace('_', ' ').title()
    region_dir = os.path.join(OUTPUT_DIR, region)
    
    # Check for worksheets
    ela_worksheet = f"{region}_ela_worksheet.pdf"
    science_worksheet = f"{region}_science_worksheet.pdf"
    
    ela_path = os.path.join(region_dir, ela_worksheet)
    science_path = os.path.join(region_dir, science_worksheet)
    
    index_html += f"""
        <div class="region-card">
            <h2>{region_display}</h2>
            <div class="worksheet-links">
"""
    
    if os.path.exists(ela_path):
        rel_path = f"{region}/{ela_worksheet}"
        index_html += f'                <a href="{rel_path}" class="worksheet-link ela">ELA Worksheet</a>\n'
    
    if os.path.exists(science_path):
        rel_path = f"{region}/{science_worksheet}"
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
index_path = os.path.join(OUTPUT_DIR, "index.html")
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f"Created index file: {index_path}")
print("Output organization complete.")