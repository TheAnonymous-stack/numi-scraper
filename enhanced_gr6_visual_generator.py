#!/usr/bin/env python3
"""
Enhanced Grade 6 Visual Generator
Focuses on creating high-quality HTML files with specific SVG implementations
for Grade 6 math questions that genuinely need visual elements.
"""

import os
import json
import re
from pathlib import Path

class EnhancedGr6VisualGenerator:
    def __init__(self):
        self.priority_exercises = [
            # Focus on exercises with rich visual content
            'Gr6_24_E1',  # Pentagon arrays - fraction models
            'Gr6_24_E2',  # More fraction arrays
            'Gr6_24_E3',  # Fraction models
            'Gr6_27_E3',  # Grid models
            'Gr6_27_E4',  # More grids
            'Gr6_33_E1',  # Geometric shapes
            'Gr6_33_E3',  # More geometry
            'Gr6_34_E3',  # Charts/graphs
            'Gr6_35_E1',  # Number lines
            'Gr6_35_E4',  # Coordinate planes
        ]
    
    def should_process_file(self, file_name):
        """Check if this file should be processed for high-quality generation"""
        for pattern in self.priority_exercises:
            if pattern in file_name:
                return True
        return False
    
    def analyze_and_generate_priority_files(self):
        """Process priority files only for high-quality visual generation"""
        print("Enhanced Grade 6 Visual Generator - Processing Priority Files")
        
        json_files = list(Path('.').glob('Gr6_*_variations.json'))
        priority_files = [f for f in json_files if self.should_process_file(f.name)]
        
        print(f"Found {len(priority_files)} priority files to process")
        
        generated_files = []
        total_visual_questions = 0
        
        for file_path in sorted(priority_files):
            print(f"\nProcessing: {file_path.name}")
            questions = self.analyze_file(file_path)
            
            if questions:
                print(f"  Found {len(questions)} visual questions")
                total_visual_questions += len(questions)
                
                # Generate HTML for first 5 questions of each exercise (sample)
                for question in questions[:5]:
                    try:
                        html_file = self.generate_enhanced_html(question)
                        generated_files.append(html_file)
                        print(f"  Generated: {html_file}")
                    except Exception as e:
                        print(f"  Error generating HTML for Q{question['question_num']}: {e}")
        
        print(f"\nGeneration complete!")
        print(f"Total visual questions found: {total_visual_questions}")
        print(f"High-quality HTML files generated: {len(generated_files)}")
        
        return generated_files
    
    def analyze_file(self, file_path):
        """Analyze a file for visual questions"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_name = os.path.basename(file_path)
            match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', file_name)
            if not match:
                return []
            
            week, exercise = match.groups()
            questions = data if isinstance(data, list) else data.get('variations', [])
            
            visual_questions = []
            for i, question in enumerate(questions, 1):
                if self.has_visual_content(question):
                    visual_questions.append({
                        'file': file_name,
                        'week': week,
                        'exercise': exercise,
                        'question_num': i,
                        'data': question
                    })
            
            return visual_questions
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return []
    
    def has_visual_content(self, question):
        """Check if question has visual content"""
        return ('image_tag' in question or 
                'solution_image_tag' in question or
                'backend_description' in question)
    
    def generate_enhanced_html(self, question_data):
        """Generate enhanced HTML with specific visual implementations"""
        week = question_data['week']
        exercise = question_data['exercise']
        question_num = question_data['question_num']
        
        filename = f"Gr6_{week}_E{exercise}_{question_num}_enhanced.html"
        filepath = f"HTML/{filename}"
        
        os.makedirs("HTML", exist_ok=True)
        
        # Get question data
        data = question_data['data']
        
        # Generate visual content based on specific patterns
        html_content = self.create_specific_visual_content(data, week, exercise)
        
        full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 Week {week} Exercise {exercise} Question {question_num}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f9f9f9;
        }}
        .item {{
            display: inline-block;
            margin: 15px;
            padding: 10px;
            vertical-align: top;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .item-label {{
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        svg {{
            border: 1px solid #ccc;
            background-color: white;
        }}
        .pentagon {{
            fill: #4CAF50;
            stroke: #2E7D32;
            stroke-width: 1;
        }}
        .pentagon-faded {{
            fill: #C8E6C9;
            stroke: #81C784;
            stroke-width: 1;
        }}
        .grid-cell {{
            fill: white;
            stroke: #333;
            stroke-width: 1;
        }}
        .grid-cell-filled {{
            fill: #2196F3;
            stroke: #1976D2;
            stroke-width: 1;
        }}
    </style>
</head>
<body>
    <h2>Grade 6 - Week {week}, Exercise {exercise}, Question {question_num}</h2>
    <div class="question-info">
        <p><strong>Question:</strong> {data.get('question_text', 'N/A')[:200]}...</p>
    </div>
    <div class="visual-content">
{html_content}
    </div>
</body>
</html>'''
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        return filepath
    
    def create_specific_visual_content(self, data, week, exercise):
        """Create specific visual content based on week/exercise patterns"""
        
        # Week 24 - Pentagon Arrays for Fractions
        if week == '24':
            return self.create_pentagon_array_visuals(data)
        
        # Week 27 - Grid Models
        elif week == '27':
            return self.create_grid_model_visuals(data)
        
        # Week 33 - Geometric Shapes
        elif week == '33':
            return self.create_geometric_shape_visuals(data)
        
        # Week 34 - Charts and Graphs
        elif week == '34':
            return self.create_chart_visuals(data)
        
        # Week 35 - Number Lines and Coordinates
        elif week == '35':
            return self.create_number_line_coordinate_visuals(data)
        
        # Default enhanced visual
        else:
            return self.create_enhanced_default_visual(data)
    
    def create_pentagon_array_visuals(self, data):
        """Create pentagon array visuals for fraction problems"""
        html_content = []
        
        # Main image (pentagon arrays)
        if 'image_tag' in data:
            backend_desc = data.get('backend_description', '')
            tag = data['image_tag']
            
            # Extract number information from description
            pentagon_count = self.extract_number(backend_desc, 27)  # Default 27
            group_count = self.extract_number(backend_desc.split('groups')[0], 3)  # Default 3
            
            svg_content = self.create_pentagon_array_svg(pentagon_count, group_count)
            
            html_content.append(f'''        <div class="item" label="{tag}">
            <div class="item-label">Main Model: {tag}</div>
{svg_content}
        </div>''')
        
        # Solution images (step-by-step pentagon arrays)
        if 'solution_image_tag' in data:
            solution_tags = data['solution_image_tag']
            if isinstance(solution_tags, list):
                for item in solution_tags:
                    if isinstance(item, list) and len(item) >= 3:
                        step, tag, description = item[0], item[1], item[2]
                        
                        # Determine how many pentagons should be highlighted
                        pentagon_count = self.extract_number(description, 27)
                        group_count = self.extract_number(description, 3)
                        highlight_groups = self.extract_highlight_count(description, step)
                        
                        svg_content = self.create_pentagon_array_svg(
                            pentagon_count, group_count, highlight_groups
                        )
                        
                        html_content.append(f'''        <div class="item" label="{tag}">
            <div class="item-label">Step {step}: {tag}</div>
{svg_content}
        </div>''')
        
        return '\n'.join(html_content) if html_content else self.create_enhanced_default_visual(data)
    
    def create_pentagon_array_svg(self, total_pentagons, groups, highlight_groups=0):
        """Create SVG with pentagon arrays"""
        pentagons_per_group = total_pentagons // groups
        
        # Calculate dimensions
        cols = min(pentagons_per_group, 9)  # Max 9 per row
        rows_per_group = (pentagons_per_group + cols - 1) // cols
        
        pentagon_size = 20
        group_spacing = 40
        total_width = cols * pentagon_size + (groups - 1) * group_spacing + 40
        total_height = rows_per_group * groups * pentagon_size + 40
        
        svg_content = f'''        <svg width="{total_width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">'''
        
        # Draw pentagons in groups
        for group in range(groups):
            is_highlighted = group < highlight_groups
            pentagon_class = "pentagon" if is_highlighted else "pentagon-faded"
            
            group_x_offset = group * (cols * pentagon_size + group_spacing) + 20
            
            for i in range(pentagons_per_group):
                row = i // cols
                col = i % cols
                
                x = group_x_offset + col * pentagon_size + pentagon_size // 2
                y = 20 + row * pentagon_size + pentagon_size // 2
                
                # Simple pentagon approximation (regular polygon)
                points = []
                for angle_step in range(5):
                    angle = (angle_step * 72 - 90) * 3.14159 / 180
                    px = x + (pentagon_size // 3) * cos(angle) if hasattr(__builtins__, 'cos') else x + (pentagon_size // 3) * (1 if angle_step % 2 == 0 else -1)
                    py = y + (pentagon_size // 3) * sin(angle) if hasattr(__builtins__, 'sin') else y + (pentagon_size // 3) * (1 if angle_step < 2 else -1)
                    points.append(f"{px:.1f},{py:.1f}")
                
                # Simplified pentagon as circle for now (can be enhanced)
                svg_content += f'''
            <circle cx="{x}" cy="{y}" r="{pentagon_size//3}" class="{pentagon_class}"/>'''
            
            # Group label
            svg_content += f'''
            <text x="{group_x_offset + cols * pentagon_size // 2}" y="{total_height - 10}" 
                  text-anchor="middle" font-size="12" font-weight="bold">Group {group + 1}</text>'''
        
        svg_content += '''
        </svg>'''
        return svg_content
    
    def create_grid_model_visuals(self, data):
        """Create grid model visuals"""
        html_content = []
        
        if 'image_tag' in data:
            tag = data['image_tag']
            backend_desc = data.get('backend_description', '')
            
            # Extract grid dimensions
            rows, cols = self.extract_grid_dimensions(backend_desc)
            svg_content = self.create_grid_svg(rows, cols)
            
            html_content.append(f'''        <div class="item" label="{tag}">
            <div class="item-label">Grid Model: {tag}</div>
{svg_content}
        </div>''')
        
        return '\n'.join(html_content) if html_content else self.create_enhanced_default_visual(data)
    
    def create_grid_svg(self, rows, cols, filled_ratio=0.5):
        """Create grid SVG"""
        cell_size = 25
        width = cols * cell_size + 20
        height = rows * cell_size + 20
        
        svg_content = f'''        <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(10,10)">'''
        
        filled_cells = int(rows * cols * filled_ratio)
        
        for r in range(rows):
            for c in range(cols):
                x = c * cell_size
                y = r * cell_size
                cell_num = r * cols + c
                cell_class = "grid-cell-filled" if cell_num < filled_cells else "grid-cell"
                
                svg_content += f'''
                <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" class="{cell_class}"/>'''
        
        svg_content += '''
            </g>
        </svg>'''
        return svg_content
    
    def create_geometric_shape_visuals(self, data):
        """Create geometric shape visuals"""
        return self.create_enhanced_default_visual(data)
    
    def create_chart_visuals(self, data):
        """Create chart and graph visuals"""
        return self.create_enhanced_default_visual(data)
    
    def create_number_line_coordinate_visuals(self, data):
        """Create number line and coordinate visuals"""
        return self.create_enhanced_default_visual(data)
    
    def create_enhanced_default_visual(self, data):
        """Create enhanced default visual"""
        tag = data.get('image_tag', 'visual_element')
        description = data.get('backend_description', 'Visual element required')
        
        return f'''        <div class="item" label="{tag}">
            <div class="item-label">Visual: {tag}</div>
            <svg width="200" height="150" xmlns="http://www.w3.org/2000/svg">
                <rect x="10" y="10" width="180" height="130" fill="#f0f8ff" stroke="#4169e1" stroke-width="2" rx="5"/>
                <text x="100" y="75" text-anchor="middle" font-size="14" fill="#4169e1">
                    Enhanced Visual Element
                </text>
                <text x="100" y="95" text-anchor="middle" font-size="10" fill="#666">
                    {description[:50]}...
                </text>
            </svg>
        </div>'''
    
    def extract_number(self, text, default):
        """Extract number from text"""
        numbers = re.findall(r'\\b(\\d+)\\b', text)
        return int(numbers[0]) if numbers else default
    
    def extract_grid_dimensions(self, description):
        """Extract grid dimensions from description"""
        patterns = [
            r'(\\d+)\\s*[x×]\\s*(\\d+)',
            r'(\\d+)\\s*by\\s*(\\d+)',
            r'(\\d+)\\s*rows?.*?(\\d+)\\s*columns?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description.lower())
            if match:
                return int(match.group(1)), int(match.group(2))
        
        return 4, 4  # Default
    
    def extract_highlight_count(self, description, step):
        """Extract how many groups to highlight based on step and description"""
        desc_lower = description.lower()
        
        if 'first 2' in desc_lower or 'two' in desc_lower:
            return 2
        elif 'first' in desc_lower:
            return 1
        elif step == '3/4' or step == '4/4':
            return 2
        else:
            return 1

def main():
    generator = EnhancedGr6VisualGenerator()
    generated_files = generator.analyze_and_generate_priority_files()
    
    if generated_files:
        print(f"\\n=== Generated Enhanced HTML Files ===")
        for file_path in generated_files:
            print(f"  {file_path}")

if __name__ == "__main__":
    main()