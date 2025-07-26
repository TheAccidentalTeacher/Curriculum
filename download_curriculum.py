#!/usr/bin/env python3
"""
Download all curriculum JSON files from the target website
"""

import requests
import json
import os
from urllib.parse import urljoin
import time

class CurriculumDownloader:
    def __init__(self, base_url="https://gorgeous-flan-dcd8c9.netlify.app/"):
        self.base_url = base_url
        self.data_url = urljoin(base_url, "data/")
        self.local_content_dir = "/workspaces/Curriculum/content"
        self.downloaded_content_dir = "/workspaces/Curriculum/downloaded_content"
        
        # Create directories if they don't exist
        os.makedirs(self.local_content_dir, exist_ok=True)
        os.makedirs(self.downloaded_content_dir, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download_json_file(self, filename):
        """Download a specific JSON file"""
        url = urljoin(self.data_url, filename)
        try:
            print(f"Downloading: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            return None
    
    def get_curriculum_map(self):
        """Download the main curriculum map to see all available units"""
        return self.download_json_file("curriculum_map.json")
    
    def download_all_units(self):
        """Download all curriculum units based on the links found in scraping"""
        
        # First, try to get the curriculum map
        curriculum_map = self.get_curriculum_map()
        if curriculum_map:
            print("Downloaded curriculum map successfully!")
            with open(os.path.join(self.downloaded_content_dir, "curriculum_map.json"), 'w') as f:
                json.dump(curriculum_map, f, indent=2)
        
        # List of all units found from the website scraping
        unit_files = [
            "a_geographer_s_world.json",
            "the_physical_world.json", 
            "the_human_world.json",
            "the_indian_subcontinent.json",
            "indian_early_civilizations_empires_and_world_religions.json",
            "world_religions_of_southwest_asia.json",
            "economics.json"
        ]
        
        # Add more units based on what was listed on the website
        additional_units = [
            "canada.json",
            "mexico.json",
            "central_america_and_the_caribbean.json",
            "south_america.json",
            "western_europe.json",
            "southern_europe.json", 
            "eastern_europe.json",
            "russia_and_the_caucasus.json",
            "north_africa.json",
            "west_and_central_africa.json",
            "east_and_southern_africa.json",
            "the_arabian_peninsula_to_central_asia.json",
            "the_eastern_mediterranean.json",
            "china,_mongolia,_and_taiwan.json",
            "china_mongolia_and_taiwan.json",  # Try both naming conventions
            "japan_and_the_koreas.json",
            "southeast_asia.json",
            "oceania_and_antarctica.json",
            "the_united_states.json",
            "early_civilizations_of_the_fertile_crescent_and_the_nile_valley.json",
            "early_civilizations_of_china.json",
            "early_civilizations_of_latin_america.json",
            "europe_before_the_1700s.json",
            "history_of_modern_europe.json",
            "history_of_sub-saharan_africa.json",
            "government_and_citizenship.json"
        ]
        
        all_units = unit_files + additional_units
        
        downloaded = []
        failed = []
        
        for unit_file in all_units:
            data = self.download_json_file(unit_file)
            if data:
                # Save to downloaded_content directory
                filepath = os.path.join(self.downloaded_content_dir, unit_file)
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)
                downloaded.append(unit_file)
                print(f"✓ Downloaded: {unit_file}")
            else:
                failed.append(unit_file)
                print(f"✗ Failed: {unit_file}")
            
            time.sleep(0.5)  # Be respectful
        
        return downloaded, failed
    
    def compare_downloaded_with_local(self, downloaded_files):
        """Compare downloaded content with existing local content"""
        comparison_results = {
            'identical': [],
            'different': [],
            'new_files': [],
            'local_only': []
        }
        
        # Get list of local files
        local_files = []
        if os.path.exists(self.local_content_dir):
            local_files = [f for f in os.listdir(self.local_content_dir) if f.endswith('.json')]
        
        # Compare each downloaded file with local version
        for downloaded_file in downloaded_files:
            local_path = os.path.join(self.local_content_dir, downloaded_file)
            downloaded_path = os.path.join(self.downloaded_content_dir, downloaded_file)
            
            if os.path.exists(local_path):
                # Compare content
                try:
                    with open(local_path, 'r') as f:
                        local_data = json.load(f)
                    with open(downloaded_path, 'r') as f:
                        downloaded_data = json.load(f)
                    
                    if local_data == downloaded_data:
                        comparison_results['identical'].append(downloaded_file)
                    else:
                        comparison_results['different'].append({
                            'file': downloaded_file,
                            'local_size': len(str(local_data)),
                            'downloaded_size': len(str(downloaded_data))
                        })
                except Exception as e:
                    print(f"Error comparing {downloaded_file}: {e}")
                    comparison_results['different'].append({
                        'file': downloaded_file,
                        'error': str(e)
                    })
            else:
                comparison_results['new_files'].append(downloaded_file)
        
        # Find files that exist locally but weren't downloaded
        for local_file in local_files:
            if local_file not in downloaded_files:
                comparison_results['local_only'].append(local_file)
        
        return comparison_results
    
    def update_local_content(self, comparison_results):
        """Update local content with newer/missing files"""
        updated_files = []
        
        # Copy new files
        for new_file in comparison_results['new_files']:
            source = os.path.join(self.downloaded_content_dir, new_file)
            dest = os.path.join(self.local_content_dir, new_file)
            
            try:
                with open(source, 'r') as src, open(dest, 'w') as dst:
                    dst.write(src.read())
                updated_files.append(f"Added: {new_file}")
                print(f"Added new file: {new_file}")
            except Exception as e:
                print(f"Error copying {new_file}: {e}")
        
        # Update different files (ask for confirmation for each)
        for diff_item in comparison_results['different']:
            if isinstance(diff_item, dict) and 'file' in diff_item:
                filename = diff_item['file']
                print(f"\nFile {filename} differs between local and downloaded versions:")
                if 'local_size' in diff_item:
                    print(f"  Local size: {diff_item['local_size']} chars")
                    print(f"  Downloaded size: {diff_item['downloaded_size']} chars")
                
                # For now, automatically update (you could add prompts here)
                source = os.path.join(self.downloaded_content_dir, filename)
                dest = os.path.join(self.local_content_dir, filename)
                
                try:
                    with open(source, 'r') as src, open(dest, 'w') as dst:
                        dst.write(src.read())
                    updated_files.append(f"Updated: {filename}")
                    print(f"Updated: {filename}")
                except Exception as e:
                    print(f"Error updating {filename}: {e}")
        
        return updated_files
    
    def run_full_download(self):
        """Run the complete download and sync process"""
        print("Starting download of all curriculum content...")
        print("="*60)
        
        # Download all units
        downloaded, failed = self.download_all_units()
        
        print(f"\nDownload Summary:")
        print(f"✓ Successfully downloaded: {len(downloaded)} files")
        print(f"✗ Failed to download: {len(failed)} files")
        
        if failed:
            print("Failed files:")
            for f in failed:
                print(f"  - {f}")
        
        # Compare with local content
        comparison = self.compare_downloaded_with_local(downloaded)
        
        print(f"\nComparison with local content:")
        print(f"  Identical files: {len(comparison['identical'])}")
        print(f"  Different files: {len(comparison['different'])}")
        print(f"  New files: {len(comparison['new_files'])}")
        print(f"  Local-only files: {len(comparison['local_only'])}")
        
        if comparison['new_files']:
            print("New files found:")
            for f in comparison['new_files']:
                print(f"  + {f}")
        
        if comparison['different']:
            print("Different files:")
            for item in comparison['different']:
                if isinstance(item, dict):
                    print(f"  ~ {item.get('file', item)}")
        
        if comparison['local_only']:
            print("Local-only files (not on website):")
            for f in comparison['local_only']:
                print(f"  - {f}")
        
        # Update local content
        updated = self.update_local_content(comparison)
        
        print(f"\nUpdate Summary:")
        print(f"Updated {len(updated)} files:")
        for update in updated:
            print(f"  {update}")
        
        return {
            'downloaded': downloaded,
            'failed': failed,
            'comparison': comparison,
            'updated': updated
        }

if __name__ == "__main__":
    downloader = CurriculumDownloader()
    results = downloader.run_full_download()
