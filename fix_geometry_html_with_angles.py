import json
import os
import re
import math

def extract_angles_from_description(backend_desc):
    """Extract angle values from backend_description"""
    # Pattern to find angles like 149°, 130°, etc.
    angle_pattern = r'(\d+)°'
    angles = re.findall(angle_pattern, backend_desc)
    return [int(a) for a in angles]

def extract_polygon_info(quiz):
    """Extract polygon type and angles from quiz data"""
    backend_desc = quiz.get('backend_description', '')
    question_text = quiz.get('question_text', '')
    
    # Determine polygon type
    polygon_info = {
        'decagon': (10, 'decagon'),
        'heptagon': (7, 'heptagon'),
        'dodecagon': (12, 'dodecagon'),
        'hexagon': (6, 'hexagon'),
        'pentagon': (5, 'pentagon'),
        'quadrilateral': (4, 'quadrilateral'),
        'triangle': (3, 'triangle'),
        'octagon': (8, 'octagon'),
        'nonagon': (9, 'nonagon')
    }
    
    sides = 4  # default
    shape_name = 'polygon'
    
    for key, (num_sides, name) in polygon_info.items():
        if key in backend_desc.lower():
            sides = num_sides
            shape_name = name
            break
    
    # Extract known angles
    angles = extract_angles_from_description(backend_desc)
    
    # Get the variable name (n, x, y, etc.)
    var_match = re.search(r'variable\s+(\w+)', backend_desc)
    variable = var_match.group(1) if var_match else 'x'
    
    return sides, shape_name, angles, variable

def create_polygon_with_angles_html(quiz, exercise_tag):
    """Create HTML with polygon showing all angle values"""
    sides, shape_name, known_angles, variable = extract_polygon_info(quiz)
    question_num = quiz['question_number']
    
    # Create polygon points based on number of sides
    cx, cy = 200, 150  # center
    radius = 120
    points = []
    for i in range(sides):
        angle = -90 + (360 / sides) * i  # Start from top
        x = cx + radius * math.cos(math.radians(angle))
        y = cy + radius * math.sin(math.radians(angle))
        points.append((x, y))
    
    # Create SVG polygon points string
    points_str = ' '.join(f'{x:.0f},{y:.0f}' for x, y in points)
    
    # Create angle labels
    angle_labels = ''
    for i, (x, y) in enumerate(points):
        # Position labels slightly inside the polygon
        label_x = cx + (x - cx) * 0.75
        label_y = cy + (y - cy) * 0.75
        
        if i < len(known_angles):
            angle_labels += f'<text x="{label_x:.0f}" y="{label_y:.0f}" font-size="14" text-anchor="middle">{known_angles[i]}°</text>\n'
        else:
            # This is the unknown angle
            angle_labels += f'<text x="{label_x:.0f}" y="{label_y:.0f}" font-size="14" text-anchor="middle" fill="red" font-weight="bold">{variable}</text>\n'
    
    # Clean question text
    clean_question = quiz['question_text'].replace('___', '').strip()
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .polygon-container {{
            margin: 20px 0;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="question">{clean_question}</div>
    
    <div class="polygon-container">
        <svg width="400" height="300" viewBox="0 0 400 300">
            <!-- {shape_name.capitalize()} -->
            <polygon points="{points_str}" fill="none" stroke="black" stroke-width="2"/>
            
            <!-- Angle labels -->
            {angle_labels}
        </svg>
    </div>
</body>
</html>"""
    
    return html

def create_protractor_with_angle_html(quiz, exercise_tag):
    """Create HTML with protractor showing the specific angle"""
    # Extract angle from correct answer
    angle_value = float(quiz['correct_answers'][0]) if quiz.get('correct_answers') else 45
    
    # Calculate angle ray endpoint
    angle_rad = angle_value * math.pi / 180
    x2 = 200 + 150 * math.cos(angle_rad)
    y2 = 200 - 150 * math.sin(angle_rad)
    
    # Calculate arc endpoint  
    arc_x = 200 + 50 * math.cos(angle_rad)
    arc_y = 200 - 50 * math.sin(angle_rad)
    
    # Determine if we need large-arc-flag for angles > 180
    large_arc = "1" if angle_value > 90 else "0"
    
    question_num = quiz['question_number']
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .protractor-container {{
            margin: 20px 0;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="question">What is the measurement of this angle?</div>
    
    <div class="protractor-container">
        <svg width="400" height="250" viewBox="0 0 400 250">
            <!-- Protractor semicircle with light fill -->
            <path d="M 50 200 A 150 150 0 0 1 350 200 Z" fill="#f0f0f0" stroke="black" stroke-width="2"/>
            
            <!-- Degree markings every 10 degrees -->
            <g id="degree-marks">"""
    
    # Add degree marks every 10 degrees
    for deg in range(0, 181, 10):
        angle_rad_mark = deg * math.pi / 180
        x1_mark = 200 + 150 * math.cos(angle_rad_mark)
        y1_mark = 200 - 150 * math.sin(angle_rad_mark)
        x2_mark = 200 + 140 * math.cos(angle_rad_mark)
        y2_mark = 200 - 140 * math.sin(angle_rad_mark)
        
        # Longer marks for multiples of 30
        if deg % 30 == 0:
            x2_mark = 200 + 135 * math.cos(angle_rad_mark)
            y2_mark = 200 - 135 * math.sin(angle_rad_mark)
        
        html += f'\n                <line x1="{x1_mark:.0f}" y1="{y1_mark:.0f}" x2="{x2_mark:.0f}" y2="{y2_mark:.0f}" stroke="black" stroke-width="1"/>'
        
        # Add text labels for key angles
        if deg % 30 == 0:
            text_x = 200 + 165 * math.cos(angle_rad_mark)
            text_y = 200 - 165 * math.sin(angle_rad_mark) + 5
            html += f'\n                <text x="{text_x:.0f}" y="{text_y:.0f}" font-size="12" text-anchor="middle">{deg}°</text>'
    
    html += f"""
            </g>
            
            <!-- Center point -->
            <circle cx="200" cy="200" r="3" fill="black"/>
            
            <!-- Base ray (0 degrees) -->
            <line x1="200" y1="200" x2="350" y2="200" stroke="blue" stroke-width="3"/>
            
            <!-- Angle ray -->
            <line x1="200" y1="200" x2="{x2:.0f}" y2="{y2:.0f}" stroke="blue" stroke-width="3"/>
            
            <!-- Angle arc -->
            <path d="M 250 200 A 50 50 0 {large_arc} 0 {arc_x:.0f} {arc_y:.0f}" fill="none" stroke="red" stroke-width="2"/>
            
            <!-- Angle value display -->
            <text x="200" y="230" font-size="16" font-weight="bold" text-anchor="middle">{angle_value:.0f}°</text>
        </svg>
    </div>
</body>
</html>"""
    
    return html

def create_trapezoid_with_dimensions_html(quiz, exercise_tag):
    """Create HTML with trapezoid showing cut line"""
    question_num = quiz['question_number']
    
    # Main question HTML with dimensions
    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .trapezoid-container {{
            margin: 20px 0;
            text-align: center;
        }}
        .options {{
            margin: 20px 0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}
        .option {{
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .option:hover {{
            background-color: #f0f0f0;
            border-color: #4CAF50;
        }}
        .option-label {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="question">Maggie cuts the trapezoid along the dashed line. Which two shapes does she make?</div>
    
    <div class="trapezoid-container">
        <svg width="400" height="250" viewBox="0 0 400 250">
            <!-- Trapezoid with dimensions -->
            <polygon points="100,80 300,80 320,180 80,180" fill="lightblue" stroke="black" stroke-width="2"/>
            
            <!-- Dashed cutting line (vertical through middle) -->
            <line x1="200" y1="80" x2="200" y2="180" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
            
            <!-- Dimension labels -->
            <text x="200" y="70" font-size="12" text-anchor="middle">Top: 200</text>
            <text x="200" y="200" font-size="12" text-anchor="middle">Bottom: 240</text>
            <text x="60" y="130" font-size="12" text-anchor="middle">Height: 100</text>
            
            <!-- Cut line label -->
            <text x="210" y="130" font-size="11" fill="red">cut</text>
        </svg>
    </div>
    
    <div class="options">
        <div class="option">
            <div class="option-label">A) Two triangles</div>
            <svg width="180" height="80" viewBox="0 0 180 80">
                <polygon points="20,20 50,20 35,60" fill="lightgreen" stroke="black" stroke-width="1"/>
                <polygon points="70,20 100,20 85,60" fill="lightgreen" stroke="black" stroke-width="1"/>
            </svg>
        </div>
        
        <div class="option">
            <div class="option-label">B) Two trapezoids</div>
            <svg width="180" height="80" viewBox="0 0 180 80">
                <polygon points="20,20 45,20 50,60 15,60" fill="lightcoral" stroke="black" stroke-width="1"/>
                <polygon points="65,20 90,20 95,60 60,60" fill="lightcoral" stroke="black" stroke-width="1"/>
            </svg>
        </div>
        
        <div class="option">
            <div class="option-label">C) Rectangle and triangle</div>
            <svg width="180" height="80" viewBox="0 0 180 80">
                <rect x="20" y="20" width="40" height="40" fill="lightyellow" stroke="black" stroke-width="1"/>
                <polygon points="80,20 110,40 80,60" fill="lightblue" stroke="black" stroke-width="1"/>
            </svg>
        </div>
        
        <div class="option">
            <div class="option-label">D) Two parallelograms</div>
            <svg width="180" height="80" viewBox="0 0 180 80">
                <polygon points="20,20 50,20 45,60 15,60" fill="lavender" stroke="black" stroke-width="1"/>
                <polygon points="70,20 100,20 95,60 65,60" fill="lavender" stroke="black" stroke-width="1"/>
            </svg>
        </div>
    </div>
</body>
</html>"""
    
    return html

def process_all_geometry_files():
    """Process all geometry exercise JSON files and create HTML files with angles/dimensions"""
    
    # Process Gr6_50_E1 and Gr6_50_E2 (protractor exercises)
    for filename in ['Gr6_50_E1_variations.json', 'Gr6_50_E2_variations.json']:
        if not os.path.exists(filename):
            continue
            
        print(f"Processing {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        exercise_tag = filename.replace('_variations.json', '')
        count = 0
        
        for quiz in data['quizzes']:
            try:
                html = create_protractor_with_angle_html(quiz, exercise_tag)
                filepath = f"HTML/{exercise_tag}_{quiz['question_number']}.html"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1
            except Exception as e:
                print(f"Error processing {quiz.get('question_number', 'unknown')}: {e}")
        
        print(f"Created {count} HTML files for {exercise_tag}")
    
    # Process Gr6_51_E1 through Gr6_51_E4 (polygon angle exercises)
    for i in range(1, 5):
        filename = f'Gr6_51_E{i}_variations.json'
        if not os.path.exists(filename):
            continue
            
        print(f"Processing {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        exercise_tag = f'Gr6_51_E{i}'
        count = 0
        
        for quiz in data['quizzes']:
            try:
                html = create_polygon_with_angles_html(quiz, exercise_tag)
                filepath = f"HTML/{exercise_tag}_{quiz['question_number']}.html"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1
            except Exception as e:
                print(f"Error processing {quiz.get('question_number', 'unknown')}: {e}")
        
        print(f"Created {count} HTML files for {exercise_tag}")
    
    # Process Gr6_52_E1 (trapezoid exercise)
    if os.path.exists('Gr6_52_E1_variations.json'):
        print("Processing Gr6_52_E1_variations.json...")
        with open('Gr6_52_E1_variations.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for quiz in data['quizzes']:
            try:
                html = create_trapezoid_with_dimensions_html(quiz, 'Gr6_52_E1')
                filepath = f"HTML/Gr6_52_E1_{quiz['question_number']}.html"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1
            except Exception as e:
                print(f"Error processing {quiz.get('question_number', 'unknown')}: {e}")
        
        print(f"Created {count} HTML files for Gr6_52_E1")

if __name__ == "__main__":
    if not os.path.exists('HTML'):
        os.makedirs('HTML')
    
    process_all_geometry_files()