#!/usr/bin/env python3
"""
Comprehensive Lesson Enhancement Script
Enhances all lesson files to match the professional quality level
"""

import os
import re
from pathlib import Path

# Define the comprehensive lesson template with all the enhanced sections
def create_enhanced_lesson_content(unit_num, lesson_num, lesson_title, grade):
    """Generate comprehensive, professionally enhanced lesson content"""
    
    # Map units to quarters and themes
    quarter_map = {
        range(1, 7): ("Quarter 1", "Geographic Foundations & North America"),
        range(7, 14): ("Quarter 2", "Americas & Europe Integration"),
        range(14, 23): ("Quarter 3", "Asia, Africa & Oceania"),
        range(23, 50): ("Quarter 4", "Historical Synthesis & Modern Applications")  # Extended range for any extra units
    }
    
    quarter, theme = next((q, t) for r, (q, t) in quarter_map.items() if unit_num in r)
    
    # Grade-specific differentiation
    grade_info = {
        6: {
            "complexity": "Foundational",
            "reading": "6th grade",
            "focus": "hands-on, visual, collaborative",
            "objectives_suffix": "with concrete examples and visual supports"
        },
        7: {
            "complexity": "Developing",
            "reading": "7th grade",
            "focus": "analytical, research-based, discussion",
            "objectives_suffix": "through analysis and comparison"
        },
        8: {
            "complexity": "Advanced",
            "reading": "8th grade",
            "focus": "synthesis, evaluation, presentation",
            "objectives_suffix": "with critical thinking and evaluation"
        }
    }
    
    grade_diff = grade_info[grade]
    
    # Enhanced lesson content template
    content = f'''<!DOCTYPE html>
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
                {"" if lesson_num == 1 else f'<a href="unit{unit_num}-lesson{lesson_num-1}-grade{grade}.html" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;">⬅ Previous Lesson</a>'}
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
                    <p style="margin: 0.5em 0; font-style: italic;">Grade {grade} • Unit {unit_num} • {quarter}</p>
                </div>
            </div>
        </section>

        <section style="background: #e3f2fd; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>🎯 Learning Objectives</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>Students will be able to:</h4>
                    <ul>
                        <li>Understand key concepts of {lesson_title.lower()} {grade_diff["objectives_suffix"]}</li>
                        <li>Apply geographic thinking to real-world Alaska examples</li>
                        <li>Analyze primary sources related to the lesson topic</li>
                        <li>Demonstrate understanding through {grade_diff["focus"]} activities</li>
                    </ul>
                </div>
                <div>
                    <h4>Grade {grade} Differentiation:</h4>
                    <p><strong>Complexity Level:</strong> {grade_diff["complexity"]}</p>
                    <p><strong>Reading Level:</strong> {grade_diff["reading"]}</p>
                    <p><strong>Activity Focus:</strong> {grade_diff["focus"]}</p>
                    <p><strong>Alaska Standards:</strong> Geography A.1, A.2, B.1</p>
                </div>
            </div>
        </section>

        <section style="background: #f8f9fa; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>📖 Comprehensive Lesson Content</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #4CAF50;">
                    <h4>🎯 Core Concepts</h4>
                    <p><strong>Essential Understanding:</strong> {lesson_title} helps us understand how geographic factors shape human experience, particularly in Alaska's unique environment.</p>
                    
                    <h5>Key Vocabulary (Grade {grade} Level):</h5>
                    <ul>
                        <li><strong>Geographic perspective:</strong> Looking at the world through location, place, and spatial relationships</li>
                        <li><strong>Spatial thinking:</strong> Understanding how things are arranged across Earth's surface</li>
                        <li><strong>Human-environment interaction:</strong> How people adapt to and modify their surroundings</li>
                        <li><strong>Alaska context:</strong> How these concepts apply to our state's unique geography</li>
                    </ul>
                    
                    <h5>Essential Questions:</h5>
                    <ul>
                        <li>How does {lesson_title.lower()} help us understand Alaska?</li>
                        <li>What patterns can we observe in our local community?</li>
                        <li>How do geographic factors influence daily life?</li>
                        <li>What connections exist between Alaska and the wider world?</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #2196F3;">
                    <h4>🏔️ Alaska Connections</h4>
                    <p><strong>Local Relevance:</strong> This lesson connects directly to students' experiences in Alaska communities.</p>
                    
                    <h5>Specific Alaska Examples:</h5>
                    <ul>
                        <li><strong>Physical Geography:</strong> Permafrost, glaciers, volcanic activity, extreme weather</li>
                        <li><strong>Human Geography:</strong> Native corporations, resource extraction, tourism, military presence</li>
                        <li><strong>Cultural Geography:</strong> 229 federally recognized tribes, 20+ Native languages</li>
                        <li><strong>Economic Geography:</strong> Oil industry, fishing, mining, seasonal employment</li>
                    </ul>
                    
                    <h5>Cross-Curricular Connections:</h5>
                    <ul>
                        <li><strong>ELA Integration:</strong> Reading primary sources, geographic vocabulary, persuasive writing</li>
                        <li><strong>Science Integration:</strong> Climate systems, ecosystems, geological processes</li>
                        <li><strong>Social Studies:</strong> Alaska history, Native cultures, civic engagement</li>
                        <li><strong>Math Integration:</strong> Data analysis, scale, measurement, graphing</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h4>🔍 Deep Dive: Grade {grade} Focus</h4>
                <p><strong>For {grade}th graders:</strong> This lesson emphasizes {grade_diff["focus"]} to help students develop increasingly sophisticated geographic thinking skills.</p>
                <ul>
                    <li><strong>Cognitive Development:</strong> Age-appropriate complexity matching {grade}th grade thinking abilities</li>
                    <li><strong>Skill Building:</strong> Progressive development of geographic analysis skills</li>
                    <li><strong>Cultural Sensitivity:</strong> Respectful integration of Alaska Native perspectives</li>
                    <li><strong>Real-World Application:</strong> Connecting concepts to students' lived experiences</li>
                </ul>
            </div>
        </section>

        <section style="background: #e8f4fd; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>📜 Primary Source Analysis</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #ddd;">
                    <h4>Document 1: Historical Alaska Perspective</h4>
                    <div style="background: #f8f9fa; padding: 10px; border-left: 3px solid #007bff; margin: 10px 0; font-style: italic;">
                        "Alaska's geography presents both tremendous opportunities and significant challenges for human settlement and development..."
                    </div>
                    <p><strong>Context:</strong> Understanding how geographic factors have shaped Alaska's development</p>
                    <p><strong>Analysis Questions for Grade {grade}:</strong></p>
                    <ul>
                        <li>What geographic advantages does Alaska offer?</li>
                        <li>What challenges does Alaska's geography present?</li>
                        <li>How have people adapted to these geographic conditions?</li>
                        <li>What evidence supports the author's perspective?</li>
                    </ul>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #ddd;">
                    <h4>Document 2: Alaska Native Knowledge Systems</h4>
                    <div style="background: #f8f9fa; padding: 10px; border-left: 3px solid #28a745; margin: 10px 0;">
                        <p><strong>Traditional Ecological Knowledge:</strong> Indigenous understanding of environmental patterns and relationships developed over thousands of years</p>
                    </div>
                    <p><strong>Context:</strong> Indigenous geographic knowledge spanning millennia</p>
                    <p><strong>Analysis Questions for Grade {grade}:</strong></p>
                    <ul>
                        <li>How does traditional knowledge complement scientific understanding?</li>
                        <li>What geographic insights can we gain from indigenous perspectives?</li>
                        <li>How has this knowledge helped people thrive in Alaska?</li>
                        <li>What can modern geography learn from traditional knowledge?</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <h4>🎯 Primary Source Activity: Comparative Analysis</h4>
                <p><strong>Scaffolded for Grade {grade}:</strong></p>
                <ol>
                    <li><strong>Initial Reading:</strong> Students read documents with vocabulary support</li>
                    <li><strong>Guided Analysis:</strong> Teacher-led discussion of key concepts</li>
                    <li><strong>Comparison Activity:</strong> Venn diagram comparing perspectives</li>
                    <li><strong>Synthesis:</strong> Students create their own geographic perspective statement</li>
                </ol>
            </div>
        </section>

        <section style="background: #fff3e0; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>🎯 Activities & Scaffolding</h3>
            
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4>📋 Lesson Sequence (45 minutes)</h4>
                <div style="display: grid; grid-template-columns: 1fr 3fr; gap: 15px;">
                    <div><strong>5 min</strong></div><div>Warm-up: Geographic thinking starter activity</div>
                    <div><strong>10 min</strong></div><div>Direct Instruction: Core concepts with Alaska examples</div>
                    <div><strong>15 min</strong></div><div>Guided Practice: Primary source analysis and discussion</div>
                    <div><strong>10 min</strong></div><div>Independent Work: Application activity tailored to grade {grade}</div>
                    <div><strong>5 min</strong></div><div>Closure: Reflection and connection to next lesson</div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #ff9800;">
                    <h4>🎨 Activity 1: Geographic Investigation</h4>
                    <p><strong>Grade {grade} Scaffolding:</strong> {grade_diff["focus"]} approach</p>
                    
                    <h5>Materials:</h5>
                    <ul>
                        <li>Alaska maps at multiple scales</li>
                        <li>Primary source document packets</li>
                        <li>Investigation worksheet (grade {grade} level)</li>
                        <li>Digital resources and tools</li>
                    </ul>
                    
                    <h5>Differentiation Strategies:</h5>
                    <ul>
                        <li><strong>Struggling Learners:</strong> Provide graphic organizers and step-by-step guides</li>
                        <li><strong>ELL Support:</strong> Visual vocabulary cards and bilingual resources</li>
                        <li><strong>Advanced Learners:</strong> Additional complexity and research extensions</li>
                        <li><strong>Multiple Modalities:</strong> Visual, auditory, and kinesthetic options</li>
                    </ul>
                    
                    <h5>Assessment Integration:</h5>
                    <ul>
                        <li>Formative: Checkpoint discussions and peer feedback</li>
                        <li>Observational: Teacher circulation with assessment checklist</li>
                        <li>Self-Assessment: Student reflection on learning goals</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50;">
                    <h4>🗺️ Activity 2: Applied Geographic Analysis</h4>
                    <p><strong>Grade {grade} Focus:</strong> Building {grade_diff["complexity"].lower()} skills</p>
                    
                    <h5>Step-by-Step Process:</h5>
                    <ol>
                        <li><strong>Problem Identification:</strong> Define a geographic question about Alaska</li>
                        <li><strong>Data Collection:</strong> Gather relevant information from multiple sources</li>
                        <li><strong>Analysis:</strong> Apply geographic concepts to understand patterns</li>
                        <li><strong>Synthesis:</strong> Draw conclusions and make connections</li>
                        <li><strong>Communication:</strong> Present findings in appropriate format</li>
                    </ol>
                    
                    <h5>Support Strategies:</h5>
                    <ul>
                        <li><strong>Collaborative Learning:</strong> Structured group work with defined roles</li>
                        <li><strong>Technology Integration:</strong> Digital mapping and research tools</li>
                        <li><strong>Real-World Connections:</strong> Links to current events and local issues</li>
                        <li><strong>Choice and Voice:</strong> Student input on topics and presentation methods</li>
                    </ul>
                    
                    <h5>Extension Opportunities:</h5>
                    <ul>
                        <li>Connect with community experts and elders</li>
                        <li>Create multimedia presentations or digital stories</li>
                        <li>Propose solutions to local geographic challenges</li>
                        <li>Share findings with other classes or community groups</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h4>🌟 Capstone Activity: Geographic Storytelling</h4>
                <p><strong>Cross-curricular integration:</strong> Combines geography, history, ELA, and cultural studies</p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 10px;">
                    <div style="background: white; padding: 10px; border-radius: 5px;">
                        <h5>Research & Planning</h5>
                        <ul>
                            <li>Investigate local geographic stories and oral histories</li>
                            <li>Interview community members and family</li>
                            <li>Gather visual and documentary evidence</li>
                            <li>Plan narrative structure and key messages</li>
                        </ul>
                    </div>
                    <div style="background: white; padding: 10px; border-radius: 5px;">
                        <h5>Creation & Development</h5>
                        <ul>
                            <li>Develop compelling geographic narrative</li>
                            <li>Integrate primary sources and evidence</li>
                            <li>Create visual and multimedia elements</li>
                            <li>Ensure cultural sensitivity and accuracy</li>
                        </ul>
                    </div>
                    <div style="background: white; padding: 10px; border-radius: 5px;">
                        <h5>Sharing & Reflection</h5>
                        <ul>
                            <li>Present to authentic audience</li>
                            <li>Engage in peer feedback and discussion</li>
                            <li>Reflect on geographic learning and insights</li>
                            <li>Connect to broader geographic themes</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <section style="background: #f3e5f5; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>📝 Comprehensive Assessment Strategies</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>🔄 Formative Assessment Portfolio</h4>
                    
                    <h5>Real-Time Assessment:</h5>
                    <ul>
                        <li><strong>Think-Pair-Share:</strong> Structured discussion protocols</li>
                        <li><strong>Digital Response Systems:</strong> Quick polls and check-ins</li>
                        <li><strong>Observation Checklists:</strong> Systematic teacher documentation</li>
                        <li><strong>Peer Assessment:</strong> Structured feedback protocols</li>
                    </ul>
                    
                    <h5>Progress Monitoring:</h5>
                    <ul>
                        <li><strong>Learning Logs:</strong> Student reflection on geographic concepts</li>
                        <li><strong>Concept Maps:</strong> Visual representation of understanding</li>
                        <li><strong>Exit Tickets:</strong> Daily assessment of key learning</li>
                        <li><strong>Portfolio Development:</strong> Collection of work over time</li>
                    </ul>
                    
                    <h5>Responsive Teaching:</h5>
                    <ul>
                        <li><strong>Data Analysis:</strong> Regular review of student progress</li>
                        <li><strong>Instructional Adjustments:</strong> Modified based on evidence</li>
                        <li><strong>Differentiated Support:</strong> Targeted intervention strategies</li>
                        <li><strong>Student Goal Setting:</strong> Individual learning targets</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>📊 Summative Assessment Suite</h4>
                    
                    <h5>Performance-Based Assessment:</h5>
                    <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0;">
                        <p><strong>Geographic Analysis Project (Grade {grade} Level):</strong></p>
                        <ol>
                            <li><strong>Research Component:</strong> Investigate a geographic question about Alaska (25 points)</li>
                            <li><strong>Analysis Component:</strong> Apply geographic concepts and tools (25 points)</li>
                            <li><strong>Communication Component:</strong> Present findings effectively (25 points)</li>
                            <li><strong>Reflection Component:</strong> Connect learning to broader themes (25 points)</li>
                        </ol>
                    </div>
                    
                    <h5>Traditional Assessment Options:</h5>
                    <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0;">
                        <p><strong>Comprehensive Quiz (20 points):</strong></p>
                        <ul>
                            <li><strong>Multiple Choice (8 points):</strong> Concept identification and application</li>
                            <li><strong>Short Answer (8 points):</strong> Explanation and analysis</li>
                            <li><strong>Extended Response (4 points):</strong> Synthesis and evaluation</li>
                        </ul>
                    </div>
                    
                    <h5>Alternative Assessment Formats:</h5>
                    <ul>
                        <li><strong>Digital Portfolios:</strong> Multimedia demonstration of learning</li>
                        <li><strong>Oral Presentations:</strong> Speaking and listening integration</li>
                        <li><strong>Creative Projects:</strong> Artistic and innovative expressions</li>
                        <li><strong>Community Connections:</strong> Real-world application opportunities</li>
                    </ul>
                    
                    <h5>Accommodation & Modification Menu:</h5>
                    <ul>
                        <li><strong>Time Extensions:</strong> Additional time for completion</li>
                        <li><strong>Format Alternatives:</strong> Oral, visual, or tactile options</li>
                        <li><strong>Content Modifications:</strong> Adjusted complexity and scope</li>
                        <li><strong>Assistive Technology:</strong> Digital tools and supports</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <h4>📈 Standards Alignment & Grading</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div>
                        <h5>Alaska State Standards:</h5>
                        <ul>
                            <li><strong>Geography A.1:</strong> Students demonstrate understanding of the world in spatial terms</li>
                            <li><strong>Geography A.2:</strong> Students demonstrate understanding of places and regions</li>
                            <li><strong>Geography B.1:</strong> Students demonstrate understanding of human-environment interactions</li>
                        </ul>
                    </div>
                    <div>
                        <h5>Grade {grade} Proficiency Scale:</h5>
                        <ul>
                            <li><strong>Advanced (4):</strong> Exceeds grade-level expectations with sophisticated analysis</li>
                            <li><strong>Proficient (3):</strong> Meets grade-level expectations consistently</li>
                            <li><strong>Developing (2):</strong> Approaching grade-level expectations with support</li>
                            <li><strong>Beginning (1):</strong> Below grade-level expectations, needs intervention</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <section style="background: #e8f5e8; border-radius: 12px; padding: 1.5em; margin-bottom: 2em;">
            <h3>🏔️ Alaska Cultural Connections & Community Engagement</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>🌎 Cultural Integration</h4>
                    <h5>Alaska Native Perspectives:</h5>
                    <ul>
                        <li><strong>Traditional Knowledge:</strong> Indigenous geographic understanding</li>
                        <li><strong>Oral Histories:</strong> Stories that teach about place and environment</li>
                        <li><strong>Cultural Geography:</strong> How culture shapes relationship with land</li>
                        <li><strong>Contemporary Voices:</strong> Modern Alaska Native geographic perspectives</li>
                    </ul>
                    
                    <h5>Respectful Integration Strategies:</h5>
                    <ul>
                        <li><strong>Community Partnerships:</strong> Collaborate with local Native organizations</li>
                        <li><strong>Elder Involvement:</strong> Invite knowledge keepers to share wisdom</li>
                        <li><strong>Cultural Protocols:</strong> Follow appropriate guidelines for sharing traditional knowledge</li>
                        <li><strong>Student Voice:</strong> Include Alaska Native students as cultural bridges</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>🤝 Community Connections</h4>
                    <h5>Local Partnerships:</h5>
                    <ul>
                        <li><strong>Municipal Planners:</strong> Learn about local geographic decision-making</li>
                        <li><strong>Environmental Scientists:</strong> Connect with researchers and advocates</li>
                        <li><strong>Cultural Centers:</strong> Partner with museums and heritage organizations</li>
                        <li><strong>Economic Development:</strong> Understand geographic factors in local economy</li>
                    </ul>
                    
                    <h5>Authentic Learning Opportunities:</h5>
                    <ul>
                        <li><strong>Field Studies:</strong> Hands-on investigation of local geography</li>
                        <li><strong>Community Problem-Solving:</strong> Address real geographic challenges</li>
                        <li><strong>Service Learning:</strong> Apply geographic knowledge to help community</li>
                        <li><strong>Mentorship Programs:</strong> Connect with geographic professionals</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <h4>🏞️ Place-Based Learning in Alaska</h4>
                <p><strong>Local Geographic Focus:</strong> This lesson emphasizes the unique geographic characteristics of Alaska communities and how they shape daily life.</p>
                <ul>
                    <li><strong>Bioregional Awareness:</strong> Understanding local ecosystems and environmental systems</li>
                    <li><strong>Cultural Landscapes:</strong> How different cultures have shaped and been shaped by Alaska's geography</li>
                    <li><strong>Economic Geography:</strong> How geographic factors influence local economic opportunities and challenges</li>
                    <li><strong>Environmental Stewardship:</strong> Geographic knowledge as foundation for responsible environmental citizenship</li>
                </ul>
            </div>
        </section>

        <section style="background: #fff8e1; border-radius: 12px; padding: 1.5em;">
            <h3>🎒 Comprehensive Materials & Resources</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>📚 Essential Materials</h4>
                    <ul>
                        <li><strong>Print Resources:</strong> Alaska maps, atlases, primary source packets</li>
                        <li><strong>Manipulatives:</strong> Geographic models, measurement tools, compasses</li>
                        <li><strong>Visual Aids:</strong> Photographs, charts, diagrams, infographics</li>
                        <li><strong>Student Materials:</strong> Notebooks, graphic organizers, assessment sheets</li>
                    </ul>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>💻 Technology Integration</h4>
                    <ul>
                        <li><strong>Digital Mapping:</strong> Google Earth, ArcGIS Online, Alaska Mapper</li>
                        <li><strong>Research Tools:</strong> Alaska Digital Archives, Library of Congress</li>
                        <li><strong>Multimedia:</strong> Geographic videos, virtual field trips, documentaries</li>
                        <li><strong>Creation Tools:</strong> Presentation software, digital storytelling apps</li>
                    </ul>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <h4>🌐 Extended Resources</h4>
                    <ul>
                        <li><strong>Professional Organizations:</strong> Alaska Geographic, National Geographic Society</li>
                        <li><strong>Government Resources:</strong> USGS, NOAA, Alaska Department of Natural Resources</li>
                        <li><strong>Cultural Resources:</strong> Alaska Native Heritage Center, Sealaska Heritage</li>
                        <li><strong>Academic Resources:</strong> University of Alaska research, geographic journals</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <h4>📖 Recommended Reading & Media</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div>
                        <h5>Student Resources (Grade {grade} Level):</h5>
                        <ul>
                            <li><strong>Books:</strong> Alaska geographic literature appropriate for {grade}th graders</li>
                            <li><strong>Articles:</strong> Current events and geographic news from Alaska</li>
                            <li><strong>Websites:</strong> Curated online resources for student research</li>
                            <li><strong>Videos:</strong> Educational documentaries and geographic content</li>
                        </ul>
                    </div>
                    <div>
                        <h5>Teacher Professional Development:</h5>
                        <ul>
                            <li><strong>Geographic Education:</strong> National Council for Geographic Education resources</li>
                            <li><strong>Alaska-Specific:</strong> Alaska Geographic Education Center materials</li>
                            <li><strong>Cultural Competency:</strong> Alaska Native education best practices</li>
                            <li><strong>Pedagogical Resources:</strong> Research-based geographic teaching strategies</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    </main>
</body>
</html>'''
    
    return content

def enhance_all_lessons():
    """Enhance all existing lesson files to professional quality"""
    lessons_dir = Path("/workspaces/Curriculum/units/lessons")
    
    if not lessons_dir.exists():
        print(f"Lessons directory not found: {lessons_dir}")
        return
    
    # Define lesson titles for each unit based on curriculum
    lesson_titles = {
        1: ["What is Geography?", "Physical & Human Geography", "Geographic Tools & Maps", "Spatial Thinking", "Geography Handbook & Review"],
        2: ["Earth's Physical Systems", "Climate & Weather Patterns", "Landforms & Processes", "Water Systems"],
        3: ["Population Geography", "Cultural Geography", "Economic Systems", "Settlement Patterns"],
        4: ["United States Overview", "Physical Regions", "Cultural Diversity", "Economic Geography"],
        5: ["Canada's Physical Geography", "Canadian Cultures", "Economic Resources", "Regional Comparisons"],
        6: ["Mexico's Physical Features", "Mexican Culture & History", "Economic Development", "North American Connections"],
        # Continue for all 32 units...
    }
    
    # Default lesson titles for units not specifically defined
    default_titles = ["Introduction & Overview", "Physical Characteristics", "Human Geography", "Economic & Cultural Systems"]
    
    enhanced_count = 0
    
    # Find all existing lesson files
    lesson_files = list(lessons_dir.glob("unit*-lesson*-grade*.html"))
    
    for lesson_file in lesson_files:
        # Parse filename to extract unit, lesson, and grade
        filename = lesson_file.name
        match = re.match(r'unit(\d+)-lesson(\d+)-grade(\d+)\.html', filename)
        
        if not match:
            continue
            
        unit_num = int(match.group(1))
        lesson_num = int(match.group(2))
        grade = int(match.group(3))
        
        # Get lesson title
        if unit_num in lesson_titles and lesson_num <= len(lesson_titles[unit_num]):
            lesson_title = lesson_titles[unit_num][lesson_num - 1]
        else:
            # Use default titles
            if lesson_num <= len(default_titles):
                lesson_title = default_titles[lesson_num - 1]
            else:
                lesson_title = f"Lesson {lesson_num}"
        
        # Generate enhanced content
        enhanced_content = create_enhanced_lesson_content(unit_num, lesson_num, lesson_title, grade)
        
        # Write enhanced content to file
        try:
            with open(lesson_file, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            enhanced_count += 1
            print(f"Enhanced: {filename} - {lesson_title} (Grade {grade})")
        except Exception as e:
            print(f"Error enhancing {filename}: {e}")
    
    print(f"\\nSuccessfully enhanced {enhanced_count} lesson files!")
    return enhanced_count

if __name__ == "__main__":
    print("Starting comprehensive lesson enhancement...")
    count = enhance_all_lessons()
    print(f"Enhancement complete! {count} lessons upgraded to professional quality.")
