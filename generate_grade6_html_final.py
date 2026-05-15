import json
import os
import glob
import re

def has_visual_components(quiz):
    """Check if a quiz has any visual components."""
    # Check for image_tag with backend_description
    if 'image_tag' in quiz and quiz.get('backend_description'):
        return True
    
    # Check for solution_image_tag (non-empty list)
    if 'solution_image_tag' in quiz and quiz['solution_image_tag']:
        return True
    
    # Check for image_choice_tags with descriptions
    if 'image_choice_tags' in quiz and quiz.get('image_choice_tags_backend_description'):
        return True
    
    # Check for shape_image_tags
    if 'shape_image_tags' in quiz and quiz['shape_image_tags']:
        return True
    
    return False

def is_placeholder_tag(tag):
    """Check if a tag is a placeholder (contains 'variations' or ends with _tag_N)."""
    if not tag:
        return False
    return 'variations' in tag or re.match(r'.*_tag_\d+$', tag)

def generate_proper_tag(week_num, exercise_num, question_num, tag_type, index=None):
    """Generate a proper tag based on the pattern."""
    # Clean up question_num (remove extra underscores if any)
    question_num = question_num.replace('_', '_')
    
    base_tag = f"Gr6_{week_num}_{question_num}"
    
    if tag_type == "main":
        return base_tag
    elif tag_type == "choice":
        choice_letter = chr(65 + index) if index is not None else "A"
        return f"{base_tag}_choice_{choice_letter}"
    elif tag_type == "solution_step":
        step_num = index + 1 if index is not None else 1
        return f"{base_tag}_step_{step_num}"
    elif tag_type == "shape":
        return f"{base_tag}_shape_{index + 1}" if index is not None else f"{base_tag}_shape"
    
    return base_tag

def generate_html_content(quiz, week_num, exercise_num):
    """Generate HTML content for a quiz with visual components."""
    question_num = quiz.get('question_number', '1_1')
    
    html_parts = []
    html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 - Week {} Exercise {} - Question {}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .item {{
            margin: 20px 0;
            padding: 15px;
            border: 2px solid #333;
            border-radius: 5px;
            background-color: #fff;
            display: inline-block;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .shape {{
            width: 150px;
            height: 150px;
            position: relative;
            margin: 10px auto;
        }}
        .circle {{
            border-radius: 50%;
            border: 2px solid #333;
        }}
        .rectangle {{
            border: 2px solid #333;
        }}
        .triangle {{
            width: 0;
            height: 0;
            border-left: 75px solid transparent;
            border-right: 75px solid transparent;
            border-bottom: 130px solid #333;
        }}
        .fraction-part {{
            position: absolute;
            background-color: #4CAF50;
            opacity: 0.7;
        }}
        .number-line {{
            position: relative;
            width: 600px;
            height: 100px;
            margin: 20px auto;
        }}
        .line {{
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 2px;
            background-color: #333;
        }}
        .tick {{
            position: absolute;
            top: 40%;
            width: 2px;
            height: 20%;
            background-color: #333;
        }}
        .tick-label {{
            position: absolute;
            top: 65%;
            transform: translateX(-50%);
            font-size: 12px;
        }}
        .counter {{
            display: inline-block;
            width: 30px;
            height: 30px;
            margin: 3px;
            background-color: #2196F3;
            border-radius: 50%;
            border: 1px solid #333;
        }}
        .place-value-chart {{
            display: table;
            border-collapse: collapse;
            margin: 20px auto;
        }}
        .place-value-row {{
            display: table-row;
        }}
        .place-value-cell {{
            display: table-cell;
            border: 2px solid #333;
            padding: 15px 25px;
            text-align: center;
            font-size: 16px;
            min-width: 100px;
        }}
        .place-value-header {{
            background-color: #e0e0e0;
            font-weight: bold;
        }}
        .area-model {{
            display: inline-block;
            border: 2px solid #333;
            margin: 10px;
        }}
        .area-cell {{
            display: inline-block;
            border: 1px solid #666;
            width: 40px;
            height: 40px;
            vertical-align: top;
        }}
        .data-table {{
            border-collapse: collapse;
            margin: 20px auto;
        }}
        .data-table th, .data-table td {{
            border: 1px solid #333;
            padding: 10px 15px;
            text-align: center;
        }}
        .data-table th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        .oval {{
            width: 120px;
            height: 80px;
            border: 2px solid #333;
            border-radius: 50%;
            display: inline-block;
            margin: 10px;
            position: relative;
            overflow: hidden;
        }}
        .arrow {{
            width: 150px;
            height: 60px;
            position: relative;
            background: #fff;
            border: 2px solid #333;
            margin: 10px;
            display: inline-block;
            overflow: hidden;
        }}
        .arrow:after {{
            content: '';
            position: absolute;
            left: 100%;
            top: 50%;
            margin-top: -20px;
            width: 0;
            height: 0;
            border-left: 20px solid #333;
            border-top: 20px solid transparent;
            border-bottom: 20px solid transparent;
        }}
        .section {{
            float: left;
            height: 100%;
            border-right: 1px solid #666;
            box-sizing: border-box;
        }}
        .shaded-blue {{
            background-color: #2196F3;
            opacity: 0.7;
        }}
        .shaded-purple {{
            background-color: #9C27B0;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Grade 6 - Week {} Exercise {} - Question {}</h1>
'''.format(week_num, exercise_num, question_num, week_num, exercise_num, question_num))
    
    # Process image_tag
    if 'image_tag' in quiz and quiz.get('backend_description'):
        tag = quiz['image_tag']
        # Check if it's a placeholder and generate proper tag
        if is_placeholder_tag(tag):
            actual_tag = generate_proper_tag(week_num, exercise_num, question_num, "main")
        else:
            actual_tag = tag
        
        description = quiz['backend_description']
        html_parts.append(f'\n        <!-- Main Image: {actual_tag} -->')
        html_parts.append(f'\n        <div class="item" label="{actual_tag}">')
        html_parts.append(generate_visual_element(description, actual_tag))
        html_parts.append('\n        </div>')
    
    # Process solution_image_tag
    if 'solution_image_tag' in quiz and quiz['solution_image_tag']:
        for i, step in enumerate(quiz['solution_image_tag']):
            if isinstance(step, list) and len(step) >= 3:
                # Extract the tag from position 1
                tag = step[1] if len(step) > 1 else ""
                # Check if it's a placeholder
                if is_placeholder_tag(tag) or not tag:
                    actual_tag = generate_proper_tag(week_num, exercise_num, question_num, "solution_step", i)
                else:
                    actual_tag = tag
                
                description = step[2] if len(step) > 2 else ""
                html_parts.append(f'\n        <!-- Solution Step {i+1}: {actual_tag} -->')
                html_parts.append(f'\n        <div class="item" label="{actual_tag}">')
                html_parts.append(generate_visual_element(description, actual_tag))
                html_parts.append('\n        </div>')
    
    # Process image_choice_tags
    if 'image_choice_tags' in quiz and quiz.get('image_choice_tags_backend_description'):
        tags = quiz['image_choice_tags']
        descriptions = quiz['image_choice_tags_backend_description']
        
        for i, tag in enumerate(tags):
            # Check if tag is a placeholder
            if is_placeholder_tag(tag):
                # Generate proper tag for choices
                actual_tag = generate_proper_tag(week_num, exercise_num, question_num, "choice", i)
            else:
                actual_tag = tag
            
            if i < len(descriptions):
                description = descriptions[i]
                html_parts.append(f'\n        <!-- Choice {chr(65+i)}: {actual_tag} -->')
                html_parts.append(f'\n        <div class="item" label="{actual_tag}">')
                html_parts.append(generate_visual_element(description, actual_tag))
                html_parts.append('\n        </div>')
    
    # Process shape_image_tags
    if 'shape_image_tags' in quiz and quiz['shape_image_tags']:
        for i, shape_data in enumerate(quiz['shape_image_tags']):
            if isinstance(shape_data, dict) and 'tag' in shape_data:
                tag = shape_data['tag']
                # Check if it's a placeholder
                if is_placeholder_tag(tag):
                    actual_tag = generate_proper_tag(week_num, exercise_num, question_num, "shape", i)
                else:
                    actual_tag = tag
                description = shape_data.get('backend_description', '')
            else:
                # Generate a tag if not provided
                actual_tag = generate_proper_tag(week_num, exercise_num, question_num, "shape", i)
                description = str(shape_data) if shape_data else ''
            
            html_parts.append(f'\n        <!-- Shape {i+1}: {actual_tag} -->')
            html_parts.append(f'\n        <div class="item" label="{actual_tag}">')
            html_parts.append(generate_visual_element(description, actual_tag))
            html_parts.append('\n        </div>')
    
    html_parts.append('''
    </div>
</body>
</html>''')
    
    return ''.join(html_parts)

def generate_visual_element(description, tag):
    """Generate appropriate visual element based on description."""
    desc_lower = description.lower()
    
    # Special handling for ovals and arrows with fractions
    if 'oval' in desc_lower and 'divided' in desc_lower:
        return generate_oval_fractions(description)
    elif 'arrow' in desc_lower and 'divided' in desc_lower:
        return generate_arrow_fractions(description)
    elif 'number line' in desc_lower:
        return generate_number_line(description)
    elif 'place value' in desc_lower or 'place-value' in desc_lower:
        return generate_place_value_chart(description)
    elif 'circle' in desc_lower and ('shaded' in desc_lower or 'fraction' in desc_lower):
        return generate_fraction_circle(description)
    elif 'rectangle' in desc_lower and ('shaded' in desc_lower or 'fraction' in desc_lower):
        return generate_fraction_rectangle(description)
    elif 'counter' in desc_lower or 'dot' in desc_lower:
        return generate_counters(description)
    elif 'area model' in desc_lower or 'multiplication' in desc_lower:
        return generate_area_model(description)
    elif 'table' in desc_lower or 'data' in desc_lower:
        return generate_data_table(description)
    elif 'triangle' in desc_lower:
        return generate_triangle(description)
    elif 'grid' in desc_lower or 'array' in desc_lower:
        return generate_grid(description)
    else:
        # Default visual element
        return f'\n            <div style="padding: 20px; background-color: #f9f9f9; border-radius: 5px;">\n                <p>{description}</p>\n            </div>'

def generate_oval_fractions(description):
    """Generate ovals with fraction shading."""
    # Extract number of ovals
    num_match = re.search(r'(\d+)\s+identical\s+oval', description.lower())
    num_ovals = int(num_match.group(1)) if num_match else 2
    
    # Extract division and shading info
    div_match = re.search(r'divided into (\d+)', description)
    sections = int(div_match.group(1)) if div_match else 8
    
    shaded_match = re.search(r'(\d+) of the (\d+) sections are shaded', description)
    shaded = int(shaded_match.group(1)) if shaded_match else 4
    
    # Determine color
    color_class = 'shaded-blue' if 'blue' in description.lower() else 'shaded-purple'
    
    html = '\n            <div>'
    for oval_num in range(num_ovals):
        html += '\n                <div class="oval">'
        section_width = 100 / sections
        for i in range(sections):
            shaded_class = color_class if i < shaded else ''
            html += f'\n                    <div class="section {shaded_class}" style="width: {section_width}%;"></div>'
        html += '\n                </div>'
    html += '\n            </div>'
    return html

def generate_arrow_fractions(description):
    """Generate arrows with fraction shading."""
    # Extract number of arrows
    num_match = re.search(r'(\d+)\s+identical\s+arrow', description.lower())
    num_arrows = int(num_match.group(1)) if num_match else 5
    
    # Extract division and shading info
    div_match = re.search(r'divided into (\d+)', description)
    sections = int(div_match.group(1)) if div_match else 8
    
    shaded_match = re.search(r'(\d+) of the (\d+) sections are shaded', description)
    shaded = int(shaded_match.group(1)) if shaded_match else 5
    
    # Determine color
    color_class = 'shaded-blue' if 'blue' in description.lower() else 'shaded-purple'
    
    html = '\n            <div>'
    for arrow_num in range(num_arrows):
        html += '\n                <div class="arrow">'
        section_width = 100 / sections
        for i in range(sections):
            shaded_class = color_class if i < shaded else ''
            html += f'\n                    <div class="section {shaded_class}" style="width: {section_width}%;"></div>'
        html += '\n                </div>'
    html += '\n            </div>'
    return html

def generate_number_line(description):
    """Generate a number line based on description."""
    html = '\n            <div class="number-line">\n                <div class="line"></div>'
    
    # Extract range from description if possible
    numbers = re.findall(r'\d+(?:\.\d+)?', description)
    
    if numbers:
        start = 0
        end = float(numbers[-1]) if numbers else 10
        num_ticks = min(11, int(end - start + 1))
        
        for i in range(num_ticks):
            position = (i / (num_ticks - 1)) * 100 if num_ticks > 1 else 50
            value = start + (end - start) * i / (num_ticks - 1) if num_ticks > 1 else start
            html += f'\n                <div class="tick" style="left: {position}%;"></div>'
            html += f'\n                <div class="tick-label" style="left: {position}%;">{value:.1f}</div>'
    else:
        # Default number line 0-10
        for i in range(11):
            position = i * 10
            html += f'\n                <div class="tick" style="left: {position}%;"></div>'
            html += f'\n                <div class="tick-label" style="left: {position}%;">{i}</div>'
    
    html += '\n            </div>'
    return html

def generate_place_value_chart(description):
    """Generate a place value chart."""
    # Extract the number from description
    numbers = re.findall(r'\d+', description)
    number = numbers[0] if numbers else "000"
    
    # Determine how many places we need
    length = len(number)
    
    html = '\n            <div class="place-value-chart">'
    html += '\n                <div class="place-value-row">'
    
    # Add headers based on number length
    if length >= 5:
        headers = ['Ten Thousands', 'Thousands', 'Hundreds', 'Tens', 'Ones']
        number = number.zfill(5)
    elif length >= 4:
        headers = ['Thousands', 'Hundreds', 'Tens', 'Ones']
        number = number.zfill(4)
    else:
        headers = ['Hundreds', 'Tens', 'Ones']
        number = number.zfill(3)
    
    for header in headers:
        html += f'\n                    <div class="place-value-cell place-value-header">{header}</div>'
    html += '\n                </div>'
    html += '\n                <div class="place-value-row">'
    
    start_index = len(number) - len(headers)
    for i, header in enumerate(headers):
        digit = number[start_index + i] if start_index + i >= 0 else '0'
        html += f'\n                    <div class="place-value-cell">{digit}</div>'
    
    html += '\n                </div>'
    html += '\n            </div>'
    return html

def generate_fraction_circle(description):
    """Generate a circle with fraction shading."""
    # Try to extract fraction from description
    fraction_match = re.search(r'(\d+)/(\d+)', description)
    
    if fraction_match:
        numerator = int(fraction_match.group(1))
        denominator = int(fraction_match.group(2))
        percentage = (numerator / denominator) * 100
    else:
        percentage = 50  # Default to 1/2
    
    html = '\n            <div class="shape circle" style="background: linear-gradient(to right, #4CAF50 0%, #4CAF50 {}%, white {}%, white 100%);">'.format(percentage, percentage)
    html += '\n            </div>'
    return html

def generate_fraction_rectangle(description):
    """Generate a rectangle with fraction shading."""
    fraction_match = re.search(r'(\d+)/(\d+)', description)
    
    if fraction_match:
        numerator = int(fraction_match.group(1))
        denominator = int(fraction_match.group(2))
    else:
        numerator, denominator = 1, 2
    
    html = '\n            <div style="display: inline-block; border: 2px solid #333;">'
    for i in range(denominator):
        color = '#4CAF50' if i < numerator else 'white'
        html += f'\n                <div style="display: inline-block; width: 40px; height: 80px; background-color: {color}; border-right: 1px solid #666;"></div>'
    html += '\n            </div>'
    return html

def generate_counters(description):
    """Generate counter dots."""
    numbers = re.findall(r'\d+', description)
    count = int(numbers[0]) if numbers else 10
    count = min(count, 50)  # Limit to 50 counters
    
    html = '\n            <div style="max-width: 400px;">'
    for i in range(count):
        html += '\n                <div class="counter"></div>'
    html += '\n            </div>'
    return html

def generate_area_model(description):
    """Generate an area model for multiplication."""
    numbers = re.findall(r'\d+', description)
    
    if len(numbers) >= 2:
        rows = min(int(numbers[0]), 10)
        cols = min(int(numbers[1]), 10)
    else:
        rows, cols = 3, 4
    
    html = '\n            <div class="area-model">'
    for r in range(rows):
        html += '\n                <div>'
        for c in range(cols):
            html += '<div class="area-cell"></div>'
        html += '</div>'
    html += '\n            </div>'
    return html

def generate_data_table(description):
    """Generate a data table."""
    html = '\n            <table class="data-table">'
    html += '\n                <thead>'
    html += '\n                    <tr>'
    html += '\n                        <th>Category</th>'
    html += '\n                        <th>Value</th>'
    html += '\n                    </tr>'
    html += '\n                </thead>'
    html += '\n                <tbody>'
    
    # Add sample rows
    for i in range(3):
        html += '\n                    <tr>'
        html += f'\n                        <td>Item {i+1}</td>'
        html += f'\n                        <td>{(i+1)*10}</td>'
        html += '\n                    </tr>'
    
    html += '\n                </tbody>'
    html += '\n            </table>'
    return html

def generate_triangle(description):
    """Generate a triangle shape."""
    html = '\n            <div class="triangle"></div>'
    return html

def generate_grid(description):
    """Generate a grid or array."""
    numbers = re.findall(r'\d+', description)
    
    if numbers:
        size = min(int(numbers[0]), 10)
    else:
        size = 5
    
    html = '\n            <div style="display: inline-block; border: 2px solid #333;">'
    for r in range(size):
        html += '\n                <div>'
        for c in range(size):
            html += '<div style="display: inline-block; width: 30px; height: 30px; border: 1px solid #666;"></div>'
        html += '</div>'
    html += '\n            </div>'
    return html

def process_json_file(json_path):
    """Process a single JSON file and generate HTML files."""
    print(f"Processing: {json_path}")
    
    # Extract week and exercise numbers from filename
    filename = os.path.basename(json_path)
    parts = filename.replace('.json', '').split('_')
    
    if len(parts) < 4:
        print(f"  Skipping - unexpected filename format: {filename}")
        return 0
    
    week_num = parts[1]
    exercise_num = parts[2].replace('E', '')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  Error reading JSON: {e}")
        return 0
    
    html_count = 0
    
    # Check if data has 'quizzes' array
    if 'quizzes' in data:
        quizzes = data['quizzes']
    else:
        # Old format - data itself contains variations
        quizzes = []
        for var_key, variation in data.items():
            if isinstance(variation, dict):
                variation['question_number'] = var_key
                quizzes.append(variation)
    
    # Process each quiz
    for quiz in quizzes:
        if not isinstance(quiz, dict):
            continue
        
        if has_visual_components(quiz):
            # Get question number
            question_num = quiz.get('question_number', '1_1')
            
            # Generate HTML filename with underscore format
            html_filename = f"Gr6_{week_num}_E{exercise_num}_{question_num}.html"
            html_path = os.path.join('html', html_filename)
            
            # Generate HTML content
            html_content = generate_html_content(quiz, week_num, exercise_num)
            
            # Write HTML file
            try:
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Extract and show the actual labels used
                labels = re.findall(r'label="([^"]*)"', html_content)
                if labels:
                    # Check if any are placeholders
                    has_placeholders = any(is_placeholder_tag(label) for label in labels)
                    if has_placeholders:
                        print(f"  WARNING: {html_filename} still has placeholder labels!")
                    else:
                        print(f"  Created: {html_filename} with proper labels: {labels[0]}...")
                else:
                    print(f"  Created: {html_filename}")
                
                html_count += 1
            except Exception as e:
                print(f"  Error writing HTML {html_filename}: {e}")
    
    return html_count

def main():
    """Main function to process all Grade 6 JSON files."""
    # Find all Grade 6 JSON files
    json_files = glob.glob('Gr6_*_E*_variations.json')
    json_files.sort()
    
    print(f"Found {len(json_files)} Grade 6 JSON files to process\n")
    
    total_html_files = 0
    files_with_placeholders = []
    
    for json_file in json_files:
        count = process_json_file(json_file)
        total_html_files += count
    
    print(f"\n{'='*50}")
    print(f"Total HTML files generated: {total_html_files}")
    print(f"All files saved in: html/")
    print(f"{'='*50}")
    
    # Verify label format in generated files
    print("\nVerifying label format in generated HTML files...")
    verify_labels()

def verify_labels():
    """Verify that labels use actual tag values, not placeholder names."""
    html_files = glob.glob('html/Gr6_*.html')
    
    if not html_files:
        print("No HTML files found to verify")
        return
    
    issues_found = 0
    good_files = 0
    
    print(f"\nChecking {len(html_files)} HTML files...")
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract all labels
        labels = re.findall(r'label="([^"]*)"', content)
        
        # Check each label
        has_issue = False
        for label in labels:
            if is_placeholder_tag(label):
                has_issue = True
                break
        
        if has_issue:
            issues_found += 1
            if issues_found <= 5:  # Show first 5 problematic files
                print(f"  Issue: {os.path.basename(html_file)} has placeholder labels")
        else:
            good_files += 1
    
    print(f"\nResults:")
    print(f"  Files with correct labels: {good_files}")
    print(f"  Files with placeholder labels: {issues_found}")
    
    if issues_found == 0:
        print("\nAll labels are properly formatted!")
        print("Example patterns used:")
        print("  - Gr6_24_3_1 (main images)")
        print("  - Gr6_24_3_1_step_1 (solution steps)")
        print("  - Gr6_24_3_1_choice_A (choice options)")
    else:
        print(f"\nWarning: {issues_found} files still have placeholder labels that need manual fixing")

if __name__ == "__main__":
    main()