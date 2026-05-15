import json
import os
import re
from pathlib import Path

def fix_latex_formatting(text):
    """Fix LaTeX expressions to ensure all $ symbols are properly closed."""
    if not text:
        return text
    
    # Pattern to find unclosed LaTeX expressions
    # Look for $ followed by LaTeX content but missing closing $
    pattern = r'\$([^$]+?)(?=[^\w\\]|$)(?!\$)'
    
    def check_and_fix(match):
        content = match.group(1)
        # Check if this looks like it should be closed
        if any(c in content for c in ['\\frac', '\\times', '\\div', '\\cdot', '\\sqrt', '^', '_']):
            return f'${content}$'
        return match.group(0)
    
    # Fix unclosed LaTeX
    text = re.sub(pattern, check_and_fix, text)
    
    # Also fix cases where $ is at the start but no closing $ before text continues
    text = re.sub(r'\$\\frac\{(\d+)\}\{(\d+)\}(?!\$)', r'$\\frac{\1}{\2}$', text)
    text = re.sub(r'\$([\d\\.]+)(?!\$)', r'$\1$', text)
    
    return text

def get_image_info_from_question(question):
    """Extract all image information from a question."""
    images = []
    
    # Check for main image_tag
    if 'image_tag' in question and question.get('backend_description'):
        images.append({
            'tag': question['image_tag'],
            'description': question['backend_description'],
            'type': 'main'
        })
    
    # Check for solution_image_tag
    if 'solution_image_tag' in question and question['solution_image_tag']:
        for item in question['solution_image_tag']:
            if isinstance(item, list) and len(item) >= 3:
                images.append({
                    'tag': item[1],  # Second element is the tag
                    'description': item[2],  # Third element is the description
                    'type': 'solution'
                })
    
    # Check for image_choice_tags
    if 'image_choice_tags' in question and question.get('image_choice_tags_backend_description'):
        tags = question['image_choice_tags']
        descriptions = question['image_choice_tags_backend_description']
        for i, tag in enumerate(tags):
            if i < len(descriptions):
                images.append({
                    'tag': tag,
                    'description': descriptions[i],
                    'type': 'choice'
                })
    
    # Check for shape_image_tags
    if 'shape_image_tags' in question and question['shape_image_tags']:
        for shape in question['shape_image_tags']:
            if isinstance(shape, dict) and 'tag' in shape and 'backend_description' in shape:
                images.append({
                    'tag': shape['tag'],
                    'description': shape['backend_description'],
                    'type': 'shape'
                })
    
    return images

def generate_html_content(question, images, week, exercise, question_num):
    """Generate HTML content for a question with visual components."""
    
    # Fix LaTeX in question text
    question_text = fix_latex_formatting(question.get('question_text', ''))
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gr6_{week}_E{exercise}_{question_num}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f0f0f0;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .question {{
            margin-bottom: 20px;
            font-size: 18px;
            color: #333;
        }}
        .visual-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
            justify-content: center;
        }}
        .item {{
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            background-color: #fafafa;
            display: inline-block;
        }}
        svg {{
            display: block;
        }}
        .number-line {{
            width: 600px;
            height: 120px;
        }}
        .fraction-model {{
            width: 200px;
            height: 200px;
        }}
        .place-value-chart {{
            width: 400px;
            height: 250px;
        }}
        .area-model {{
            width: 300px;
            height: 300px;
        }}
        .bar-model {{
            width: 500px;
            height: 150px;
        }}
        .data-table {{
            width: 400px;
            height: 300px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">
            <h2>Question {question_num}</h2>
            <p>{question_text}</p>
        </div>
        <div class="visual-container">
'''
    
    # Generate visual components based on descriptions
    for img in images:
        tag = img['tag']
        desc = img['description'].lower() if img['description'] else ''
        
        html += f'            <div class="item" label="{tag}">\n'
        
        # Determine what type of visual to create based on description
        if 'number line' in desc:
            html += generate_number_line(desc)
        elif 'fraction' in desc and ('circle' in desc or 'pie' in desc or 'circular' in desc):
            html += generate_fraction_circle(desc)
        elif 'fraction' in desc and ('rectangle' in desc or 'bar' in desc):
            html += generate_fraction_bar(desc)
        elif 'place value' in desc or 'chart' in desc:
            html += generate_place_value_chart(desc)
        elif 'area model' in desc or 'multiplication' in desc:
            html += generate_area_model(desc)
        elif 'table' in desc or 'data' in desc:
            html += generate_data_table(desc)
        elif 'shape' in desc or 'polygon' in desc or 'triangle' in desc or 'square' in desc:
            html += generate_shape(desc)
        else:
            # Default visual
            html += generate_default_visual(desc)
        
        html += '            </div>\n'
    
    html += '''        </div>
    </div>
</body>
</html>'''
    
    return html

def generate_number_line(description):
    """Generate a number line SVG based on description."""
    # Extract range and marks from description
    start = 0
    end = 10
    marks = 11
    
    # Try to extract numbers from description
    numbers = re.findall(r'\d+', description)
    if len(numbers) >= 2:
        start = int(numbers[0])
        end = int(numbers[1])
        marks = min(end - start + 1, 21)  # Limit marks for readability
    
    svg = f'''                <svg class="number-line" viewBox="0 0 600 120">
                    <!-- Main line -->
                    <line x1="50" y1="60" x2="550" y2="60" stroke="black" stroke-width="2"/>
                    
                    <!-- Arrow heads -->
                    <path d="M 45 60 L 50 55 L 50 65 Z" fill="black"/>
                    <path d="M 555 60 L 550 55 L 550 65 Z" fill="black"/>
                    
                    <!-- Tick marks and labels -->'''
    
    for i in range(marks):
        x = 50 + (500 / (marks - 1)) * i
        value = start + (end - start) * i / (marks - 1)
        
        svg += f'''
                    <line x1="{x}" y1="55" x2="{x}" y2="65" stroke="black" stroke-width="1.5"/>
                    <text x="{x}" y="85" text-anchor="middle" font-size="14">{value:.0f}</text>'''
    
    svg += '''
                </svg>
'''
    return svg

def generate_fraction_circle(description):
    """Generate a circular fraction model."""
    # Default to showing quarters
    parts = 4
    shaded = 1
    
    # Try to extract fraction from description
    frac_match = re.search(r'(\d+)[/\\](\d+)', description)
    if frac_match:
        shaded = int(frac_match.group(1))
        parts = int(frac_match.group(2))
    
    svg = '''                <svg class="fraction-model" viewBox="0 0 200 200">
                    <circle cx="100" cy="100" r="80" fill="none" stroke="black" stroke-width="2"/>'''
    
    angle_per_part = 360 / parts
    for i in range(parts):
        start_angle = i * angle_per_part - 90
        end_angle = start_angle + angle_per_part
        
        # Convert to radians
        start_rad = start_angle * 3.14159 / 180
        end_rad = end_angle * 3.14159 / 180
        
        # Calculate arc points
        x1 = 100 + 80 * round(100 * (start_rad).cos()) / 100
        y1 = 100 + 80 * round(100 * (start_rad).sin()) / 100
        x2 = 100 + 80 * round(100 * (end_rad).cos()) / 100
        y2 = 100 + 80 * round(100 * (end_rad).sin()) / 100
        
        fill_color = '#4CAF50' if i < shaded else 'white'
        
        # Use a simplified arc path
        svg += f'''
                    <path d="M 100 100 L {100 + 80 * ((start_angle * 3.14159 / 180).__round__(2).__cos__().__round__(2)} {100 + 80 * ((start_angle * 3.14159 / 180).__round__(2).__sin__().__round__(2)} A 80 80 0 0 1 {100 + 80 * ((end_angle * 3.14159 / 180).__round__(2).__cos__().__round__(2)} {100 + 80 * ((end_angle * 3.14159 / 180).__round__(2).__sin__().__round__(2)} Z" 
                          fill="{fill_color}" stroke="black" stroke-width="1"/>'''
    
    svg += '''
                </svg>
'''
    return svg

def generate_fraction_bar(description):
    """Generate a rectangular fraction bar model."""
    # Default to showing thirds
    parts = 3
    shaded = 1
    
    # Try to extract fraction from description
    frac_match = re.search(r'(\d+)[/\\](\d+)', description)
    if frac_match:
        shaded = int(frac_match.group(1))
        parts = int(frac_match.group(2))
    
    svg = '''                <svg class="fraction-model" viewBox="0 0 300 100">'''
    
    width_per_part = 240 / parts
    for i in range(parts):
        x = 30 + i * width_per_part
        fill_color = '#4CAF50' if i < shaded else 'white'
        
        svg += f'''
                    <rect x="{x}" y="30" width="{width_per_part}" height="40" 
                          fill="{fill_color}" stroke="black" stroke-width="1.5"/>'''
    
    svg += '''
                </svg>
'''
    return svg

def generate_place_value_chart(description):
    """Generate a place value chart."""
    svg = '''                <svg class="place-value-chart" viewBox="0 0 400 250">
                    <!-- Header row -->
                    <rect x="20" y="20" width="90" height="40" fill="#e3f2fd" stroke="black" stroke-width="1"/>
                    <text x="65" y="45" text-anchor="middle" font-size="14" font-weight="bold">Hundreds</text>
                    
                    <rect x="110" y="20" width="90" height="40" fill="#e3f2fd" stroke="black" stroke-width="1"/>
                    <text x="155" y="45" text-anchor="middle" font-size="14" font-weight="bold">Tens</text>
                    
                    <rect x="200" y="20" width="90" height="40" fill="#e3f2fd" stroke="black" stroke-width="1"/>
                    <text x="245" y="45" text-anchor="middle" font-size="14" font-weight="bold">Ones</text>
                    
                    <rect x="290" y="20" width="90" height="40" fill="#e3f2fd" stroke="black" stroke-width="1"/>
                    <text x="335" y="45" text-anchor="middle" font-size="14" font-weight="bold">Tenths</text>
                    
                    <!-- Value row -->
                    <rect x="20" y="60" width="90" height="40" fill="white" stroke="black" stroke-width="1"/>
                    <rect x="110" y="60" width="90" height="40" fill="white" stroke="black" stroke-width="1"/>
                    <rect x="200" y="60" width="90" height="40" fill="white" stroke="black" stroke-width="1"/>
                    <rect x="290" y="60" width="90" height="40" fill="white" stroke="black" stroke-width="1"/>
                </svg>
'''
    return svg

def generate_area_model(description):
    """Generate an area model for multiplication."""
    svg = '''                <svg class="area-model" viewBox="0 0 300 300">
                    <!-- Main rectangle -->
                    <rect x="50" y="50" width="200" height="200" fill="#fff3e0" stroke="black" stroke-width="2"/>
                    
                    <!-- Horizontal division -->
                    <line x1="50" y1="150" x2="250" y2="150" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
                    
                    <!-- Vertical division -->
                    <line x1="150" y1="50" x2="150" y2="250" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
                    
                    <!-- Labels -->
                    <text x="100" y="35" text-anchor="middle" font-size="16">10</text>
                    <text x="200" y="35" text-anchor="middle" font-size="16">5</text>
                    <text x="30" y="100" text-anchor="middle" font-size="16">20</text>
                    <text x="30" y="200" text-anchor="middle" font-size="16">3</text>
                </svg>
'''
    return svg

def generate_data_table(description):
    """Generate a data table."""
    svg = '''                <svg class="data-table" viewBox="0 0 400 300">
                    <!-- Table structure -->
                    <rect x="50" y="30" width="300" height="240" fill="white" stroke="black" stroke-width="2"/>
                    
                    <!-- Header row -->
                    <rect x="50" y="30" width="300" height="40" fill="#f5f5f5" stroke="black" stroke-width="1"/>
                    
                    <!-- Column dividers -->
                    <line x1="200" y1="30" x2="200" y2="270" stroke="black" stroke-width="1"/>
                    
                    <!-- Row dividers -->
                    <line x1="50" y1="70" x2="350" y2="70" stroke="black" stroke-width="1"/>
                    <line x1="50" y1="120" x2="350" y2="120" stroke="black" stroke-width="1"/>
                    <line x1="50" y1="170" x2="350" y2="170" stroke="black" stroke-width="1"/>
                    <line x1="50" y1="220" x2="350" y2="220" stroke="black" stroke-width="1"/>
                    
                    <!-- Sample headers -->
                    <text x="125" y="55" text-anchor="middle" font-size="14" font-weight="bold">Category</text>
                    <text x="275" y="55" text-anchor="middle" font-size="14" font-weight="bold">Value</text>
                </svg>
'''
    return svg

def generate_shape(description):
    """Generate a geometric shape."""
    if 'triangle' in description:
        svg = '''                <svg class="fraction-model" viewBox="0 0 200 200">
                    <polygon points="100,30 170,150 30,150" fill="#ffeb3b" stroke="black" stroke-width="2"/>
                </svg>
'''
    elif 'square' in description:
        svg = '''                <svg class="fraction-model" viewBox="0 0 200 200">
                    <rect x="50" y="50" width="100" height="100" fill="#ff9800" stroke="black" stroke-width="2"/>
                </svg>
'''
    elif 'hexagon' in description:
        svg = '''                <svg class="fraction-model" viewBox="0 0 200 200">
                    <polygon points="100,30 150,60 150,120 100,150 50,120 50,60" fill="#9c27b0" stroke="black" stroke-width="2"/>
                </svg>
'''
    else:
        # Default pentagon
        svg = '''                <svg class="fraction-model" viewBox="0 0 200 200">
                    <polygon points="100,30 160,80 140,140 60,140 40,80" fill="#2196f3" stroke="black" stroke-width="2"/>
                </svg>
'''
    return svg

def generate_default_visual(description):
    """Generate a default visual element."""
    svg = '''                <svg class="fraction-model" viewBox="0 0 200 200">
                    <rect x="20" y="20" width="160" height="160" rx="10" fill="#e8eaf6" stroke="#3f51b5" stroke-width="2"/>
                    <text x="100" y="100" text-anchor="middle" font-size="16" fill="#3f51b5">Visual Component</text>
                </svg>
'''
    return svg

def process_json_file(json_path):
    """Process a JSON file and generate HTML files for questions with visuals."""
    
    # Extract week and exercise from filename
    filename = os.path.basename(json_path)
    match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', filename)
    if not match:
        print(f"Skipping {filename} - doesn't match expected pattern")
        return 0
    
    week = match.group(1)
    exercise = match.group(2)
    
    # Read JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_path}: {e}")
        return 0
    
    # Create html directory if it doesn't exist
    os.makedirs('html', exist_ok=True)
    
    html_count = 0
    
    # Process each question
    for question_key, question_data in data.items():
        if not isinstance(question_data, dict):
            continue
            
        # Get image information
        images = get_image_info_from_question(question_data)
        
        # Only generate HTML if there are images
        if images:
            # Extract question number (e.g., "1_1" -> "1")
            question_num = question_key.replace('_', '')
            
            # Generate HTML filename
            html_filename = f"Gr6_{week}_E{exercise}_{question_num}.html"
            html_path = os.path.join('html', html_filename)
            
            # Generate and save HTML content
            html_content = generate_html_content(question_data, images, week, exercise, question_num)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            html_count += 1
    
    return html_count

def main():
    """Main function to process all Grade 6 JSON files."""
    
    # Target weeks and exercises
    target_weeks = {
        9: [1, 2, 3],
        10: [1, 2, 3],
        11: [1, 2, 3],
        12: [1, 2, 3],
        13: [1, 2, 3, 4],  # Check if E3 exists
        14: [1, 2, 3],
        15: [1, 2, 3, 4, 5],
        18: [1, 2, 3],
        19: [1, 2, 3],
        20: [1, 2, 3],
        21: [1, 2, 3]
    }
    
    # Also check all other weeks to ensure 51 variations
    all_json_files = list(Path('.').glob('Gr6_*_E*_variations.json'))
    
    total_generated = 0
    files_processed = []
    
    # Process all Grade 6 JSON files
    for json_file in all_json_files:
        count = process_json_file(json_file)
        if count > 0:
            total_generated += count
            files_processed.append(str(json_file))
            print(f"Generated {count} HTML files for {json_file.name}")
    
    print(f"\nTotal HTML files generated: {total_generated}")
    print(f"JSON files processed: {len(files_processed)}")
    
    # Check which target files are missing
    print("\n=== Checking target weeks ===")
    for week, exercises in target_weeks.items():
        for exercise in exercises:
            json_filename = f"Gr6_{week}_E{exercise}_variations.json"
            json_path = Path(json_filename)
            if json_path.exists():
                print(f"✓ {json_filename} exists")
            else:
                print(f"✗ {json_filename} NOT FOUND")
    
    # List all HTML files created
    html_files = list(Path('html').glob('*.html'))
    print(f"\n=== HTML files in html/ folder: {len(html_files)} ===")
    
    # Group by week and exercise to check coverage
    coverage = {}
    for html_file in html_files:
        match = re.match(r'Gr6_(\d+)_E(\d+)_(\d+)\.html', html_file.name)
        if match:
            week = int(match.group(1))
            exercise = int(match.group(2))
            key = f"Week {week} Exercise {exercise}"
            if key not in coverage:
                coverage[key] = 0
            coverage[key] += 1
    
    print("\n=== Coverage Report ===")
    for key in sorted(coverage.keys()):
        count = coverage[key]
        status = "✓ COMPLETE" if count >= 51 else f"⚠ INCOMPLETE ({count}/51)"
        print(f"{key}: {count} variations {status}")

if __name__ == "__main__":
    main()