import json
import os
import re

def create_shape_svg(shape_type, x, y, size=40, color='#FFB6C1', stroke_color='#FF0000', stroke_width=2):
    """Create SVG for a basic shape at given position"""
    
    if shape_type == 'square':
        return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_width}" />'
    elif shape_type == 'triangle':
        # Equilateral triangle
        points = f"{x},{y+size} {x+size/2},{y} {x+size},{y+size}"
        return f'<polygon points="{points}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_width}" />'
    elif shape_type == 'L-shape':
        # L-shaped polygon
        points = f"{x},{y} {x+size},{y} {x+size},{y+size/2} {x+size/2},{y+size/2} {x+size/2},{y+size} {x},{y+size}"
        return f'<polygon points="{points}" fill="{color}" stroke="{stroke_color}" stroke-width="{stroke_width}" />'
    else:
        return create_shape_svg('square', x, y, size, color, stroke_color, stroke_width)

def apply_transformation(shape_svg, transform_type, grid_size=400, original_x=60, original_y=60, size=40):
    """Apply transformation to a shape and return transformed SVG"""
    
    if transform_type == 'rotation_90':
        # Rotate 90 degrees clockwise around center
        center_x = grid_size / 2
        center_y = grid_size / 2
        return f'<g transform="rotate(90, {center_x}, {center_y})">{shape_svg}</g>'
    
    elif transform_type == 'rotation_180':
        # Rotate 180 degrees around center
        center_x = grid_size / 2
        center_y = grid_size / 2
        return f'<g transform="rotate(180, {center_x}, {center_y})">{shape_svg}</g>'
    
    elif transform_type == 'rotation_270':
        # Rotate 270 degrees clockwise around center
        center_x = grid_size / 2
        center_y = grid_size / 2
        return f'<g transform="rotate(270, {center_x}, {center_y})">{shape_svg}</g>'
    
    elif transform_type == 'translation':
        # Translate by specified units
        dx = 160  # 4 units right (40 pixels per unit)
        dy = 80   # 2 units down
        return f'<g transform="translate({dx}, {dy})">{shape_svg}</g>'
    
    elif transform_type == 'reflection_horizontal':
        # Reflect horizontally (flip across vertical axis)
        return f'<g transform="scale(-1, 1) translate(-{grid_size}, 0)">{shape_svg}</g>'
    
    elif transform_type == 'reflection_vertical':
        # Reflect vertically (flip across horizontal axis)
        return f'<g transform="scale(1, -1) translate(0, -{grid_size})">{shape_svg}</g>'
    
    elif transform_type == 'reflection_diagonal':
        # Reflect diagonally (flip across y=x line)
        # This is achieved by transposing the coordinates
        return f'<g transform="matrix(0, 1, 1, 0, 0, 0)">{shape_svg}</g>'
    
    else:
        return shape_svg

def create_grid_svg(width=400, height=400, cell_size=40):
    """Create background grid SVG"""
    
    grid_lines = ''
    
    # Vertical lines
    for x in range(0, width + 1, cell_size):
        grid_lines += f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="#ddd" stroke-width="1" />\n'
    
    # Horizontal lines
    for y in range(0, height + 1, cell_size):
        grid_lines += f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#ddd" stroke-width="1" />\n'
    
    return grid_lines

def parse_transformation_from_description(description):
    """Parse transformation type from backend description"""
    
    desc_lower = description.lower()
    
    if 'rotated 90' in desc_lower:
        return 'rotation_90'
    elif 'rotated 180' in desc_lower:
        return 'rotation_180'
    elif 'rotated 270' in desc_lower:
        return 'rotation_270'
    elif 'translated' in desc_lower:
        return 'translation'
    elif 'reflected' in desc_lower or 'flipped' in desc_lower:
        if 'horizontal' in desc_lower:
            return 'reflection_horizontal'
        elif 'vertical' in desc_lower:
            return 'reflection_vertical'
        elif 'diagonal' in desc_lower:
            return 'reflection_diagonal'
    
    return None

def parse_position_from_description(description):
    """Extract position from backend description"""
    
    desc_lower = description.lower()
    
    # Default position
    x, y = 60, 60  # top-left with padding
    
    if 'top-left' in desc_lower:
        x, y = 60, 60
    elif 'top-right' in desc_lower:
        x, y = 300, 60
    elif 'bottom-left' in desc_lower:
        x, y = 60, 300
    elif 'bottom-right' in desc_lower:
        x, y = 300, 300
    elif 'center' in desc_lower:
        x, y = 180, 180
    
    return x, y

def create_transformation_svg(quiz):
    """Create SVG visualizations for transformation questions"""
    
    backend_desc = quiz.get('backend_description', '')
    option_descs = quiz.get('image_choice_tags_backend_description', [])
    solution_image_tags = quiz.get('solution_image_tag', [])
    
    # Parse shape type and position
    shape_type = 'square'  # Default shape
    if 'triangle' in backend_desc.lower():
        shape_type = 'triangle'
    elif 'l-shape' in backend_desc.lower():
        shape_type = 'L-shape'
    
    x, y = parse_position_from_description(backend_desc)
    
    # SVG dimensions
    svg_width = 400
    svg_height = 400
    
    # Create main shape SVG
    main_svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg" style="background: white; border: 2px solid #333;">
    {create_grid_svg(svg_width, svg_height)}
    {create_shape_svg(shape_type, x, y)}
</svg>'''
    
    # Create option SVGs with transformations
    option_svgs = []
    for desc in option_descs:
        transform_type = parse_transformation_from_description(desc)
        
        svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg" style="background: white; border: 2px solid #333;">
    {create_grid_svg(svg_width, svg_height)}
    {apply_transformation(create_shape_svg(shape_type, x, y), transform_type, svg_width, x, y)}
</svg>'''
        option_svgs.append(svg)
    
    # Create solution step SVGs
    solution_svgs = []
    
    # Original shape (Step 1)
    solution_svgs.append(f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg" style="background: white; border: 2px solid #333;">
    {create_grid_svg(svg_width, svg_height)}
    {create_shape_svg(shape_type, x, y, color='#FFB6C1', stroke_color='#FF0000', stroke_width=3)}
</svg>''')
    
    # Add transformation examples for other steps
    for img_tag_info in solution_image_tags[1:]:  # Skip first as we already created it
        if len(img_tag_info) > 2:
            desc = img_tag_info[2]
            transform_type = parse_transformation_from_description(desc)
            
            if transform_type:
                svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg" style="background: white; border: 2px solid #333;">
    {create_grid_svg(svg_width, svg_height)}
    {apply_transformation(create_shape_svg(shape_type, x, y, color='#87CEEB', stroke_color='#0000FF', stroke_width=2), transform_type, svg_width, x, y)}
    <text x="10" y="390" font-size="14" fill="#333">{transform_type.replace('_', ' ').title()}</text>
</svg>'''
                solution_svgs.append(svg)
    
    return main_svg, option_svgs, solution_svgs

def create_html_with_svgs(quiz):
    """Create HTML with embedded SVG transformations"""
    
    question_text = quiz.get('question_text', '')
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    correct_answer = quiz.get('correct_answers', [''])[0]
    solution_steps = quiz.get('solution', [])
    
    # Generate SVGs
    main_svg, option_svgs, solution_svgs = create_transformation_svg(quiz)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tag} Question {question_number}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .question {{
            font-size: 24px;
            margin-bottom: 30px;
            color: #333;
            font-weight: 500;
        }}
        .main-visual {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }}
        .options {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 40px 0;
            flex-wrap: wrap;
        }}
        .option {{
            text-align: center;
            padding: 15px;
            border: 3px solid #ddd;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            background-color: white;
        }}
        .option:hover {{
            border-color: #4CAF50;
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        .option-label {{
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 15px;
        }}
        .correct {{
            background-color: #e8f5e9;
            border-color: #4CAF50;
        }}
        .solution {{
            margin-top: 50px;
            padding-top: 30px;
            border-top: 3px solid #e0e0e0;
        }}
        .solution-title {{
            font-size: 28px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 25px;
            text-align: center;
        }}
        .solution-step {{
            margin: 30px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }}
        .step-text {{
            font-size: 18px;
            color: #555;
            margin-bottom: 20px;
            font-weight: 500;
        }}
        .visual-container {{
            text-align: center;
            margin: 20px 0;
        }}
        svg {{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">{question_text.replace('=_', '')}</div>
        
        <div class="main-visual">
            <div class="visual-container">
                {main_svg}
            </div>
        </div>
        
        <div class="options">
"""
    
    # Add options
    for i, svg in enumerate(option_svgs):
        option_letter = chr(65 + i)
        is_correct = option_letter == correct_answer
        correct_class = ' correct' if is_correct else ''
        
        html_content += f"""
            <div class="option{correct_class}">
                <div class="option-label">Option {option_letter}</div>
                <div class="visual-container">
                    {svg}
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="solution">
            <div class="solution-title">Solution</div>
"""
    
    # Add solution steps
    for i, step_info in enumerate(solution_steps):
        step_num = step_info[0] if len(step_info) > 0 else f"{i+1}"
        step_text = step_info[1] if len(step_info) > 1 else ""
        
        html_content += f"""
            <div class="solution-step">
                <div class="step-text">Step {step_num}: {step_text}</div>
"""
        
        if i < len(solution_svgs):
            html_content += f"""
                <div class="visual-container">
                    {solution_svgs[i]}
                </div>
"""
        
        html_content += """
            </div>
"""
    
    html_content += """
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    """Process Gr6_48_E1 and create HTML with actual SVG visualizations"""
    
    json_file = 'Gr6_48_E1_variations.json'
    output_dir = 'HTML'
    
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Creating HTML files with embedded SVG visualizations for {json_file}...")
    print("-" * 60)
    
    count = 0
    for quiz in data['quizzes']:
        question_number = quiz.get('question_number', '')
        tag = quiz.get('tag', '')
        
        filename = f"{tag}_{question_number}.html"
        filepath = os.path.join(output_dir, filename)
        
        html_content = create_html_with_svgs(quiz)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        count += 1
        if count % 10 == 0:
            print(f"  Processed {count} files...")
    
    print(f"\nCreated {count} HTML files with embedded SVG visualizations")
    print(f"Files saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()