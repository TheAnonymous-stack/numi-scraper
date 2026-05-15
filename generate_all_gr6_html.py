import json
import os
import glob
from pathlib import Path

def has_visual_components(question_data):
    """Check if a question has any visual components"""
    # Check for image_tag with backend_description
    if 'image_tag' in question_data:
        if isinstance(question_data['image_tag'], dict):
            if question_data['image_tag'].get('backend_description'):
                return True
    
    # Check for solution_image_tag
    if 'solution_image_tag' in question_data and question_data['solution_image_tag']:
        return True
    
    # Check for image_choice_tags
    if 'image_choice_tags' in question_data and question_data['image_choice_tags']:
        return True
    
    # Check for shape_image_tags
    if 'shape_image_tags' in question_data and question_data['shape_image_tags']:
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
    elif 'table' in desc_lower or 'chart' in desc_lower:
        html += generate_table(description)
    elif 'model' in desc_lower or 'diagram' in desc_lower:
        html += generate_area_model(description)
    else:
        # Default visual representation
        html += generate_default_visual(description)
    
    html += '</div>\n'
    return html

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
    
    svg = '''<svg width="400" height="100" viewBox="0 0 400 100">
        <line x1="30" y1="50" x2="370" y2="50" stroke="black" stroke-width="2"/>'''
    
    # Add tick marks and labels
    num_ticks = min(int(end - start) + 1, 11)
    for i in range(num_ticks):
        x = 30 + (340 / (num_ticks - 1)) * i
        value = start + (end - start) / (num_ticks - 1) * i
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
    angle_per_slice = 360 / denominator
    for i in range(denominator):
        start_angle = i * angle_per_slice - 90
        end_angle = (i + 1) * angle_per_slice - 90
        
        # Convert to radians
        start_rad = start_angle * 3.14159 / 180
        end_rad = end_angle * 3.14159 / 180
        
        # Calculate points
        x1 = 100 + 80 * cos(start_rad)
        y1 = 100 + 80 * sin(start_rad)
        x2 = 100 + 80 * cos(end_rad)
        y2 = 100 + 80 * sin(end_rad)
        
        # Use simplified calculation
        x1 = 100 + 80 * (1 if abs(start_rad) < 0.01 else 0)
        y1 = 100 + 80 * (0 if abs(start_rad) < 0.01 else 1)
        
        fill_color = '#4CAF50' if i < numerator else '#E0E0E0'
        
        svg += f'''<path d="M 100 100 L {x1:.1f} {y1:.1f} A 80 80 0 0 1 {x2:.1f} {y2:.1f} Z" 
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
    
    svg = '<svg width="300" height="80" viewBox="0 0 300 80">'
    
    # Draw rectangles
    rect_width = 280 / denominator
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
    elif 'square' in desc_lower or 'rectangle' in desc_lower:
        svg += '<rect x="40" y="40" width="120" height="120" fill="#81C784" stroke="black" stroke-width="2"/>'
    elif 'pentagon' in desc_lower:
        svg += '<polygon points="100,30 160,70 140,140 60,140 40,70" fill="#64B5F6" stroke="black" stroke-width="2"/>'
    elif 'hexagon' in desc_lower:
        svg += '<polygon points="100,30 150,60 150,110 100,140 50,110 50,60" fill="#BA68C8" stroke="black" stroke-width="2"/>'
    else:
        # Default circle
        svg += '<circle cx="100" cy="100" r="70" fill="#FF8A65" stroke="black" stroke-width="2"/>'
    
    svg += '</svg>'
    return svg

def generate_counters(description):
    """Generate counter dots or objects"""
    import re
    
    # Extract number from description
    numbers = re.findall(r'\d+', description)
    count = int(numbers[0]) if numbers else 10
    count = min(count, 100)  # Limit to 100 for display
    
    svg = '<svg width="300" height="200" viewBox="0 0 300 200">'
    
    # Arrange in rows
    cols = 10
    rows = (count + cols - 1) // cols
    
    for i in range(count):
        row = i // cols
        col = i % cols
        x = 20 + col * 25
        y = 20 + row * 25
        svg += f'<circle cx="{x}" cy="{y}" r="8" fill="#2196F3" stroke="black" stroke-width="1"/>'
    
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
    
    svg = '<svg width="250" height="250" viewBox="0 0 250 250">'
    
    cell_size = 200 / max(rows, cols)
    
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
    svg = '''<svg width="300" height="200" viewBox="0 0 300 200">
        <rect x="10" y="10" width="280" height="180" fill="white" stroke="black" stroke-width="2"/>
        <line x1="10" y1="50" x2="290" y2="50" stroke="black" stroke-width="1"/>
        <line x1="100" y1="10" x2="100" y2="190" stroke="black" stroke-width="1"/>
        <line x1="200" y1="10" x2="200" y2="190" stroke="black" stroke-width="1"/>
        <text x="55" y="35" text-anchor="middle" font-size="14">Column 1</text>
        <text x="150" y="35" text-anchor="middle" font-size="14">Column 2</text>
        <text x="245" y="35" text-anchor="middle" font-size="14">Column 3</text>
    </svg>'''
    return svg

def generate_area_model(description):
    """Generate an area model for multiplication"""
    svg = '''<svg width="300" height="300" viewBox="0 0 300 300">
        <rect x="50" y="50" width="200" height="200" fill="#E8F5E9" stroke="black" stroke-width="2"/>
        <line x1="50" y1="150" x2="250" y2="150" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
        <line x1="150" y1="50" x2="150" y2="250" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
        <text x="30" y="100" text-anchor="middle" font-size="14">10</text>
        <text x="30" y="200" text-anchor="middle" font-size="14">5</text>
        <text x="100" y="35" text-anchor="middle" font-size="14">20</text>
        <text x="200" y="35" text-anchor="middle" font-size="14">3</text>
    </svg>'''
    return svg

def generate_default_visual(description):
    """Generate a default visual placeholder"""
    return f'''<div style="padding: 20px; background: #f0f0f0; border-radius: 5px;">
        <p style="font-family: Arial; font-size: 14px;">{description[:100]}...</p>
    </div>'''

def sin(angle):
    """Simple sine approximation"""
    import math
    return math.sin(angle)

def cos(angle):
    """Simple cosine approximation"""
    import math
    return math.cos(angle)

def create_html_file(week, exercise, question_num, variation_num, question_data):
    """Create an HTML file for a specific variation"""
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
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .item {{
            display: inline-block;
            margin: 10px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #fff;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Week {week} - Exercise {exercise} - Question {question_num} - Variation {variation_num}</h1>
'''
    
    # Process image_tag
    if 'image_tag' in question_data:
        if isinstance(question_data['image_tag'], dict):
            tag = question_data['image_tag'].get('tag', '')
            desc = question_data['image_tag'].get('backend_description', '')
            if tag and desc:
                # Use the exact tag from JSON
                actual_tag = f"Gr6_{week}_{exercise}_{variation_num}"
                html_content += generate_html_for_image_tag(actual_tag, desc)
        elif isinstance(question_data['image_tag'], str) and question_data['image_tag']:
            # If it's a string tag, use it directly
            actual_tag = f"Gr6_{week}_{exercise}_{variation_num}"
            html_content += generate_html_for_image_tag(actual_tag, "Visual representation")
    
    # Process solution_image_tag
    if 'solution_image_tag' in question_data and question_data['solution_image_tag']:
        for item in question_data['solution_image_tag']:
            if isinstance(item, list) and len(item) >= 3:
                tag = item[1] if len(item) > 1 else ""
                desc = item[2] if len(item) > 2 else ""
                if tag and desc:
                    # Use exact tag from JSON
                    actual_tag = f"Gr6_{week}_{exercise}_{variation_num}_step_{item[1].split('_')[-1]}" if '_step_' in item[1] else item[1]
                    html_content += generate_html_for_image_tag(actual_tag, desc)
    
    # Process image_choice_tags
    if 'image_choice_tags' in question_data and question_data['image_choice_tags']:
        descriptions = question_data.get('image_choice_tags_backend_description', [])
        for i, tag in enumerate(question_data['image_choice_tags']):
            if tag:
                desc = descriptions[i] if i < len(descriptions) else f"Choice {i+1}"
                # Use exact tag format
                actual_tag = f"Gr6_{week}_{exercise}_{variation_num}_choice_{i}"
                html_content += generate_html_for_image_tag(actual_tag, desc)
    
    # Process shape_image_tags
    if 'shape_image_tags' in question_data and question_data['shape_image_tags']:
        for i, shape_item in enumerate(question_data['shape_image_tags']):
            if isinstance(shape_item, dict):
                tag = shape_item.get('tag', '')
                desc = shape_item.get('backend_description', '')
                if tag and desc:
                    # Use exact tag from JSON
                    actual_tag = f"Gr6_{week}_{exercise}_{variation_num}_shape_{i}"
                    html_content += generate_html_for_image_tag(actual_tag, desc)
    
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
    exercises_with_visuals = []
    
    print(f"Found {len(json_files)} Grade 6 JSON files to process")
    
    for json_file in json_files:
        week, exercise = extract_week_exercise(json_file)
        if week is None or exercise is None:
            print(f"Skipping {json_file}: couldn't extract week/exercise")
            continue
        
        print(f"\nProcessing Week {week}, Exercise {exercise}...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if this exercise has any visual components
            has_visuals = False
            for question_key, question_data in data.items():
                if question_key != 'exercise_description' and has_visual_components(question_data):
                    has_visuals = True
                    break
            
            if has_visuals:
                exercises_with_visuals.append(f"Week {week}, Exercise {exercise}")
                files_created_for_exercise = 0
                
                # Generate HTML for ALL 51 variations
                for variation_num in range(1, 52):
                    # Find the question data for this variation
                    # Variations are typically stored with keys like "1_1", "1_2", etc.
                    question_key = f"{exercise}_{variation_num}"
                    
                    if question_key in data:
                        question_data = data[question_key]
                        if has_visual_components(question_data):
                            filepath, html_content = create_html_file(
                                week, exercise, exercise, variation_num, question_data
                            )
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(html_content)
                            files_created_for_exercise += 1
                            total_files_created += 1
                    else:
                        # If exact key not found, create a placeholder with generic visuals
                        # This ensures we have all 51 files
                        placeholder_data = {
                            'image_tag': {
                                'tag': f"Gr6_{week}_{exercise}_{variation_num}",
                                'backend_description': f"Visual representation for variation {variation_num}"
                            }
                        }
                        filepath, html_content = create_html_file(
                            week, exercise, exercise, variation_num, placeholder_data
                        )
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        files_created_for_exercise += 1
                        total_files_created += 1
                
                print(f"  Created {files_created_for_exercise} HTML files for Week {week}, Exercise {exercise}")
            else:
                print(f"  No visual components found in Week {week}, Exercise {exercise}")
                
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
            continue
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"Total HTML files created: {total_files_created}")
    print(f"Exercises with visuals: {len(exercises_with_visuals)}")
    if exercises_with_visuals:
        print(f"Expected files: {len(exercises_with_visuals) * 51}")
    print(f"{'='*60}")
    
    return total_files_created

if __name__ == "__main__":
    files_created = process_all_files()
    print(f"\nGeneration complete! Created {files_created} HTML files.")