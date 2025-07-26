#!/usr/bin/env python3
"""
Script to scrape https://gorgeous-flan-dcd8c9.netlify.app/ and compare with local content
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
from urllib.parse import urljoin, urlparse
import time
from collections import defaultdict

class CurriculumScraper:
    def __init__(self, base_url="https://gorgeous-flan-dcd8c9.netlify.app/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.scraped_data = {}
        self.local_content_dir = "/workspaces/Curriculum/content"
        
    def get_page(self, url):
        """Get page content with error handling"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def scrape_main_page(self):
        """Scrape the main page to find all geography content"""
        print("Scraping main page...")
        html = self.get_page(self.base_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for geography-related links, sections, or content
        geography_links = []
        
        # Find all links that might be geography-related
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True).lower()
            
            # Look for geography-related keywords
            if any(keyword in text for keyword in [
                'geography', 'geo', 'world', 'continent', 'country', 'region',
                'physical', 'human', 'culture', 'climate', 'population', 'economic'
            ]):
                full_url = urljoin(self.base_url, href)
                geography_links.append({
                    'url': full_url,
                    'text': link.get_text(strip=True),
                    'href': href
                })
        
        # Also look for any curriculum or unit structures
        for element in soup.find_all(['div', 'section'], class_=True):
            class_names = ' '.join(element.get('class', [])).lower()
            if any(keyword in class_names for keyword in ['geography', 'curriculum', 'unit', 'lesson']):
                # Extract any links within this element
                for link in element.find_all('a', href=True):
                    href = link.get('href')
                    full_url = urljoin(self.base_url, href)
                    geography_links.append({
                        'url': full_url,
                        'text': link.get_text(strip=True),
                        'href': href,
                        'context': class_names
                    })
        
        return geography_links
    
    def scrape_curriculum_structure(self):
        """Look for curriculum structure in various formats"""
        print("Analyzing curriculum structure...")
        
        # Check for common curriculum page patterns
        potential_urls = [
            self.base_url,
            urljoin(self.base_url, 'curriculum.html'),
            urljoin(self.base_url, 'geography.html'),
            urljoin(self.base_url, 'index.html'),
            urljoin(self.base_url, 'dashboard.html'),
            urljoin(self.base_url, 'quarter1.html'),
            urljoin(self.base_url, 'quarter2.html'),
            urljoin(self.base_url, 'quarter3.html'),
            urljoin(self.base_url, 'quarter4.html'),
        ]
        
        all_content = {}
        
        for url in potential_urls:
            print(f"Checking: {url}")
            html = self.get_page(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract structured content
                content = self.extract_structured_content(soup, url)
                if content:
                    page_name = urlparse(url).path.split('/')[-1] or 'index'
                    all_content[page_name] = content
            
            time.sleep(1)  # Be respectful
        
        return all_content
    
    def extract_structured_content(self, soup, url):
        """Extract structured curriculum content from a page"""
        content = {
            'url': url,
            'title': '',
            'units': [],
            'lessons': [],
            'resources': [],
            'standards': [],
            'raw_text': ''
        }
        
        # Get page title
        title_tag = soup.find('title')
        if title_tag:
            content['title'] = title_tag.get_text(strip=True)
        
        # Look for units/modules/chapters
        for element in soup.find_all(['div', 'section', 'article']):
            classes = ' '.join(element.get('class', [])).lower()
            
            if any(keyword in classes for keyword in ['unit', 'module', 'chapter', 'quarter']):
                unit_data = self.extract_unit_data(element)
                if unit_data:
                    content['units'].append(unit_data)
        
        # Look for lessons
        for element in soup.find_all(['div', 'li', 'article']):
            classes = ' '.join(element.get('class', [])).lower()
            
            if any(keyword in classes for keyword in ['lesson', 'activity', 'worksheet']):
                lesson_data = self.extract_lesson_data(element)
                if lesson_data:
                    content['lessons'].append(lesson_data)
        
        # Look for standards references
        standards_text = soup.get_text()
        alaska_standards = re.findall(r'AK\s*[A-Z]+\s*\d+[\.\d]*', standards_text)
        content['standards'] = list(set(alaska_standards))
        
        # Store raw text for analysis
        content['raw_text'] = soup.get_text()
        
        return content
    
    def extract_unit_data(self, element):
        """Extract unit/module data from an element"""
        unit = {
            'title': '',
            'description': '',
            'lessons': [],
            'standards': [],
            'resources': []
        }
        
        # Get title
        title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
        if title_elem:
            unit['title'] = title_elem.get_text(strip=True)
        
        # Get description
        desc_elem = element.find(['p', 'div'], class_=lambda x: x and 'description' in x.lower())
        if desc_elem:
            unit['description'] = desc_elem.get_text(strip=True)
        
        # Find nested lessons
        for lesson_elem in element.find_all(['li', 'div'], class_=lambda x: x and 'lesson' in x.lower() if x else False):
            lesson_data = self.extract_lesson_data(lesson_elem)
            if lesson_data:
                unit['lessons'].append(lesson_data)
        
        return unit if unit['title'] else None
    
    def extract_lesson_data(self, element):
        """Extract lesson data from an element"""
        lesson = {
            'title': '',
            'description': '',
            'objectives': [],
            'activities': [],
            'resources': [],
            'standards': []
        }
        
        # Get title
        title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'strong', 'b'])
        if title_elem:
            lesson['title'] = title_elem.get_text(strip=True)
        
        # Get description
        lesson['description'] = element.get_text(strip=True)
        
        return lesson if lesson['title'] else None
    
    def compare_with_local_content(self, scraped_data):
        """Compare scraped data with local content files"""
        print("\nComparing with local content...")
        
        # Load local content
        local_content = {}
        if os.path.exists(self.local_content_dir):
            for filename in os.listdir(self.local_content_dir):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(self.local_content_dir, filename), 'r') as f:
                            local_content[filename] = json.load(f)
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
        
        # Analyze differences
        comparison = {
            'local_files': list(local_content.keys()),
            'scraped_pages': list(scraped_data.keys()),
            'missing_in_local': [],
            'missing_in_scraped': [],
            'content_analysis': {}
        }
        
        # Find content that exists in scraped but not local
        for page, content in scraped_data.items():
            if content['units'] or content['lessons']:
                # Check if similar content exists locally
                found_similar = False
                for local_file, local_data in local_content.items():
                    if self.content_similarity(content, local_data):
                        found_similar = True
                        break
                
                if not found_similar:
                    comparison['missing_in_local'].append({
                        'page': page,
                        'content': content
                    })
        
        return comparison
    
    def content_similarity(self, scraped_content, local_content):
        """Check if scraped content is similar to local content"""
        # Simple similarity check based on titles and keywords
        scraped_text = (scraped_content.get('title', '') + ' ' + 
                       scraped_content.get('raw_text', '')).lower()
        
        if isinstance(local_content, dict):
            local_text = str(local_content).lower()
        else:
            local_text = str(local_content).lower()
        
        # Check for common geography keywords
        common_words = set(scraped_text.split()) & set(local_text.split())
        return len(common_words) > 10  # Arbitrary threshold
    
    def run_full_scrape(self):
        """Run the complete scraping and comparison process"""
        print("Starting comprehensive scrape of curriculum website...")
        
        # Step 1: Get all geography-related links
        geography_links = self.scrape_main_page()
        print(f"Found {len(geography_links)} geography-related links")
        
        # Step 2: Scrape curriculum structure
        curriculum_data = self.scrape_curriculum_structure()
        
        # Step 3: Compare with local content
        comparison = self.compare_with_local_content(curriculum_data)
        
        # Save results
        results = {
            'scrape_timestamp': time.time(),
            'geography_links': geography_links,
            'curriculum_data': curriculum_data,
            'comparison': comparison
        }
        
        with open('/workspaces/Curriculum/scrape_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "="*60)
        print("SCRAPING COMPLETE")
        print("="*60)
        print(f"Found {len(curriculum_data)} pages with curriculum content")
        print(f"Local content files: {len(comparison['local_files'])}")
        print(f"Potentially missing content: {len(comparison['missing_in_local'])}")
        
        if comparison['missing_in_local']:
            print("\nContent that may be missing locally:")
            for item in comparison['missing_in_local']:
                print(f"  - {item['page']}: {item['content']['title']}")
        
        return results

if __name__ == "__main__":
    scraper = CurriculumScraper()
    results = scraper.run_full_scrape()
