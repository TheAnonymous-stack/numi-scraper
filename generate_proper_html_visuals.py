import json
import os
import re
from pathlib import Path

def create_decimal_grid_svg(value, width=200, height=200):
    """Create a 10x10 grid SVG for decimal representation"""
    # Extract decimal value
    decimal_val = float(value) if isinstance(value, (int, float, str)) else 0
    shaded_squares = int(decimal_val * 100)
    
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    
    # Draw grid
    square_size = width // 10
    for row in range(10):
        for col in range(10):
            square_num = row * 10 + col
            x = col * square_size
            y = row * square_size
            
            # Shade squares based on value
            if square_num < shaded_squares:
                fill = "#4CAF50"
            else:
                fill = "white"
            
            svg += f'  <rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" '
            svg += f'fill="{fill}" stroke="black" stroke-width="1"/>\n'
    
    svg += '</svg>'
    return svg

def create_fraction_circle_svg(numerator, denominator, width=200, height=200):
    """Create a circle divided into sections for fraction representation"""
    import math
    
    cx, cy = width // 2, height // 2
    radius = min(width, height) // 2 - 10
    
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    
    # Draw circle sections
    angle_per_section = 360 / denominator
    
    for i in range(denominator):
        start_angle = i * angle_per_section - 90
        end_angle = (i + 1) * angle_per_section - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate points
        x1 = cx + radius * math.cos(start_rad)
        y1 = cy + radius * math.sin(start_rad)
        x2 = cx + radius * math.cos(end_rad)
        y2 = cy + radius * math.sin(end_rad)
        
        # Determine if this section should be filled
        fill = "#FF9800" if i < numerator else "white"
        
        # Create path for wedge
        large_arc = 0 if angle_per_section <= 180 else 1
        svg += f'  <path d="M {cx},{cy} L {x1},{y1} A {radius},{radius} 0 {large_arc},1 {x2},{y2} Z" '
        svg += f'fill="{fill}" stroke="black" stroke-width="2"/>\n'
    
    svg += '</svg>'
    return svg

def create_number_line_svg(numbers, highlight=None, width=400, height=100):
    """Create a number line SVG"""
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    
    # Draw main line
    line_y = height // 2
    margin = 30
    svg += f'  <line x1="{margin}" y1="{line_y}" x2="{width-margin}" y2="{line_y}" stroke="black" stroke-width="2"/>\n'
    
    # Find min and max for scale
    num_values = [float(n) for n in numbers if isinstance(n, (int, float, str)) and str(n).replace('.','').replace('-','').isdigit()]
    if num_values:
        min_val = min(num_values)
        max_val = max(num_values)
        range_val = max_val - min_val if max_val != min_val else 1
        
        # Draw tick marks and labels
        for num in num_values:
            x = margin + ((num - min_val) / range_val) * (width - 2*margin)
            
            # Tick mark
            svg += f'  <line x1="{x}" y1="{line_y-5}" x2="{x}" y2="{line_y+5}" stroke="black" stroke-width="2"/>\n'
            
            # Point
            color = "red" if highlight and str(num) == str(highlight) else "blue"
            svg += f'  <circle cx="{x}" cy="{line_y}" r="5" fill="{color}"/>\n'
            
            # Label
            svg += f'  <text x="{x}" y="{line_y+20}" text-anchor="middle" font-size="12">{num}</text>\n'
    
    svg += '</svg>'
    return svg

def create_place_value_chart_svg(number, width=500, height=150):
    """Create a place value chart SVG"""
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    
    # Parse number to get digits
    num_str = str(number).replace('.', '')
    decimal_pos = str(number).find('.')
    
    # Define columns based on number
    if '.' in str(number):
        columns = ['Ones', 'Tenths', 'Hundredths', 'Thousandths'][:len(num_str)]
    else:
        columns = ['Thousands', 'Hundreds', 'Tens', 'Ones'][-min(4, len(num_str)):]
    
    col_width = width // len(columns)
    
    # Draw header row
    for i, col in enumerate(columns):
        x = i * col_width
        svg += f'  <rect x="{x}" y="10" width="{col_width}" height="40" fill="#E3F2FD" stroke="black" stroke-width="1"/>\n'
        svg += f'  <text x="{x + col_width//2}" y="35" text-anchor="middle" font-size="14">{col}</text>\n'
    
    # Draw value row
    for i, digit in enumerate(num_str):
        if i < len(columns):
            x = i * col_width
            svg += f'  <rect x="{x}" y="50" width="{col_width}" height="40" fill="white" stroke="black" stroke-width="1"/>\n'
            svg += f'  <text x="{x + col_width//2}" y="75" text-anchor="middle" font-size="18" font-weight="bold">{digit}</text>\n'
    
    svg += '</svg>'
    return svg

def generate_html_for_question(question, week, exercise):
    """Generate proper HTML based on question type and content"""
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 - Visual Elements</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .visual-element {
            margin: 20px auto;
            display: inline-block;
        }
        .grid-container {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }
    </style>
</head>
<body>
    <div class="container">
'''
    
    # Determine what type of visual to create based on question
    question_text = question.get('question_text', '').lower()
    skills = question.get('skills', '')
    
    # For decimal comparison questions
    if 'compare' in question_text and 'decimal' in skills:
        # Extract decimal values from question text
        decimals = re.findall(r'\d+\.\d+', question.get('question_text', ''))
        if len(decimals) >= 2:
            html += '        <div class="grid-container">\n'
            for decimal in decimals[:2]:
                html += f'            <div class="visual-element">\n'
                html += f'                <div style="margin-bottom: 10px; font-weight: bold;">{decimal}</div>\n'
                html += f'                {create_decimal_grid_svg(decimal)}\n'
                html += f'            </div>\n'
            html += '        </div>\n'
    
    # For fraction questions
    elif 'fraction' in skills:
        fractions = re.findall(r'(\d+)/(\d+)', question.get('question_text', ''))
        if fractions:
            html += '        <div class="grid-container">\n'
            for num, den in fractions[:3]:
                html += f'            <div class="visual-element">\n'
                html += f'                <div style="margin-bottom: 10px; font-weight: bold;">{num}/{den}</div>\n'
                html += f'                {create_fraction_circle_svg(int(num), int(den))}\n'
                html += f'            </div>\n'
            html += '        </div>\n'
    
    # For ordering questions
    elif 'order' in skills or 'order' in question_text:
        choices = question.get('choices', [])
        if choices:
            # Extract numeric values
            numbers = []
            for choice in choices:
                # Try to extract number from choice
                num_match = re.search(r'[\d.]+', str(choice))
                if num_match:
                    numbers.append(num_match.group())
            
            if numbers:
                html += f'        <div class="visual-element">\n'
                html += f'            {create_number_line_svg(numbers)}\n'
                html += f'        </div>\n'
    
    # For place value questions
    elif 'place' in skills or 'place value' in question_text:
        numbers = re.findall(r'\d+\.?\d*', question.get('question_text', ''))
        if numbers:
            html += '        <div class="grid-container">\n'
            for number in numbers[:2]:
                html += f'            <div class="visual-element">\n'
                html += f'                {create_place_value_chart_svg(number)}\n'
                html += f'            </div>\n'
            html += '        </div>\n'
    
    # Add solution images if they exist
    solution_images = question.get('solution_image_tag', [])
    if solution_images:
        for img_info in solution_images:
            if len(img_info) >= 3:
                step, label, description = img_info[0], img_info[1], img_info[2]
                html += f'        <div class="visual-element" label="{label}">\n'
                
                # Create appropriate visual based on description
                if 'grid' in description.lower() and 'shaded' in description.lower():
                    # Extract number of shaded squares
                    shaded_match = re.search(r'(\d+)\s+squares?\s+are\s+shaded', description)
                    if shaded_match:
                        shaded = int(shaded_match.group(1))
                        html += f'            {create_decimal_grid_svg(shaded/100)}\n'
                elif 'circle' in description.lower() and 'divided' in description.lower():
                    # Extract fraction info
                    parts_match = re.search(r'(\d+)\s+parts?\s+shaded.*?(\d+)\s+equal\s+parts', description)
                    if parts_match:
                        html += f'            {create_fraction_circle_svg(int(parts_match.group(1)), int(parts_match.group(2)))}\n'
                
                html += f'        </div>\n'
    
    html += '''    </div>
</body>
</html>'''
    
    return html

def process_all_grade6_files():
    """Process all Grade 6 JSON files and generate proper HTML"""
    
    base_path = Path(r'C:\Users\kapil\numi-scraper')
    html_path = base_path / 'HTML'
    
    # Find all Grade 6 variation JSON files
    json_files = list(base_path.glob('Gr6_*_E*_variations.json'))
    
    total_files = 0
    for json_file in json_files:
        # Parse week and exercise from filename
        match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', json_file.name)
        if not match:
            continue
            
        week = match.group(1)
        exercise = match.group(2)
        
        print(f"Processing {json_file.name}...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions = data.get('quizzes', [])
            
            for question in questions:
                q_num = question.get('question_number', '1_1')
                
                # Generate HTML
                html_content = generate_html_for_question(question, week, exercise)
                
                # Save HTML file
                html_filename = f'Gr6_{week}_E{exercise}_{q_num}.html'
                html_filepath = html_path / html_filename
                
                with open(html_filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                total_files += 1
        
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
    
    print(f"\nGenerated {total_files} HTML files with proper visual elements")

if __name__ == "__main__":
    process_all_grade6_files()