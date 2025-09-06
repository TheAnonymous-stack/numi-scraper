import json
import os
import glob
import re

def extract_week_exercise(filename):
    """Extract week and exercise numbers from filename."""
    match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def has_visual_elements(question):
    """Check if a question has visual elements."""
    return any(key in question for key in ['image_tag', 'solution_image_tag', 'image_choice_tags', 'shape_image_tags'])

def generate_fraction_circle(parts, colored, color="lightblue"):
    """Generate SVG for a fraction circle."""
    svg = f'''<svg width="150" height="150" xmlns="http://www.w3.org/2000/svg">
    <circle cx="75" cy="75" r="70" fill="white" stroke="black" stroke-width="2"/>'''
    
    angle_per_part = 360 / parts
    for i in range(parts):
        start_angle = i * angle_per_part - 90
        end_angle = (i + 1) * angle_per_part - 90
        
        start_rad = start_angle * 3.14159 / 180
        end_rad = end_angle * 3.14159 / 180
        
        x1 = 75 + 70 * (start_rad).cos() if hasattr(start_rad, 'cos') else 75 + 70 * __import__('math').cos(start_rad)
        y1 = 75 + 70 * (start_rad).sin() if hasattr(start_rad, 'sin') else 75 + 70 * __import__('math').sin(start_rad)
        x2 = 75 + 70 * (end_rad).cos() if hasattr(end_rad, 'cos') else 75 + 70 * __import__('math').cos(end_rad)
        y2 = 75 + 70 * (end_rad).sin() if hasattr(end_rad, 'sin') else 75 + 70 * __import__('math').sin(end_rad)
        
        large_arc = 1 if angle_per_part > 180 else 0
        fill = color if i < colored else "white"
        
        svg += f'''
    <path d="M 75 75 L {x1:.2f} {y1:.2f} A 70 70 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z" 
          fill="{fill}" stroke="black" stroke-width="1"/>'''
    
    svg += '\n</svg>'
    return svg

def generate_rectangle_fraction(parts, colored, color="lightblue"):
    """Generate SVG for a fraction rectangle."""
    svg = f'''<svg width="200" height="100" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="0" width="200" height="100" fill="white" stroke="black" stroke-width="2"/>'''
    
    part_width = 200 / parts
    for i in range(parts):
        x = i * part_width
        fill = color if i < colored else "white"
        svg += f'''
    <rect x="{x:.2f}" y="0" width="{part_width:.2f}" height="100" 
          fill="{fill}" stroke="black" stroke-width="1"/>'''
    
    svg += '\n</svg>'
    return svg

def generate_number_line(start, end, step=1, marked_points=None):
    """Generate SVG for a number line."""
    width = 600
    height = 100
    margin = 50
    line_y = 50
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <line x1="{margin}" y1="{line_y}" x2="{width-margin}" y2="{line_y}" stroke="black" stroke-width="2"/>'''
    
    # Add arrow
    svg += f'''
    <polygon points="{width-margin},{ line_y} {width-margin-10},{line_y-5} {width-margin-10},{line_y+5}" 
             fill="black"/>'''
    
    # Calculate positions
    line_width = width - 2 * margin
    num_steps = (end - start) / step
    step_width = line_width / num_steps
    
    # Add tick marks and labels
    current = start
    pos = 0
    while current <= end:
        x = margin + pos * step_width
        svg += f'''
    <line x1="{x:.2f}" y1="{line_y-10}" x2="{x:.2f}" y2="{line_y+10}" stroke="black" stroke-width="1"/>
    <text x="{x:.2f}" y="{line_y+25}" text-anchor="middle" font-size="12">{current}</text>'''
        
        # Mark specific points if provided
        if marked_points and current in marked_points:
            svg += f'''
    <circle cx="{x:.2f}" cy="{line_y}" r="4" fill="red"/>'''
        
        current += step
        pos += 1
    
    svg += '\n</svg>'
    return svg

def generate_bar_graph(data, labels=None):
    """Generate SVG for a bar graph."""
    width = 400
    height = 300
    margin = 40
    
    if not data:
        return '<svg width="400" height="300"></svg>'
    
    max_value = max(data) if data else 1
    bar_width = (width - 2 * margin) / len(data)
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <!-- Y-axis -->
    <line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>
    <!-- X-axis -->
    <line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>'''
    
    # Add bars
    for i, value in enumerate(data):
        x = margin + i * bar_width + bar_width * 0.1
        bar_height = (value / max_value) * (height - 2 * margin)
        y = height - margin - bar_height
        
        svg += f'''
    <rect x="{x:.2f}" y="{y:.2f}" width="{bar_width * 0.8:.2f}" height="{bar_height:.2f}" 
          fill="steelblue" stroke="black" stroke-width="1"/>'''
        
        # Add label if provided
        if labels and i < len(labels):
            svg += f'''
    <text x="{x + bar_width * 0.4:.2f}" y="{height - margin + 15}" text-anchor="middle" font-size="10">
        {labels[i]}
    </text>'''
    
    svg += '\n</svg>'
    return svg

def generate_html_content(question, week, exercise, question_num):
    """Generate HTML content for a question with visual elements."""
    html_parts = []
    
    # Handle image_tag
    if 'image_tag' in question and 'backend_description' in question:
        desc = question['backend_description']
        tag = question['image_tag']
        
        # Parse description to generate appropriate visual
        if 'circle' in desc.lower() and 'fraction' in desc.lower():
            # Extract numbers from description
            numbers = re.findall(r'\d+', desc)
            if len(numbers) >= 2:
                parts = int(numbers[0])
                colored = int(numbers[1])
                svg = generate_fraction_circle(parts, colored)
                html_parts.append(f'<div class="item" label="{tag}">\n{svg}\n</div>')
        elif 'rectangle' in desc.lower() and 'fraction' in desc.lower():
            numbers = re.findall(r'\d+', desc)
            if len(numbers) >= 2:
                parts = int(numbers[0])
                colored = int(numbers[1])
                svg = generate_rectangle_fraction(parts, colored)
                html_parts.append(f'<div class="item" label="{tag}">\n{svg}\n</div>')
        elif 'number line' in desc.lower():
            # Default number line
            svg = generate_number_line(0, 10, 1)
            html_parts.append(f'<div class="item" label="{tag}">\n{svg}\n</div>')
        elif 'bar' in desc.lower() or 'graph' in desc.lower():
            # Default bar graph
            svg = generate_bar_graph([3, 5, 2, 7, 4])
            html_parts.append(f'<div class="item" label="{tag}">\n{svg}\n</div>')
        else:
            # Generic placeholder
            html_parts.append(f'<div class="item" label="{tag}">\n<svg width="200" height="200">\n<rect width="200" height="200" fill="lightgray"/>\n<text x="100" y="100" text-anchor="middle">Visual: {tag}</text>\n</svg>\n</div>')
    
    # Handle solution_image_tag
    if 'solution_image_tag' in question and 'solution' in question:
        tag = question['solution_image_tag']
        # Try to extract description from solution
        if isinstance(question['solution'], list) and len(question['solution']) > 0:
            if isinstance(question['solution'][0], list) and len(question['solution'][0]) > 2:
                desc = str(question['solution'][0][2]) if len(question['solution'][0]) > 2 else ""
                
                # Generate appropriate visual based on description
                if 'circle' in desc.lower():
                    svg = generate_fraction_circle(4, 2, "lightgreen")
                elif 'rectangle' in desc.lower():
                    svg = generate_rectangle_fraction(4, 2, "lightgreen")
                else:
                    svg = '<svg width="200" height="200">\n<rect width="200" height="200" fill="lightyellow"/>\n<text x="100" y="100" text-anchor="middle">Solution Visual</text>\n</svg>'
                
                html_parts.append(f'<div class="item" label="{tag}">\n{svg}\n</div>')
    
    # Handle image_choice_tags
    if 'image_choice_tags' in question:
        tags = question['image_choice_tags']
        descriptions = question.get('image_choice_tags_backend_description', [])
        
        for i, tag in enumerate(tags):
            if i < len(descriptions):
                desc = descriptions[i]
                # Generate visual based on description
                if 'fraction' in desc.lower():
                    numbers = re.findall(r'\d+', desc)
                    if len(numbers) >= 2:
                        parts = int(numbers[0])
                        colored = int(numbers[1])
                        svg = generate_fraction_circle(parts, colored, "lightcoral")
                    else:
                        svg = generate_fraction_circle(4, 1, "lightcoral")
                else:
                    svg = f'<svg width="150" height="150">\n<rect width="150" height="150" fill="lightblue"/>\n<text x="75" y="75" text-anchor="middle">Choice {i+1}</text>\n</svg>'
            else:
                svg = f'<svg width="150" height="150">\n<rect width="150" height="150" fill="lightgray"/>\n<text x="75" y="75" text-anchor="middle">Option {i+1}</text>\n</svg>'
            
            html_parts.append(f'<div class="item" label="{tag}">\n{svg}\n</div>')
    
    # Handle shape_image_tags
    if 'shape_image_tags' in question:
        for shape_info in question['shape_image_tags']:
            if isinstance(shape_info, dict):
                tag = shape_info.get('tag', 'shape')
                desc = shape_info.get('backend_description', '')
                
                # Generate shape based on description
                if 'triangle' in desc.lower():
                    svg = '''<svg width="150" height="150">
    <polygon points="75,20 130,130 20,130" fill="lightgreen" stroke="black" stroke-width="2"/>
</svg>'''
                elif 'square' in desc.lower():
                    svg = '''<svg width="150" height="150">
    <rect x="25" y="25" width="100" height="100" fill="lightyellow" stroke="black" stroke-width="2"/>
</svg>'''
                elif 'circle' in desc.lower():
                    svg = '''<svg width="150" height="150">
    <circle cx="75" cy="75" r="60" fill="lightpink" stroke="black" stroke-width="2"/>
</svg>'''
                else:
                    svg = f'<svg width="150" height="150">\n<rect width="150" height="150" fill="lightgray"/>\n<text x="75" y="75" text-anchor="middle">{tag}</text>\n</svg>'
                
                html_parts.append(f'<div class="item" label="{tag}">\n{svg}\n</div>')
    
    if html_parts:
        # Create complete HTML document
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Gr6_{week}_E{exercise} {question_num}</title>
    <style>
        .item {{
            display: inline-block;
            margin: 10px;
            padding: 10px;
            border: 1px solid #ccc;
        }}
    </style>
</head>
<body>
    <h2>Grade 6 - Week {week} - Exercise {exercise} - Question {question_num}</h2>
    {''.join(html_parts)}
</body>
</html>'''
        return html_content
    
    return None

def main():
    # Get all Grade 6 JSON files
    json_files = glob.glob('Gr6_*_E*_variations.json')
    
    # Create HTML directory if it doesn't exist
    os.makedirs('HTML', exist_ok=True)
    
    total_files_processed = 0
    total_html_generated = 0
    errors = []
    
    print(f"Found {len(json_files)} Grade 6 JSON files to process")
    
    for json_file in json_files:
        filename = os.path.basename(json_file)
        week, exercise = extract_week_exercise(filename)
        
        if week is None or exercise is None:
            errors.append(f"Could not parse filename: {filename}")
            continue
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            total_files_processed += 1
            
            # Process each question
            for i, question in enumerate(data):
                if has_visual_elements(question):
                    question_num = i + 1
                    html_filename = f"Gr6_{week}_E{exercise} {question_num}.html"
                    html_path = os.path.join('HTML', html_filename)
                    
                    # Generate HTML content
                    html_content = generate_html_content(question, week, exercise, question_num)
                    
                    if html_content:
                        with open(html_path, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        total_html_generated += 1
                        print(f"Generated: {html_filename}")
        
        except json.JSONDecodeError as e:
            errors.append(f"JSON decode error in {filename}: {str(e)}")
        except Exception as e:
            errors.append(f"Error processing {filename}: {str(e)}")
    
    # Print summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    print(f"Total JSON files processed: {total_files_processed}")
    print(f"Total HTML files generated: {total_html_generated}")
    print(f"Errors encountered: {len(errors)}")
    
    if errors:
        print("\nErrors:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

if __name__ == "__main__":
    main()