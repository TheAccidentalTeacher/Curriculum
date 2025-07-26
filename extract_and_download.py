#!/usr/bin/env python3
"""
Extract all unit names from curriculum map and download them
"""

import json
import requests
import os
from urllib.parse import urljoin
import time

def extract_and_download_all_units():
    # Load curriculum map
    with open('/workspaces/Curriculum/downloaded_content/curriculum_map.json', 'r') as f:
        curriculum_map = json.load(f)
    
    print(f"Found {len(curriculum_map['units'])} units in curriculum map")
    
    base_url = "https://gorgeous-flan-dcd8c9.netlify.app/data/"
    downloaded_dir = "/workspaces/Curriculum/downloaded_content"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    successful_downloads = []
    failed_downloads = []
    
    for unit in curriculum_map['units']:
        unit_name = unit['name']
        unit_title = unit['title']
        filename = f"{unit_name}.json"
        url = urljoin(base_url, filename)
        
        print(f"Downloading: {unit_title} ({filename})")
        
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            # Save the file
            filepath = os.path.join(downloaded_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(response.json(), f, indent=2)
            
            successful_downloads.append(filename)
            print(f"  ✓ Success: {filename}")
            
        except Exception as e:
            failed_downloads.append((filename, str(e)))
            print(f"  ✗ Failed: {filename} - {e}")
        
        time.sleep(0.5)  # Be respectful
    
    print(f"\n" + "="*60)
    print(f"DOWNLOAD SUMMARY")
    print(f"="*60)
    print(f"Total units in map: {len(curriculum_map['units'])}")
    print(f"Successfully downloaded: {len(successful_downloads)}")
    print(f"Failed downloads: {len(failed_downloads)}")
    
    if successful_downloads:
        print(f"\nSuccessful downloads:")
        for filename in successful_downloads:
            print(f"  ✓ {filename}")
    
    if failed_downloads:
        print(f"\nFailed downloads:")
        for filename, error in failed_downloads:
            print(f"  ✗ {filename}: {error}")
    
    return successful_downloads, failed_downloads

if __name__ == "__main__":
    extract_and_download_all_units()
