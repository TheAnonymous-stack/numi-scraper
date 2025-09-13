import json
import os
import re
import math

def update_json_with_angles(json_file):
    """Update JSON files to include angle values in question text"""
    if not os.path.exists(json_file):
        return False
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    
    for quiz in data['quizzes']:
        backend_desc = quiz.get('backend_description', '')
        question_text = quiz.get('question_text', '')
        
        # For Gr6_51_E1 and similar - extract angles from backend description
        if 'Gr6_51_E1' in json_file or 'Gr6_51_E4' in json_file:
            # Extract all angle values
            angle_pattern = r'(\d+)°'
            angles = re.findall(angle_pattern, backend_desc)
            
            # Find variable name
            var_match = re.search(r'variable\s+(\w+)', backend_desc)
            variable = var_match.group(1) if var_match else 'x'
            
            # Extract polygon type
            polygon_types = {
                'triangle': 'triangle',
                'quadrilateral': 'quadrilateral', 
                'pentagon': 'pentagon',
                'hexagon': 'hexagon',
                'heptagon': 'heptagon',
                'octagon': 'octagon',
                'nonagon': 'nonagon',
                'decagon': 'decagon',
                'dodecagon': 'dodecagon'
            }
            
            shape = 'polygon'
            for key, val in polygon_types.items():
                if key in backend_desc.lower():
                    shape = val
                    break
            
            if angles and len(angles) > 0:
                # Create new question text with angle values
                angles_str = ', '.join(angles[:-1]) + f'° and one angle marked as {variable}'
                new_question = f"In this {shape}, the angles are {angles_str}. Find {variable}.\n{variable} = ___°"
                quiz['question_text'] = new_question
                modified = True
        
        # For Gr6_50_E1 and E2 - protractor questions
        elif 'Gr6_50' in json_file:
            if 'correct_answers' in quiz and quiz['correct_answers']:
                angle = quiz['correct_answers'][0]
                new_question = f"Measure the angle shown on the protractor. The angle measures {angle}°.\nAngle = ___°"
                quiz['question_text'] = new_question
                modified = True
        
        # For Gr6_52_E1 - trapezoid cutting
        elif 'Gr6_52_E1' in json_file:
            new_question = "Maggie cuts a trapezoid (top: 8 cm, bottom: 12 cm, height: 6 cm) along a vertical dashed line through the middle. Which two shapes does she make?"
            quiz['question_text'] = new_question
            modified = True
    
    if modified:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated {json_file}")
    
    return modified

def create_enhanced_polygon_html(quiz, exercise_tag):
    """Create HTML with polygon showing all angle values clearly"""
    backend_desc = quiz.get('backend_description', '')
    question_text = quiz.get('question_text', '')
    question_num = quiz['question_number']
    
    # Extract angles from backend description
    angle_pattern = r'(\d+)°'
    angles = re.findall(angle_pattern, backend_desc)
    angles = [int(a) for a in angles]
    
    # Find variable name
    var_match = re.search(r'variable\s+(\w+)', backend_desc)
    variable = var_match.group(1) if var_match else 'x'
    
    # Determine polygon type and number of sides
    polygon_info = {
        'triangle': 3,
        'quadrilateral': 4,
        'pentagon': 5,
        'hexagon': 6,
        'heptagon': 7,
        'octagon': 8,
        'nonagon': 9,
        'decagon': 10,
        'dodecagon': 12
    }
    
    sides = 4  # default
    shape_name = 'polygon'
    
    for key, num_sides in polygon_info.items():
        if key in backend_desc.lower():
            sides = num_sides
            shape_name = key
            break
    
    # For Gr6_51_E2 - exterior angles (always 360)
    if 'exterior' in question_text.lower():
        # Create a simple polygon with exterior angle visualization
        cx, cy = 200, 150
        radius = 80
        points = []
        for i in range(sides):
            angle = -90 + (360 / sides) * i
            x = cx + radius * math.cos(math.radians(angle))
            y = cy + radius * math.sin(math.radians(angle))
            points.append((x, y))
        
        points_str = ' '.join(f'{x:.0f},{y:.0f}' for x, y in points)
        
        # Add exterior angle arcs
        exterior_arcs = ''
        for i in range(sides):
            curr = points[i]
            next_pt = points[(i + 1) % sides]
            prev = points[(i - 1) % sides]
            
            # Draw small arc to show exterior angle
            arc_cx = curr[0]
            arc_cy = curr[1]
            exterior_arcs += f'''
            <path d="M {arc_cx-10:.0f} {arc_cy:.0f} A 15 15 0 0 1 {arc_cx:.0f} {arc_cy-10:.0f}" 
                  fill="none" stroke="red" stroke-width="1.5" opacity="0.7"/>'''
        
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
        .info {{
            font-size: 14px;
            color: #666;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="question">What is the sum of the exterior angle measures of this {shape_name}?</div>
    
    <div class="polygon-container">
        <svg width="400" height="300" viewBox="0 0 400 300">
            <!-- {shape_name.capitalize()} -->
            <polygon points="{points_str}" fill="lightblue" fill-opacity="0.3" stroke="black" stroke-width="2"/>
            
            <!-- Exterior angle indicators -->
            {exterior_arcs}
            
            <!-- Label -->
            <text x="200" y="250" font-size="16" text-anchor="middle" font-weight="bold">
                Sum of exterior angles = 360°
            </text>
        </svg>
    </div>
    
    <div class="info">
        For any convex polygon, the sum of exterior angles is always 360°
    </div>
</body>
</html>"""
    
    # For Gr6_51_E1, E3, E4 - interior angles with specific values
    else:
        # Create polygon with labeled angles
        cx, cy = 200, 150
        radius = 100
        points = []
        for i in range(sides):
            angle = -90 + (360 / sides) * i
            x = cx + radius * math.cos(math.radians(angle))
            y = cy + radius * math.sin(math.radians(angle))
            points.append((x, y))
        
        points_str = ' '.join(f'{x:.0f},{y:.0f}' for x, y in points)
        
        # Create angle labels
        angle_labels = ''
        for i in range(sides):
            # Position labels inside the polygon
            x, y = points[i]
            label_x = cx + (x - cx) * 0.7
            label_y = cy + (y - cy) * 0.7
            
            if i < len(angles):
                # Known angle
                angle_labels += f'''
                <circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="black"/>
                <text x="{label_x:.0f}" y="{label_y:.0f}" font-size="14" text-anchor="middle" fill="black">
                    {angles[i]}°
                </text>'''
            else:
                # Unknown angle
                angle_labels += f'''
                <circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="red"/>
                <text x="{label_x:.0f}" y="{label_y:.0f}" font-size="16" text-anchor="middle" fill="red" font-weight="bold">
                    {variable}
                </text>'''
        
        # Clean up question text
        clean_question = question_text.replace('___', '').replace('_', '').strip()
        
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
        .given-angles {{
            font-size: 14px;
            margin-top: 15px;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="question">{clean_question}</div>
    
    <div class="polygon-container">
        <svg width="400" height="300" viewBox="0 0 400 300">
            <!-- {shape_name.capitalize()} with {sides} sides -->
            <polygon points="{points_str}" fill="lightyellow" fill-opacity="0.3" stroke="black" stroke-width="2"/>
            
            <!-- Angle labels and vertices -->
            {angle_labels}
        </svg>
    </div>
    
    <div class="given-angles">
        Given angles: {', '.join(str(a) + '°' for a in angles)}
    </div>
</body>
</html>"""
    
    return html

def create_enhanced_protractor_html(quiz, exercise_tag):
    """Create HTML with protractor showing specific angle measurement"""
    angle_value = float(quiz['correct_answers'][0]) if quiz.get('correct_answers') else 45
    question_num = quiz['question_number']
    
    # Calculate angle ray endpoint
    angle_rad = angle_value * math.pi / 180
    x2 = 200 + 140 * math.cos(angle_rad)
    y2 = 200 - 140 * math.sin(angle_rad)
    
    # Calculate arc
    arc_x = 200 + 60 * math.cos(angle_rad)
    arc_y = 200 - 60 * math.sin(angle_rad)
    
    large_arc = "1" if angle_value > 90 else "0"
    
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
    <div class="question">What is the measurement of the angle shown on the protractor?</div>
    
    <div class="protractor-container">
        <svg width="400" height="250" viewBox="0 0 400 250">
            <!-- Protractor background -->
            <path d="M 60 200 A 140 140 0 0 1 340 200 Z" fill="#f9f9f9" stroke="black" stroke-width="2"/>
            
            <!-- Degree markings -->"""
    
    # Add detailed degree markings
    for deg in range(0, 181, 5):
        angle_rad_mark = deg * math.pi / 180
        
        # Outer marks
        x1 = 200 + 140 * math.cos(angle_rad_mark)
        y1 = 200 - 140 * math.sin(angle_rad_mark)
        
        if deg % 10 == 0:
            # Longer marks every 10 degrees
            x2_mark = 200 + 130 * math.cos(angle_rad_mark)
            y2_mark = 200 - 130 * math.sin(angle_rad_mark)
            stroke_width = "1.5"
        else:
            # Shorter marks every 5 degrees
            x2_mark = 200 + 135 * math.cos(angle_rad_mark)
            y2_mark = 200 - 135 * math.sin(angle_rad_mark)
            stroke_width = "0.5"
        
        html += f'\n            <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2_mark:.0f}" y2="{y2_mark:.0f}" stroke="black" stroke-width="{stroke_width}"/>'
        
        # Add text labels for major angles
        if deg % 30 == 0:
            text_x = 200 + 155 * math.cos(angle_rad_mark)
            text_y = 200 - 155 * math.sin(angle_rad_mark) + 4
            html += f'\n            <text x="{text_x:.0f}" y="{text_y:.0f}" font-size="11" text-anchor="middle">{deg}°</text>'
    
    html += f"""
            
            <!-- Center point -->
            <circle cx="200" cy="200" r="4" fill="black"/>
            
            <!-- Base ray -->
            <line x1="200" y1="200" x2="340" y2="200" stroke="blue" stroke-width="3"/>
            
            <!-- Angle ray -->
            <line x1="200" y1="200" x2="{x2:.0f}" y2="{y2:.0f}" stroke="blue" stroke-width="3"/>
            
            <!-- Angle arc -->
            <path d="M 260 200 A 60 60 0 {large_arc} 0 {arc_x:.0f} {arc_y:.0f}" 
                  fill="none" stroke="red" stroke-width="2.5"/>
            
            <!-- Angle measurement display -->
            <rect x="160" y="220" width="80" height="25" fill="white" stroke="black" stroke-width="1" rx="3"/>
            <text x="200" y="237" font-size="16" font-weight="bold" text-anchor="middle">{angle_value:.0f}°</text>
        </svg>
    </div>
</body>
</html>"""
    
    return html

def create_enhanced_trapezoid_html(quiz, exercise_tag):
    """Create HTML with trapezoid and clear options"""
    question_num = quiz['question_number']
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .trapezoid-container {{
            margin: 30px 0;
            text-align: center;
        }}
        .options {{
            margin: 30px 0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .option {{
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .option:hover {{
            background-color: #f0f8ff;
            border-color: #4CAF50;
            transform: scale(1.02);
        }}
        .option-label {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="question">Maggie cuts a trapezoid along the vertical dashed line through the middle. Which two shapes does she make?</div>
    
    <div class="trapezoid-container">
        <svg width="500" height="250" viewBox="0 0 500 250">
            <!-- Trapezoid -->
            <polygon points="150,70 350,70 380,180 120,180" fill="lightblue" stroke="black" stroke-width="2"/>
            
            <!-- Vertical cutting line -->
            <line x1="250" y1="70" x2="250" y2="180" stroke="red" stroke-width="2" stroke-dasharray="5,5"/>
            
            <!-- Dimensions -->
            <text x="250" y="60" font-size="12" text-anchor="middle">Top: 200</text>
            <text x="250" y="200" font-size="12" text-anchor="middle">Bottom: 260</text>
            <text x="100" y="125" font-size="12" text-anchor="middle">H: 110</text>
            
            <!-- Cut label -->
            <text x="260" y="125" font-size="11" fill="red">cut line</text>
            
            <!-- Arrows showing the cut -->
            <path d="M 235 100 L 245 100 M 240 95 L 240 105" stroke="red" stroke-width="1.5"/>
            <path d="M 255 100 L 265 100 M 260 95 L 260 105" stroke="red" stroke-width="1.5"/>
        </svg>
    </div>
    
    <div class="options">
        <div class="option">
            <div class="option-label">A) Two identical trapezoids</div>
            <svg width="200" height="100" viewBox="0 0 200 100">
                <polygon points="30,25 55,25 60,75 25,75" fill="#FFE4B5" stroke="black" stroke-width="1.5"/>
                <polygon points="90,25 115,25 120,75 85,75" fill="#FFE4B5" stroke="black" stroke-width="1.5"/>
                <text x="42" y="50" font-size="10" text-anchor="middle">Trap 1</text>
                <text x="102" y="50" font-size="10" text-anchor="middle">Trap 2</text>
            </svg>
        </div>
        
        <div class="option">
            <div class="option-label">B) Two triangles</div>
            <svg width="200" height="100" viewBox="0 0 200 100">
                <polygon points="40,25 70,25 55,75" fill="#90EE90" stroke="black" stroke-width="1.5"/>
                <polygon points="90,25 120,25 105,75" fill="#90EE90" stroke="black" stroke-width="1.5"/>
                <text x="55" y="50" font-size="10" text-anchor="middle">Tri 1</text>
                <text x="105" y="50" font-size="10" text-anchor="middle">Tri 2</text>
            </svg>
        </div>
        
        <div class="option">
            <div class="option-label">C) Rectangle and parallelogram</div>
            <svg width="200" height="100" viewBox="0 0 200 100">
                <rect x="25" y="25" width="40" height="50" fill="#FFFFE0" stroke="black" stroke-width="1.5"/>
                <polygon points="85,25 125,25 120,75 80,75" fill="#E6E6FA" stroke="black" stroke-width="1.5"/>
                <text x="45" y="50" font-size="10" text-anchor="middle">Rect</text>
                <text x="102" y="50" font-size="10" text-anchor="middle">Para</text>
            </svg>
        </div>
        
        <div class="option">
            <div class="option-label">D) Two pentagons</div>
            <svg width="200" height="100" viewBox="0 0 200 100">
                <polygon points="30,25 55,25 60,50 55,75 25,75" fill="#FFB6C1" stroke="black" stroke-width="1.5"/>
                <polygon points="90,25 115,25 120,50 115,75 85,75" fill="#FFB6C1" stroke="black" stroke-width="1.5"/>
                <text x="42" y="50" font-size="10" text-anchor="middle">Pent 1</text>
                <text x="102" y="50" font-size="10" text-anchor="middle">Pent 2</text>
            </svg>
        </div>
    </div>
</body>
</html>"""
    
    return html

def process_all_files():
    """Process all geometry files - update JSON and create HTML"""
    
    # First update all JSON files
    json_files = [
        'Gr6_50_E1_variations.json',
        'Gr6_50_E2_variations.json', 
        'Gr6_51_E1_variations.json',
        'Gr6_51_E2_variations.json',
        'Gr6_51_E3_variations.json',
        'Gr6_51_E4_variations.json',
        'Gr6_52_E1_variations.json'
    ]
    
    print("Updating JSON files...")
    for json_file in json_files:
        update_json_with_angles(json_file)
    
    print("\nCreating enhanced HTML files...")
    
    # Create HTML directory if needed
    if not os.path.exists('HTML'):
        os.makedirs('HTML')
    
    # Process protractor exercises (Gr6_50_E1, E2)
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
                html = create_enhanced_protractor_html(quiz, exercise_tag)
                filepath = f"HTML/{exercise_tag}_{quiz['question_number']}.html"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1
            except Exception as e:
                print(f"Error: {e}")
        
        print(f"  Created {count} HTML files")
    
    # Process polygon exercises (Gr6_51_E1-E4)
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
                html = create_enhanced_polygon_html(quiz, exercise_tag)
                filepath = f"HTML/{exercise_tag}_{quiz['question_number']}.html"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1
            except Exception as e:
                print(f"Error: {e}")
        
        print(f"  Created {count} HTML files")
    
    # Process trapezoid exercise (Gr6_52_E1)
    if os.path.exists('Gr6_52_E1_variations.json'):
        print("Processing Gr6_52_E1_variations.json...")
        with open('Gr6_52_E1_variations.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for quiz in data['quizzes']:
            try:
                html = create_enhanced_trapezoid_html(quiz, 'Gr6_52_E1')
                filepath = f"HTML/Gr6_52_E1_{quiz['question_number']}.html"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1
            except Exception as e:
                print(f"Error: {e}")
        
        print(f"  Created {count} HTML files")

if __name__ == "__main__":
    process_all_files()