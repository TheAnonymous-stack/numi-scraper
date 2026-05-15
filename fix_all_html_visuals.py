import json
import os
import re
from pathlib import Path
import math

def create_decimal_grid_svg(value, width=200, height=200):
    """Create a 10x10 grid SVG for decimal representation"""
    try:
        decimal_val = float(value) if isinstance(value, (int, float, str)) else 0
        shaded_squares = int(decimal_val * 100)
    except:
        shaded_squares = 0
    
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

def create_fraction_visual_svg(numerator, denominator, width=200, height=200):
    """Create a visual representation for fractions"""
    try:
        num = int(numerator)
        den = int(denominator)
    except:
        return create_generic_math_visual()
    
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    
    if den <= 12:  # Use circle for smaller denominators
        cx, cy = width // 2, height // 2
        radius = min(width, height) // 2 - 10
        
        # Draw circle sections
        angle_per_section = 360 / den
        
        for i in range(den):
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
            fill = "#FF9800" if i < num else "white"
            
            # Create path for wedge
            large_arc = 0 if angle_per_section <= 180 else 1
            svg += f'  <path d="M {cx},{cy} L {x1},{y1} A {radius},{radius} 0 {large_arc},1 {x2},{y2} Z" '
            svg += f'fill="{fill}" stroke="black" stroke-width="2"/>\n'
    else:  # Use bar for larger denominators
        bar_width = width - 20
        bar_height = 40
        y_pos = (height - bar_height) // 2
        
        # Draw background bar
        svg += f'  <rect x="10" y="{y_pos}" width="{bar_width}" height="{bar_height}" '
        svg += f'fill="white" stroke="black" stroke-width="2"/>\n'
        
        # Draw filled portion
        filled_width = (num / den) * bar_width if den > 0 else 0
        svg += f'  <rect x="10" y="{y_pos}" width="{filled_width}" height="{bar_height}" '
        svg += f'fill="#FF9800" stroke="none"/>\n'
        
        # Add fraction text
        svg += f'  <text x="{width//2}" y="{height//2 + 5}" text-anchor="middle" '
        svg += f'font-size="20" font-weight="bold">{num}/{den}</text>\n'
    
    svg += '</svg>'
    return svg

def create_number_line_svg(min_val=0, max_val=10, points=[], width=400, height=100):
    """Create a number line SVG"""
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
    
    # Draw main line
    line_y = height // 2
    margin = 30
    svg += f'  <line x1="{margin}" y1="{line_y}" x2="{width-margin}" y2="{line_y}" stroke="black" stroke-width="2"/>\n'
    
    # Draw tick marks
    num_ticks = min(11, int(max_val - min_val + 1))
    for i in range(num_ticks):
        x = margin + i * ((width - 2*margin) / (num_ticks - 1))
        value = min_val + i * ((max_val - min_val) / (num_ticks - 1))
        
        # Tick mark
        svg += f'  <line x1="{x}" y1="{line_y-5}" x2="{x}" y2="{line_y+5}" stroke="black" stroke-width="2"/>\n'
        
        # Label
        label = str(int(value)) if value == int(value) else f"{value:.1f}"
        svg += f'  <text x="{x}" y="{line_y+20}" text-anchor="middle" font-size="12">{label}</text>\n'
    
    # Add points if provided
    for point in points:
        try:
            val = float(point)
            if min_val <= val <= max_val:
                x = margin + ((val - min_val) / (max_val - min_val)) * (width - 2*margin)
                svg += f'  <circle cx="{x}" cy="{line_y}" r="5" fill="red"/>\n'
        except:
            pass
    
    svg += '</svg>'
    return svg

def create_generic_math_visual():
    """Create a generic math visual when specific type can't be determined"""
    return '''<svg width="300" height="200" viewBox="0 0 300 200">
  <rect x="10" y="10" width="280" height="180" fill="#f0f8ff" stroke="#4169e1" stroke-width="2" rx="10"/>
  <text x="150" y="60" text-anchor="middle" font-size="24" fill="#4169e1" font-weight="bold">Math</text>
  <line x1="50" y1="100" x2="250" y2="100" stroke="#4169e1" stroke-width="2"/>
  <circle cx="100" cy="140" r="20" fill="#87ceeb" stroke="#4169e1" stroke-width="2"/>
  <rect x="140" y="120" width="40" height="40" fill="#87ceeb" stroke="#4169e1" stroke-width="2"/>
  <polygon points="220,160 200,120 240,120" fill="#87ceeb" stroke="#4169e1" stroke-width="2"/>
</svg>'''

def extract_numbers_from_text(text):
    """Extract numbers from question text"""
    # Look for decimals and fractions
    numbers = []
    
    # Find decimals
    decimal_pattern = r'\d+\.\d+'
    decimals = re.findall(decimal_pattern, text)
    numbers.extend(decimals)
    
    # Find fractions (including LaTeX format)
    fraction_pattern = r'\\frac\{(\d+)\}\{(\d+)\}|(\d+)/(\d+)'
    fractions = re.findall(fraction_pattern, text)
    for frac in fractions:
        if frac[0] and frac[1]:  # LaTeX format
            numbers.append(f"{frac[0]}/{frac[1]}")
        elif frac[2] and frac[3]:  # Regular format
            numbers.append(f"{frac[2]}/{frac[3]}")
    
    # Find whole numbers
    if not numbers:
        whole_pattern = r'\b\d+\b'
        wholes = re.findall(whole_pattern, text)
        numbers.extend(wholes[:3])  # Limit to first 3
    
    return numbers

def generate_visual_for_question(question):
    """Generate appropriate visual based on question content"""
    visuals = []
    
    question_text = question.get('question_text', '').lower()
    skills = question.get('skills', '').lower()
    
    # For decimal comparison questions
    if 'compare' in question_text and ('decimal' in skills or '.' in question.get('question_text', '')):
        decimals = re.findall(r'\d+\.\d+', question.get('question_text', ''))
        if decimals:
            for decimal in decimals[:2]:
                visuals.append(f'''
            <div class="visual-element">
                <div style="margin-bottom: 10px; font-weight: bold; font-size: 18px;">{decimal}</div>
                {create_decimal_grid_svg(decimal)}
            </div>''')
    
    # For fraction operations
    elif 'fraction' in skills or '\\frac' in question.get('question_text', ''):
        # Extract fractions from LaTeX
        latex_fractions = re.findall(r'\\frac\{(\d+)\}\{(\d+)\}', question.get('question_text', ''))
        regular_fractions = re.findall(r'(\d+)/(\d+)', question.get('question_text', ''))
        
        all_fractions = [(n, d) for n, d in latex_fractions] + [(n, d) for n, d in regular_fractions]
        
        if all_fractions:
            for num, den in all_fractions[:3]:
                visuals.append(f'''
            <div class="visual-element">
                <div style="margin-bottom: 10px; font-weight: bold; font-size: 18px;">{num}/{den}</div>
                {create_fraction_visual_svg(num, den)}
            </div>''')
    
    # For ordering questions
    elif 'order' in skills or 'order' in question_text or 'greatest' in question_text or 'least' in question_text:
        choices = question.get('choices', [])
        if choices:
            # Create number line
            numbers = []
            for choice in choices:
                # Extract numeric value
                choice_str = str(choice)
                # Try decimal
                decimal_match = re.search(r'(\d+\.?\d*)', choice_str)
                if decimal_match:
                    numbers.append(float(decimal_match.group(1)))
                # Try fraction
                elif '\\frac' in choice_str:
                    frac_match = re.search(r'\\frac\{(\d+)\}\{(\d+)\}', choice_str)
                    if frac_match:
                        numbers.append(int(frac_match.group(1)) / int(frac_match.group(2)))
            
            if numbers:
                min_val = min(numbers) - 0.5
                max_val = max(numbers) + 0.5
                visuals.append(f'''
            <div class="visual-element">
                {create_number_line_svg(min_val, max_val, numbers)}
            </div>''')
    
    # For place value questions
    elif 'place' in skills or 'place value' in question_text:
        numbers = extract_numbers_from_text(question.get('question_text', ''))
        if numbers:
            for number in numbers[:2]:
                visuals.append(f'''
            <div class="visual-element">
                <div style="margin-bottom: 10px; font-weight: bold; font-size: 18px;">{number}</div>
                {create_generic_math_visual()}
            </div>''')
    
    # Check for solution image tags
    solution_images = question.get('solution_image_tag', [])
    if solution_images:
        for img_info in solution_images:
            if len(img_info) >= 3:
                step, label, description = img_info[0], img_info[1], img_info[2]
                
                # Create visual based on description
                if 'grid' in description.lower() and 'shaded' in description.lower():
                    shaded_match = re.search(r'(\d+)\s+squares?\s+are\s+shaded', description)
                    if shaded_match:
                        shaded = int(shaded_match.group(1))
                        visuals.append(f'''
            <div class="visual-element" label="{label}">
                {create_decimal_grid_svg(shaded/100)}
            </div>''')
                elif 'circle' in description.lower() or 'fraction' in description.lower():
                    parts_match = re.search(r'(\d+).*?shaded.*?(\d+)', description)
                    if parts_match:
                        visuals.append(f'''
            <div class="visual-element" label="{label}">
                {create_fraction_visual_svg(int(parts_match.group(1)), int(parts_match.group(2)))}
            </div>''')
                else:
                    # Add label div for other types
                    visuals.append(f'''
            <div class="visual-element" label="{label}">
                {create_generic_math_visual()}
            </div>''')
    
    # If no visuals were created, add a generic one
    if not visuals:
        # Try to extract any numbers and create something
        numbers = extract_numbers_from_text(question.get('question_text', ''))
        if numbers:
            for num in numbers[:2]:
                if '/' in str(num):
                    parts = str(num).split('/')
                    if len(parts) == 2:
                        visuals.append(f'''
            <div class="visual-element">
                <div style="margin-bottom: 10px; font-weight: bold; font-size: 18px;">{num}</div>
                {create_fraction_visual_svg(parts[0], parts[1])}
            </div>''')
                elif '.' in str(num):
                    visuals.append(f'''
            <div class="visual-element">
                <div style="margin-bottom: 10px; font-weight: bold; font-size: 18px;">{num}</div>
                {create_decimal_grid_svg(num)}
            </div>''')
                else:
                    visuals.append(f'''
            <div class="visual-element">
                {create_generic_math_visual()}
            </div>''')
        else:
            visuals.append(f'''
            <div class="visual-element">
                {create_generic_math_visual()}
            </div>''')
    
    return visuals

def generate_html_file(question, week, exercise):
    """Generate complete HTML file with visuals"""
    
    visuals = generate_visual_for_question(question)
    
    # Wrap visuals in grid container if multiple
    if len(visuals) > 1:
        visual_content = '        <div class="grid-container">\n' + '\n'.join(visuals) + '\n        </div>'
    else:
        visual_content = '\n'.join(visuals)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 - Week {week} - Exercise {exercise}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 900px;
        }}
        .visual-element {{
            margin: 20px auto;
            display: inline-block;
            padding: 10px;
        }}
        .grid-container {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            align-items: center;
        }}
    </style>
</head>
<body>
    <div class="container">
{visual_content}
    </div>
</body>
</html>'''
    
    return html

def process_all_files():
    """Process all Grade 6 JSON files and generate HTML"""
    
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
                html_content = generate_html_file(question, week, exercise)
                
                # Save HTML file
                html_filename = f'Gr6_{week}_E{exercise}_{q_num}.html'
                html_filepath = html_path / html_filename
                
                with open(html_filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                total_files += 1
                
                if total_files % 100 == 0:
                    print(f"  Generated {total_files} files...")
        
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
    
    print(f"\nCompleted! Generated {total_files} HTML files with proper visual elements")

if __name__ == "__main__":
    process_all_files()