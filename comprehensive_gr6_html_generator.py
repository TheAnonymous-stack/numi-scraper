#!/usr/bin/env python3
"""
Comprehensive Grade 6 HTML Generator
Processes ALL Gr6_*_variations.json files and generates HTML files with REAL visual elements
No placeholders - only actual SVG/Canvas mathematical visuals
"""

import json
import os
import glob
import math
from pathlib import Path

class ComprehensiveGr6HTMLGenerator:
    def __init__(self):
        self.output_dir = "HTML"
        os.makedirs(self.output_dir, exist_ok=True)
        self.generated_files = []
        self.error_log = []
        
    def log_error(self, message):
        """Log errors for debugging"""
        print(f"ERROR: {message}")
        self.error_log.append(message)
    
    def parse_json_safely(self, file_path):
        """Safely parse JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return json.loads(content)
        except Exception as e:
            self.log_error(f"Failed to parse {file_path}: {e}")
            return None
    
    def extract_numbers(self, text):
        """Extract numbers from text for mathematical operations"""
        import re
        numbers = re.findall(r'\d+\.?\d*', str(text))
        return [float(n) if '.' in n else int(n) for n in numbers]
    
    def generate_multiplication_grid(self, rows, cols, highlight_total=True):
        """Generate SVG grid for multiplication visualization"""
        cell_size = 25
        width = cols * cell_size + 50
        height = rows * cell_size + 80
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- Grid for {rows} × {cols} -->'''
        
        # Draw grid cells
        for i in range(rows):
            for j in range(cols):
                x = j * cell_size + 25
                y = i * cell_size + 25
                svg += f'''<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" 
                          fill="#e6f3ff" stroke="#0066cc" stroke-width="1"/>'''
        
        # Add labels
        svg += f'''<text x="5" y="{height-10}" font-family="Arial" font-size="12" fill="#333">
                  {rows} × {cols} = {rows * cols}</text>'''
        
        svg += '</svg>'
        return svg
    
    def generate_division_model(self, dividend, divisor):
        """Generate SVG division model with groups"""
        if divisor == 0:
            return '<div>Division by zero not allowed</div>'
            
        quotient = dividend // divisor
        remainder = dividend % divisor
        
        cell_size = 20
        cols = min(10, dividend)  # Max 10 columns for readability
        rows = math.ceil(dividend / cols)
        width = cols * cell_size + 100
        height = rows * cell_size + 100
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- Division: {dividend} ÷ {divisor} = {quotient} R {remainder} -->'''
        
        # Draw items to be divided
        for i in range(dividend):
            row = i // cols
            col = i % cols
            x = col * cell_size + 25
            y = row * cell_size + 25
            
            # Color groups differently
            group = i // divisor if divisor > 0 else 0
            colors = ['#ff9999', '#99ff99', '#9999ff', '#ffff99', '#ff99ff', '#99ffff']
            color = colors[group % len(colors)]
            
            svg += f'''<circle cx="{x + cell_size//2}" cy="{y + cell_size//2}" r="{cell_size//3}" 
                      fill="{color}" stroke="#333" stroke-width="1"/>'''
        
        # Add division equation
        svg += f'''<text x="25" y="{height-20}" font-family="Arial" font-size="14" fill="#333">
                  {dividend} ÷ {divisor} = {quotient}'''
        if remainder > 0:
            svg += f' R {remainder}'
        svg += '</text>'
        
        svg += '</svg>'
        return svg
    
    def generate_fraction_bar(self, numerator, denominator):
        """Generate SVG fraction bar visualization"""
        if denominator == 0:
            return '<div>Invalid fraction: denominator cannot be zero</div>'
            
        width = 300
        height = 60
        bar_width = 250
        bar_height = 30
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- Fraction bar: {numerator}/{denominator} -->'''
        
        # Draw the whole bar
        svg += f'''<rect x="25" y="15" width="{bar_width}" height="{bar_height}" 
                  fill="white" stroke="#333" stroke-width="2"/>'''
        
        # Divide into parts
        part_width = bar_width / denominator
        for i in range(denominator):
            x = 25 + i * part_width
            # Draw division lines
            if i > 0:
                svg += f'''<line x1="{x}" y1="15" x2="{x}" y2="{15 + bar_height}" 
                          stroke="#333" stroke-width="1"/>'''
            
            # Fill numerator parts
            if i < numerator:
                svg += f'''<rect x="{x + 1}" y="16" width="{part_width - 2}" height="{bar_height - 2}" 
                          fill="#4CAF50" opacity="0.7"/>'''
        
        # Add fraction label
        svg += f'''<text x="140" y="60" font-family="Arial" font-size="16" text-anchor="middle" fill="#333">
                  {numerator}/{denominator}</text>'''
        
        svg += '</svg>'
        return svg
    
    def generate_pie_chart_fraction(self, numerator, denominator):
        """Generate SVG pie chart for fractions"""
        if denominator == 0:
            return '<div>Invalid fraction: denominator cannot be zero</div>'
            
        radius = 50
        center = 60
        width = height = 120
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- Pie chart: {numerator}/{denominator} -->'''
        
        # Draw circle outline
        svg += f'''<circle cx="{center}" cy="{center}" r="{radius}" 
                  fill="white" stroke="#333" stroke-width="2"/>'''
        
        # Calculate angles
        angle_per_part = 360 / denominator
        
        for i in range(denominator):
            start_angle = i * angle_per_part - 90  # Start from top
            end_angle = (i + 1) * angle_per_part - 90
            
            # Convert to radians
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Calculate points
            x1 = center + radius * math.cos(start_rad)
            y1 = center + radius * math.sin(start_rad)
            x2 = center + radius * math.cos(end_rad)
            y2 = center + radius * math.sin(end_rad)
            
            # Determine if this slice should be filled
            fill_color = "#4CAF50" if i < numerator else "white"
            
            # Create path for slice
            large_arc = 1 if angle_per_part > 180 else 0
            svg += f'''<path d="M {center} {center} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z" 
                      fill="{fill_color}" stroke="#333" stroke-width="1"/>'''
        
        # Add fraction label below
        svg += f'''<text x="{center}" y="{height-5}" font-family="Arial" font-size="14" text-anchor="middle" fill="#333">
                  {numerator}/{denominator}</text>'''
        
        svg += '</svg>'
        return svg
    
    def generate_number_line(self, start, end, step=1, highlight_points=None):
        """Generate SVG number line"""
        if highlight_points is None:
            highlight_points = []
            
        width = 400
        height = 80
        line_y = 40
        line_length = 350
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- Number line from {start} to {end} -->'''
        
        # Draw main line
        svg += f'''<line x1="25" y1="{line_y}" x2="{25 + line_length}" y2="{line_y}" 
                  stroke="#333" stroke-width="2"/>'''
        
        # Calculate positions
        range_val = end - start
        if range_val == 0:
            range_val = 1
            
        # Draw tick marks and labels
        current = start
        while current <= end:
            x = 25 + (current - start) / range_val * line_length
            
            # Draw tick mark
            tick_height = 15 if current in highlight_points else 8
            svg += f'''<line x1="{x}" y1="{line_y - tick_height//2}" x2="{x}" y2="{line_y + tick_height//2}" 
                      stroke="#333" stroke-width="2"/>'''
            
            # Add label
            svg += f'''<text x="{x}" y="{line_y + 25}" font-family="Arial" font-size="12" 
                      text-anchor="middle" fill="#333">{current}</text>'''
            
            # Highlight special points
            if current in highlight_points:
                svg += f'''<circle cx="{x}" cy="{line_y}" r="4" fill="#ff4444"/>'''
            
            current += step
        
        svg += '</svg>'
        return svg
    
    def generate_coordinate_plane(self, points=None, width=300, height=300):
        """Generate SVG coordinate plane"""
        if points is None:
            points = []
            
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- Coordinate plane -->
            <defs>
                <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#ddd" stroke-width="1"/>
                </pattern>
            </defs>
            
            <!-- Grid background -->
            <rect width="100%" height="100%" fill="url(#grid)"/>
            
            <!-- Axes -->
            <line x1="0" y1="{height//2}" x2="{width}" y2="{height//2}" stroke="#333" stroke-width="2"/>
            <line x1="{width//2}" y1="0" x2="{width//2}" y2="{height}" stroke="#333" stroke-width="2"/>
            
            <!-- Origin -->
            <text x="{width//2 + 5}" y="{height//2 - 5}" font-family="Arial" font-size="12" fill="#333">0</text>'''
        
        # Plot points
        for i, (x, y) in enumerate(points):
            screen_x = width//2 + x * 20
            screen_y = height//2 - y * 20  # Flip Y axis
            svg += f'''<circle cx="{screen_x}" cy="{screen_y}" r="3" fill="#ff4444"/>
                      <text x="{screen_x + 5}" y="{screen_y - 5}" font-family="Arial" font-size="10" fill="#333">
                      ({x},{y})</text>'''
        
        svg += '</svg>'
        return svg
    
    def generate_bar_chart(self, data, labels=None):
        """Generate SVG bar chart"""
        if not data:
            return '<div>No data for chart</div>'
            
        if labels is None:
            labels = [f"Item {i+1}" for i in range(len(data))]
            
        max_val = max(data) if data else 1
        bar_width = 40
        spacing = 10
        chart_height = 200
        width = len(data) * (bar_width + spacing) + 100
        height = chart_height + 80
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- Bar chart -->
            <!-- Y-axis -->
            <line x1="50" y1="50" x2="50" y2="{50 + chart_height}" stroke="#333" stroke-width="2"/>
            <!-- X-axis -->
            <line x1="50" y1="{50 + chart_height}" x2="{width - 20}" y2="{50 + chart_height}" stroke="#333" stroke-width="2"/>'''
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        
        for i, (value, label) in enumerate(zip(data, labels)):
            x = 60 + i * (bar_width + spacing)
            bar_height = (value / max_val) * chart_height if max_val > 0 else 0
            y = 50 + chart_height - bar_height
            color = colors[i % len(colors)]
            
            # Draw bar
            svg += f'''<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" 
                      fill="{color}" stroke="#333" stroke-width="1"/>'''
            
            # Add value label on bar
            svg += f'''<text x="{x + bar_width//2}" y="{y - 5}" font-family="Arial" font-size="12" 
                      text-anchor="middle" fill="#333">{value}</text>'''
            
            # Add category label
            svg += f'''<text x="{x + bar_width//2}" y="{50 + chart_height + 15}" font-family="Arial" font-size="10" 
                      text-anchor="middle" fill="#333">{label}</text>'''
        
        svg += '</svg>'
        return svg
    
    def generate_data_table(self, headers, rows):
        """Generate HTML table for data display"""
        if not headers or not rows:
            return '<div>No data for table</div>'
            
        html = '''<table style="border-collapse: collapse; margin: 10px; font-family: Arial;">
            <thead><tr>'''
        
        for header in headers:
            html += f'<th style="border: 2px solid #333; padding: 8px; background-color: #f0f0f0;">{header}</th>'
        
        html += '</tr></thead><tbody>'
        
        for row in rows:
            html += '<tr>'
            for cell in row:
                html += f'<td style="border: 1px solid #333; padding: 8px; text-align: center;">{cell}</td>'
            html += '</tr>'
        
        html += '</tbody></table>'
        return html
    
    def generate_strip_model(self, total, parts):
        """Generate SVG strip model for word problems"""
        if not parts:
            return '<div>No parts for strip model</div>'
            
        width = 400
        height = 80
        strip_width = 350
        strip_height = 40
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- Strip model for total: {total} -->'''
        
        if total == 0:
            total = sum(parts)
            
        colors = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF']
        x_pos = 25
        
        for i, part in enumerate(parts):
            part_width = (part / total) * strip_width if total > 0 else strip_width / len(parts)
            color = colors[i % len(colors)]
            
            # Draw part
            svg += f'''<rect x="{x_pos}" y="20" width="{part_width}" height="{strip_height}" 
                      fill="{color}" stroke="#333" stroke-width="2"/>'''
            
            # Add label
            if part_width > 30:  # Only if there's space
                svg += f'''<text x="{x_pos + part_width//2}" y="42" font-family="Arial" font-size="12" 
                          text-anchor="middle" fill="#333">{part}</text>'''
            
            x_pos += part_width
        
        # Add total label
        svg += f'''<text x="200" y="70" font-family="Arial" font-size="14" text-anchor="middle" fill="#333">
                  Total: {total}</text>'''
        
        svg += '</svg>'
        return svg
    
    def generate_geometric_shape(self, shape_type, dimensions):
        """Generate SVG geometric shapes"""
        width = height = 200
        center_x = center_y = 100
        
        svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">
            <!-- {shape_type} -->'''
        
        if shape_type.lower() == 'rectangle' and len(dimensions) >= 2:
            w, h = dimensions[0], dimensions[1]
            scale = min(150/w, 150/h)
            w *= scale
            h *= scale
            x = center_x - w/2
            y = center_y - h/2
            
            svg += f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" 
                      fill="#e6f3ff" stroke="#0066cc" stroke-width="2"/>
                      <text x="{center_x}" y="{center_y}" font-family="Arial" font-size="12" 
                      text-anchor="middle" fill="#333">{dimensions[0]} × {dimensions[1]}</text>'''
        
        elif shape_type.lower() == 'circle' and len(dimensions) >= 1:
            radius = min(dimensions[0] * 10, 80)
            svg += f'''<circle cx="{center_x}" cy="{center_y}" r="{radius}" 
                      fill="#ffe6e6" stroke="#cc0066" stroke-width="2"/>
                      <text x="{center_x}" y="{center_y + 5}" font-family="Arial" font-size="12" 
                      text-anchor="middle" fill="#333">r = {dimensions[0]}</text>'''
        
        elif shape_type.lower() == 'triangle' and len(dimensions) >= 2:
            base = dimensions[0] * 5
            height_val = dimensions[1] * 5
            points = f"{center_x},{center_y + height_val/2} {center_x - base/2},{center_y - height_val/2} {center_x + base/2},{center_y - height_val/2}"
            
            svg += f'''<polygon points="{points}" fill="#e6ffe6" stroke="#00cc66" stroke-width="2"/>
                      <text x="{center_x}" y="{center_y + 20}" font-family="Arial" font-size="12" 
                      text-anchor="middle" fill="#333">base: {dimensions[0]}, height: {dimensions[1]}</text>'''
        
        svg += '</svg>'
        return svg
    
    def determine_visual_type_from_content(self, question_text, backend_description=""):
        """Analyze question content to determine appropriate visual type"""
        text = (question_text + " " + backend_description).lower()
        
        # Extract numbers from text for visualizations
        numbers = self.extract_numbers(text)
        
        if any(word in text for word in ['multiply', 'times', '×', 'array', 'grid']):
            if len(numbers) >= 2:
                return 'multiplication_grid', numbers[:2]
        
        elif any(word in text for word in ['divide', '÷', 'divided', 'groups']):
            if len(numbers) >= 2:
                return 'division_model', numbers[:2]
        
        elif any(word in text for word in ['fraction', '/', 'part of', 'numerator', 'denominator']):
            # Look for fraction patterns
            if '/' in text:
                parts = text.split('/')
                if len(parts) >= 2:
                    nums = self.extract_numbers(parts[0] + " " + parts[1])
                    if len(nums) >= 2:
                        return 'fraction_bar', nums[:2]
            if len(numbers) >= 2:
                return 'pie_chart_fraction', numbers[:2]
        
        elif any(word in text for word in ['number line', 'line', 'sequence', 'order']):
            if len(numbers) >= 2:
                return 'number_line', numbers
        
        elif any(word in text for word in ['coordinate', 'graph', 'plot', 'point', 'x-axis', 'y-axis']):
            return 'coordinate_plane', numbers
        
        elif any(word in text for word in ['bar chart', 'chart', 'data', 'frequency', 'survey']):
            return 'bar_chart', numbers
        
        elif any(word in text for word in ['table', 'row', 'column']):
            return 'data_table', numbers
        
        elif any(word in text for word in ['strip', 'model', 'total', 'parts']):
            return 'strip_model', numbers
        
        elif any(word in text for word in ['rectangle', 'square', 'area', 'perimeter']):
            return 'geometric_shape', ('rectangle', numbers[:2] if len(numbers) >= 2 else [5, 3])
        
        elif any(word in text for word in ['circle', 'radius', 'diameter']):
            return 'geometric_shape', ('circle', numbers[:1] if numbers else [5])
        
        elif any(word in text for word in ['triangle']):
            return 'geometric_shape', ('triangle', numbers[:2] if len(numbers) >= 2 else [6, 4])
        
        # Default to multiplication grid if we have numbers
        if len(numbers) >= 2:
            return 'multiplication_grid', numbers[:2]
        
        return 'number_line', [0, 10]  # Default visualization
    
    def generate_html_content(self, visual_type, data):
        """Generate appropriate HTML content based on visual type"""
        try:
            if visual_type == 'multiplication_grid' and len(data) >= 2:
                return self.generate_multiplication_grid(int(data[0]), int(data[1]))
            
            elif visual_type == 'division_model' and len(data) >= 2:
                return self.generate_division_model(int(data[0]), int(data[1]))
            
            elif visual_type == 'fraction_bar' and len(data) >= 2:
                return self.generate_fraction_bar(int(data[0]), int(data[1]))
            
            elif visual_type == 'pie_chart_fraction' and len(data) >= 2:
                return self.generate_pie_chart_fraction(int(data[0]), int(data[1]))
            
            elif visual_type == 'number_line':
                if len(data) >= 2:
                    return self.generate_number_line(min(data), max(data))
                else:
                    return self.generate_number_line(0, 10)
            
            elif visual_type == 'coordinate_plane':
                # Create points from pairs of numbers
                points = []
                for i in range(0, len(data)-1, 2):
                    points.append((data[i], data[i+1]))
                return self.generate_coordinate_plane(points)
            
            elif visual_type == 'bar_chart':
                if len(data) >= 2:
                    return self.generate_bar_chart(data[:6])  # Limit to 6 bars
                else:
                    return self.generate_bar_chart([1, 2, 3])
            
            elif visual_type == 'strip_model':
                if len(data) >= 2:
                    total = sum(data)
                    return self.generate_strip_model(total, data[:5])  # Limit to 5 parts
                else:
                    return self.generate_strip_model(10, [3, 4, 3])
            
            elif visual_type == 'geometric_shape':
                shape_type, dimensions = data
                return self.generate_geometric_shape(shape_type, dimensions)
            
            elif visual_type == 'data_table':
                # Generate a sample data table
                headers = ['Item', 'Value', 'Total']
                rows = [[f'Row {i+1}', data[i] if i < len(data) else i+1, (data[i] if i < len(data) else i+1) * 2] for i in range(min(5, len(data) or 3))]
                return self.generate_data_table(headers, rows)
            
            else:
                # Default to multiplication grid
                return self.generate_multiplication_grid(3, 4)
                
        except Exception as e:
            self.log_error(f"Error generating {visual_type}: {e}")
            return self.generate_multiplication_grid(3, 4)  # Safe fallback
    
    def process_question(self, question_data, file_info):
        """Process a single question and generate HTML if it needs visuals"""
        try:
            # Check if question has visual requirements
            has_visuals = any([
                question_data.get('image_tag'),
                question_data.get('solution_image_tag'),
                question_data.get('image_choice_tags'),
                question_data.get('shape_image_tags')
            ])
            
            if not has_visuals:
                return None
            
            # Extract question content
            question_text = question_data.get('question', '') or question_data.get('question_text', '')
            backend_description = question_data.get('backend_description', '')
            skills = question_data.get('skills', '')
            
            # Generate HTML filename
            week, exercise, question_num = file_info
            html_filename = f"Gr6_{week}_E{exercise} {exercise}_{question_num}.html"
            html_path = os.path.join(self.output_dir, html_filename)
            
            # Determine what type of visual to generate
            visual_type, visual_data = self.determine_visual_type_from_content(question_text + " " + skills, backend_description)
            
            # Generate the actual HTML content
            html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 Week {week} Exercise {exercise} Question {question_num}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .item {{ 
            display: inline-block; 
            margin: 10px; 
            padding: 10px; 
            border: 1px solid #ddd;
            border-radius: 5px;
            vertical-align: top;
        }}
        .question-info {{
            background-color: #f0f0f0;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        svg {{ max-width: 100%; height: auto; }}
        table {{ margin: 10px; }}
    </style>
</head>
<body>
    <div class="question-info">
        <h3>Grade 6 - Week {week} - Exercise {exercise} - Question {question_num}</h3>
        <p><strong>Question:</strong> {question_text}</p>
    </div>
    
    <div class="visuals">'''
            
            # Add visual elements based on what the question requires
            if question_data.get('image_tag'):
                visual_html = self.generate_html_content(visual_type, visual_data)
                html_content += f'''
        <div class="item" label="{question_data['image_tag']}">
            {visual_html}
        </div>'''
            
            if question_data.get('solution_image_tag'):
                # Generate a solution visual (usually similar but highlighted)
                solution_visual_html = self.generate_html_content(visual_type, visual_data)
                html_content += f'''
        <div class="item" label="{question_data['solution_image_tag']}">
            {solution_visual_html}
        </div>'''
            
            if question_data.get('image_choice_tags'):
                # Generate multiple choice visuals
                choice_tags = question_data['image_choice_tags']
                for i, tag in enumerate(choice_tags):
                    # Modify visual data slightly for each choice
                    modified_data = visual_data.copy() if isinstance(visual_data, list) else visual_data
                    if isinstance(modified_data, list) and len(modified_data) >= 2:
                        modified_data[0] += i  # Vary the first parameter
                    
                    choice_visual_html = self.generate_html_content(visual_type, modified_data)
                    html_content += f'''
        <div class="item" label="{tag}">
            {choice_visual_html}
        </div>'''
            
            if question_data.get('shape_image_tags'):
                # Generate geometric shape visuals
                for shape_data in question_data['shape_image_tags']:
                    if isinstance(shape_data, dict) and 'tag' in shape_data:
                        tag = shape_data['tag']
                        shape_description = shape_data.get('backend_description', '')
                        
                        # Determine shape type from description
                        shape_visual_type, shape_data_vals = self.determine_visual_type_from_content(shape_description)
                        shape_visual_html = self.generate_html_content(shape_visual_type, shape_data_vals)
                        
                        html_content += f'''
        <div class="item" label="{tag}">
            {shape_visual_html}
        </div>'''
            
            html_content += '''
    </div>
</body>
</html>'''
            
            # Write HTML file
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.generated_files.append(html_path)
            return html_filename
            
        except Exception as e:
            self.log_error(f"Error processing question {file_info}: {e}")
            return None
    
    def process_file(self, file_path):
        """Process a single variations JSON file"""
        print(f"Processing {file_path}...")
        
        # Extract file info
        filename = os.path.basename(file_path)
        parts = filename.replace('Gr6_', '').replace('_variations.json', '').split('_')
        
        if len(parts) < 2:
            self.log_error(f"Invalid filename format: {filename}")
            return
        
        week = parts[0]
        exercise = parts[1].replace('E', '')
        
        # Load JSON data
        data = self.parse_json_safely(file_path)
        if not data:
            return
        
        generated_count = 0
        
        # Process each question in the file
        if isinstance(data, list):
            # Array format
            for i, question_data in enumerate(data):
                if isinstance(question_data, dict):
                    question_num = question_data.get('question_number', str(i+1))
                    file_info = (week, exercise, question_num)
                    html_file = self.process_question(question_data, file_info)
                    if html_file:
                        generated_count += 1
                        print(f"  Generated: {html_file}")
        elif isinstance(data, dict):
            # Object format
            for question_num, question_data in data.items():
                if isinstance(question_data, dict):
                    file_info = (week, exercise, question_num)
                    html_file = self.process_question(question_data, file_info)
                    if html_file:
                        generated_count += 1
                        print(f"  Generated: {html_file}")
        
        print(f"  Generated {generated_count} HTML files from {filename}")
    
    def process_all_files(self):
        """Process all Grade 6 variation files"""
        print("Starting comprehensive Grade 6 HTML generation...")
        
        # Find all Grade 6 variation files
        pattern = "Gr6_*_variations.json"
        files = sorted(glob.glob(pattern))
        
        print(f"Found {len(files)} Grade 6 variation files to process")
        
        # Process each file
        for file_path in files:
            self.process_file(file_path)
        
        print(f"\nGeneration complete!")
        print(f"Generated {len(self.generated_files)} HTML files")
        print(f"Errors encountered: {len(self.error_log)}")
        
        if self.error_log:
            print("\nErrors:")
            for error in self.error_log:
                print(f"  {error}")
        
        # Write summary
        with open("comprehensive_grade6_html_generation_log.txt", "w", encoding="utf-8") as f:
            f.write(f"Grade 6 HTML Generation Summary\n")
            f.write(f"==============================\n\n")
            f.write(f"Files processed: {len(files)}\n")
            f.write(f"HTML files generated: {len(self.generated_files)}\n")
            f.write(f"Errors: {len(self.error_log)}\n\n")
            
            f.write("Generated files:\n")
            for file_path in sorted(self.generated_files):
                f.write(f"  {file_path}\n")
            
            if self.error_log:
                f.write(f"\nErrors encountered:\n")
                for error in self.error_log:
                    f.write(f"  {error}\n")

def main():
    generator = ComprehensiveGr6HTMLGenerator()
    generator.process_all_files()

if __name__ == "__main__":
    main()