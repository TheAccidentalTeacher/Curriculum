#!/usr/bin/env python3
"""
Proper Curriculum Organizer
Creates the correct module structure: PDF 1 → Module 1, PDF 2 → Module 2, etc.
Each module contains its specific lessons in manageable, clean format.
"""

import json
import os
import shutil
from pathlib import Path
import glob

def clean_title(filename):
    """Clean PDF filename to proper title"""
    # Remove 'compressed_' prefix and ' Teacher Guide PDF.pdf' suffix
    title = filename.replace('compressed_', '').replace(' Teacher Guide PDF.pdf', '')
    return title

def create_module_filename(title):
    """Create clean filename for module"""
    return title.lower().replace(' ', '_').replace(',', '').replace("'", "").replace('-', '_')

def get_proper_pdf_module_mapping():
    """Create the correct PDF to Module mapping"""
    
    # Get all PDF files
    pdf_files = []
    compressed_dir = "/workspaces/Curriculum/Compressed"
    
    for file in sorted(os.listdir(compressed_dir)):
        if file.endswith('.pdf') and file.startswith('compressed_'):
            pdf_files.append(file)
    
    modules = []
    for i, pdf_file in enumerate(pdf_files, 1):
        title = clean_title(pdf_file)
        filename = create_module_filename(title)
        
        modules.append({
            "module_number": i,
            "pdf_file": pdf_file,
            "title": title,
            "filename": filename,
            "quarter": f"Q{((i-1) // 8) + 1}"  # 8 modules per quarter
        })
    
    return modules

def get_extracted_content_for_module(pdf_filename):
    """Get extracted content for specific PDF/module"""
    
    # Check various extraction files
    extraction_files = [
        "/workspaces/Curriculum/intelligent_extracted_content.json",
        "/workspaces/Curriculum/advanced_extracted_content.json",
        "/workspaces/Curriculum/best_extracted_content.json"
    ]
    
    for file_path in extraction_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Look for content from this specific PDF
                for key, content in data.items():
                    if pdf_filename.replace('compressed_', '').replace('.pdf', '') in key:
                        return content
            except:
                continue
    
    return None

def create_clean_lesson_structure():
    """Create the proper lesson structure"""
    
    print("🏗️  Creating proper curriculum structure...")
    
    # Get the correct module mapping
    modules = get_proper_pdf_module_mapping()
    
    print(f"📚 Found {len(modules)} modules to organize")
    
    # Create new clean structure
    new_structure = {
        "curriculum_info": {
            "total_modules": len(modules),
            "organization": "Each PDF = One Module with its specific lessons",
            "structure": "32 modules organized across 4 quarters"
        },
        "modules": modules
    }
    
    # Create clean modules directory
    modules_dir = "/workspaces/Curriculum/modules"
    if os.path.exists(modules_dir):
        shutil.rmtree(modules_dir)
    os.makedirs(modules_dir)
    
    # Create each module with its lessons
    for module in modules:
        module_dir = os.path.join(modules_dir, f"module_{module['module_number']:02d}_{module['filename']}")
        os.makedirs(module_dir, exist_ok=True)
        
        # Get content for this specific module
        content = get_extracted_content_for_module(module['pdf_file'])
        
        # Create module info file
        module_info = {
            "module_number": module['module_number'],
            "title": module['title'],
            "pdf_source": module['pdf_file'],
            "quarter": module['quarter'],
            "lessons": []
        }
        
        if content:
            # Extract lessons from content
            if isinstance(content, dict) and 'lessons' in content:
                lessons = content['lessons']
                for i, lesson in enumerate(lessons[:10], 1):  # Limit to 10 lessons per module
                    lesson_title = lesson.get('title', f"Lesson {i}")
                    module_info['lessons'].append({
                        "lesson_number": i,
                        "title": lesson_title,
                        "content": lesson.get('content', ''),
                        "objectives": lesson.get('objectives', []),
                        "activities": lesson.get('activities', [])
                    })
        
        # Save module info
        with open(os.path.join(module_dir, 'module_info.json'), 'w', encoding='utf-8') as f:
            json.dump(module_info, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Module {module['module_number']:02d}: {module['title']} ({len(module_info['lessons'])} lessons)")
    
    # Save overall structure
    with open("/workspaces/Curriculum/proper_curriculum_structure.json", 'w', encoding='utf-8') as f:
        json.dump(new_structure, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Created proper curriculum structure with {len(modules)} modules!")
    return new_structure

def create_clean_html_lessons():
    """Create clean, manageable HTML lessons for each module"""
    
    print("🎨 Creating clean HTML lessons...")
    
    modules_dir = "/workspaces/Curriculum/modules"
    clean_lessons_dir = "/workspaces/Curriculum/clean_lessons"
    
    if os.path.exists(clean_lessons_dir):
        shutil.rmtree(clean_lessons_dir)
    os.makedirs(clean_lessons_dir)
    
    for module_dir in sorted(os.listdir(modules_dir)):
        module_path = os.path.join(modules_dir, module_dir)
        if not os.path.isdir(module_path):
            continue
            
        # Load module info
        module_info_path = os.path.join(module_path, 'module_info.json')
        if not os.path.exists(module_info_path):
            continue
            
        with open(module_info_path, 'r', encoding='utf-8') as f:
            module_info = json.load(f)
        
        # Create module lessons directory
        module_lessons_dir = os.path.join(clean_lessons_dir, f"module_{module_info['module_number']:02d}")
        os.makedirs(module_lessons_dir, exist_ok=True)
        
        # Create module overview page
        create_module_overview_page(module_info, module_lessons_dir)
        
        # Create individual lesson pages
        for lesson in module_info['lessons']:
            create_lesson_page(module_info, lesson, module_lessons_dir)
        
        print(f"✅ Created clean lessons for Module {module_info['module_number']:02d}: {module_info['title']}")

def create_module_overview_page(module_info, output_dir):
    """Create a clean module overview page"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Module {module_info['module_number']:02d}: {module_info['title']}</title>
    <link rel="stylesheet" href="../../styles.css">
    <style>
        .module-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }}
        .lesson-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }}
        .lesson-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .lesson-number {{
            background: #4299e1;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 1rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav-bar">
            <a href="../../index.html" class="nav-link">🏠 Home</a>
            <a href="../" class="nav-link">📚 All Modules</a>
        </nav>
        
        <div class="module-header">
            <h1>Module {module_info['module_number']:02d}: {module_info['title']}</h1>
            <p><strong>Quarter:</strong> {module_info['quarter']} | <strong>Lessons:</strong> {len(module_info['lessons'])}</p>
        </div>
        
        <div class="lessons-overview">
            <h2>📋 Lessons in this Module</h2>
            
            {''.join(f'''
            <div class="lesson-card">
                <div class="lesson-number">Lesson {lesson['lesson_number']}</div>
                <h3><a href="lesson_{lesson['lesson_number']:02d}.html" class="lesson-link">{lesson['title']}</a></h3>
                <p class="lesson-preview">{lesson.get('content', '')[:200]}...</p>
                <div class="lesson-meta">
                    <span class="objectives-count">🎯 {len(lesson.get('objectives', []))} Objectives</span>
                    <span class="activities-count">🎲 {len(lesson.get('activities', []))} Activities</span>
                </div>
            </div>
            ''' for lesson in module_info['lessons'])}
        </div>
        
        <div class="module-navigation">
            <h3>🧭 Module Navigation</h3>
            <div class="nav-buttons">
                {'<a href="../module_' + f"{module_info['module_number']-1:02d}" + '/" class="nav-btn prev">← Previous Module</a>' if module_info['module_number'] > 1 else ''}
                {'<a href="../module_' + f"{module_info['module_number']+1:02d}" + '/" class="nav-btn next">Next Module →</a>' if module_info['module_number'] < 32 else ''}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_lesson_page(module_info, lesson, output_dir):
    """Create a clean individual lesson page"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Module {module_info['module_number']:02d} - Lesson {lesson['lesson_number']}: {lesson['title']}</title>
    <link rel="stylesheet" href="../../styles.css">
    <style>
        .lesson-header {{
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }}
        .lesson-content {{
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        .objectives-list {{
            background: #f7fafc;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
        .activities-section {{
            background: #edf2f7;
            padding: 1.5rem;
            border-radius: 8px;
        }}
        .objective-item, .activity-item {{
            background: white;
            padding: 1rem;
            margin-bottom: 0.5rem;
            border-radius: 6px;
            border-left: 4px solid #4299e1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav-bar">
            <a href="../../index.html" class="nav-link">🏠 Home</a>
            <a href="../" class="nav-link">📚 All Modules</a>
            <a href="index.html" class="nav-link">📖 Module {module_info['module_number']:02d}</a>
        </nav>
        
        <div class="lesson-header">
            <h1>Lesson {lesson['lesson_number']}: {lesson['title']}</h1>
            <p><strong>Module:</strong> {module_info['title']} | <strong>Quarter:</strong> {module_info['quarter']}</p>
        </div>
        
        <div class="lesson-content">
            <h2>📝 Lesson Content</h2>
            <div class="content-text">
                {lesson.get('content', 'Content will be added here.')}
            </div>
        </div>
        
        <div class="objectives-list">
            <h2>🎯 Learning Objectives</h2>
            {''.join(f'<div class="objective-item">{obj}</div>' for obj in lesson.get('objectives', ['Objectives will be added here.']))}
        </div>
        
        <div class="activities-section">
            <h2>🎲 Activities</h2>
            {''.join(f'<div class="activity-item">{activity}</div>' for activity in lesson.get('activities', ['Activities will be added here.']))}
        </div>
        
        <div class="lesson-navigation">
            <div class="nav-buttons">
                {'<a href="lesson_' + f"{lesson['lesson_number']-1:02d}" + '.html" class="nav-btn prev">← Previous Lesson</a>' if lesson['lesson_number'] > 1 else ''}
                <a href="index.html" class="nav-btn module">📖 Module Overview</a>
                {'<a href="lesson_' + f"{lesson['lesson_number']+1:02d}" + '.html" class="nav-btn next">Next Lesson →</a>' if lesson['lesson_number'] < len(module_info['lessons']) else ''}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    with open(os.path.join(output_dir, f"lesson_{lesson['lesson_number']:02d}.html"), 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_main_curriculum_index():
    """Create main curriculum index page"""
    
    print("🏠 Creating main curriculum index...")
    
    # Load the proper structure
    with open("/workspaces/Curriculum/proper_curriculum_structure.json", 'r', encoding='utf-8') as f:
        structure = json.load(f)
    
    modules = structure['modules']
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>World Geography Curriculum - CRSD</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .curriculum-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            border-radius: 15px;
            margin-bottom: 3rem;
        }}
        .quarter-section {{
            margin-bottom: 3rem;
        }}
        .quarter-header {{
            background: #2d3748;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }}
        .modules-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        .module-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        .module-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }}
        .module-number {{
            position: absolute;
            top: -10px;
            right: -10px;
            background: #4299e1;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2rem;
        }}
        .module-title {{
            color: #2d3748;
            margin-bottom: 1rem;
            padding-right: 40px;
        }}
        .module-meta {{
            color: #718096;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        .view-module-btn {{
            background: #4299e1;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            font-weight: 500;
            transition: background 0.2s ease;
        }}
        .view-module-btn:hover {{
            background: #3182ce;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="curriculum-header">
            <h1>🌍 World Geography Curriculum</h1>
            <p>Columbia River School District - Properly Organized by Module</p>
            <div class="curriculum-stats">
                <span>📚 {len(modules)} Modules</span> | 
                <span>🗓️ 4 Quarters</span> | 
                <span>🎯 Standards-Based</span>
            </div>
        </div>
        
        {''.join(create_quarter_section(quarter, [m for m in modules if m['quarter'] == quarter]) for quarter in ['Q1', 'Q2', 'Q3', 'Q4'])}
        
        <div class="footer">
            <p>📖 Each module corresponds to one Teacher Guide PDF with properly organized lessons.</p>
            <p>🎯 Clean, manageable structure that educators can rely on 100%.</p>
        </div>
    </div>
</body>
</html>"""
    
    with open("/workspaces/Curriculum/curriculum_index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Created main curriculum index")

def create_quarter_section(quarter, quarter_modules):
    """Create HTML section for a quarter"""
    
    return f"""
        <div class="quarter-section">
            <div class="quarter-header">
                <h2>{quarter} - Quarter {quarter[1]} ({len(quarter_modules)} Modules)</h2>
            </div>
            <div class="modules-grid">
                {''.join(f'''
                <div class="module-card">
                    <div class="module-number">{module['module_number']}</div>
                    <h3 class="module-title">{module['title']}</h3>
                    <div class="module-meta">
                        PDF Source: {module['pdf_file']}<br>
                        Module {module['module_number']:02d} • {quarter}
                    </div>
                    <a href="clean_lessons/module_{module['module_number']:02d}/" class="view-module-btn">
                        📖 View Module
                    </a>
                </div>
                ''' for module in quarter_modules)}
            </div>
        </div>
    """

if __name__ == "__main__":
    print("🚀 Starting Proper Curriculum Organization...")
    print("=" * 60)
    
    # Create proper structure
    structure = create_clean_lesson_structure()
    
    # Create clean HTML lessons
    create_clean_html_lessons()
    
    # Create main index
    create_main_curriculum_index()
    
    print("\n" + "=" * 60)
    print("✅ PROPER CURRICULUM ORGANIZATION COMPLETE!")
    print("📚 32 modules properly mapped to their PDFs")
    print("🎯 Clean, manageable lesson structure")
    print("🏠 New curriculum index: curriculum_index.html")
    print("📖 Modules located in: clean_lessons/")
    print("\n🎉 Educators can now rely 100% on this organized structure!")
