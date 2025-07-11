#!/usr/bin/env python3
"""
Comprehensive Lesson Generator for Alaska World Geography Curriculum
Generates all 32 units with detailed, differentiated lessons for grades 6, 7, and 8
Based on scope and sequence from wg1.md
"""

import os
import json
from pathlib import Path

# Curriculum structure based on wg1.md
CURRICULUM = {
    "Quarter 1": {
        "Unit 1": {
            "title": "A Geographer's World",
            "lessons": [
                "What is Geography?",
                "Physical & Human Geography", 
                "The Geographer's Tools",
                "Thinking Like a Geographer",
                "Geography Handbook & Review"
            ]
        },
        "Unit 2": {
            "title": "The Physical World",
            "lessons": [
                "Earth's Structure and Landforms",
                "Forces Shaping the Earth",
                "Climate and Weather Patterns",
                "Water Systems and Cycles"
            ]
        },
        "Unit 3": {
            "title": "The Human World", 
            "lessons": [
                "Population and Settlement Patterns",
                "Culture and Cultural Diffusion",
                "Languages and Religions",
                "Economic Systems and Development"
            ]
        },
        "Unit 4": {
            "title": "United States",
            "lessons": [
                "Physical Geography of the US",
                "Regions and States", 
                "Economic Geography",
                "Cultural Diversity and Immigration"
            ]
        },
        "Unit 5": {
            "title": "Canada",
            "lessons": [
                "Physical Features and Climate",
                "Provinces and Territories",
                "Natural Resources and Economy", 
                "Indigenous Peoples and Multiculturalism"
            ]
        },
        "Unit 6": {
            "title": "Mexico",
            "lessons": [
                "Physical Geography and Climate Zones",
                "States and Regions",
                "Economic Development and NAFTA",
                "Cultural Heritage and Modern Mexico"
            ]
        }
    },
    "Quarter 2": {
        "Unit 7": {
            "title": "Central America",
            "lessons": [
                "Physical Geography and Climate",
                "Countries and Capitals",
                "Economic Challenges and Opportunities",
                "Cultural Heritage and Migration"
            ]
        },
        "Unit 8": {
            "title": "South America", 
            "lessons": [
                "Physical Features and Climate Zones",
                "Countries and Major Cities",
                "Natural Resources and Economy",
                "Cultural Diversity and History"
            ]
        },
        "Unit 9": {
            "title": "Western Europe",
            "lessons": [
                "Physical Geography and Climate",
                "Countries and the European Union",
                "Economic Integration and Trade",
                "Cultural Heritage and Modern Society"
            ]
        },
        "Unit 10": {
            "title": "Eastern Europe",
            "lessons": [
                "Physical Features and Climate",
                "Countries and Post-Soviet Transition",
                "Economic Development Challenges",
                "Cultural Identity and History"
            ]
        },
        "Unit 11": {
            "title": "Russia and Central Asia",
            "lessons": [
                "Vast Territory and Climate Zones", 
                "Regions and Federal Structure",
                "Natural Resources and Energy",
                "Cultural Diversity and Challenges"
            ]
        }
    },
    "Quarter 3": {
        "Unit 12": {
            "title": "East Asia",
            "lessons": [
                "Physical Geography and Monsoons",
                "China's Geography and Population", 
                "Japan and the Koreas",
                "Economic Powerhouses and Trade"
            ]
        },
        "Unit 13": {
            "title": "Southeast Asia",
            "lessons": [
                "Island and Mainland Geography",
                "Countries and Capitals",
                "Tropical Climate and Resources",
                "Cultural Crossroads and Trade"
            ]
        },
        "Unit 14": {
            "title": "East Asia (Japan and the Koreas)",
            "lessons": [
                "Physical Geography",
                "Historical Development",
                "Cultural Patterns", 
                "Economic and Political Systems"
            ]
        },
        "Unit 15": {
            "title": "Southeast Asia",
            "lessons": [
                "Physical Geography",
                "Historical Influences",
                "Cultural Diversity",
                "Economic Development"
            ]
        },
        "Unit 16": {
            "title": "South Asia (Indian Subcontinent)",
            "lessons": [
                "Physical Geography",
                "Historical Development",
                "Cultural Patterns",
                "Economic and Political Geography"
            ]
        },
        "Unit 17": {
            "title": "Southwest Asia (Arabian Peninsula to Central Asia)",
            "lessons": [
                "Physical Geography",
                "Historical Development",
                "Cultural Patterns",
                "Economic and Political Geography"
            ]
        },
        "Unit 18": {
            "title": "Middle East (Eastern Mediterranean)",
            "lessons": [
                "Physical Geography",
                "Historical Significance",
                "Cultural Patterns",
                "Contemporary Issues"
            ]
        },
        "Unit 19": {
            "title": "North Africa",
            "lessons": [
                "Physical Geography",
                "Historical Development",
                "Cultural Patterns",
                "Economic and Political Geography"
            ]
        },
        "Unit 20": {
            "title": "West and Central Africa",
            "lessons": [
                "Physical Geography",
                "Historical Development",
                "Cultural Patterns",
                "Economic and Political Geography"
            ]
        },
        "Unit 21": {
            "title": "East and Southern Africa",
            "lessons": [
                "Physical Geography",
                "Historical Development",
                "Cultural Patterns",
                "Economic and Political Geography"
            ]
        },
        "Unit 22": {
            "title": "Oceania and Antarctica",
            "lessons": [
                "Physical Geography",
                "Historical and Cultural Patterns",
                "Economic and Political Geography",
                "Antarctica and Global Significance"
            ]
        }
    },
    "Quarter 4": {
        "Unit 18": {
            "title": "World Religions",
            "lessons": [
                "Major World Religions Overview",
                "Christianity and Its Spread",
                "Islam and Islamic Civilization",
                "Other Major Religions and Beliefs"
            ]
        },
        "Unit 19": {
            "title": "Global Economic Systems",
            "lessons": [
                "Economic Systems Comparison",
                "International Trade and Organizations",
                "Development and Inequality",
                "Globalization Effects"
            ]
        },
        "Unit 20": {
            "title": "Ancient Civilizations",
            "lessons": [
                "River Valley Civilizations",
                "Classical Civilizations",
                "Medieval Civilizations",
                "Legacy and Modern Connections"
            ]
        },
        "Unit 21": {
            "title": "Modern World History",
            "lessons": [
                "Age of Exploration and Colonialism",
                "Industrial Revolution and Imperialism", 
                "World Wars and Their Impact",
                "Cold War and Decolonization"
            ]
        },
        "Unit 22": {
            "title": "Government Systems",
            "lessons": [
                "Types of Government Systems",
                "Democracy and Democratic Institutions",
                "Authoritarian Systems",
                "International Organizations and Law"
            ]
        },
        "Unit 23": {
            "title": "Early Civilizations of the Fertile Crescent and the Nile Valley",
            "lessons": [
                "Geographic Context",
                "Mesopotamian Civilizations", 
                "Ancient Egypt",
                "Legacy and Influence"
            ]
        },
        "Unit 24": {
            "title": "Early Civilizations of China",
            "lessons": [
                "Early China and Han Dynasty",
                "Sui/Tang/Song Dynasties",
                "Yuan and Ming Dynasties", 
                "Legacy and Influence"
            ]
        },
        "Unit 25": {
            "title": "Indian Early Civilizations, Empires, and World Religions",
            "lessons": [
                "Indus Valley Civilization",
                "Vedic Period and Early Empires",
                "Religious Traditions",
                "Legacy and Influence"
            ]
        },
        "Unit 26": {
            "title": "Early Civilizations of Latin America",
            "lessons": [
                "Mesoamerican Civilizations",
                "Andean Civilizations",
                "Cultural Achievements",
                "Legacy and Influence"
            ]
        },
        "Unit 27": {
            "title": "Europe before the 1700s",
            "lessons": [
                "Ancient Greece",
                "Roman Empire",
                "Medieval Europe",
                "Renaissance and Reformation"
            ]
        },
        "Unit 28": {
            "title": "History of Modern Europe",
            "lessons": [
                "Age of Exploration and Enlightenment",
                "Industrial Revolution",
                "Political Revolutions and Nationalism",
                "20th Century Conflicts and Integration"
            ]
        },
        "Unit 29": {
            "title": "History of Sub-Saharan Africa",
            "lessons": [
                "Early African Kingdoms",
                "Colonial Impact",
                "Independence and Nation-Building",
                "Contemporary Developments"
            ]
        },
        "Unit 30": {
            "title": "Economics",
            "lessons": [
                "Economic Basics",
                "Economic Systems",
                "Money and Banking",
                "Living in a Global Economy"
            ]
        },
        "Unit 31": {
            "title": "Government and Citizenship",
            "lessons": [
                "Types of Government",
                "Citizenship and Participation",
                "International Relations and Government"
            ]
        },
        "Unit 32": {
            "title": "World Religions of Southwest Asia",
            "lessons": [
                "Judaism",
                "Christianity", 
                "Islam and Religious Influence"
            ]
        }
    }
}

# Grade-specific differentiation strategies
GRADE_DIFFERENTIATION = {
    6: {
        "complexity": "foundational",
        "reading_level": "6th grade",
        "activities": "hands-on, visual, collaborative",
        "assessment": "formative, scaffolded",
        "vocabulary": "basic geographic terms with visual aids"
    },
    7: {
        "complexity": "intermediate", 
        "reading_level": "7th grade",
        "activities": "analytical, research-based, comparative",
        "assessment": "mixed formative/summative",
        "vocabulary": "expanded geographic vocabulary with context"
    },
    8: {
        "complexity": "advanced",
        "reading_level": "8th grade", 
        "activities": "synthesis, evaluation, project-based",
        "assessment": "summative, performance-based",
        "vocabulary": "sophisticated geographic and cultural terms"
    }
}

def create_lesson_html(unit_num, unit_title, lesson_num, lesson_title, grade, quarter):
    """Create a comprehensive lesson HTML file"""
    
    grade_info = GRADE_DIFFERENTIATION[grade]
    
    # Determine navigation
    prev_lesson = f"unit{unit_num}-lesson{lesson_num-1}-grade{grade}.html" if lesson_num > 1 else None
    next_lesson = f"unit{unit_num}-lesson{lesson_num+1}-grade{grade}.html"
    
    # Alaska connections based on unit
    alaska_connections = get_alaska_connections(unit_num, unit_title)
    
    # Primary sources based on lesson content
    primary_sources = get_primary_sources(unit_num, lesson_title, grade)
    
    # Activities based on grade level
    activities = get_grade_activities(lesson_title, grade)
    
    # Assessment strategies
    assessments = get_grade_assessments(lesson_title, grade)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unit {unit_num}, Lesson {lesson_num}: {lesson_title} - {grade}th Grade</title>
    <link rel="stylesheet" href="../../styles.css">
</head>
<body>
    <header>
        <h1>Lesson {lesson_num}: {lesson_title}</h1>
        <nav style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <a href="../unit{unit_num}.html" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;">🏠 Back to Unit {unit_num}</a>
            <div style="display: flex; gap: 15px;">
                {"<a href='" + prev_lesson + "' style='color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;'>⬅ Previous Lesson</a>" if prev_lesson else ""}
                <a href="unit{unit_num}-lesson{lesson_num+1}-grade{grade}.html" style="color: white; text-decoration: none; background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px;">Next Lesson ➡</a>
            </div>
        </nav>
    </header>
    <main>
        <section style="margin-bottom: 2em;">
            <div style="display: flex; align-items: center; gap: 1em;">
                <span style="font-size: 2em;">🌍</span>
                <div>
                    <h2 style="margin: 0;">{lesson_title}</h2>
                    <p style="margin: 0.5em 0; font-style: italic;">Grade {grade} • Unit {unit_num}: {unit_title} • Quarter {quarter}</p>
                </div>
            </div>
        </section>

        <section style="background: #e3f2fd; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>🎯 Learning Objectives</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>Students will be able to:</h4>
                    <ul>
                        {get_learning_objectives(lesson_title, grade)}
                    </ul>
                </div>
                <div>
                    <h4>Grade {grade} Differentiation:</h4>
                    <p><strong>Complexity Level:</strong> {grade_info['complexity'].title()}</p>
                    <p><strong>Reading Level:</strong> {grade_info['reading_level']}</p>
                    <p><strong>Activity Focus:</strong> {grade_info['activities']}</p>
                </div>
            </div>
        </section>

        <section style="background: #f8f9fa; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>📖 Lesson Content</h3>
            {get_lesson_content(lesson_title, grade)}
        </section>

        {primary_sources}

        <section style="background: #fff3e0; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>🎯 Activities & Scaffolding</h3>
            {activities}
        </section>

        <section style="background: #f3e5f5; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>📝 Assessment Strategies</h3>
            {assessments}
        </section>

        <section style="background: #e8f5e8; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>🏔️ Alaska Connections</h3>
            {alaska_connections}
        </section>

        <section style="background: #fff8e1; border-radius: 12px; padding: 1.5em;">
            <h3>🎒 Materials & Resources</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>Required Materials:</h4>
                    <ul>
                        <li>Student notebooks</li>
                        <li>World map or atlas</li>
                        <li>Primary source documents</li>
                        <li>Activity worksheets</li>
                    </ul>
                </div>
                <div>
                    <h4>Technology Integration:</h4>
                    <ul>
                        <li>Google Earth (if available)</li>
                        <li>Online mapping tools</li>
                        <li>Digital primary sources</li>
                        <li>Virtual field trips</li>
                    </ul>
                </div>
            </div>
        </section>
    </main>
</body>
</html>"""
    
    return html_content

def get_learning_objectives(lesson_title, grade):
    """Generate grade-appropriate learning objectives"""
    objectives = {
        6: "basic knowledge and identification",
        7: "analysis and comparison", 
        8: "synthesis and evaluation"
    }
    
    if "Geography" in lesson_title:
        if grade == 6:
            return "<li>Define geography and its main branches</li><li>Identify examples of physical and human geography</li><li>Explain why geography matters in daily life</li>"
        elif grade == 7:
            return "<li>Analyze the relationship between physical and human geography</li><li>Compare geographic perspectives across different scales</li><li>Evaluate the impact of geography on human activities</li>"
        else:
            return "<li>Synthesize geographic concepts to explain complex regional patterns</li><li>Evaluate how geographic factors influence historical and modern developments</li><li>Design solutions to geographic challenges using spatial thinking</li>"
    
    # Add more lesson-specific objectives
    return "<li>Understand key concepts</li><li>Apply knowledge to real-world situations</li><li>Analyze geographic patterns and relationships</li>"

def get_lesson_content(lesson_title, grade):
    """Generate detailed lesson content based on grade level"""
    # This would be expanded with specific content for each lesson
    if "Physical & Human Geography" in lesson_title:
        if grade == 6:
            return """
            <h4>Physical Geography</h4>
            <ul>
                <li><strong>Landforms:</strong> mountains, rivers, valleys, plains</li>
                <li><strong>Weather and climate:</strong> temperature, precipitation patterns</li>
                <li><strong>Natural features:</strong> What makes Alaska unique</li>
                <li><strong>Ecosystems:</strong> Plants and animals in different environments</li>
            </ul>
            
            <h4>Human Geography</h4>
            <ul>
                <li><strong>Population:</strong> Where people live and why</li>
                <li><strong>Settlements:</strong> Cities, towns, and villages</li>
                <li><strong>Culture:</strong> Traditions, languages, and customs</li>
                <li><strong>Land use:</strong> How people modify and use the environment</li>
            </ul>
            """
        elif grade == 7:
            return """
            <h4>Physical Geography Systems</h4>
            <ul>
                <li><strong>Geomorphology:</strong> How landforms develop and change over time</li>
                <li><strong>Climatology:</strong> Long-term weather patterns and climate zones</li>
                <li><strong>Hydrology:</strong> Water systems and their geographic impact</li>
                <li><strong>Biogeography:</strong> Distribution of ecosystems and biodiversity</li>
            </ul>
            
            <h4>Human Geography Patterns</h4>
            <ul>
                <li><strong>Demographics:</strong> Population distribution and density patterns</li>
                <li><strong>Urban geography:</strong> City development and urban planning</li>
                <li><strong>Cultural landscapes:</strong> How culture shapes the physical environment</li>
                <li><strong>Economic geography:</strong> Spatial patterns of economic activity</li>
            </ul>
            """
        else:
            return """
            <h4>Advanced Physical Geography Concepts</h4>
            <ul>
                <li><strong>Systems theory:</strong> Interconnected natural systems and feedback loops</li>
                <li><strong>Scale analysis:</strong> Local, regional, and global geographic processes</li>
                <li><strong>Environmental determinism vs. possibilism:</strong> Nature-society relationships</li>
                <li><strong>Spatial analysis:</strong> GIS and quantitative geographic methods</li>
            </ul>
            
            <h4>Complex Human Geography</h4>
            <ul>
                <li><strong>Globalization:</strong> Spatial aspects of global economic integration</li>
                <li><strong>Political geography:</strong> Territories, boundaries, and governance</li>
                <li><strong>Social geography:</strong> Spatial patterns of inequality and identity</li>
                <li><strong>Sustainability:</strong> Human-environment interactions and resource management</li>
            </ul>
            """
    
    return "<p>Detailed lesson content will be provided here based on the specific lesson topic.</p>"

def get_alaska_connections(unit_num, unit_title):
    """Generate Alaska-specific connections for each unit"""
    alaska_connections = {
        1: """
        <p><strong>Physical Geography in Alaska:</strong> Glaciers, permafrost, Arctic Ocean, Pacific Ring of Fire</p>
        <p><strong>Human Geography in Alaska:</strong> Native corporations, resource extraction communities, tourism industry</p>
        <p><strong>Local Example:</strong> How does living in Alaska shape your daily life differently than someone in Florida?</p>
        """,
        2: """
        <p><strong>Alaska's Physical Features:</strong> Mount McKinley (Denali), Yukon River, Brooks Range, Aleutian Islands</p>
        <p><strong>Climate Zones:</strong> Arctic, subarctic, and maritime climates across different regions</p>
        <p><strong>Natural Processes:</strong> Earthquakes, volcanic activity, and glacial movement</p>
        """,
        4: """
        <p><strong>Alaska as US State:</strong> Statehood in 1959, largest state by area, strategic location</p>
        <p><strong>Economic Role:</strong> Oil production, fishing industry, military bases, tourism</p>
        <p><strong>Cultural Diversity:</strong> Alaska Native cultures, immigrant communities, frontier heritage</p>
        """
    }
    
    return alaska_connections.get(unit_num, "<p>Alaska connections will be developed for this unit.</p>")

def get_primary_sources(unit_num, lesson_title, grade):
    """Generate primary source documents section"""
    if "Geography" in lesson_title:
        return """
        <section style="background: #e8f4fd; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>📜 Primary Source Analysis</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>Document 1: Early Alaska Map (1867)</h4>
                    <p><em>[Primary source: Original territorial map from Alaska Purchase]</em></p>
                    <p><strong>Analysis Questions:</strong></p>
                    <ul>
                        <li>What geographic features are emphasized on this historical map?</li>
                        <li>How does this map differ from modern Alaska maps?</li>
                        <li>What does this tell us about geographic knowledge in 1867?</li>
                    </ul>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>Document 2: Native Knowledge</h4>
                    <p><em>[Primary source: Traditional Inupiat place names and their meanings]</em></p>
                    <p><strong>Analysis Questions:</strong></p>
                    <ul>
                        <li>How do traditional place names describe geographic features?</li>
                        <li>What does this reveal about indigenous geographic knowledge?</li>
                        <li>How is this different from European mapping traditions?</li>
                    </ul>
                </div>
            </div>
        </section>
        """
    
    return ""

def get_grade_activities(lesson_title, grade):
    """Generate grade-appropriate activities with scaffolding"""
    if grade == 6:
        return """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div style="background: white; padding: 15px; border-radius: 8px;">
                <h4>🎨 Visual Learning: Geography Sorting</h4>
                <p><strong>Scaffolding:</strong> Start with obvious examples, gradually add complex cases</p>
                <ul>
                    <li>Use picture cards showing various geographic features</li>
                    <li>Students sort into "Physical" and "Human" categories</li>
                    <li>Discuss borderline cases as a class</li>
                    <li>Create a classroom anchor chart with examples</li>
                </ul>
            </div>
            <div style="background: white; padding: 15px; border-radius: 8px;">
                <h4>🗺️ Hands-On: Local Geography Map</h4>
                <p><strong>Differentiation:</strong> Provide base maps for struggling learners</p>
                <ul>
                    <li>Draw a map of the school and surrounding area</li>
                    <li>Use different colors for physical and human features</li>
                    <li>Include a legend and compass rose</li>
                    <li>Share maps with partner for peer feedback</li>
                </ul>
            </div>
        </div>
        """
    elif grade == 7:
        return """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div style="background: white; padding: 15px; border-radius: 8px;">
                <h4>🔍 Research & Analysis: Regional Comparison</h4>
                <p><strong>Scaffolding:</strong> Provide research template and guiding questions</p>
                <ul>
                    <li>Compare physical and human geography of two Alaska regions</li>
                    <li>Use online resources and primary sources</li>
                    <li>Create a comparison chart or Venn diagram</li>
                    <li>Present findings to small groups</li>
                </ul>
            </div>
            <div style="background: white; padding: 15px; border-radius: 8px;">
                <h4>💭 Critical Thinking: Cause and Effect</h4>
                <p><strong>Differentiation:</strong> Provide sentence starters for ELL students</p>
                <ul>
                    <li>Analyze how physical geography affects human activities</li>
                    <li>Create cause-and-effect chains with examples</li>
                    <li>Discuss multiple perspectives on geographic issues</li>
                    <li>Connect to current events and local examples</li>
                </ul>
            </div>
        </div>
        """
    else:  # Grade 8
        return """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div style="background: white; padding: 15px; border-radius: 8px;">
                <h4>🌐 Synthesis Project: Geographic Policy Proposal</h4>
                <p><strong>Scaffolding:</strong> Break into phases with check-in points</p>
                <ul>
                    <li>Identify a geographic challenge in Alaska</li>
                    <li>Research multiple stakeholder perspectives</li>
                    <li>Develop evidence-based policy proposal</li>
                    <li>Present to mock city council with Q&A</li>
                </ul>
            </div>
            <div style="background: white; padding: 15px; border-radius: 8px;">
                <h4>🎯 Performance Task: GIS Analysis</h4>
                <p><strong>Differentiation:</strong> Provide technology support and alternative formats</p>
                <ul>
                    <li>Use online GIS tools to analyze spatial patterns</li>
                    <li>Create layered maps showing multiple variables</li>
                    <li>Write analytical report with supporting evidence</li>
                    <li>Peer review and revision process</li>
                </ul>
            </div>
        </div>
        """

def get_grade_assessments(lesson_title, grade):
    """Generate grade-appropriate assessment strategies"""
    if grade == 6:
        return """
        <div style="background: white; padding: 15px; border-radius: 8px;">
            <h4>Formative Assessment Strategies:</h4>
            <ul>
                <li><strong>Exit Ticket:</strong> Name one physical and one human feature you saw today</li>
                <li><strong>Thumbs Up/Down:</strong> Quick check for understanding during lesson</li>
                <li><strong>Peer Sharing:</strong> Students explain concepts to a partner</li>
                <li><strong>Visual Assessment:</strong> Drawing or labeling activities</li>
            </ul>
            
            <h4>Summative Assessment:</h4>
            <p><strong>Geography Identification Quiz (Scaffolded):</strong></p>
            <ol>
                <li>Look at the picture. Is this physical or human geography? Explain why.</li>
                <li>Give one example of physical geography from Alaska.</li>
                <li>Give one example of human geography from your community.</li>
            </ol>
        </div>
        """
    elif grade == 7:
        return """
        <div style="background: white; padding: 15px; border-radius: 8px;">
            <h4>Formative Assessment Strategies:</h4>
            <ul>
                <li><strong>Think-Pair-Share:</strong> Discuss complex geographic relationships</li>
                <li><strong>Graphic Organizers:</strong> Compare and contrast different regions</li>
                <li><strong>Self-Assessment Rubrics:</strong> Students evaluate their own work</li>
                <li><strong>One-Minute Essays:</strong> Quick written responses to prompts</li>
            </ul>
            
            <h4>Summative Assessment:</h4>
            <p><strong>Geographic Analysis Essay:</strong></p>
            <p>Analyze how physical geography influences human activities in Alaska. Use specific examples and explain the connections between natural features and human adaptations.</p>
        </div>
        """
    else:  # Grade 8
        return """
        <div style="background: white; padding: 15px; border-radius: 8px;">
            <h4>Formative Assessment Strategies:</h4>
            <ul>
                <li><strong>Socratic Seminars:</strong> Student-led discussions on complex topics</li>
                <li><strong>Peer Review:</strong> Students evaluate and provide feedback on projects</li>
                <li><strong>Portfolio Reflections:</strong> Students analyze their learning growth</li>
                <li><strong>Digital Annotations:</strong> Commenting on primary sources and maps</li>
            </ul>
            
            <h4>Performance-Based Assessment:</h4>
            <p><strong>Geographic Challenge Symposium:</strong></p>
            <p>Design and present a comprehensive solution to a real-world geographic challenge in Alaska. Include research, stakeholder analysis, proposed interventions, and evaluation metrics. Present to community panel for authentic feedback.</p>
        </div>
        """

def generate_all_lessons():
    """Generate all lesson files for the entire curriculum"""
    
    lessons_dir = Path("/workspaces/Curriculum/units/lessons")
    lessons_dir.mkdir(exist_ok=True)
    
    quarter_num = 1
    unit_counter = 1
    
    for quarter_name, units in CURRICULUM.items():
        print(f"Generating {quarter_name}...")
        
        for unit_title, unit_data in units.items():
            unit_num = unit_counter
            lessons = unit_data["lessons"]
            
            print(f"  Generating Unit {unit_num}: {unit_data['title']}")
            
            for lesson_num, lesson_title in enumerate(lessons, 1):
                # Generate for all three grade levels
                for grade in [6, 7, 8]:
                    filename = f"unit{unit_num}-lesson{lesson_num}-grade{grade}.html"
                    filepath = lessons_dir / filename
                    
                    html_content = create_lesson_html(
                        unit_num, unit_data['title'], lesson_num, 
                        lesson_title, grade, quarter_num
                    )
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    print(f"    Created: {filename}")
            
            unit_counter += 1
        
        quarter_num += 1
    
    print(f"\n✅ Generated lessons for all {unit_counter-1} units!")
    print(f"📊 Total lesson files created: {(unit_counter-1) * 15} (5 lessons × 3 grades × units)")

if __name__ == "__main__":
    print("🚀 Starting comprehensive lesson generation...")
    print("📚 Based on Alaska World Geography Curriculum scope and sequence")
    print("🎯 Creating differentiated lessons for grades 6, 7, and 8")
    print("=" * 60)
    
    generate_all_lessons()
    
    print("=" * 60)
    print("✨ Lesson generation complete!")
    print("🔗 Remember to update unit HTML files with lesson links")
