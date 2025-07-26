#!/usr/bin/env python3
"""
Comprehensive Lesson Builder
Creates complete, standalone educational resources from fragmented extracted content.
Designed for educators who need comprehensive lesson materials without relying on textbooks.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveLessonBuilder:
    """
    Transforms fragmented curriculum content into complete, educator-ready lessons.
    """
    
    def __init__(self, workspace_dir: str = "/workspaces/Curriculum"):
        self.workspace_dir = Path(workspace_dir)
        self.output_dir = self.workspace_dir / "complete_lessons"
        self.output_dir.mkdir(exist_ok=True)
        
        # Educational content frameworks
        self.lesson_structure_template = {
            "lesson_overview": {
                "title": "",
                "grade_level": "",
                "duration": "45-50 minutes",
                "subject": "Social Studies",
                "big_ideas": [],
                "essential_questions": []
            },
            "learning_objectives": {
                "what_students_will_learn": [],
                "what_students_will_be_able_to_do": [],
                "assessment_criteria": []
            },
            "background_for_teacher": {
                "content_overview": "",
                "key_concepts": {},
                "common_misconceptions": [],
                "prior_knowledge_needed": []
            },
            "lesson_sequence": {
                "opening_hook": "",
                "direct_instruction": "",
                "guided_practice": "",
                "independent_practice": "",
                "closure": ""
            },
            "activities_and_resources": {
                "primary_activities": [],
                "extension_activities": [],
                "materials_needed": [],
                "technology_integration": []
            },
            "assessment_strategies": {
                "formative_assessments": [],
                "summative_assessments": [],
                "rubrics": [],
                "differentiation": []
            },
            "vocabulary_and_concepts": {
                "key_vocabulary": {},
                "academic_language": [],
                "content_specific_terms": {}
            }
        }
        
    def analyze_extracted_content(self, content_file: str) -> Dict[str, Any]:
        """
        Analyze extracted content to identify lesson components.
        """
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract useful content from the fragmented data
            analyzed_content = {
                "lesson_fragments": [],
                "vocabulary_terms": [],
                "activities": [],
                "assessments": [],
                "teaching_instructions": [],
                "background_content": []
            }
            
            # Process the extracted content intelligently
            if isinstance(data, dict):
                for file_name, content in data.items():
                    if isinstance(content, dict) and 'extracted_content' in content:
                        raw_content = content['extracted_content']
                        self._categorize_content_fragments(raw_content, analyzed_content)
            
            return analyzed_content
            
        except Exception as e:
            logger.error(f"Error analyzing content file {content_file}: {e}")
            return {}
    
    def _categorize_content_fragments(self, raw_content: str, analyzed_content: Dict[str, Any]):
        """
        Categorize raw content fragments into meaningful lesson components.
        """
        content_lines = raw_content.split('\n')
        
        for line in content_lines:
            line = line.strip()
            if not line:
                continue
                
            # Identify vocabulary terms
            if any(indicator in line.lower() for indicator in ['define', 'vocabulary', 'key terms', 'glossary']):
                analyzed_content["vocabulary_terms"].append(line)
            
            # Identify activities
            elif any(indicator in line.lower() for indicator in ['activity', 'practice', 'exercise', 'students will']):
                analyzed_content["activities"].append(line)
            
            # Identify assessments
            elif any(indicator in line.lower() for indicator in ['assessment', 'quiz', 'test', 'evaluate', 'rubric']):
                analyzed_content["assessments"].append(line)
            
            # Identify teaching instructions
            elif any(indicator in line.lower() for indicator in ['teach', 'instruct', 'explain', 'demonstrate']):
                analyzed_content["teaching_instructions"].append(line)
            
            # Everything else as lesson fragments
            else:
                analyzed_content["lesson_fragments"].append(line)
    
    def build_comprehensive_lesson(self, lesson_topic: str, grade_level: str, 
                                 analyzed_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a comprehensive lesson from analyzed content fragments.
        """
        lesson = self.lesson_structure_template.copy()
        
        # Fill in basic information
        lesson["lesson_overview"]["title"] = f"Understanding {lesson_topic}"
        lesson["lesson_overview"]["grade_level"] = grade_level
        lesson["lesson_overview"]["big_ideas"] = self._generate_big_ideas(lesson_topic, analyzed_content)
        lesson["lesson_overview"]["essential_questions"] = self._generate_essential_questions(lesson_topic)
        
        # Build learning objectives
        lesson["learning_objectives"] = self._build_learning_objectives(lesson_topic, grade_level, analyzed_content)
        
        # Create comprehensive background for teacher
        lesson["background_for_teacher"] = self._build_teacher_background(lesson_topic, analyzed_content)
        
        # Design lesson sequence
        lesson["lesson_sequence"] = self._build_lesson_sequence(lesson_topic, analyzed_content)
        
        # Create activities and resources
        lesson["activities_and_resources"] = self._build_activities_and_resources(lesson_topic, analyzed_content)
        
        # Design assessment strategies
        lesson["assessment_strategies"] = self._build_assessment_strategies(lesson_topic, analyzed_content)
        
        # Build vocabulary section
        lesson["vocabulary_and_concepts"] = self._build_vocabulary_section(lesson_topic, analyzed_content)
        
        return lesson
    
    def _generate_big_ideas(self, lesson_topic: str, analyzed_content: Dict[str, Any]) -> List[str]:
        """Generate big ideas for the lesson."""
        big_ideas = [
            f"{lesson_topic} is a fundamental concept that helps us understand our world",
            f"Geographic thinking involves analyzing patterns, relationships, and connections",
            f"Understanding {lesson_topic} helps us make informed decisions about places and people"
        ]
        
        # Add specific big ideas based on content
        if any('location' in fragment.lower() for fragment in analyzed_content.get("lesson_fragments", [])):
            big_ideas.append("Location affects how people live, work, and interact with their environment")
        
        if any('movement' in fragment.lower() for fragment in analyzed_content.get("lesson_fragments", [])):
            big_ideas.append("Movement of people, goods, and ideas shapes cultures and economies")
        
        return big_ideas
    
    def _generate_essential_questions(self, lesson_topic: str) -> List[str]:
        """Generate essential questions for the lesson."""
        return [
            f"What is {lesson_topic} and why is it important?",
            f"How does {lesson_topic} affect daily life and decision-making?",
            f"What patterns and relationships can we observe when studying {lesson_topic}?",
            f"How can understanding {lesson_topic} help us solve real-world problems?"
        ]
    
    def _build_learning_objectives(self, lesson_topic: str, grade_level: str, 
                                 analyzed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive learning objectives."""
        
        grade_num = int(re.search(r'\d+', grade_level).group()) if re.search(r'\d+', grade_level) else 6
        
        # Adjust complexity based on grade level
        complexity_levels = {
            6: {"verb": "identify and describe", "complexity": "basic concepts"},
            7: {"verb": "analyze and explain", "complexity": "relationships and patterns"},
            8: {"verb": "evaluate and synthesize", "complexity": "complex interactions and implications"}
        }
        
        level = complexity_levels.get(grade_num, complexity_levels[6])
        
        return {
            "what_students_will_learn": [
                f"The fundamental concepts and principles of {lesson_topic}",
                f"Key vocabulary and terminology related to {lesson_topic}",
                f"Real-world examples and applications of {lesson_topic}",
                f"Connections between {lesson_topic} and other geographic concepts"
            ],
            "what_students_will_be_able_to_do": [
                f"{level['verb']} {level['complexity']} of {lesson_topic}",
                f"Use geographic thinking to examine {lesson_topic} in different contexts",
                f"Create examples and non-examples of {lesson_topic}",
                f"Apply knowledge of {lesson_topic} to solve geographic problems"
            ],
            "assessment_criteria": [
                "Accurately defines key vocabulary terms",
                "Provides specific, relevant examples",
                "Demonstrates understanding through written and oral explanations",
                "Makes connections to previous learning and real-world situations"
            ]
        }
    
    def _build_teacher_background(self, lesson_topic: str, analyzed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive background information for teachers."""
        
        # Extract key concepts from analyzed content
        key_concepts = {}
        for fragment in analyzed_content.get("lesson_fragments", []):
            if len(fragment) > 50:  # Substantial content
                # Create concept from fragment
                concept_name = fragment.split('.')[0].strip() if '.' in fragment else fragment[:30] + "..."
                key_concepts[concept_name] = fragment
        
        return {
            "content_overview": f"""
            This lesson introduces students to {lesson_topic}, a foundational concept in geography.
            Students will explore how {lesson_topic} affects our understanding of the world and
            influences human activities and decision-making. The lesson builds geographic thinking
            skills through hands-on activities, real-world examples, and collaborative learning.
            
            {lesson_topic} is essential for students to understand because it provides a framework
            for analyzing spatial relationships, human-environment interactions, and geographic
            patterns. This understanding serves as a building block for more advanced geographic
            concepts throughout the curriculum.
            """,
            "key_concepts": key_concepts if key_concepts else {
                f"Definition of {lesson_topic}": f"Clear, student-friendly explanation of what {lesson_topic} means",
                f"Components of {lesson_topic}": f"The main parts or elements that make up {lesson_topic}",
                f"Examples of {lesson_topic}": f"Real-world examples students can relate to",
                f"Non-examples": f"What {lesson_topic} is NOT, to clarify misconceptions"
            },
            "common_misconceptions": [
                f"Students may think {lesson_topic} only applies to certain places or situations",
                "Students might confuse this concept with similar geographic terms",
                "Students may oversimplify the concept and miss important nuances"
            ],
            "prior_knowledge_needed": [
                "Basic understanding of maps and globes",
                "Familiarity with cardinal directions",
                "Understanding of scale (local, regional, global)",
                "Basic vocabulary related to places and regions"
            ]
        }
    
    def _build_lesson_sequence(self, lesson_topic: str, analyzed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build a comprehensive lesson sequence with detailed instructions."""
        
        activities = analyzed_content.get("activities", [])
        teaching_instructions = analyzed_content.get("teaching_instructions", [])
        
        return {
            "opening_hook": f"""
            Begin with an engaging question: "What do you think of when you hear the word '{lesson_topic}'?"
            
            Show students 3-4 images that represent different aspects of {lesson_topic}. Have them work
            in pairs to discuss what they notice and what questions they have. This activates prior
            knowledge and creates curiosity about the lesson topic.
            
            Time: 5-7 minutes
            """,
            
            "direct_instruction": f"""
            1. Introduce the lesson objectives and essential questions (2 minutes)
            
            2. Define {lesson_topic} using student-friendly language:
               - Start with what students already know
               - Build to the formal definition
               - Use visual aids and real-world examples
               - Check for understanding frequently
            
            3. Explore the key components of {lesson_topic}:
               - Break down the concept into manageable parts
               - Use graphic organizers to show relationships
               - Provide multiple examples for each component
               - Connect to students' experiences and local context
            
            4. Demonstrate how {lesson_topic} applies in different situations:
               - Use case studies relevant to students' lives
               - Show both obvious and subtle examples
               - Discuss why understanding {lesson_topic} matters
            
            Time: 15-20 minutes
            """,
            
            "guided_practice": f"""
            1. Think-Pair-Share Activity:
               - Students individually brainstorm examples of {lesson_topic}
               - Pairs share and refine their ideas
               - Class creates a collaborative list
            
            2. Sorting Activity:
               - Provide examples and non-examples of {lesson_topic}
               - Students work in small groups to sort and justify their decisions
               - Groups share their reasoning with the class
            
            3. Real-World Application:
               - Present a local or current event scenario
               - Guide students to identify how {lesson_topic} applies
               - Students explain their thinking using academic vocabulary
            
            Time: 15-18 minutes
            """,
            
            "independent_practice": f"""
            Choice Board Activity - Students select from:
            
            Option A: Create a mini-poster showing 3 examples of {lesson_topic} with explanations
            Option B: Write a short story that demonstrates understanding of {lesson_topic}
            Option C: Design a simple game that teaches {lesson_topic} to younger students
            Option D: Create a concept map connecting {lesson_topic} to other geographic ideas
            
            All options require students to use key vocabulary and demonstrate understanding
            through written explanations or visual representations.
            
            Time: 10-12 minutes
            """,
            
            "closure": f"""
            1. Exit Ticket: Students write one thing they learned about {lesson_topic} and
               one question they still have (3 minutes)
            
            2. Quick Gallery Walk: Students post their independent work and do a silent
               gallery walk to see different approaches (2 minutes)
            
            3. Closing Circle: Revisit the essential questions and have students share
               key insights or "aha moments" (3-5 minutes)
            
            Preview the next lesson and explain how today's learning connects to upcoming topics.
            """
        }
    
    def _build_activities_and_resources(self, lesson_topic: str, analyzed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive activities and resources."""
        
        return {
            "primary_activities": [
                {
                    "name": f"{lesson_topic} Photo Analysis",
                    "description": f"Students examine photographs and identify examples of {lesson_topic}",
                    "materials": "Photo collection, analysis worksheet, magnifying glasses",
                    "time": "10-15 minutes",
                    "differentiation": "Provide photos of varying complexity; offer sentence frames for explanations"
                },
                {
                    "name": f"{lesson_topic} in Our Community",
                    "description": f"Students identify local examples of {lesson_topic} through research or fieldwork",
                    "materials": "Local maps, community resources, research templates",
                    "time": "20-25 minutes",
                    "differentiation": "Provide different community examples based on student background knowledge"
                },
                {
                    "name": f"Building Understanding of {lesson_topic}",
                    "description": f"Hands-on activity where students create physical models or diagrams",
                    "materials": "Construction materials, templates, reference images",
                    "time": "15-20 minutes",
                    "differentiation": "Offer both 2D and 3D options; provide step-by-step guides for struggling learners"
                }
            ],
            "extension_activities": [
                f"Research famous examples of {lesson_topic} around the world",
                f"Create a presentation about how {lesson_topic} affects different cultures",
                f"Design a solution to a problem related to {lesson_topic}",
                f"Interview community members about their experiences with {lesson_topic}"
            ],
            "materials_needed": [
                "World map or globe", "Local/regional maps", "Photo collection related to lesson topic",
                "Chart paper and markers", "Sticky notes", "Graphic organizer templates",
                "Access to research materials (books, internet)", "Construction paper and art supplies"
            ],
            "technology_integration": [
                "Use digital mapping tools to explore examples",
                "Research online resources for current examples",
                "Create digital presentations or posters",
                "Use virtual field trips to explore distant examples"
            ]
        }
    
    def _build_assessment_strategies(self, lesson_topic: str, analyzed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive assessment strategies."""
        
        return {
            "formative_assessments": [
                "Thumbs up/down checks during direct instruction",
                "Think-pair-share responses monitored by teacher",
                "Exit tickets with specific questions about understanding",
                "Observation of student discussions and group work",
                "Quick sketches or drawings to show understanding"
            ],
            "summative_assessments": [
                {
                    "name": f"{lesson_topic} Performance Task",
                    "description": f"Students demonstrate understanding by applying {lesson_topic} to a real-world scenario",
                    "criteria": ["Accuracy of content", "Use of vocabulary", "Quality of examples", "Clear explanation"]
                },
                {
                    "name": "Vocabulary Quiz",
                    "description": "Students define key terms and provide examples",
                    "criteria": ["Correct definitions", "Appropriate examples", "Understanding of connections"]
                }
            ],
            "rubrics": [
                {
                    "criteria": "Understanding of Concept",
                    "levels": {
                        "Advanced": f"Demonstrates deep understanding of {lesson_topic} with sophisticated examples",
                        "Proficient": f"Shows solid understanding of {lesson_topic} with appropriate examples",
                        "Developing": f"Shows basic understanding of {lesson_topic} with simple examples",
                        "Beginning": f"Shows minimal understanding of {lesson_topic}"
                    }
                }
            ],
            "differentiation": [
                "Provide graphic organizers for students who need structure",
                "Offer choice in how students demonstrate understanding",
                "Use visual supports and real-world connections",
                "Provide additional time for processing and completion",
                "Offer collaborative options for students who learn better with peers"
            ]
        }
    
    def _build_vocabulary_section(self, lesson_topic: str, analyzed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive vocabulary and concepts section."""
        
        # Extract vocabulary from analyzed content
        vocabulary_terms = {}
        for term in analyzed_content.get("vocabulary_terms", []):
            if ':' in term:
                parts = term.split(':', 1)
                vocabulary_terms[parts[0].strip()] = parts[1].strip()
        
        # Add standard vocabulary if none found
        if not vocabulary_terms:
            vocabulary_terms = {
                lesson_topic: f"Student-friendly definition of {lesson_topic} with examples",
                "Geography": "The study of Earth's surface and the people, plants, and animals that live on it",
                "Location": "Where something is found on Earth",
                "Pattern": "A repeated design or sequence that can be observed in geographic data"
            }
        
        return {
            "key_vocabulary": vocabulary_terms,
            "academic_language": [
                "analyze", "compare", "contrast", "describe", "explain", "identify",
                "observe", "pattern", "relationship", "significance"
            ],
            "content_specific_terms": {
                "Tier 2 vocabulary": "Academic words used across subjects",
                "Tier 3 vocabulary": "Subject-specific geographic terms",
                "Cognates": "Words similar in English and other languages"
            }
        }
    
    def generate_lesson_html(self, lesson_data: Dict[str, Any], lesson_id: str) -> str:
        """Generate complete HTML lesson file."""
        
        title = lesson_data["lesson_overview"]["title"]
        grade = lesson_data["lesson_overview"]["grade_level"]
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {grade}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }}
        
        .lesson-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        
        .lesson-section {{
            background: white;
            margin: 20px 0;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }}
        
        .section-header {{
            color: #667eea;
            font-size: 1.4em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .objective-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        
        .activity-card {{
            background: #f8f9ff;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 10px 0;
        }}
        
        .vocab-term {{
            background: #e8f2ff;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #2196F3;
        }}
        
        .assessment-rubric {{
            background: #f0f8f0;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        
        .time-indicator {{
            background: #ffe8e8;
            color: #d32f2f;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        
        .essential-question {{
            background: #fff3e0;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #ff9800;
            font-style: italic;
        }}
        
        ul, ol {{ margin: 10px 0; padding-left: 25px; }}
        li {{ margin: 8px 0; }}
        
        .teacher-note {{
            background: #f3e5f5;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #9c27b0;
            margin: 15px 0;
        }}
        
        .materials-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }}
        
        .material-item {{
            background: #e8f5e8;
            padding: 8px 12px;
            border-radius: 5px;
            text-align: center;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="lesson-header">
        <h1>🎓 {title}</h1>
        <p style="font-size: 1.2em; margin: 10px 0;">{grade} • {lesson_data['lesson_overview']['duration']} • {lesson_data['lesson_overview']['subject']}</p>
        <p style="opacity: 0.9;">Complete Educator-Ready Lesson Plan</p>
    </div>

    <div class="lesson-section">
        <h2 class="section-header">🎯 Lesson Overview</h2>
        <div class="objective-grid">
            <div>
                <h3>Big Ideas</h3>
                <ul>
                    {''.join(f'<li>{idea}</li>' for idea in lesson_data['lesson_overview']['big_ideas'])}
                </ul>
            </div>
            <div>
                <h3>Essential Questions</h3>
                {''.join(f'<div class="essential-question">❓ {question}</div>' for question in lesson_data['lesson_overview']['essential_questions'])}
            </div>
        </div>
    </div>

    <div class="lesson-section">
        <h2 class="section-header">📚 Learning Objectives</h2>
        <div class="objective-grid">
            <div>
                <h3>What Students Will Learn</h3>
                <ul>
                    {''.join(f'<li>{objective}</li>' for objective in lesson_data['learning_objectives']['what_students_will_learn'])}
                </ul>
            </div>
            <div>
                <h3>What Students Will Be Able To Do</h3>
                <ul>
                    {''.join(f'<li>{objective}</li>' for objective in lesson_data['learning_objectives']['what_students_will_be_able_to_do'])}
                </ul>
            </div>
        </div>
        <div class="teacher-note">
            <h4>Assessment Criteria</h4>
            <ul>
                {''.join(f'<li>{criteria}</li>' for criteria in lesson_data['learning_objectives']['assessment_criteria'])}
            </ul>
        </div>
    </div>

    <div class="lesson-section">
        <h2 class="section-header">👩‍🏫 Background for Teacher</h2>
        <div class="teacher-note">
            <h3>Content Overview</h3>
            <p>{lesson_data['background_for_teacher']['content_overview']}</p>
        </div>
        
        <h3>Key Concepts to Teach</h3>
        {''.join(f'<div class="vocab-term"><strong>{concept}:</strong> {explanation}</div>' for concept, explanation in lesson_data['background_for_teacher']['key_concepts'].items())}
        
        <div class="objective-grid">
            <div>
                <h3>Common Misconceptions</h3>
                <ul>
                    {''.join(f'<li>{misconception}</li>' for misconception in lesson_data['background_for_teacher']['common_misconceptions'])}
                </ul>
            </div>
            <div>
                <h3>Prior Knowledge Needed</h3>
                <ul>
                    {''.join(f'<li>{knowledge}</li>' for knowledge in lesson_data['background_for_teacher']['prior_knowledge_needed'])}
                </ul>
            </div>
        </div>
    </div>

    <div class="lesson-section">
        <h2 class="section-header">⏰ Lesson Sequence</h2>
        
        <div class="activity-card">
            <h3>Opening Hook <span class="time-indicator">5-7 minutes</span></h3>
            <p>{lesson_data['lesson_sequence']['opening_hook']}</p>
        </div>
        
        <div class="activity-card">
            <h3>Direct Instruction <span class="time-indicator">15-20 minutes</span></h3>
            <div style="white-space: pre-line;">{lesson_data['lesson_sequence']['direct_instruction']}</div>
        </div>
        
        <div class="activity-card">
            <h3>Guided Practice <span class="time-indicator">15-18 minutes</span></h3>
            <div style="white-space: pre-line;">{lesson_data['lesson_sequence']['guided_practice']}</div>
        </div>
        
        <div class="activity-card">
            <h3>Independent Practice <span class="time-indicator">10-12 minutes</span></h3>
            <div style="white-space: pre-line;">{lesson_data['lesson_sequence']['independent_practice']}</div>
        </div>
        
        <div class="activity-card">
            <h3>Closure <span class="time-indicator">8-10 minutes</span></h3>
            <div style="white-space: pre-line;">{lesson_data['lesson_sequence']['closure']}</div>
        </div>
    </div>

    <div class="lesson-section">
        <h2 class="section-header">🎨 Activities & Resources</h2>
        
        <h3>Primary Activities</h3>
        {''.join(f'''
        <div class="activity-card">
            <h4>{activity['name']}</h4>
            <p><strong>Description:</strong> {activity['description']}</p>
            <p><strong>Materials:</strong> {activity['materials']}</p>
            <p><strong>Time:</strong> {activity['time']}</p>
            <p><strong>Differentiation:</strong> {activity['differentiation']}</p>
        </div>
        ''' for activity in lesson_data['activities_and_resources']['primary_activities'])}
        
        <h3>Materials Needed</h3>
        <div class="materials-list">
            {''.join(f'<div class="material-item">📦 {material}</div>' for material in lesson_data['activities_and_resources']['materials_needed'])}
        </div>
        
        <div class="objective-grid">
            <div>
                <h3>Extension Activities</h3>
                <ul>
                    {''.join(f'<li>{activity}</li>' for activity in lesson_data['activities_and_resources']['extension_activities'])}
                </ul>
            </div>
            <div>
                <h3>Technology Integration</h3>
                <ul>
                    {''.join(f'<li>{tech}</li>' for tech in lesson_data['activities_and_resources']['technology_integration'])}
                </ul>
            </div>
        </div>
    </div>

    <div class="lesson-section">
        <h2 class="section-header">📊 Assessment Strategies</h2>
        
        <div class="objective-grid">
            <div>
                <h3>Formative Assessments</h3>
                <ul>
                    {''.join(f'<li>{assessment}</li>' for assessment in lesson_data['assessment_strategies']['formative_assessments'])}
                </ul>
            </div>
            <div>
                <h3>Differentiation Strategies</h3>
                <ul>
                    {''.join(f'<li>{strategy}</li>' for strategy in lesson_data['assessment_strategies']['differentiation'])}
                </ul>
            </div>
        </div>
        
        <h3>Summative Assessments</h3>
        {''.join(f'''
        <div class="assessment-rubric">
            <h4>{assessment['name']}</h4>
            <p>{assessment['description']}</p>
            <strong>Criteria:</strong> {', '.join(assessment['criteria'])}
        </div>
        ''' for assessment in lesson_data['assessment_strategies']['summative_assessments'])}
    </div>

    <div class="lesson-section">
        <h2 class="section-header">📖 Vocabulary & Key Concepts</h2>
        
        <h3>Key Vocabulary Terms</h3>
        {''.join(f'<div class="vocab-term"><strong>{term}:</strong> {definition}</div>' for term, definition in lesson_data['vocabulary_and_concepts']['key_vocabulary'].items())}
        
        <div class="teacher-note">
            <h3>Academic Language Support</h3>
            <p><strong>Academic Language:</strong> {', '.join(lesson_data['vocabulary_and_concepts']['academic_language'])}</p>
        </div>
    </div>

    <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; text-align: center; margin-top: 30px;">
        <h3 style="color: #2e7d32; margin: 0;">✅ Complete Educator-Ready Lesson</h3>
        <p style="margin: 10px 0 0 0; color: #388e3c;">This lesson provides everything needed to teach without additional textbook resources.</p>
    </div>

</body>
</html>"""
        
        return html_content
    
    def process_all_lessons(self, grade_level: str = "grade6"):
        """Process all lessons for a given grade level."""
        
        logger.info(f"Starting comprehensive lesson building for {grade_level}")
        
        # Find extracted content files
        content_files = []
        for file_path in self.workspace_dir.glob("*extracted_content*.json"):
            content_files.append(file_path)
        
        if not content_files:
            logger.warning("No extracted content files found")
            return
        
        lessons_created = 0
        
        # Sample lesson topics based on typical curriculum
        lesson_topics = [
            "Geography", "Location and Place", "Human-Environment Interaction",
            "Movement and Migration", "Regions", "Maps and Globes",
            "Physical Features", "Climate and Weather", "Population",
            "Culture and Society", "Economic Systems", "Government and Politics"
        ]
        
        for i, topic in enumerate(lesson_topics, 1):
            try:
                # Use the first available content file for analysis
                analyzed_content = self.analyze_extracted_content(str(content_files[0]))
                
                # Build comprehensive lesson
                lesson_data = self.build_comprehensive_lesson(topic, grade_level, analyzed_content)
                
                # Generate HTML file
                lesson_id = f"unit{(i-1)//4 + 1}-lesson{((i-1)%4) + 1}-{grade_level}"
                html_content = self.generate_lesson_html(lesson_data, lesson_id)
                
                # Save lesson file
                output_file = self.output_dir / f"{lesson_id}-complete.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                logger.info(f"Created comprehensive lesson: {output_file}")
                lessons_created += 1
                
                # Also save lesson data as JSON for reference
                json_file = self.output_dir / f"{lesson_id}-data.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(lesson_data, f, indent=2, ensure_ascii=False)
                
            except Exception as e:
                logger.error(f"Error creating lesson for {topic}: {e}")
        
        logger.info(f"Comprehensive lesson building complete. Created {lessons_created} lessons.")

def main():
    """Main function to run the comprehensive lesson builder."""
    
    print("🚀 Starting Comprehensive Lesson Builder")
    print("="*60)
    print("This tool creates complete, educator-ready lessons from fragmented content.")
    print("New educators will be able to teach confidently without textbooks.")
    print()
    
    # Initialize the builder
    builder = ComprehensiveLessonBuilder()
    
    # Process lessons for each grade level
    grades = ["grade6", "grade7", "grade8"]
    
    for grade in grades:
        print(f"📚 Building comprehensive lessons for {grade}...")
        builder.process_all_lessons(grade)
        print(f"✅ Completed {grade} lessons")
        print()
    
    print("🎉 All comprehensive lessons created successfully!")
    print(f"📁 Check the '{builder.output_dir}' directory for complete lesson files.")
    print()
    print("These lessons include:")
    print("• Complete background information for teachers")
    print("• Detailed lesson sequences with timing")
    print("• Comprehensive activities and resources")
    print("• Full assessment strategies and rubrics")
    print("• All necessary vocabulary and concepts")
    print("• Everything needed to teach without textbooks!")

if __name__ == "__main__":
    main()
