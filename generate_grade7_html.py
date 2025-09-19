import json
import os
import glob
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

def generate_html_for_question(question, week_num, exercise_num):
    """Generate HTML content for a question with images"""
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
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }}
        .item {{
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            display: inline-block;
        }}
        svg {{
            display: block;
        }}
        .fraction-model {{
            width: 200px;
            height: 200px;
        }}
        .number-line {{
            width: 600px;
            height: 100px;
        }}
        .area-model {{
            width: 400px;
            height: 300px;
        }}
        .geometric-shape {{
            width: 300px;
            height: 300px;
        }}
        .table {{
            border-collapse: collapse;
            margin: 10px;
        }}
        .table td, .table th {{
            border: 1px solid #333;
            padding: 8px;
            text-align: center;
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
        html_content += generate_visual_component(tag, description, 'main')

    # Process solution_image_tag
    if 'solution_image_tag' in question and question['solution_image_tag']:
        solution_steps = question.get('solution_image_tag', [])
        if isinstance(solution_steps, list):
            for i, step in enumerate(solution_steps, 1):
                if isinstance(step, list) and len(step) >= 3:
                    tag = f"{question['image_tag']}_step_{i}" if 'image_tag' in question else f"solution_step_{i}"
                    description = step[2] if len(step) > 2 else ""
                    html_content += generate_visual_component(tag, description, f'step_{i}')

    # Process image_choice_tags
    if 'image_choice_tags' in question and question['image_choice_tags']:
        choices = question.get('image_choice_tags', [])
        descriptions = question.get('image_choice_tags_backend_description', [])
        for i, (tag, desc) in enumerate(zip(choices, descriptions)):
            if tag:
                html_content += generate_visual_component(tag, desc, f'choice_{chr(65+i)}')

    # Process shape_image_tags
    if 'shape_image_tags' in question and question['shape_image_tags']:
        shapes = question.get('shape_image_tags', [])
        if isinstance(shapes, list):
            for i, shape_info in enumerate(shapes):
                if isinstance(shape_info, dict):
                    tag = shape_info.get('tag', f'shape_{i+1}')
                    description = shape_info.get('backend_description', '')
                    html_content += generate_visual_component(tag, description, f'shape_{i+1}')

    html_content += """
    </div>
</body>
</html>"""

    return html_content

def generate_visual_component(tag, description, component_type):
    """Generate HTML for a specific visual component based on description"""

    # Default SVG component
    html = f"""
        <div class="item" label="{tag}">
            <svg viewBox="0 0 200 200" class="geometric-shape">
                <rect x="10" y="10" width="180" height="180" fill="lightblue" stroke="black" stroke-width="2"/>
                <text x="100" y="100" text-anchor="middle" font-size="14">{component_type}</text>
            </svg>
        </div>
"""

    # Analyze description to determine component type
    desc_lower = description.lower() if description else ""

    if 'fraction' in desc_lower or 'pie' in desc_lower or 'circle' in desc_lower:
        # Generate fraction/pie chart
        html = f"""
        <div class="item" label="{tag}">
            <svg viewBox="0 0 200 200" class="fraction-model">
                <circle cx="100" cy="100" r="80" fill="white" stroke="black" stroke-width="2"/>
                <!-- Fraction visualization will be based on description -->
            </svg>
        </div>
"""
    elif 'number line' in desc_lower:
        # Generate number line
        html = f"""
        <div class="item" label="{tag}">
            <svg viewBox="0 0 600 100" class="number-line">
                <line x1="50" y1="50" x2="550" y2="50" stroke="black" stroke-width="2"/>
                <!-- Number line details based on description -->
            </svg>
        </div>
"""
    elif 'table' in desc_lower or 'grid' in desc_lower:
        # Generate table/grid
        html = f"""
        <div class="item" label="{tag}">
            <table class="table">
                <tr><td>Cell 1</td><td>Cell 2</td></tr>
                <tr><td>Cell 3</td><td>Cell 4</td></tr>
            </table>
        </div>
"""
    elif 'area' in desc_lower or 'rectangle' in desc_lower:
        # Generate area model
        html = f"""
        <div class="item" label="{tag}">
            <svg viewBox="0 0 400 300" class="area-model">
                <rect x="10" y="10" width="380" height="280" fill="lightgray" stroke="black" stroke-width="2"/>
                <!-- Area model details based on description -->
            </svg>
        </div>
"""
    elif 'coordinate' in desc_lower or 'graph' in desc_lower or 'plot' in desc_lower:
        # Generate coordinate plane
        html = f"""
        <div class="item" label="{tag}">
            <svg viewBox="0 0 400 400" class="geometric-shape">
                <!-- Coordinate axes -->
                <line x1="200" y1="20" x2="200" y2="380" stroke="black" stroke-width="2"/>
                <line x1="20" y1="200" x2="380" y2="200" stroke="black" stroke-width="2"/>
                <!-- Grid lines -->
                <g stroke="lightgray" stroke-width="0.5">
                    <!-- Vertical grid lines -->
                    <line x1="40" y1="20" x2="40" y2="380"/>
                    <line x1="80" y1="20" x2="80" y2="380"/>
                    <line x1="120" y1="20" x2="120" y2="380"/>
                    <line x1="160" y1="20" x2="160" y2="380"/>
                    <line x1="240" y1="20" x2="240" y2="380"/>
                    <line x1="280" y1="20" x2="280" y2="380"/>
                    <line x1="320" y1="20" x2="320" y2="380"/>
                    <line x1="360" y1="20" x2="360" y2="380"/>
                    <!-- Horizontal grid lines -->
                    <line x1="20" y1="40" x2="380" y2="40"/>
                    <line x1="20" y1="80" x2="380" y2="80"/>
                    <line x1="20" y1="120" x2="380" y2="120"/>
                    <line x1="20" y1="160" x2="380" y2="160"/>
                    <line x1="20" y1="240" x2="380" y2="240"/>
                    <line x1="20" y1="280" x2="380" y2="280"/>
                    <line x1="20" y1="320" x2="380" y2="320"/>
                    <line x1="20" y1="360" x2="380" y2="360"/>
                </g>
            </svg>
        </div>
"""
    elif 'triangle' in desc_lower:
        # Generate triangle
        html = f"""
        <div class="item" label="{tag}">
            <svg viewBox="0 0 300 300" class="geometric-shape">
                <polygon points="150,50 50,250 250,250" fill="lightcoral" stroke="black" stroke-width="2"/>
            </svg>
        </div>
"""
    elif 'angle' in desc_lower:
        # Generate angle visualization
        html = f"""
        <div class="item" label="{tag}">
            <svg viewBox="0 0 300 300" class="geometric-shape">
                <line x1="150" y1="150" x2="250" y2="150" stroke="black" stroke-width="2"/>
                <line x1="150" y1="150" x2="200" y2="80" stroke="black" stroke-width="2"/>
                <path d="M 200 150 A 50 50 0 0 0 185 115" stroke="blue" stroke-width="2" fill="none"/>
            </svg>
        </div>
"""

    return html

def process_json_file(json_file_path, output_dir):
    """Process a single JSON file and generate HTML files for questions with images"""
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
                output_filename = f"Gr7_{week_num}_E{exercise_num}_{question_num}.html"
                output_path = os.path.join(output_dir, output_filename)

                # Skip if file already exists
                if os.path.exists(output_path):
                    print(f"Skipping {output_filename} - already exists")
                    continue

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
    # List of files to process for weeks 11-29
    files_to_process = [
        "Gr7_11_E1_variations.json", "Gr7_11_E2_variations.json", "Gr7_11_E3_variations.json",
        "Gr7_12_E1_variations.json", "Gr7_12_E2_variations.json", "Gr7_12_E3_variations.json",
        "Gr7_13_E1_variations.json", "Gr7_13_E2_variations.json",
        "Gr7_14_E1_variations.json", "Gr7_14_E2_variations.json",
        "Gr7_15_E1_variations.json", "Gr7_15_E2_variations.json",
        "Gr7_16_E1_variations.json", "Gr7_16_E2_variations.json",
        "Gr7_17_E1_variations.json", "Gr7_17_E2_variations.json",
        "Gr7_18_E1_variations.json", "Gr7_18_E2_variations.json", "Gr7_18_E3_variations.json",
        "Gr7_19_E1_variations.json", "Gr7_19_E2_variations.json", "Gr7_19_E3_variations.json",
        "Gr7_20_E1_variations.json", "Gr7_20_E2_variations.json", "Gr7_20_E3_variations.json",
        "Gr7_21_E1_variations.json", "Gr7_21_E2_variations.json",
        "Gr7_22_E1_variations.json", "Gr7_22_E2_variations.json", "Gr7_22_E3_variations.json", "Gr7_22_E4_variations.json",
        "Gr7_23_E1_variations.json", "Gr7_23_E2_variations.json", "Gr7_23_E3_variations.json",
        "Gr7_24_E1_variations.json", "Gr7_24_E2_variations.json", "Gr7_24_E3_variations.json",
        "Gr7_25_E1_variations.json", "Gr7_25_E2_variations.json", "Gr7_25_E3_variations.json",
        "Gr7_25_E4_variations.json", "Gr7_25_E5_variations.json",
        "Gr7_26_E1_variations.json", "Gr7_26_E2_variations.json", "Gr7_26_E3_variations.json",
        "Gr7_26_E4_variations.json", "Gr7_26_E5_variations.json",
        "Gr7_27_E1_variations.json", "Gr7_27_E2_variations.json", "Gr7_27_E3_variations.json", "Gr7_27_E4_variations.json",
        "Gr7_28_E1_variations.json", "Gr7_28_E2_variations.json", "Gr7_28_E3_variations.json",
        "Gr7_29_E1_variations.json", "Gr7_29_E2_variations.json", "Gr7_29_E3_variations.json",
        "Gr7_29_E4_variations.json", "Gr7_29_E5_variations.json"
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
    print(f"Total HTML files generated: {total_generated}")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()