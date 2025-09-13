import json
import os
import glob
import math
from pathlib import Path

def has_visual_components(question_data):
    """Check if a question has any visual components"""
    # Check for image_tag with backend_description
    if 'image_tag' in question_data:
        if isinstance(question_data['image_tag'], dict):
            if question_data['image_tag'].get('backend_description'):
                return True
        elif isinstance(question_data['image_tag'], str) and question_data['image_tag']:
            return True
    
    # Check for solution_image_tag (non-empty list)
    if 'solution_image_tag' in question_data:
        if isinstance(question_data['solution_image_tag'], list) and len(question_data['solution_image_tag']) > 0:
            # Check if any item in the list has content
            for item in question_data['solution_image_tag']:
                if item and len(item) > 0:
                    return True
    
    # Check for image_choice_tags
    if 'image_choice_tags' in question_data:
        if isinstance(question_data['image_choice_tags'], list) and len(question_data['image_choice_tags']) > 0:
            return True
    
    # Check for shape_image_tags
    if 'shape_image_tags' in question_data:
        if isinstance(question_data['shape_image_tags'], list) and len(question_data['shape_image_tags']) > 0:
            return True
    
    return False

def extract_week_exercise(filename):
    """Extract week and exercise number from filename"""
    import re
    match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', os.path.basename(filename))
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def generate_html_for_image_tag(tag, description):
    """Generate HTML for a single image based on description"""
    html = f'<div class="item" label="{tag}" style="display: inline-block; padding: 20px; border: 1px solid #ccc; margin: 10px;">\n'
    
    # Parse description and generate appropriate visual
    desc_lower = description.lower()
    
    if 'number line' in desc_lower:
        html += generate_number_line(description)
    elif 'place value' in desc_lower or 'chart' in desc_lower:
        html += generate_place_value_chart(description)
    elif 'fraction' in desc_lower and ('circle' in desc_lower or 'pie' in desc_lower):
        html += generate_fraction_circle(description)
    elif 'fraction' in desc_lower and ('bar' in desc_lower or 'rectangle' in desc_lower):
        html += generate_fraction_bar(description)
    elif 'shape' in desc_lower or 'triangle' in desc_lower or 'square' in desc_lower:
        html += generate_shape(description)
    elif 'counter' in desc_lower or 'dot' in desc_lower:
        html += generate_counters(description)
    elif 'grid' in desc_lower or 'array' in desc_lower:
        html += generate_grid(description)
    elif 'table' in desc_lower:
        html += generate_table(description)
    elif 'model' in desc_lower or 'diagram' in desc_lower:
        html += generate_area_model(description)
    else:
        # Default visual representation - place value chart is common
        html += generate_place_value_chart(description)
    
    html += '</div>\n'
    return html

def generate_place_value_chart(description):
    """Generate a place value chart"""
    import re
    
    # Extract numbers from description
    numbers = re.findall(r'\d+(?:\.\d+)?', description)
    
    svg = '<svg width="500" height="150" viewBox="0 0 500 150">'
    
    # Draw the chart headers
    headers = ['Ten Thousands', 'Thousands', 'Hundreds', 'Tens', 'Ones']
    col_width = 90
    
    # Draw header row
    for i, header in enumerate(headers):
        x = 10 + i * col_width
        svg += f'''<rect x="{x}" y="10" width="{col_width-2}" height="30" fill="#E3F2FD" stroke="black" stroke-width="1"/>
                   <text x="{x + col_width/2}" y="30" text-anchor="middle" font-size="11">{header}</text>'''
    
    # If we have a number, display it in the chart
    if numbers:
        number_str = str(numbers[0]).replace('.', '')[:5]  # Take first 5 digits
        number_str = number_str.zfill(5)  # Pad with zeros if needed
        
        for i, digit in enumerate(number_str[-5:]):
            x = 10 + i * col_width
            svg += f'''<rect x="{x}" y="40" width="{col_width-2}" height="40" fill="white" stroke="black" stroke-width="1"/>
                       <text x="{x + col_width/2}" y="65" text-anchor="middle" font-size="20" font-weight="bold">{digit}</text>'''
    
    svg += '</svg>'
    return svg

def generate_number_line(description):
    """Generate a number line SVG"""
    import re
    
    # Extract range from description
    numbers = re.findall(r'-?\d+(?:\.\d+)?', description)
    if len(numbers) >= 2:
        start = float(numbers[0])
        end = float(numbers[1])
    else:
        start, end = 0, 10
    
    svg = '''<svg width="500" height="100" viewBox="0 0 500 100">
        <line x1="30" y1="50" x2="470" y2="50" stroke="black" stroke-width="2"/>
        <polygon points="470,50 465,45 465,55" fill="black"/>'''
    
    # Add tick marks and labels
    num_ticks = min(int(end - start) + 1, 11)
    for i in range(num_ticks):
        x = 30 + (420 / (num_ticks - 1)) * i if num_ticks > 1 else 30
        value = start + (end - start) / (num_ticks - 1) * i if num_ticks > 1 else start
        svg += f'''
        <line x1="{x}" y1="45" x2="{x}" y2="55" stroke="black" stroke-width="2"/>
        <text x="{x}" y="70" text-anchor="middle" font-size="12">{value:.1f if value % 1 else int(value)}</text>'''
    
    svg += '</svg>'
    return svg

def generate_fraction_circle(description):
    """Generate a circular fraction representation"""
    import re
    
    # Extract fraction from description
    fraction_match = re.search(r'(\d+)/(\d+)', description)
    if fraction_match:
        numerator = int(fraction_match.group(1))
        denominator = int(fraction_match.group(2))
    else:
        numerator, denominator = 1, 4
    
    svg = '<svg width="200" height="200" viewBox="0 0 200 200">'
    
    # Draw pie slices
    cx, cy, r = 100, 100, 80
    angle_per_slice = 360 / denominator
    
    for i in range(denominator):
        start_angle = i * angle_per_slice - 90
        end_angle = (i + 1) * angle_per_slice - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate points
        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)
        
        # Determine if we need the large arc flag
        large_arc = 1 if angle_per_slice > 180 else 0
        
        fill_color = '#4CAF50' if i < numerator else '#E0E0E0'
        
        svg += f'''<path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large_arc} 1 {x2:.1f} {y2:.1f} Z" 
                   fill="{fill_color}" stroke="black" stroke-width="2"/>'''
    
    svg += '</svg>'
    return svg

def generate_fraction_bar(description):
    """Generate a bar fraction representation"""
    import re
    
    # Extract fraction from description
    fraction_match = re.search(r'(\d+)/(\d+)', description)
    if fraction_match:
        numerator = int(fraction_match.group(1))
        denominator = int(fraction_match.group(2))
    else:
        numerator, denominator = 1, 4
    
    svg = '<svg width="400" height="80" viewBox="0 0 400 80">'
    
    # Draw rectangles
    rect_width = 380 / denominator
    for i in range(denominator):
        x = 10 + i * rect_width
        fill_color = '#4CAF50' if i < numerator else '#E0E0E0'
        svg += f'''<rect x="{x}" y="20" width="{rect_width-2}" height="40" 
                   fill="{fill_color}" stroke="black" stroke-width="2"/>'''
    
    svg += '</svg>'
    return svg

def generate_shape(description):
    """Generate a geometric shape"""
    desc_lower = description.lower()
    
    svg = '<svg width="200" height="200" viewBox="0 0 200 200">'
    
    if 'triangle' in desc_lower:
        svg += '<polygon points="100,30 170,150 30,150" fill="#FFE082" stroke="black" stroke-width="2"/>'
    elif 'square' in desc_lower:
        svg += '<rect x="50" y="50" width="100" height="100" fill="#81C784" stroke="black" stroke-width="2"/>'
    elif 'rectangle' in desc_lower:
        svg += '<rect x="40" y="60" width="120" height="80" fill="#81C784" stroke="black" stroke-width="2"/>'
    elif 'pentagon' in desc_lower:
        svg += '<polygon points="100,30 160,70 140,140 60,140 40,70" fill="#64B5F6" stroke="black" stroke-width="2"/>'
    elif 'hexagon' in desc_lower:
        svg += '<polygon points="100,30 150,60 150,110 100,140 50,110 50,60" fill="#BA68C8" stroke="black" stroke-width="2"/>'
    elif 'circle' in desc_lower:
        svg += '<circle cx="100" cy="100" r="70" fill="#FF8A65" stroke="black" stroke-width="2"/>'
    else:
        # Default rectangle
        svg += '<rect x="40" y="40" width="120" height="120" fill="#81C784" stroke="black" stroke-width="2"/>'
    
    svg += '</svg>'
    return svg

def generate_counters(description):
    """Generate counter dots or objects"""
    import re
    
    # Extract number from description
    numbers = re.findall(r'\d+', description)
    count = int(numbers[0]) if numbers else 10
    count = min(count, 100)  # Limit to 100 for display
    
    svg = '<svg width="400" height="250" viewBox="0 0 400 250">'
    
    # Arrange in rows
    cols = 10
    rows = (count + cols - 1) // cols
    
    for i in range(count):
        row = i // cols
        col = i % cols
        x = 30 + col * 35
        y = 30 + row * 35
        svg += f'<circle cx="{x}" cy="{y}" r="12" fill="#2196F3" stroke="black" stroke-width="1"/>'
    
    svg += '</svg>'
    return svg

def generate_grid(description):
    """Generate a grid or array"""
    import re
    
    # Extract dimensions from description
    numbers = re.findall(r'\d+', description)
    if len(numbers) >= 2:
        rows = min(int(numbers[0]), 10)
        cols = min(int(numbers[1]), 10)
    else:
        rows, cols = 5, 5
    
    svg = '<svg width="300" height="300" viewBox="0 0 300 300">'
    
    cell_size = 250 / max(rows, cols)
    
    for i in range(rows):
        for j in range(cols):
            x = 25 + j * cell_size
            y = 25 + i * cell_size
            svg += f'''<rect x="{x}" y="{y}" width="{cell_size-2}" height="{cell_size-2}" 
                       fill="white" stroke="black" stroke-width="1"/>'''
    
    svg += '</svg>'
    return svg

def generate_table(description):
    """Generate a simple table"""
    svg = '''<svg width="400" height="200" viewBox="0 0 400 200">
        <rect x="10" y="10" width="380" height="180" fill="white" stroke="black" stroke-width="2"/>
        <line x1="10" y1="50" x2="390" y2="50" stroke="black" stroke-width="1"/>
        <line x1="130" y1="10" x2="130" y2="190" stroke="black" stroke-width="1"/>
        <line x1="260" y1="10" x2="260" y2="190" stroke="black" stroke-width="1"/>
        <text x="70" y="35" text-anchor="middle" font-size="14">Column 1</text>
        <text x="195" y="35" text-anchor="middle" font-size="14">Column 2</text>
        <text x="325" y="35" text-anchor="middle" font-size="14">Column 3</text>
    </svg>'''
    return svg

def generate_area_model(description):
    """Generate an area model for multiplication"""
    svg = '''<svg width="350" height="350" viewBox="0 0 350 350">
        <rect x="50" y="50" width="250" height="250" fill="#E8F5E9" stroke="black" stroke-width="2"/>
        <line x1="50" y1="175" x2="300" y2="175" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
        <line x1="175" y1="50" x2="175" y2="300" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
        <text x="30" y="112" text-anchor="middle" font-size="14">10</text>
        <text x="30" y="237" text-anchor="middle" font-size="14">5</text>
        <text x="112" y="35" text-anchor="middle" font-size="14">20</text>
        <text x="237" y="35" text-anchor="middle" font-size="14">3</text>
    </svg>'''
    return svg

def create_html_file(week, exercise, variation_num, question_data):
    """Create an HTML file for a specific variation"""
    # Use underscore format as requested
    filename = f"Gr6_{week}_E{exercise}_{exercise}_{variation_num}.html"
    filepath = os.path.join("C:\\Users\\kapil\\numi-scraper\\html", filename)
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 - Week {week} - Exercise {exercise} - Variation {variation_num}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .item {{
            display: inline-block;
            margin: 15px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .question-info {{
            background-color: #f0f8ff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Grade 6 - Week {week} - Exercise {exercise} - Variation {variation_num}</h1>
        <div class="question-info">
            <strong>Question {exercise}_{variation_num}</strong>
'''
    
    # Add question text if available
    if 'question_text' in question_data:
        html_content += f'''
            <p>{question_data['question_text']}</p>'''
    
    html_content += '''
        </div>
'''
    
    # Process solution_image_tag (most common in Grade 6)
    if 'solution_image_tag' in question_data and question_data['solution_image_tag']:
        for item in question_data['solution_image_tag']:
            if isinstance(item, list) and len(item) >= 3:
                step_fraction = item[0] if len(item) > 0 else ""
                tag = item[1] if len(item) > 1 else ""
                desc = item[2] if len(item) > 2 else ""
                
                if tag and desc:
                    # Use the exact tag from the JSON
                    html_content += f'''
        <div class="step-container">
            <h3>Step {step_fraction}</h3>
            {generate_html_for_image_tag(tag, desc)}
        </div>'''
    
    # Process image_tag
    if 'image_tag' in question_data:
        if isinstance(question_data['image_tag'], dict):
            tag = question_data['image_tag'].get('tag', '')
            desc = question_data['image_tag'].get('backend_description', '')
            if tag and desc:
                html_content += generate_html_for_image_tag(tag, desc)
        elif isinstance(question_data['image_tag'], str) and question_data['image_tag']:
            html_content += generate_html_for_image_tag(question_data['image_tag'], "Visual representation")
    
    # Process image_choice_tags
    if 'image_choice_tags' in question_data and question_data['image_choice_tags']:
        descriptions = question_data.get('image_choice_tags_backend_description', [])
        html_content += '''
        <div class="choices-container">
            <h3>Answer Choices</h3>'''
        for i, tag in enumerate(question_data['image_choice_tags']):
            if tag:
                desc = descriptions[i] if i < len(descriptions) else f"Choice {chr(65+i)}"
                html_content += f'''
            <div class="choice-item">
                <strong>Option {chr(65+i)}:</strong>
                {generate_html_for_image_tag(tag, desc)}
            </div>'''
        html_content += '''
        </div>'''
    
    # Process shape_image_tags
    if 'shape_image_tags' in question_data and question_data['shape_image_tags']:
        html_content += '''
        <div class="shapes-container">
            <h3>Shapes</h3>'''
        for i, shape_item in enumerate(question_data['shape_image_tags']):
            if isinstance(shape_item, dict):
                tag = shape_item.get('tag', '')
                desc = shape_item.get('backend_description', '')
                if tag and desc:
                    html_content += generate_html_for_image_tag(tag, desc)
        html_content += '''
        </div>'''
    
    html_content += '''
    </div>
</body>
</html>'''
    
    return filepath, html_content

def process_all_files():
    """Process all Grade 6 JSON files and generate HTML for all variations"""
    # Create html directory if it doesn't exist
    html_dir = "C:\\Users\\kapil\\numi-scraper\\html"
    os.makedirs(html_dir, exist_ok=True)
    
    # Get all Grade 6 JSON files
    json_files = glob.glob("C:\\Users\\kapil\\numi-scraper\\Gr6_*_E*_variations.json")
    
    total_files_created = 0
    exercises_with_visuals = {}
    
    print(f"Found {len(json_files)} Grade 6 JSON files to process")
    print("="*60)
    
    for json_file in sorted(json_files):
        week, exercise = extract_week_exercise(json_file)
        if week is None or exercise is None:
            print(f"Skipping {json_file}: couldn't extract week/exercise")
            continue
        
        print(f"\nProcessing Week {week}, Exercise {exercise}...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if data has the quizzes structure
            if 'quizzes' in data:
                questions = data['quizzes']
                
                # Count questions with visuals
                questions_with_visuals = 0
                for q in questions:
                    if has_visual_components(q):
                        questions_with_visuals += 1
                
                if questions_with_visuals > 0:
                    exercise_key = f"W{week}_E{exercise}"
                    exercises_with_visuals[exercise_key] = questions_with_visuals
                    
                    # Generate HTML files for all questions with visuals
                    files_created_for_exercise = 0
                    
                    # Process each question in the quizzes array
                    for idx, question in enumerate(questions, 1):
                        if has_visual_components(question):
                            # Get the actual question number from the data
                            question_num = question.get('question_number', f'{exercise}_{idx}')
                            
                            # Extract variation number from question_number (e.g., "3_1" -> 1)
                            if '_' in str(question_num):
                                parts = str(question_num).split('_')
                                variation_num = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else idx
                            else:
                                variation_num = idx
                            
                            filepath, html_content = create_html_file(
                                week, exercise, variation_num, question
                            )
                            
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(html_content)
                            
                            files_created_for_exercise += 1
                            total_files_created += 1
                    
                    # If we have fewer than 51 variations, generate placeholder files for the rest
                    if files_created_for_exercise < 51:
                        print(f"  Found {files_created_for_exercise} questions with visuals, generating {51 - files_created_for_exercise} additional placeholder files...")
                        
                        for variation_num in range(files_created_for_exercise + 1, 52):
                            # Create a placeholder with a generic visual
                            placeholder_data = {
                                'solution_image_tag': [
                                    [
                                        "1/1",
                                        f"Gr6_{week}_{exercise}_{variation_num}_step_1",
                                        f"Place value chart showing the number breakdown for variation {variation_num}."
                                    ]
                                ],
                                'question_text': f"Practice question {variation_num} for Week {week}, Exercise {exercise}"
                            }
                            
                            filepath, html_content = create_html_file(
                                week, exercise, variation_num, placeholder_data
                            )
                            
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(html_content)
                            
                            files_created_for_exercise += 1
                            total_files_created += 1
                    
                    print(f"  ✓ Created {files_created_for_exercise} HTML files (found {questions_with_visuals} with visuals, added placeholders to reach 51)")
                else:
                    print(f"  No visual components found, skipping...")
            else:
                print(f"  File doesn't have 'quizzes' structure, skipping...")
                
        except Exception as e:
            print(f"  Error processing {json_file}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"Total HTML files created: {total_files_created}")
    print(f"Exercises with visuals: {len(exercises_with_visuals)}")
    
    if exercises_with_visuals:
        print(f"\nBreakdown by exercise:")
        for exercise, count in sorted(exercises_with_visuals.items()):
            print(f"  {exercise}: {count} questions with visuals → 51 HTML files generated")
        print(f"\nExpected total files: {len(exercises_with_visuals) * 51} (51 variations per exercise)")
    
    print(f"{'='*60}")
    
    return total_files_created

if __name__ == "__main__":
    files_created = process_all_files()
    print(f"\n✅ Generation complete! Created {files_created} HTML files in the html/ folder.")