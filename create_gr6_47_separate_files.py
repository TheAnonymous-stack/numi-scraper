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
            points.append({
                'label': label,
                'x': int(x),
                'y': int(y),
                'color': '#FF6B6B' if label == highlight_point else '#4ECDC4'
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
        if x != 0 and x % 2 == 0:  # Show every other number
            svg_x, _ = to_svg_coords(x, 0)
            svg += f'<text x="{svg_x}" y="{origin_y + 20}" font-size="12" text-anchor="middle" fill="#666">{x}</text>\n'
    
    for y in range(int(y_min), int(y_max) + 1):
        if y != 0 and y % 2 == 0:  # Show every other number
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
        opacity = '0.3' if show_line and p['label'] != highlight_point else '1'
        svg += f'<circle cx="{svg_x}" cy="{svg_y}" r="6" fill="{p["color"]}" stroke="#333" stroke-width="2" opacity="{opacity}" />\n'
        svg += f'<text x="{svg_x + 10}" y="{svg_y - 10}" font-size="14" font-weight="bold" fill="#333" opacity="{opacity}">{p["label"]}</text>\n'
    
    svg += '</svg>'
    return svg

def create_main_html(quiz):
    """Create main HTML file that references separate image files"""
    
    question_text = quiz.get('question_text', '')
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    
    # Clean question text
    question_text = question_text.replace('=_', '')
    
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
            font-size: 24px;
            margin-bottom: 30px;
            color: #333;
            font-weight: 500;
        }}
        .main-visual {{
            text-align: center;
            margin: 30px 0;
        }}
        .main-visual img {{
            max-width: 100%;
            height: auto;
            border: 2px solid #333;
            border-radius: 5px;
            background: white;
        }}
        .answer-section {{
            margin: 30px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }}
        .answer-input {{
            font-size: 20px;
            padding: 10px;
            width: 100px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
            text-align: center;
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
        .visual-container img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">{question_text}</div>
        
        <div class="main-visual">
            <img src="{tag}_{question_number}_question.html" alt="Coordinate Plane">
        </div>
        
        <div class="answer-section">
            <input type="text" class="answer-input" placeholder="Answer">
        </div>
        
        <div class="solution">
            <div class="solution-title">Solution</div>
"""
    
    # Add solution steps
    solution_steps = quiz.get('solution', [])
    for i, step_info in enumerate(solution_steps):
        step_num = step_info[0] if len(step_info) > 0 else f"{i+1}"
        step_text = step_info[1] if len(step_info) > 1 else ""
        
        html_content += f"""
            <div class="solution-step">
                <div class="step-text">Step {step_num}: {step_text}</div>"""
        
        # Add solution image if it exists
        if i == 0:  # First step usually has the visual
            html_content += f"""
                <div class="visual-container">
                    <img src="{tag}_{question_number}_solution_{i+1}.html" alt="Solution Step {i+1}">
                </div>"""
        
        html_content += """
            </div>"""
    
    html_content += """
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def create_image_html(svg_content):
    """Create HTML file containing just the SVG image"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: white;
        }}
    </style>
</head>
<body>
    {svg_content}
</body>
</html>"""
    
    return html_content

def process_quiz(quiz, output_dir):
    """Process a single quiz and create all necessary HTML files"""
    
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    backend_desc = quiz.get('backend_description', '')
    solution_image_tags = quiz.get('solution_image_tag', [])
    
    # Extract point to highlight from question
    question_text = quiz.get('question_text', '')
    highlight_point = None
    if 'point' in question_text.lower():
        match = re.search(r'point (\w+)', question_text, re.IGNORECASE)
        if match:
            highlight_point = match.group(1).upper()
    
    # Create main HTML
    main_html = create_main_html(quiz)
    main_file = os.path.join(output_dir, f"{tag}_{question_number}.html")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(main_html)
    
    # Create question image HTML
    question_svg = create_coordinate_plane_svg(backend_desc, highlight_point)
    question_html = create_image_html(question_svg)
    question_file = os.path.join(output_dir, f"{tag}_{question_number}_question.html")
    with open(question_file, 'w', encoding='utf-8') as f:
        f.write(question_html)
    
    # Create solution image HTML files
    for i, img_info in enumerate(solution_image_tags):
        if len(img_info) > 2:
            desc = img_info[2]
            # Determine if we need to show a line
            show_line = None
            if 'vertical line' in desc:
                show_line = 'vertical'
            elif 'horizontal line' in desc:
                show_line = 'horizontal'
            
            solution_svg = create_coordinate_plane_svg(desc, highlight_point, show_line)
            solution_html = create_image_html(solution_svg)
            solution_file = os.path.join(output_dir, f"{tag}_{question_number}_solution_{i+1}.html")
            with open(solution_file, 'w', encoding='utf-8') as f:
                f.write(solution_html)

def main():
    """Process Gr6_47_E1 and Gr6_47_E2"""
    
    exercises = ['Gr6_47_E1_variations.json', 'Gr6_47_E2_variations.json']
    output_dir = 'HTML'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Creating HTML files with separate components for Gr6_47_E1 and Gr6_47_E2...")
    print("-" * 60)
    
    total_files = 0
    
    for json_file in exercises:
        if not os.path.exists(json_file):
            print(f"Warning: {json_file} not found, skipping...")
            continue
        
        print(f"\nProcessing {json_file}...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for quiz in data['quizzes']:
            process_quiz(quiz, output_dir)
            count += 1
            
            if count % 10 == 0:
                print(f"  Processed {count} quizzes...")
        
        # Each quiz generates: 1 main + 1 question + ~1 solution = ~3 files per quiz
        files_created = count * 3
        total_files += files_created
        print(f"  Created approximately {files_created} HTML files for {count} quizzes")
    
    print("\n" + "-" * 60)
    print(f"Total files created: approximately {total_files}")
    print(f"Files saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()