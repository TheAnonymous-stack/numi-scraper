import json
import os
import re
import math

def extract_angle_from_solution(quiz):
    """Extract angle value from the correct answer or solution"""
    if 'correct_answers' in quiz and quiz['correct_answers']:
        return float(quiz['correct_answers'][0])
    return 45  # default

def create_protractor_html(quiz, exercise_tag):
    """Create HTML with protractor visualization for angle measurement"""
    angle_value = extract_angle_from_solution(quiz)
    
    # Calculate angle ray endpoint
    angle_rad = angle_value * math.pi / 180
    x2 = 200 + 150 * math.cos(angle_rad)
    y2 = 200 - 150 * math.sin(angle_rad)
    
    # Calculate arc endpoint  
    arc_x = 200 + 50 * math.cos(angle_rad)
    arc_y = 200 - 50 * math.sin(angle_rad)
    
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
            <!-- Protractor semicircle -->
            <path d="M 50 200 A 150 150 0 0 1 350 200" fill="none" stroke="black" stroke-width="2"/>
            
            <!-- Degree markings -->
            <g id="degree-marks">
                <!-- 0 degrees -->
                <line x1="350" y1="200" x2="340" y2="200" stroke="black" stroke-width="1"/>
                <text x="355" y="205" font-size="12">0°</text>
                
                <!-- 30 degrees -->
                <line x1="325" y1="113" x2="318" y2="107" stroke="black" stroke-width="1"/>
                <text x="328" y="105" font-size="12">30°</text>
                
                <!-- 60 degrees -->
                <line x1="250" y1="70" x2="250" y2="60" stroke="black" stroke-width="1"/>
                <text x="245" y="55" font-size="12">60°</text>
                
                <!-- 90 degrees -->
                <line x1="200" y1="50" x2="200" y2="40" stroke="black" stroke-width="1"/>
                <text x="190" y="35" font-size="12">90°</text>
                
                <!-- 120 degrees -->
                <line x1="150" y1="70" x2="150" y2="60" stroke="black" stroke-width="1"/>
                <text x="140" y="55" font-size="12">120°</text>
                
                <!-- 150 degrees -->
                <line x1="75" y1="113" x2="82" y2="107" stroke="black" stroke-width="1"/>
                <text x="55" y="105" font-size="12">150°</text>
                
                <!-- 180 degrees -->
                <line x1="50" y1="200" x2="60" y2="200" stroke="black" stroke-width="1"/>
                <text x="20" y="205" font-size="12">180°</text>
            </g>
            
            <!-- Center point -->
            <circle cx="200" cy="200" r="3" fill="black"/>
            
            <!-- Angle rays -->
            <line x1="200" y1="200" x2="350" y2="200" stroke="blue" stroke-width="2"/>
            <line x1="200" y1="200" x2="{x2:.0f}" y2="{y2:.0f}" stroke="blue" stroke-width="2"/>
            
            <!-- Angle arc -->
            <path d="M 250 200 A 50 50 0 0 0 {arc_x:.0f} {arc_y:.0f}" fill="none" stroke="red" stroke-width="2"/>
        </svg>
    </div>
    
</body>
</html>"""
    
    return html

def create_polygon_html(quiz, exercise_tag):
    """Create HTML with polygon visualization for angle problems"""
    question_text = quiz.get('question_text', '')
    
    # Extract polygon type from question
    polygon_type = "polygon"
    if "triangle" in question_text.lower():
        polygon_type = "triangle"
    elif "quadrilateral" in question_text.lower() or "rectangle" in question_text.lower():
        polygon_type = "quadrilateral"
    elif "pentagon" in question_text.lower():
        polygon_type = "pentagon"
    elif "hexagon" in question_text.lower():
        polygon_type = "hexagon"
    
    # Extract any angle values mentioned
    angle_matches = re.findall(r'(\d+)°', question_text)
    given_angles = [int(a) for a in angle_matches] if angle_matches else []
    
    # Create appropriate polygon
    if polygon_type == "triangle":
        svg_content = """
            <!-- Triangle -->
            <polygon points="200,50 100,200 300,200" fill="none" stroke="black" stroke-width="2"/>
            <circle cx="200" cy="50" r="3" fill="red"/>
            <circle cx="100" cy="200" r="3" fill="red"/>
            <circle cx="300" cy="200" r="3" fill="red"/>
            <text x="190" y="40" font-size="14">A</text>
            <text x="85" y="205" font-size="14">B</text>
            <text x="305" y="205" font-size="14">C</text>"""
        if given_angles:
            if len(given_angles) >= 1:
                svg_content += f'<text x="180" y="70" font-size="12">{given_angles[0]}°</text>'
            if len(given_angles) >= 2:
                svg_content += f'<text x="110" y="185" font-size="12">{given_angles[1]}°</text>'
    elif polygon_type == "quadrilateral":
        svg_content = """
            <!-- Quadrilateral -->
            <polygon points="150,80 280,80 300,180 120,180" fill="none" stroke="black" stroke-width="2"/>
            <circle cx="150" cy="80" r="3" fill="red"/>
            <circle cx="280" cy="80" r="3" fill="red"/>
            <circle cx="300" cy="180" r="3" fill="red"/>
            <circle cx="120" cy="180" r="3" fill="red"/>
            <text x="140" y="70" font-size="14">A</text>
            <text x="285" y="70" font-size="14">B</text>
            <text x="305" y="185" font-size="14">C</text>
            <text x="105" y="185" font-size="14">D</text>"""
        if given_angles:
            if len(given_angles) >= 1:
                svg_content += f'<text x="155" y="95" font-size="12">{given_angles[0]}°</text>'
            if len(given_angles) >= 2:
                svg_content += f'<text x="260" y="95" font-size="12">{given_angles[1]}°</text>'
            if len(given_angles) >= 3:
                svg_content += f'<text x="280" y="170" font-size="12">{given_angles[2]}°</text>'
    elif polygon_type == "pentagon":
        svg_content = """
            <!-- Pentagon -->
            <polygon points="200,60 280,120 250,200 150,200 120,120" fill="none" stroke="black" stroke-width="2"/>
            <circle cx="200" cy="60" r="3" fill="red"/>
            <circle cx="280" cy="120" r="3" fill="red"/>
            <circle cx="250" cy="200" r="3" fill="red"/>
            <circle cx="150" cy="200" r="3" fill="red"/>
            <circle cx="120" cy="120" r="3" fill="red"/>"""
    else:  # hexagon
        svg_content = """
            <!-- Hexagon -->
            <polygon points="200,60 260,90 260,150 200,180 140,150 140,90" fill="none" stroke="black" stroke-width="2"/>
            <circle cx="200" cy="60" r="3" fill="red"/>
            <circle cx="260" cy="90" r="3" fill="red"/>
            <circle cx="260" cy="150" r="3" fill="red"/>
            <circle cx="200" cy="180" r="3" fill="red"/>
            <circle cx="140" cy="150" r="3" fill="red"/>
            <circle cx="140" cy="90" r="3" fill="red"/>"""
    
    question_num = quiz['question_number']
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
    </style>
</head>
<body>
    <div class="question">{clean_question}</div>
    
    <div class="polygon-container">
        <svg width="400" height="250" viewBox="0 0 400 250">
            {svg_content}
        </svg>
    </div>
    
</body>
</html>"""
    
    return html

def create_trapezoid_html(quiz, exercise_tag):
    """Create HTML with trapezoid and option images for Gr6_52_E1"""
    question_num = quiz['question_number']
    
    # Main question HTML
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
        }}
        .option {{
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
        }}
        .option:hover {{
            background-color: #f0f0f0;
        }}
        .option input {{
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="question">Maggie cuts the trapezoid along the dashed line. Which two shapes does she make?</div>
    
    <div class="trapezoid-container">
        <svg width="400" height="200" viewBox="0 0 400 200">
            <!-- Trapezoid -->
            <polygon points="100,50 300,50 320,150 80,150" fill="lightblue" stroke="black" stroke-width="2"/>
            <!-- Dashed cutting line -->
            <line x1="200" y1="50" x2="200" y2="150" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
        </svg>
    </div>
    
    <div class="options">
        <div class="option">
            <input type="radio" name="answer" value="A">
            <label>A) <img src="{exercise_tag}_{question_num}_A.html" alt="Option A" style="height: 50px;"></label>
        </div>
        <div class="option">
            <input type="radio" name="answer" value="B">
            <label>B) <img src="{exercise_tag}_{question_num}_B.html" alt="Option B" style="height: 50px;"></label>
        </div>
        <div class="option">
            <input type="radio" name="answer" value="C">
            <label>C) <img src="{exercise_tag}_{question_num}_C.html" alt="Option C" style="height: 50px;"></label>
        </div>
        <div class="option">
            <input type="radio" name="answer" value="D">
            <label>D) <img src="{exercise_tag}_{question_num}_D.html" alt="Option D" style="height: 50px;"></label>
        </div>
    </div>
</body>
</html>"""
    
    # Option A HTML - Two triangles
    option_a_html = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:10px;">
    <svg width="150" height="60" viewBox="0 0 150 60">
        <polygon points="10,10 40,10 25,50" fill="lightgreen" stroke="black" stroke-width="1"/>
        <polygon points="60,10 90,10 75,50" fill="lightgreen" stroke="black" stroke-width="1"/>
    </svg>
</body>
</html>"""
    
    # Option B HTML - Two trapezoids
    option_b_html = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:10px;">
    <svg width="150" height="60" viewBox="0 0 150 60">
        <polygon points="10,10 35,10 40,50 5,50" fill="lightcoral" stroke="black" stroke-width="1"/>
        <polygon points="55,10 80,10 85,50 50,50" fill="lightcoral" stroke="black" stroke-width="1"/>
    </svg>
</body>
</html>"""
    
    # Option C HTML - Rectangle and triangle
    option_c_html = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:10px;">
    <svg width="150" height="60" viewBox="0 0 150 60">
        <rect x="10" y="10" width="30" height="40" fill="lightyellow" stroke="black" stroke-width="1"/>
        <polygon points="60,10 90,30 60,50" fill="lightblue" stroke="black" stroke-width="1"/>
    </svg>
</body>
</html>"""
    
    # Option D HTML - Two parallelograms
    option_d_html = """<!DOCTYPE html>
<html>
<body style="margin:0;padding:10px;">
    <svg width="150" height="60" viewBox="0 0 150 60">
        <polygon points="10,10 40,10 35,50 5,50" fill="lavender" stroke="black" stroke-width="1"/>
        <polygon points="55,10 85,10 80,50 50,50" fill="lavender" stroke="black" stroke-width="1"/>
    </svg>
</body>
</html>"""
    
    return [
        (html, f"HTML/{exercise_tag}_{question_num}.html"),
        (option_a_html, f"HTML/{exercise_tag}_{question_num}_A.html"),
        (option_b_html, f"HTML/{exercise_tag}_{question_num}_B.html"),
        (option_c_html, f"HTML/{exercise_tag}_{question_num}_C.html"),
        (option_d_html, f"HTML/{exercise_tag}_{question_num}_D.html")
    ]

def process_geometry_exercises():
    """Process all geometry exercise JSON files and create HTML files"""
    exercises = [
        ('Gr6_50_E1_variations.json', 'Gr6_50_E1', 'protractor'),
        ('Gr6_50_E2_variations.json', 'Gr6_50_E2', 'protractor'),
        ('Gr6_51_E1_variations.json', 'Gr6_51_E1', 'polygon'),
        ('Gr6_51_E2_variations.json', 'Gr6_51_E2', 'polygon'),
        ('Gr6_51_E3_variations.json', 'Gr6_51_E3', 'polygon'),
        ('Gr6_51_E4_variations.json', 'Gr6_51_E4', 'polygon'),
        ('Gr6_52_E1_variations.json', 'Gr6_52_E1', 'trapezoid')
    ]
    
    total_created = 0
    
    for json_file, exercise_tag, viz_type in exercises:
        if not os.path.exists(json_file):
            print(f"File {json_file} not found, skipping...")
            continue
        
        print(f"Processing {json_file}...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for quiz in data['quizzes']:
            try:
                question_num = quiz['question_number']
                
                if viz_type == 'protractor':
                    html = create_protractor_html(quiz, exercise_tag)
                    filepath = f"HTML/{exercise_tag}_{question_num}.html"
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html)
                    count += 1
                    
                elif viz_type == 'polygon':
                    html = create_polygon_html(quiz, exercise_tag)
                    filepath = f"HTML/{exercise_tag}_{question_num}.html"
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html)
                    count += 1
                    
                elif viz_type == 'trapezoid':
                    html_files = create_trapezoid_html(quiz, exercise_tag)
                    for html_content, filepath in html_files:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                    count += len(html_files)
                
            except Exception as e:
                print(f"Error processing quiz {quiz.get('tag', 'unknown')}: {e}")
                continue
        
        print(f"Created {count} HTML files for {exercise_tag}")
        total_created += count
    
    print(f"\nTotal HTML files created: {total_created}")

if __name__ == "__main__":
    # Create HTML directory if it doesn't exist
    if not os.path.exists('HTML'):
        os.makedirs('HTML')
    
    process_geometry_exercises()