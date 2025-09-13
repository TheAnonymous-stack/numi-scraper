import json
import os
import re

def create_3d_cube_svg(width, height, depth, colors=None):
    """Create SVG for 3D rectangular prism made of cubes"""
    
    # Set up colors
    if colors is None:
        colors = {'front': '#FFB6C1', 'top': '#FFD4E5', 'side': '#FF91A4'}
    
    # Calculate dimensions
    cube_size = 30
    offset_x = 15
    offset_y = 10
    
    svg_width = width * cube_size + depth * offset_x + 100
    svg_height = height * cube_size + depth * offset_y + 100
    
    svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .cube-front {{ fill: {colors['front']}; stroke: #333; stroke-width: 1; }}
        .cube-top {{ fill: {colors['top']}; stroke: #333; stroke-width: 1; }}
        .cube-side {{ fill: {colors['side']}; stroke: #333; stroke-width: 1; }}
    </style>
    '''
    
    # Draw cubes in 3D perspective
    start_x = 50
    start_y = svg_height - 50
    
    for d in range(depth):
        for h in range(height):
            for w in range(width):
                x = start_x + w * cube_size + d * offset_x
                y = start_y - h * cube_size - d * offset_y - cube_size
                
                # Draw cube faces (back to front for proper layering)
                # Top face
                svg += f'''
    <path class="cube-top" d="M {x},{y} 
                              L {x + cube_size},{y} 
                              L {x + cube_size + offset_x},{y - offset_y} 
                              L {x + offset_x},{y - offset_y} 
                              Z" />'''
                
                # Right side face
                svg += f'''
    <path class="cube-side" d="M {x + cube_size},{y} 
                               L {x + cube_size + offset_x},{y - offset_y} 
                               L {x + cube_size + offset_x},{y - offset_y + cube_size} 
                               L {x + cube_size},{y + cube_size} 
                               Z" />'''
                
                # Front face
                svg += f'''
    <rect class="cube-front" x="{x}" y="{y}" width="{cube_size}" height="{cube_size}" />'''
    
    svg += '\n</svg>'
    return svg

def create_2d_grid_svg(rows, cols, color='#FFB6C1'):
    """Create SVG for 2D grid view"""
    
    cell_size = 40
    svg_width = cols * cell_size + 20
    svg_height = rows * cell_size + 20
    
    svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .grid-cell {{ fill: {color}; stroke: #333; stroke-width: 2; }}
    </style>
    '''
    
    for row in range(rows):
        for col in range(cols):
            x = 10 + col * cell_size
            y = 10 + row * cell_size
            svg += f'''
    <rect class="grid-cell" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" />'''
    
    svg += '\n</svg>'
    return svg

def parse_dimensions(backend_desc):
    """Extract dimensions from backend description"""
    
    # Look for patterns like "8 cubes from front to back", "2 cubes from bottom to top", etc.
    length_match = re.search(r'(\d+)\s+cubes?\s+from\s+front\s+to\s+back', backend_desc)
    height_match = re.search(r'(\d+)\s+cubes?\s+from\s+bottom\s+to\s+top', backend_desc)
    width_match = re.search(r'(\d+)\s+cubes?\s+from\s+left\s+to\s+right', backend_desc)
    
    length = int(length_match.group(1)) if length_match else 3
    height = int(height_match.group(1)) if height_match else 2
    width = int(width_match.group(1)) if width_match else 3
    
    return width, height, length

def parse_2d_grid(backend_desc):
    """Extract 2D grid dimensions from backend description"""
    
    # Look for patterns like "8 rows and 2 columns"
    match = re.search(r'(\d+)\s+rows?\s+and\s+(\d+)\s+columns?', backend_desc)
    if match:
        rows = int(match.group(1))
        cols = int(match.group(2))
        return rows, cols
    
    # Alternative pattern "3 by 2"
    match = re.search(r'(\d+)\s+by\s+(\d+)', backend_desc)
    if match:
        rows = int(match.group(1))
        cols = int(match.group(2))
        return rows, cols
    
    return 3, 2  # default

def create_html_with_svgs(quiz):
    """Create HTML with embedded SVG images"""
    
    question_text = quiz.get('question_text', '')
    backend_desc = quiz.get('backend_description', '')
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    
    # Parse dimensions for main 3D object
    width, height, depth = parse_dimensions(backend_desc)
    
    # Get option descriptions
    option_descs = quiz.get('image_choice_backend_description', [])
    correct_answer = quiz.get('correct_answers', [''])[0]
    
    # Determine view type from question
    view_type = 'front'
    if 'top' in question_text.lower():
        view_type = 'top'
    elif 'side' in question_text.lower():
        view_type = 'side'
    
    # Create main 3D cube SVG
    main_svg = create_3d_cube_svg(width, height, depth)
    
    # Create option SVGs (2D grids)
    option_svgs = []
    for desc in option_descs:
        rows, cols = parse_2d_grid(desc)
        option_svgs.append(create_2d_grid_svg(rows, cols))
    
    # Create solution SVGs
    solution_svgs = []
    
    # Step 1: 3D object with highlighted face
    highlight_colors = {
        'front': {'front': '#FF6B6B', 'top': '#FFD4E5', 'side': '#FF91A4'},
        'top': {'front': '#FFB6C1', 'top': '#FF6B6B', 'side': '#FF91A4'},
        'side': {'front': '#FFB6C1', 'top': '#FFD4E5', 'side': '#FF6B6B'}
    }
    solution_svgs.append(create_3d_cube_svg(width, height, depth, highlight_colors[view_type]))
    
    # Step 2: 2D view
    if view_type == 'front':
        solution_svgs.append(create_2d_grid_svg(height, width, '#FF6B6B'))
    elif view_type == 'top':
        solution_svgs.append(create_2d_grid_svg(depth, width, '#FF6B6B'))
    else:  # side
        solution_svgs.append(create_2d_grid_svg(height, depth, '#FF6B6B'))
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tag} Question {question_number}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1000px;
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
            font-size: 22px;
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
            gap: 40px;
            margin: 40px 0;
            flex-wrap: wrap;
        }}
        .option {{
            text-align: center;
            padding: 20px;
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
            font-size: 26px;
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
            margin-bottom: 15px;
        }}
        .visual-container {{
            text-align: center;
            margin: 20px 0;
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
    solution_steps = quiz.get('solution', [])
    for i, (step_info, svg) in enumerate(zip(solution_steps, solution_svgs)):
        step_num = step_info[0] if len(step_info) > 0 else f"{i+1}"
        step_text = step_info[1] if len(step_info) > 1 else ""
        
        html_content += f"""
            <div class="solution-step">
                <div class="step-text">Step {step_num}: {step_text}</div>
                <div class="visual-container">
                    {svg}
                </div>
            </div>
"""
    
    html_content += """
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    """Process Gr6_46_E3 and create HTML with actual SVG visualizations"""
    
    json_file = 'Gr6_46_E3_variations.json'
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