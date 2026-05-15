import json
import os
import re

def extract_angle_from_desc(desc):
    """Extract angle measurement from backend description"""
    match = re.search(r'(\d+)°', desc)
    if match:
        return int(match.group(1))
    return 45  # default

def create_protractor_html(quiz, exercise_tag):
    """Create HTML for protractor angle measurement (Gr6_50_E1, Gr6_50_E2)"""
    question_num = quiz['question_number']
    angle = quiz['correct_answers'][0] if quiz.get('correct_answers') else '45'
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Measure Angles</title>
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
            max-width: 600px;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 25px;
            color: #333;
        }}
        .protractor-container {{
            margin: 20px auto;
            position: relative;
            width: 400px;
            height: 250px;
        }}
        .answer-input {{
            width: 60px;
            padding: 8px;
            border: 2px solid #666;
            border-radius: 4px;
            font-size: 16px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">What is the measurement of this angle?</div>
        
        <div class="protractor-container">
            <svg width="400" height="250" viewBox="0 0 400 250">
                <!-- Protractor semicircle -->
                <path d="M 50 200 A 150 150 0 0 1 350 200 Z" 
                      fill="none" stroke="#333" stroke-width="2"/>
                
                <!-- Degree markings -->
                <g stroke="#666" stroke-width="0.5">"""
    
    # Add degree markings
    for i in range(0, 181, 10):
        angle_rad = i * 3.14159 / 180
        x1 = 200 - 140 * np.cos(angle_rad) if 'np' in dir() else 200 - 140
        y1 = 200 - 140 * np.sin(angle_rad) if 'np' in dir() else 200
        x2 = 200 - 150 * np.cos(angle_rad) if 'np' in dir() else 200 - 150
        y2 = 200 - 150 * np.sin(angle_rad) if 'np' in dir() else 200
        
        # Simplified calculation without numpy
        import math
        angle_rad = i * math.pi / 180
        x1 = 200 - 140 * math.cos(angle_rad)
        y1 = 200 - 140 * math.sin(angle_rad)
        x2 = 200 - 150 * math.cos(angle_rad)
        y2 = 200 - 150 * math.sin(angle_rad)
        
        html += f"""
                    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>"""
        
        if i % 30 == 0:
            # Add number labels for major angles
            label_x = 200 - 165 * math.cos(angle_rad)
            label_y = 200 - 165 * math.sin(angle_rad) + 5
            html += f"""
                    <text x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="middle" font-size="12">{i}</text>"""
    
    # Add the angle rays
    angle_value = float(angle)
    angle_rad = angle_value * math.pi / 180
    end_x = 200 + 180 * math.cos(angle_rad)
    end_y = 200 - 180 * math.sin(angle_rad)
    
    html += f"""
                </g>
                
                <!-- Center point -->
                <circle cx="200" cy="200" r="3" fill="#333"/>
                
                <!-- Base ray (0 degrees) -->
                <line x1="200" y1="200" x2="380" y2="200" 
                      stroke="#ff6b35" stroke-width="2"/>
                
                <!-- Angle ray -->
                <line x1="200" y1="200" x2="{end_x:.1f}" y2="{end_y:.1f}" 
                      stroke="#ff6b35" stroke-width="2"/>
                
                <!-- Angle arc -->
                <path d="M 250 200 A 50 50 0 0 0 {200 + 50*math.cos(angle_rad):.1f} {200 - 50*math.sin(angle_rad):.1f}"
                      fill="none" stroke="#4CAF50" stroke-width="2"/>
            </svg>
        </div>
        
        <div>
            <input type="text" class="answer-input" placeholder="?">°
        </div>
    </div>
</body>
</html>"""
    
    return html, f"HTML/{exercise_tag}_{question_num}.html"

def create_polygon_angle_html(quiz, exercise_tag):
    """Create HTML for polygon angle problems (Gr6_51_E1-E4)"""
    question_num = quiz['question_number']
    backend_desc = quiz.get('backend_description', '')
    
    # Extract polygon type and number of sides
    polygon_match = re.search(r'(\w+agon)', backend_desc.lower())
    polygon_type = polygon_match.group(1) if polygon_match else 'polygon'
    
    # Map polygon names to number of sides
    sides_map = {
        'pentagon': 5, 'hexagon': 6, 'heptagon': 7, 'octagon': 8,
        'nonagon': 9, 'decagon': 10, 'dodecagon': 12
    }
    sides = sides_map.get(polygon_type, 6)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Polygon Angles</title>
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
            max-width: 600px;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 25px;
            color: #333;
        }}
        .polygon-container {{
            margin: 25px auto;
        }}
        .angle-label {{
            font-size: 14px;
            fill: #333;
        }}
        .answer-input {{
            width: 60px;
            padding: 8px;
            border: 2px solid #666;
            border-radius: 4px;
            font-size: 16px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">What is n?</div>
        
        <div class="polygon-container">
            <svg width="400" height="400" viewBox="0 0 400 400">"""
    
    # Draw polygon
    import math
    cx, cy = 200, 200
    radius = 150
    points = []
    
    for i in range(sides):
        angle = (i * 2 * math.pi / sides) - math.pi/2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append(f"{x:.1f},{y:.1f}")
    
    html += f"""
                <!-- Polygon -->
                <polygon points="{' '.join(points)}" 
                         fill="none" stroke="#333" stroke-width="2"/>"""
    
    # Add angle labels (simplified - just show some angles and n)
    angles = ['120°', '135°', '110°', '125°', 'n', '140°', '130°'][:sides]
    for i, angle_label in enumerate(angles):
        angle = (i * 2 * math.pi / sides) - math.pi/2
        label_x = cx + (radius - 30) * math.cos(angle)
        label_y = cy + (radius - 30) * math.sin(angle)
        
        color = "#ff6b35" if angle_label == 'n' else "#333"
        html += f"""
                <text x="{label_x:.1f}" y="{label_y:.1f}" 
                      text-anchor="middle" class="angle-label"
                      fill="{color}" font-weight="{'bold' if angle_label == 'n' else 'normal'}">
                    {angle_label}
                </text>"""
    
    html += """
            </svg>
        </div>
        
        <div>
            n = <input type="text" class="answer-input" placeholder="?">°
        </div>
    </div>
</body>
</html>"""
    
    return html, f"HTML/{exercise_tag}_{question_num}.html"

def create_trapezoid_html(quiz, exercise_tag):
    """Create HTML for trapezoid problems (Gr6_52_E1)"""
    question_num = quiz['question_number']
    backend_desc = quiz.get('backend_description', '')
    
    # Extract dimensions
    top_match = re.search(r'top base measuring (\d+)', backend_desc)
    bottom_match = re.search(r'bottom base measuring (\d+)', backend_desc)
    height_match = re.search(r'height labeled as (\d+)', backend_desc)
    
    top = top_match.group(1) if top_match else '8'
    bottom = bottom_match.group(1) if bottom_match else '10'
    height = height_match.group(1) if height_match else '5'
    
    # Main question HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 - Trapezoid Area</title>
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
            max-width: 700px;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 25px;
            color: #333;
            line-height: 1.5;
        }}
        .trapezoid-container {{
            margin: 25px auto;
        }}
        .options {{
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
        }}
        .option {{
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .option:hover {{
            border-color: #4CAF50;
            background-color: #f0f8ff;
        }}
        .option-label {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">
            You can find the area of this trapezoid by cutting it into two triangles.<br>
            Which shows how to cut the trapezoid into two triangles?
        </div>
        
        <div class="trapezoid-container">
            <svg width="400" height="250" viewBox="0 0 400 250">
                <!-- Trapezoid -->
                <polygon points="150,50 250,50 300,150 100,150" 
                         fill="#4CAF50" fill-opacity="0.3" 
                         stroke="#333" stroke-width="2"/>
                
                <!-- Labels -->
                <text x="200" y="40" text-anchor="middle" font-size="14">{top} m</text>
                <text x="200" y="170" text-anchor="middle" font-size="14">{bottom} m</text>
                <text x="60" y="100" text-anchor="middle" font-size="14">{height} m</text>
                
                <!-- Height line -->
                <line x1="150" y1="50" x2="150" y2="150" 
                      stroke="#666" stroke-width="1" stroke-dasharray="3,3"/>
            </svg>
        </div>
        
        <div class="options">
            <div class="option">
                <div class="option-label">A</div>
                <img src="{exercise_tag}_{question_num}_A.html" alt="Option A" style="width: 150px;">
            </div>
            <div class="option">
                <div class="option-label">B</div>
                <img src="{exercise_tag}_{question_num}_B.html" alt="Option B" style="width: 150px;">
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # Create option images as separate HTML files
    option_a_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Option A</title>
</head>
<body style="margin: 0; padding: 10px; background: white;">
    <svg width="200" height="125" viewBox="0 0 200 125">
        <!-- Trapezoid with horizontal cut -->
        <polygon points="75,25 125,25 150,75 50,75" 
                 fill="#4CAF50" fill-opacity="0.3" 
                 stroke="#333" stroke-width="2"/>
        <!-- Horizontal line cutting trapezoid -->
        <line x1="60" y1="50" x2="140" y2="50" 
              stroke="white" stroke-width="3"/>
    </svg>
</body>
</html>"""
    
    option_b_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Option B</title>
</head>
<body style="margin: 0; padding: 10px; background: white;">
    <svg width="200" height="125" viewBox="0 0 200 125">
        <!-- Trapezoid with diagonal cut -->
        <polygon points="75,25 125,25 150,75 50,75" 
                 fill="#4CAF50" fill-opacity="0.3" 
                 stroke="#333" stroke-width="2"/>
        <!-- Diagonal line cutting trapezoid -->
        <line x1="75" y1="25" x2="150" y2="75" 
              stroke="white" stroke-width="3"/>
    </svg>
</body>
</html>"""
    
    return [
        (html, f"HTML/{exercise_tag}_{question_num}.html"),
        (option_a_html, f"HTML/{exercise_tag}_{question_num}_A.html"),
        (option_b_html, f"HTML/{exercise_tag}_{question_num}_B.html")
    ]

def process_exercise(json_file, create_func, exercise_tag):
    """Process a single exercise JSON file"""
    print(f"\nProcessing {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for quiz in data['quizzes']:
        result = create_func(quiz, exercise_tag)
        
        # Handle multiple files (for exercises with option images)
        if isinstance(result, list):
            for html_content, filename in result:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"Created {filename}")
        else:
            html_content, filename = result
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Created {filename}")
        
        count += 1
    
    print(f"Created files for {count} questions in {exercise_tag}")
    return count

def main():
    os.makedirs('HTML', exist_ok=True)
    
    # Define exercises and their corresponding creation functions
    exercises = [
        ('Gr6_50_E1_variations.json', create_protractor_html, 'Gr6_50_E1'),
        ('Gr6_50_E2_variations.json', create_protractor_html, 'Gr6_50_E2'),
        ('Gr6_51_E1_variations.json', create_polygon_angle_html, 'Gr6_51_E1'),
        ('Gr6_51_E2_variations.json', create_polygon_angle_html, 'Gr6_51_E2'),
        ('Gr6_51_E3_variations.json', create_polygon_angle_html, 'Gr6_51_E3'),
        ('Gr6_51_E4_variations.json', create_polygon_angle_html, 'Gr6_51_E4'),
        ('Gr6_52_E1_variations.json', create_trapezoid_html, 'Gr6_52_E1')
    ]
    
    total_count = 0
    for json_file, create_func, exercise_tag in exercises:
        if os.path.exists(json_file):
            count = process_exercise(json_file, create_func, exercise_tag)
            total_count += count
        else:
            print(f"Warning: {json_file} not found")
    
    print(f"\nTotal questions processed: {total_count}")

if __name__ == "__main__":
    import math
    main()