#!/usr/bin/env python3
"""
Targeted Grade 6 HTML Generator
Efficiently processes Grade 6 JSON files and generates HTML according to exact specifications
"""

import json
import os
import glob
import re
from pathlib import Path

class TargetedGr6HTMLGenerator:
    def __init__(self):
        self.output_dir = "HTML"
        os.makedirs(self.output_dir, exist_ok=True)
        self.generated_files = []
        self.files_with_visuals = []
        
    def scan_for_visual_questions(self):
        """Scan all files to identify which ones have visual requirements"""
        print("Scanning files for visual requirements...")
        
        pattern = "Gr6_*_variations.json"
        files = sorted(glob.glob(pattern))
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                
                visual_questions = 0
                if isinstance(data, list):
                    for question in data:
                        if self.has_visual_requirements(question):
                            visual_questions += 1
                elif isinstance(data, dict):
                    for question in data.values():
                        if self.has_visual_requirements(question):
                            visual_questions += 1
                
                if visual_questions > 0:
                    self.files_with_visuals.append((file_path, visual_questions))
                    print(f"  {file_path}: {visual_questions} visual questions")
                    
            except Exception as e:
                print(f"  Error scanning {file_path}: {e}")
        
        print(f"\nFound {len(self.files_with_visuals)} files with visual questions")
    
    def has_visual_requirements(self, question_data):
        """Check if question has visual requirements"""
        if not isinstance(question_data, dict):
            return False
            
        return any([
            question_data.get('image_tag'),
            question_data.get('solution_image_tag'),
            question_data.get('image_choice_tags'),
            question_data.get('shape_image_tags'),
            # Also check content for grade 6 specific visual cues
            self.needs_visual_from_content(question_data)
        ])
    
    def needs_visual_from_content(self, question_data):
        """Check if content suggests need for visuals"""
        question_text = (question_data.get('question_text', '') + ' ' + 
                        question_data.get('skills', '')).lower()
        
        visual_keywords = [
            'graph', 'plot', 'chart', 'coordinate', 'number line',
            'fraction bar', 'pie chart', 'grid', 'array', 'diagram',
            'geometric shape', 'rectangle', 'triangle', 'circle',
            'data table', 'strip model', 'visual model'
        ]
        
        return any(keyword in question_text for keyword in visual_keywords)
    
    def generate_fraction_visual(self, numerator, denominator):
        """Generate fraction visualization"""
        if denominator == 0:
            return '<div>Invalid fraction</div>'
            
        width = 300
        height = 80
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <rect x="25" y="20" width="250" height="40" fill="white" stroke="#333" stroke-width="2"/>'''
        
        part_width = 250 / denominator
        for i in range(denominator):
            x = 25 + i * part_width
            if i > 0:
                svg += f'<line x1="{x}" y1="20" x2="{x}" y2="60" stroke="#333" stroke-width="1"/>'
            if i < numerator:
                svg += f'<rect x="{x + 1}" y="21" width="{part_width - 2}" height="38" fill="#4CAF50" opacity="0.7"/>'
        
        svg += f'<text x="150" y="75" font-family="Arial" font-size="14" text-anchor="middle">{numerator}/{denominator}</text>'
        svg += '</svg>'
        return svg
    
    def generate_multiplication_grid(self, rows, cols):
        """Generate multiplication grid"""
        cell_size = 20
        width = cols * cell_size + 60
        height = rows * cell_size + 60
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'''
        
        for i in range(rows):
            for j in range(cols):
                x = j * cell_size + 30
                y = i * cell_size + 30
                svg += f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="#e6f3ff" stroke="#0066cc" stroke-width="1"/>'
        
        svg += f'<text x="30" y="{height-10}" font-family="Arial" font-size="12">{rows} × {cols} = {rows * cols}</text>'
        svg += '</svg>'
        return svg
    
    def generate_number_line(self, start, end, highlight=None):
        """Generate number line"""
        width = 350
        height = 80
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <line x1="25" y1="40" x2="325" y2="40" stroke="#333" stroke-width="2"/>'''
        
        range_val = end - start
        if range_val == 0:
            range_val = 1
            
        for i in range(int(end - start) + 1):
            val = start + i
            x = 25 + (val - start) / range_val * 300
            svg += f'<line x1="{x}" y1="35" x2="{x}" y2="45" stroke="#333" stroke-width="2"/>'
            svg += f'<text x="{x}" y="60" font-family="Arial" font-size="10" text-anchor="middle">{val}</text>'
            
            if highlight and val in highlight:
                svg += f'<circle cx="{x}" cy="40" r="4" fill="#ff4444"/>'
        
        svg += '</svg>'
        return svg
    
    def determine_visual_from_question(self, question_data):
        """Determine appropriate visual based on question content"""
        question_text = question_data.get('question_text', '').lower()
        skills = question_data.get('skills', '').lower()
        
        # Extract numbers for calculations
        import re
        numbers = re.findall(r'\d+', question_text + ' ' + skills)
        numbers = [int(n) for n in numbers[:4]]  # Limit to first 4 numbers
        
        if 'fraction' in question_text or '/' in question_text:
            if len(numbers) >= 2:
                return self.generate_fraction_visual(numbers[0], numbers[1])
            else:
                return self.generate_fraction_visual(3, 4)
        
        elif any(word in question_text for word in ['multiply', '×', 'times']):
            if len(numbers) >= 2:
                return self.generate_multiplication_grid(min(numbers[0], 8), min(numbers[1], 8))
            else:
                return self.generate_multiplication_grid(3, 4)
        
        elif 'number line' in question_text:
            if len(numbers) >= 2:
                return self.generate_number_line(numbers[0], numbers[1])
            else:
                return self.generate_number_line(0, 10)
        
        else:
            # Default visual
            if len(numbers) >= 2:
                return self.generate_fraction_visual(numbers[0], numbers[1])
            else:
                return self.generate_multiplication_grid(3, 4)
    
    def process_visual_files(self):
        """Process only files that have visual requirements"""
        if not self.files_with_visuals:
            print("No files with visual requirements found.")
            return
        
        print(f"\nProcessing {len(self.files_with_visuals)} files with visual requirements...")
        
        for file_path, visual_count in self.files_with_visuals:
            print(f"\nProcessing {file_path} ({visual_count} visual questions)...")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                
                # Extract file info
                filename = os.path.basename(file_path)
                parts = filename.replace('Gr6_', '').replace('_variations.json', '').split('_')
                week = parts[0]
                exercise = parts[1].replace('E', '')
                
                generated = 0
                
                if isinstance(data, list):
                    for i, question_data in enumerate(data):
                        if self.has_visual_requirements(question_data):
                            question_num = question_data.get('question_number', str(i+1))
                            html_file = self.generate_html_file(question_data, week, exercise, question_num)
                            if html_file:
                                generated += 1
                                print(f"  Generated: {html_file}")
                
                elif isinstance(data, dict):
                    for question_num, question_data in data.items():
                        if self.has_visual_requirements(question_data):
                            html_file = self.generate_html_file(question_data, week, exercise, question_num)
                            if html_file:
                                generated += 1
                                print(f"  Generated: {html_file}")
                
                print(f"  Generated {generated} HTML files from {filename}")
                
            except Exception as e:
                print(f"  Error processing {file_path}: {e}")
    
    def generate_html_file(self, question_data, week, exercise, question_num):
        """Generate HTML file for a question with visual requirements"""
        try:
            question_text = question_data.get('question_text', question_data.get('question', ''))
            skills = question_data.get('skills', '')
            
            html_filename = f"Gr6_{week}_E{exercise} {exercise}_{question_num}.html"
            html_path = os.path.join(self.output_dir, html_filename)
            
            # Generate visual content
            visual_html = self.determine_visual_from_question(question_data)
            
            html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 Week {week} Exercise {exercise} Question {question_num}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .question-info {{ background-color: #e3f2fd; padding: 15px; margin-bottom: 20px; border-radius: 5px; border-left: 4px solid #2196f3; }}
        .item {{ 
            display: inline-block; 
            margin: 15px; 
            padding: 15px; 
            border: 2px solid #ddd;
            border-radius: 8px;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            vertical-align: top;
        }}
        svg {{ max-width: 100%; height: auto; }}
        h3 {{ color: #1976d2; margin-top: 0; }}
        .question-text {{ font-size: 16px; line-height: 1.5; }}
        .skills {{ font-style: italic; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question-info">
            <h3>Grade 6 - Week {week} - Exercise {exercise} - Question {question_num}</h3>
            <div class="question-text"><strong>Question:</strong> {question_text}</div>
            {f'<div class="skills"><strong>Skills:</strong> {skills}</div>' if skills else ''}
        </div>
        
        <div class="visuals">
            <div class="item" label="visual_main">
                {visual_html}
            </div>
        </div>
    </div>
</body>
</html>'''
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.generated_files.append(html_path)
            return html_filename
            
        except Exception as e:
            print(f"    Error generating HTML for {question_num}: {e}")
            return None
    
    def run(self):
        """Main execution function"""
        self.scan_for_visual_questions()
        self.process_visual_files()
        
        print(f"\n=== GENERATION COMPLETE ===")
        print(f"Total HTML files generated: {len(self.generated_files)}")
        
        # Write summary
        with open("targeted_grade6_html_generation_summary.txt", "w", encoding="utf-8") as f:
            f.write(f"Targeted Grade 6 HTML Generation Summary\n")
            f.write(f"========================================\n\n")
            f.write(f"Files scanned: {len(glob.glob('Gr6_*_variations.json'))}\n")
            f.write(f"Files with visuals: {len(self.files_with_visuals)}\n")
            f.write(f"HTML files generated: {len(self.generated_files)}\n\n")
            
            f.write("Files with visual requirements:\n")
            for file_path, count in self.files_with_visuals:
                f.write(f"  {file_path}: {count} visual questions\n")
            
            f.write(f"\nGenerated HTML files:\n")
            for file_path in sorted(self.generated_files):
                f.write(f"  {file_path}\n")

if __name__ == "__main__":
    generator = TargetedGr6HTMLGenerator()
    generator.run()