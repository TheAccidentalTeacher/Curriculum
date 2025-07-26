#!/usr/bin/env python3
"""
Comprehensive analysis of local vs website content
"""

import json
import os
from collections import defaultdict

def analyze_content_differences():
    print("COMPREHENSIVE CONTENT ANALYSIS")
    print("=" * 80)
    
    # Load downloaded curriculum map
    with open('/workspaces/Curriculum/downloaded_content/curriculum_map.json', 'r') as f:
        website_map = json.load(f)
    
    # Load local content files
    local_content_dir = '/workspaces/Curriculum/content'
    local_files = {}
    
    for filename in os.listdir(local_content_dir):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(local_content_dir, filename), 'r') as f:
                    local_files[filename] = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    print(f"Website curriculum map contains: {len(website_map.get('units', []))} units")
    print(f"Local content directory contains: {len(local_files)} files")
    
    # Compare website units with local files
    website_units = {unit['name'] + '.json': unit for unit in website_map.get('units', [])}
    
    print(f"\nWEBSITE UNITS:")
    for unit_name, unit_data in website_units.items():
        print(f"  {unit_name} - {unit_data['title']}")
        print(f"    Lessons: {unit_data['lesson_count']} ({', '.join(unit_data['lessons'][:3])}...)")
        print(f"    Key terms: {len(unit_data['key_terms'])}")
    
    print(f"\nLOCAL FILES (sample):")
    for i, (filename, content) in enumerate(list(local_files.items())[:10]):
        print(f"  {filename}")
        if isinstance(content, dict):
            if 'metadata' in content:
                print(f"    Has metadata: {content['metadata'].get('title', 'No title')}")
            if 'lessons' in content:
                lesson_count = len(content['lessons']) if isinstance(content['lessons'], list) else 'unknown'
                print(f"    Lessons: {lesson_count}")
            if 'content' in content and 'key_terms' in content['content']:
                key_terms_count = len(content['content']['key_terms']) if isinstance(content['content']['key_terms'], dict) else 'unknown'
                print(f"    Key terms: {key_terms_count}")
        else:
            print(f"    Content type: {type(content)}")
    
    # Check content richness comparison
    print(f"\nCONTENT RICHNESS COMPARISON:")
    
    # Compare a_geographer_s_world specifically since it exists in both
    local_geo_file = 'a_geographer_s_world.json'
    if local_geo_file in local_files:
        local_geo = local_files[local_geo_file]
        website_geo = website_units.get(local_geo_file, {})
        
        print(f"\n  A Geographer's World comparison:")
        print(f"    Website version:")
        print(f"      Lessons: {len(website_geo.get('lessons', []))}")
        print(f"      Key terms: {len(website_geo.get('key_terms', []))}")
        print(f"      Big ideas: {len(website_geo.get('big_ideas', []))}")
        
        print(f"    Local version:")
        if isinstance(local_geo, dict):
            local_lessons = local_geo.get('lessons', [])
            if isinstance(local_lessons, list):
                print(f"      Lessons: {len(local_lessons)}")
            
            local_content = local_geo.get('content', {})
            if isinstance(local_content, dict):
                local_key_terms = local_content.get('key_terms', {})
                if isinstance(local_key_terms, dict):
                    print(f"      Key terms: {len(local_key_terms)}")
                
                local_big_ideas = local_content.get('big_ideas', [])
                if isinstance(local_big_ideas, list):
                    print(f"      Big ideas: {len(local_big_ideas)}")
                
                # Check for additional content types
                for key in ['activities', 'assessments', 'resources', 'teacher_content', 'student_content']:
                    if key in local_content:
                        content_item = local_content[key]
                        if isinstance(content_item, list):
                            print(f"      {key.title()}: {len(content_item)}")
                        elif isinstance(content_item, dict):
                            print(f"      {key.title()}: {len(content_item)} items")
    
    # Check for content that exists locally but not on website
    print(f"\nCONTENT ANALYSIS:")
    print(f"  Local files not represented on website:")
    website_unit_names = {unit['name'] + '.json' for unit in website_map.get('units', [])}
    local_only = set(local_files.keys()) - website_unit_names
    for filename in sorted(local_only):
        print(f"    ✓ {filename}")
    
    print(f"\n  CONCLUSION:")
    if len(local_files) > len(website_units):
        print(f"    Your local project appears to be MORE comprehensive than the website!")
        print(f"    Local: {len(local_files)} units vs Website: {len(website_units)} units")
        print(f"    Your project contains {len(local_only)} additional units not on the website.")
    else:
        print(f"    The website may have content not in your local project.")
    
    # Check if local content is more detailed
    if local_geo_file in local_files:
        local_size = len(str(local_files[local_geo_file]))
        website_size = len(str(website_units.get(local_geo_file, {})))
        
        print(f"\n  CONTENT DETAIL COMPARISON:")
        print(f"    Local 'A Geographer's World': {local_size:,} characters")
        print(f"    Website 'A Geographer's World': {website_size:,} characters")
        
        if local_size > website_size * 2:
            print(f"    ✓ Your local content is significantly more detailed!")
        elif local_size > website_size:
            print(f"    ✓ Your local content is more detailed.")
        else:
            print(f"    Website content is more detailed.")

if __name__ == "__main__":
    analyze_content_differences()
