import json
import os
import re
from pathlib import Path

def extract_week_exercise(filename):
    """Extract week number and exercise number from filename"""
    parts = filename.replace('.json', '').split('_')
    if len(parts) >= 3:
        return parts[1], parts[2].replace('E', '')
    return None, None

def has_images(question):
    """Check if question has any image fields"""
    image_fields = ['image_tag', 'solution_image_tag', 'image_choice_tags', 'shape_image_tags']
    return any(field in question and question[field] for field in image_fields)

def generate_counters_visual(description, num_red=0, num_yellow=0):
    """Generate HTML for counter visualizations (common in integer operations)"""
    # Parse description for counter counts
    if description:
        # Look for patterns like "4 red circles" or "2 negative counters"
        red_match = re.search(r'(\d+)\s*(red|negative)\s*(circles?|counters?)', description.lower())
        yellow_match = re.search(r'(\d+)\s*(yellow|positive)\s*(circles?|counters?)', description.lower())

        if red_match:
            num_red = int(red_match.group(1))
        if yellow_match:
            num_yellow = int(yellow_match.group(1))

    # Calculate grid dimensions
    total_counters = num_red + num_yellow
    cols = min(6, total_counters)
    rows = (total_counters + cols - 1) // cols if total_counters > 0 else 1

    svg_width = cols * 50 + 20
    svg_height = rows * 50 + 20

    html = f"""<svg viewBox="0 0 {svg_width} {svg_height}" style="width: {svg_width}px; height: {svg_height}px;">"""

    counter_index = 0
    # Draw red counters (negative)
    for i in range(num_red):
        row = counter_index // cols
        col = counter_index % cols
        cx = col * 50 + 35
        cy = row * 50 + 35
        html += f"""
        <circle cx="{cx}" cy="{cy}" r="18" fill="#ff6b6b" stroke="#cc0000" stroke-width="2"/>
        <line x1="{cx-10}" y1="{cy}" x2="{cx+10}" y2="{cy}" stroke="white" stroke-width="3"/>"""
        counter_index += 1

    # Draw yellow counters (positive)
    for i in range(num_yellow):
        row = counter_index // cols
        col = counter_index % cols
        cx = col * 50 + 35
        cy = row * 50 + 35
        html += f"""
        <circle cx="{cx}" cy="{cy}" r="18" fill="#ffd93d" stroke="#ffb300" stroke-width="2"/>
        <line x1="{cx-10}" y1="{cy}" x2="{cx+10}" y2="{cy}" stroke="#333" stroke-width="3"/>
        <line x1="{cx}" y1="{cy-10}" x2="{cx}" y2="{cy+10}" stroke="#333" stroke-width="3"/>"""
        counter_index += 1

    html += """</svg>"""
    return html

def generate_number_line_visual(description):
    """Generate HTML for number line visualizations"""
    html = """<svg viewBox="0 0 700 150" style="width: 700px; height: 150px;">
        <!-- Main line -->
        <line x1="50" y1="75" x2="650" y2="75" stroke="black" stroke-width="2"/>

        <!-- Tick marks and labels for a standard -10 to 10 number line -->"""

    # Generate tick marks from -10 to 10
    for i in range(-10, 11):
        x = 350 + (i * 30)  # Center at 350, 30 pixels per unit

        # Major tick for integers
        tick_height = 15 if i % 5 == 0 else 10
        html += f"""
        <line x1="{x}" y1="{75-tick_height}" x2="{x}" y2="{75+tick_height}" stroke="black" stroke-width="1"/>
        <text x="{x}" y="105" text-anchor="middle" font-size="12">{i}</text>"""

    # Add arrows
    html += """
        <!-- Arrows -->
        <polygon points="45,75 55,70 55,80" fill="black"/>
        <polygon points="655,75 645,70 645,80" fill="black"/>
    </svg>"""

    return html

def generate_coordinate_plane_visual(description):
    """Generate HTML for coordinate plane visualizations"""
    html = """<svg viewBox="0 0 500 500" style="width: 500px; height: 500px;">
        <!-- Grid lines -->
        <g stroke="#e0e0e0" stroke-width="0.5">"""

    # Vertical grid lines
    for i in range(0, 501, 25):
        html += f"""<line x1="{i}" y1="0" x2="{i}" y2="500"/>"""

    # Horizontal grid lines
    for i in range(0, 501, 25):
        html += f"""<line x1="0" y1="{i}" x2="500" y2="{i}"/>"""

    html += """</g>

        <!-- Axes -->
        <line x1="250" y1="0" x2="250" y2="500" stroke="black" stroke-width="2"/>
        <line x1="0" y1="250" x2="500" y2="250" stroke="black" stroke-width="2"/>

        <!-- Axis labels -->"""

    # X-axis labels
    for i in range(-10, 11, 2):
        if i != 0:
            x = 250 + (i * 25)
            html += f"""<text x="{x}" y="265" text-anchor="middle" font-size="11">{i}</text>"""

    # Y-axis labels
    for i in range(-10, 11, 2):
        if i != 0:
            y = 250 - (i * 25)
            html += f"""<text x="235" y="{y+4}" text-anchor="end" font-size="11">{i}</text>"""

    # Origin label
    html += """<text x="235" y="265" text-anchor="end" font-size="11">0</text>

        <!-- Arrows -->
        <polygon points="250,0 245,10 255,10" fill="black"/>
        <polygon points="500,250 490,245 490,255" fill="black"/>

        <!-- Axis names -->
        <text x="480" y="240" font-size="14" font-style="italic">x</text>
        <text x="260" y="20" font-size="14" font-style="italic">y</text>
    </svg>"""

    return html

def generate_fraction_visual(description):
    """Generate HTML for fraction/pie chart visualizations"""
    # Default to showing a simple fraction representation
    html = """<svg viewBox="0 0 200 200" style="width: 200px; height: 200px;">
        <circle cx="100" cy="100" r="80" fill="white" stroke="black" stroke-width="2"/>"""

    # Try to parse fraction from description
    if description:
        fraction_match = re.search(r'(\d+)/(\d+)', description)
        if fraction_match:
            numerator = int(fraction_match.group(1))
            denominator = int(fraction_match.group(2))

            # Create pie slices for the fraction
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

                # Determine fill color (filled for numerator parts)
                fill_color = "#4a90e2" if i < numerator else "white"

                # Create path for slice
                large_arc = 0 if angle_per_slice <= 180 else 1
                html += f"""
        <path d="M 100 100 L {x1:.2f} {y1:.2f} A 80 80 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z"
              fill="{fill_color}" stroke="black" stroke-width="1"/>"""

    html += """</svg>"""
    return html

def generate_enhanced_visual_component(tag, description, component_type):
    """Generate enhanced HTML for visual components based on description"""

    desc_lower = description.lower() if description else ""

    # Determine component type and generate appropriate visualization
    if 'counter' in desc_lower or ('circle' in desc_lower and ('red' in desc_lower or 'yellow' in desc_lower)):
        visual_html = generate_counters_visual(description)
    elif 'number line' in desc_lower:
        visual_html = generate_number_line_visual(description)
    elif 'coordinate' in desc_lower or 'graph' in desc_lower or 'plane' in desc_lower:
        visual_html = generate_coordinate_plane_visual(description)
    elif 'fraction' in desc_lower or 'pie' in desc_lower:
        visual_html = generate_fraction_visual(description)
    else:
        # Default visualization
        visual_html = """<svg viewBox="0 0 200 200" style="width: 200px; height: 200px;">
            <rect x="10" y="10" width="180" height="180" fill="#f0f0f0" stroke="black" stroke-width="2"/>
            <text x="100" y="100" text-anchor="middle" font-size="14">Visual Component</text>
        </svg>"""

    return f"""
        <div class="item" label="{tag}">
            {visual_html}
        </div>
"""

def generate_html_for_question(question, week_num, exercise_num):
    """Generate HTML content for a question with enhanced images"""
    question_num = question.get('question_number', '1')

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gr7_{week}_E{exercise}_{question}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
        }}
        .item {{
            background: white;
            border: 2px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            display: inline-block;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .item::before {{
            content: attr(label);
            display: block;
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        svg {{
            display: block;
        }}
    </style>
</head>
<body>
    <h1>Grade 7 - Week {week} - Exercise {exercise} - Question {question}</h1>
    <div class="container">
""".format(week=week_num, exercise=exercise_num, question=question_num)

    # Process image_tag
    if 'image_tag' in question and question['image_tag']:
        tag = question['image_tag']
        description = question.get('backend_description', '')
        html_content += generate_enhanced_visual_component(tag, description, 'main')

    # Process solution_image_tag
    if 'solution_image_tag' in question and question['solution_image_tag']:
        solution_steps = question.get('solution_image_tag', [])
        if isinstance(solution_steps, list):
            for i, step in enumerate(solution_steps, 1):
                if isinstance(step, list) and len(step) >= 3:
                    tag = f"{question.get('image_tag', 'solution')}_step_{i}"
                    description = step[2] if len(step) > 2 else ""
                    html_content += generate_enhanced_visual_component(tag, description, f'step_{i}')

    # Process image_choice_tags
    if 'image_choice_tags' in question and question['image_choice_tags']:
        choices = question.get('image_choice_tags', [])
        descriptions = question.get('image_choice_tags_backend_description', [])
        for i, (tag, desc) in enumerate(zip(choices, descriptions)):
            if tag:
                html_content += generate_enhanced_visual_component(tag, desc, f'choice_{chr(65+i)}')

    # Process shape_image_tags
    if 'shape_image_tags' in question and question['shape_image_tags']:
        shapes = question.get('shape_image_tags', [])
        if isinstance(shapes, list):
            for i, shape_info in enumerate(shapes):
                if isinstance(shape_info, dict):
                    tag = shape_info.get('tag', f'shape_{i+1}')
                    description = shape_info.get('backend_description', '')
                    html_content += generate_enhanced_visual_component(tag, description, f'shape_{i+1}')

    html_content += """
    </div>
</body>
</html>"""

    return html_content

# Helper functions for trigonometry (simplified)
def cos(angle):
    import math
    return math.cos(angle)

def sin(angle):
    import math
    return math.sin(angle)

def process_json_file(json_file_path, output_dir):
    """Process a single JSON file and generate enhanced HTML files"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        filename = os.path.basename(json_file_path)
        week_num, exercise_num = extract_week_exercise(filename)

        if not week_num or not exercise_num:
            print(f"Could not extract week/exercise from {filename}")
            return 0

        generated_count = 0

        # Handle nested structure with 'quizzes' key
        if isinstance(data, dict) and 'quizzes' in data:
            questions = data['quizzes']
        elif isinstance(data, list):
            questions = data
        else:
            questions = [data]

        print(f"  Found {len(questions)} questions in {filename}")

        for question in questions:
            if has_images(question):
                question_num = question.get('question_number', '1')
                output_filename = f"Gr7_{week_num}_E{exercise_num}_{question_num}_enhanced.html"
                output_path = os.path.join(output_dir, output_filename)

                html_content = generate_html_for_question(question, week_num, exercise_num)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                print(f"Generated {output_filename}")
                generated_count += 1

        return generated_count

    except Exception as e:
        print(f"Error processing {json_file_path}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 0

def main():
    # Process a sample of files to demonstrate enhanced visualization
    files_to_process = [
        "Gr7_11_E1_variations.json",  # Has counter visualizations
        "Gr7_12_E1_variations.json",  # May have number lines
        "Gr7_20_E1_variations.json",  # May have coordinate planes
    ]

    output_dir = "C:/Users/kapil/numi-scraper/HTML"
    os.makedirs(output_dir, exist_ok=True)

    total_generated = 0

    for filename in files_to_process:
        json_path = f"C:/Users/kapil/numi-scraper/{filename}"
        if os.path.exists(json_path):
            print(f"\nProcessing {filename}...")
            count = process_json_file(json_path, output_dir)
            total_generated += count
        else:
            print(f"File not found: {filename}")

    print(f"\n{'='*50}")
    print(f"Total enhanced HTML files generated: {total_generated}")
    print(f"Output directory: {output_dir}")
    print("\nNote: Enhanced files have '_enhanced' suffix to distinguish from basic versions")

if __name__ == "__main__":
    main()