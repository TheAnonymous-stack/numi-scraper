import json
import os
import re

def create_coordinate_plane_svg(points_data, highlight_point=None, show_line=None, width=500, height=500):
    """Create SVG for coordinate plane with points"""
    
    # Parse points from backend description
    points = []
    if isinstance(points_data, str):
        # Extract points from description
        pattern = r'Point (\w+) is labeled.*?at the point \((-?\d+), (-?\d+)\)'
        matches = re.findall(pattern, points_data)
        for label, x, y in matches:
            # Check if this point should be faded
            is_faded = 'faded out' in points_data and f'Point {label} is faded' in points_data
            points.append({
                'label': label,
                'x': int(x),
                'y': int(y),
                'color': '#FF6B6B' if label == highlight_point else '#4ECDC4',
                'opacity': '0.3' if is_faded else '1.0'
            })
    
    # Determine grid range
    x_values = [p['x'] for p in points] + [0]
    y_values = [p['y'] for p in points] + [0]
    
    x_min = min(x_values) - 2
    x_max = max(x_values) + 2
    y_min = min(y_values) - 2
    y_max = max(y_values) + 2
    
    # Calculate SVG coordinates
    padding = 40
    grid_width = width - 2 * padding
    grid_height = height - 2 * padding
    
    x_scale = grid_width / (x_max - x_min)
    y_scale = grid_height / (y_max - y_min)
    
    def to_svg_coords(x, y):
        svg_x = padding + (x - x_min) * x_scale
        svg_y = padding + (y_max - y) * y_scale
        return svg_x, svg_y
    
    origin_x, origin_y = to_svg_coords(0, 0)
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background: white;">
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
        </marker>
    </defs>
    '''
    
    # Draw grid lines
    for x in range(int(x_min), int(x_max) + 1):
        svg_x, _ = to_svg_coords(x, 0)
        color = '#333' if x == 0 else '#e0e0e0'
        width_val = 2 if x == 0 else 1
        svg += f'<line x1="{svg_x}" y1="{padding}" x2="{svg_x}" y2="{height - padding}" stroke="{color}" stroke-width="{width_val}" />\n'
    
    for y in range(int(y_min), int(y_max) + 1):
        _, svg_y = to_svg_coords(0, y)
        color = '#333' if y == 0 else '#e0e0e0'
        width_val = 2 if y == 0 else 1
        svg += f'<line x1="{padding}" y1="{svg_y}" x2="{width - padding}" y2="{svg_y}" stroke="{color}" stroke-width="{width_val}" />\n'
    
    # Draw axes arrows
    svg += f'<line x1="{width - padding}" y1="{origin_y}" x2="{width - padding + 10}" y2="{origin_y}" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)" />\n'
    svg += f'<line x1="{origin_x}" y1="{padding}" x2="{origin_x}" y2="{padding - 10}" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)" />\n'
    
    # Draw axis labels
    svg += f'<text x="{width - padding + 20}" y="{origin_y + 5}" font-size="16" font-weight="bold" fill="#333">x</text>\n'
    svg += f'<text x="{origin_x - 5}" y="{padding - 15}" font-size="16" font-weight="bold" fill="#333">y</text>\n'
    
    # Draw axis numbers
    for x in range(int(x_min), int(x_max) + 1):
        if x != 0 and x % 2 == 0:
            svg_x, _ = to_svg_coords(x, 0)
            svg += f'<text x="{svg_x}" y="{origin_y + 20}" font-size="12" text-anchor="middle" fill="#666">{x}</text>\n'
    
    for y in range(int(y_min), int(y_max) + 1):
        if y != 0 and y % 2 == 0:
            _, svg_y = to_svg_coords(0, y)
            svg += f'<text x="{origin_x - 15}" y="{svg_y + 5}" font-size="12" text-anchor="end" fill="#666">{y}</text>\n'
    
    # Draw special line if requested
    if show_line and highlight_point:
        for p in points:
            if p['label'] == highlight_point:
                px, py = to_svg_coords(p['x'], p['y'])
                if 'vertical' in show_line:
                    line_x, _ = to_svg_coords(p['x'], 0)
                    svg += f'<line x1="{px}" y1="{py}" x2="{line_x}" y2="{origin_y}" stroke="#FF0000" stroke-width="2" stroke-dasharray="5,5" />\n'
                elif 'horizontal' in show_line:
                    _, line_y = to_svg_coords(0, p['y'])
                    svg += f'<line x1="{px}" y1="{py}" x2="{origin_x}" y2="{line_y}" stroke="#FF0000" stroke-width="2" stroke-dasharray="5,5" />\n'
    
    # Draw points
    for p in points:
        svg_x, svg_y = to_svg_coords(p['x'], p['y'])
        svg += f'<circle cx="{svg_x}" cy="{svg_y}" r="6" fill="{p["color"]}" stroke="#333" stroke-width="2" opacity="{p["opacity"]}" />\n'
        svg += f'<text x="{svg_x + 10}" y="{svg_y - 10}" font-size="14" font-weight="bold" fill="#333" opacity="{p["opacity"]}">{p["label"]}</text>\n'
    
    svg += '</svg>'
    return svg

def create_main_html_with_image(quiz):
    """Create main HTML that actually displays the coordinate plane"""
    
    question_text = quiz.get('question_text', '').replace('=_', '')
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    backend_desc = quiz.get('backend_description', '')
    
    # Extract point to highlight from question
    highlight_point = None
    if 'point' in question_text.lower():
        match = re.search(r'point (\w+)', question_text, re.IGNORECASE)
        if match:
            highlight_point = match.group(1).upper()
    
    # Add context to question based on what we're asking
    if 'x-coordinate' in question_text.lower():
        context = "Look at the coordinate plane below. The x-coordinate tells us how far left or right a point is from the origin (0,0)."
    elif 'y-coordinate' in question_text.lower():
        context = "Look at the coordinate plane below. The y-coordinate tells us how far up or down a point is from the origin (0,0)."
    else:
        context = "Look at the coordinate plane below with the labeled points."
    
    # Generate the SVG for the coordinate plane
    svg_content = create_coordinate_plane_svg(backend_desc, highlight_point)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tag} Question {question_number}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
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
        .context {{
            font-size: 18px;
            color: #666;
            margin-bottom: 20px;
            font-style: italic;
        }}
        .question {{
            font-size: 26px;
            color: #333;
            font-weight: 500;
            margin-bottom: 30px;
        }}
        .coordinate-plane {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 30px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        .answer-box {{
            margin: 30px 0;
            padding: 20px;
            background: #e8f5e9;
            border-radius: 8px;
            text-align: center;
        }}
        .answer-input {{
            font-size: 24px;
            padding: 10px 20px;
            width: 150px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }}
        svg {{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="context">{context}</div>
        <div class="question">{question_text}</div>
        
        <div class="coordinate-plane">
            {svg_content}
        </div>
        
        <div class="answer-box">
            <input type="text" class="answer-input" placeholder="Your answer">
        </div>
    </div>
</body>
</html>"""

def create_solution_step_html(step_num, step_text, tag, question_number):
    """Create HTML for a solution step"""
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tag} {question_number} Step {step_num}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .step {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .step-number {{
            color: #4CAF50;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .step-text {{
            font-size: 18px;
            color: #555;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="step">
        <div class="step-number">Step {step_num}</div>
        <div class="step-text">{step_text}</div>
    </div>
</body>
</html>"""

def create_solution_image_html(svg_content, step_num, tag, question_number):
    """Create HTML for a solution image"""
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tag} {question_number} Solution Visual {step_num}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        svg {{
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        {svg_content}
    </div>
</body>
</html>"""

def process_quiz(quiz, output_dir):
    """Create all separate HTML files for a quiz"""
    
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    backend_desc = quiz.get('backend_description', '')
    solution_image_tags = quiz.get('solution_image_tag', [])
    solution_steps = quiz.get('solution', [])
    question_text = quiz.get('question_text', '')
    
    # Extract point to highlight
    highlight_point = None
    if 'point' in question_text.lower():
        match = re.search(r'point (\w+)', question_text, re.IGNORECASE)
        if match:
            highlight_point = match.group(1).upper()
    
    files_created = []
    
    # 1. Create main HTML with actual coordinate plane displayed
    main_html = create_main_html_with_image(quiz)
    main_file = os.path.join(output_dir, f"{tag}_{question_number}.html")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(main_html)
    files_created.append(main_file)
    
    # 2. Create separate solution step text files
    for i, step_info in enumerate(solution_steps):
        step_num = step_info[0] if len(step_info) > 0 else f"{i+1}"
        step_text = step_info[1] if len(step_info) > 1 else ""
        
        step_html = create_solution_step_html(step_num, step_text, tag, question_number)
        step_file = os.path.join(output_dir, f"{tag}_{question_number}_step_{step_num.replace('/', '_')}.html")
        with open(step_file, 'w', encoding='utf-8') as f:
            f.write(step_html)
        files_created.append(step_file)
    
    # 3. Create solution image files
    for i, img_info in enumerate(solution_image_tags):
        step_num = img_info[0] if len(img_info) > 0 else f"{i+1}"
        desc = img_info[2] if len(img_info) > 2 else ""
        
        # Determine if we need to show a line
        show_line = None
        if 'vertical line' in desc:
            show_line = 'vertical'
        elif 'horizontal line' in desc:
            show_line = 'horizontal'
        
        solution_svg = create_coordinate_plane_svg(desc, highlight_point, show_line)
        solution_html = create_solution_image_html(solution_svg, step_num, tag, question_number)
        
        solution_file = os.path.join(output_dir, f"{tag}_{question_number}_solution_{step_num.replace('/', '_')}.html")
        with open(solution_file, 'w', encoding='utf-8') as f:
            f.write(solution_html)
        files_created.append(solution_file)
    
    return files_created

def main():
    """Process Gr6_47_E1 and Gr6_47_E2 with proper display"""
    
    exercises = ['Gr6_47_E1_variations.json', 'Gr6_47_E2_variations.json']
    output_dir = 'HTML'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Creating HTML files with ACTUAL DISPLAYED CONTENT for Gr6_47...")
    print("-" * 60)
    
    total_files = 0
    
    for json_file in exercises:
        if not os.path.exists(json_file):
            print(f"Warning: {json_file} not found, skipping...")
            continue
        
        print(f"\nProcessing {json_file}...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        file_count = 0
        quiz_count = 0
        for quiz in data['quizzes']:
            files = process_quiz(quiz, output_dir)
            file_count += len(files)
            quiz_count += 1
            
            if quiz_count % 10 == 0:
                print(f"  Processed {quiz_count} quizzes...")
        
        print(f"  Created {file_count} HTML files for {quiz_count} quizzes")
        total_files += file_count
    
    print("\n" + "-" * 60)
    print(f"Total files created: {total_files}")
    print("\nFile structure:")
    print("  - Main HTML: Shows question WITH coordinate plane displayed")
    print("  - Solution step files: Individual step explanations")
    print("  - Solution image files: Coordinate planes with annotations")
    print(f"\nFiles saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()