import json
import os
from pathlib import Path

def create_number_line_html(description, tag):
    """Generate HTML for number line visualization"""
    # Parse the description to extract details
    # Example: "A number line from -1 to 6 with tick marks at each integer..."

    html = f'''
    <div class="item" label="{tag}">
        <svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
            <style>
                .number-line {{ stroke: black; stroke-width: 2; }}
                .tick {{ stroke: black; stroke-width: 2; }}
                .number {{ font-size: 14px; text-anchor: middle; }}
                .box {{ fill: white; stroke: black; stroke-width: 1; }}
            </style>

            <!-- Number line -->
            <line x1="50" y1="75" x2="550" y2="75" class="number-line"/>

            <!-- Tick marks and numbers from -1 to 6 -->
            <line x1="50" y1="65" x2="50" y2="85" class="tick"/>
            <text x="50" y="100" class="number">-1</text>

            <line x1="112.5" y1="65" x2="112.5" y2="85" class="tick"/>
            <text x="112.5" y="100" class="number">0</text>

            <line x1="175" y1="65" x2="175" y2="85" class="tick"/>
            <text x="175" y="100" class="number">1</text>

            <line x1="237.5" y1="65" x2="237.5" y2="85" class="tick"/>
            <text x="237.5" y="100" class="number">2</text>

            <line x1="300" y1="65" x2="300" y2="85" class="tick"/>
            <text x="300" y="100" class="number">3</text>

            <line x1="362.5" y1="65" x2="362.5" y2="85" class="tick"/>
            <rect x="347.5" y="60" width="30" height="30" class="box"/>

            <line x1="425" y1="65" x2="425" y2="85" class="tick"/>
            <text x="425" y="100" class="number">5</text>

            <line x1="487.5" y1="65" x2="487.5" y2="85" class="tick"/>
            <text x="487.5" y="100" class="number">6</text>

            <line x1="550" y1="65" x2="550" y2="85" class="tick"/>
        </svg>
    </div>'''
    return html

def process_json_file(json_path, output_dir):
    """Process a single JSON file and generate HTML files for questions with images"""

    # Extract week and exercise numbers from filename
    filename = os.path.basename(json_path)
    parts = filename.replace('_variations.json', '').split('_')
    grade = parts[0]  # Gr7
    week = parts[1]    # week number
    exercise = parts[2]  # Exercise number (E1, E2, etc.)

    # Read JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    quizzes = data.get('quizzes', [])

    for quiz in quizzes:
        # Check if question has image tags
        has_images = False
        html_content = []

        # Get question number
        question_num = quiz.get('question_number', '')

        # Process main image tag
        if 'image_tag' in quiz and quiz['image_tag']:
            has_images = True
            tag = quiz['image_tag']
            description = quiz.get('backend_description', '')
            html_content.append(create_number_line_html(description, tag))

        # Process solution image tags
        if 'solution_image_tag' in quiz and quiz['solution_image_tag']:
            has_images = True
            for step in quiz['solution_image_tag']:
                if len(step) >= 3:
                    tag = step[1]  # The tag is the second element
                    description = step[2]  # The description is the third element
                    html_content.append(create_number_line_html(description, tag))

        # If this question has images, create an HTML file
        if has_images:
            # Create filename according to convention: Gr7_[week]_E[exercise]_[variation_number].html
            variation_num = question_num.split('_')[-1] if '_' in question_num else question_num
            html_filename = f"{grade}_{week}_{exercise}_{variation_num}.html"
            html_path = os.path.join(output_dir, html_filename)

            # Create complete HTML document
            full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{grade} Week {week} Exercise {exercise} Variation {variation_num}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .item {{
            margin: 20px 0;
            display: inline-block;
        }}
    </style>
</head>
<body>
    <h1>{grade} Week {week} Exercise {exercise} - Variation {variation_num}</h1>
    {''.join(html_content)}
</body>
</html>'''

            # Write HTML file
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)

            print(f"Created: {html_filename}")

def main():
    """Main function to process all JSON files"""

    # Create HTML directory if it doesn't exist
    output_dir = Path("HTML")
    output_dir.mkdir(exist_ok=True)

    # List of JSON files to process
    json_files = [
        "Gr7_1_E1_variations.json",
        "Gr7_1_E2_variations.json",
        "Gr7_1_E3_variations.json",
        "Gr7_2_E1_variations.json",
        "Gr7_2_E2_variations.json",
        "Gr7_2_E3_variations.json",
        "Gr7_3_E1_variations.json",
        "Gr7_3_E2_variations.json",
        "Gr7_3_E3_variations.json",
        "Gr7_3_E4_variations.json",
        "Gr7_3_E5_variations.json",
        "Gr7_4_E1_variations.json",
        "Gr7_4_E2_variations.json",
        "Gr7_4_E3_variations.json",
        "Gr7_4_E4_variations.json",
        "Gr7_5_E1_variations.json",
        "Gr7_5_E2_variations.json",
        "Gr7_5_E3_variations.json",
        "Gr7_6_E1_variations.json",
        "Gr7_6_E2_variations.json",
        "Gr7_7_E1_variations.json",
        "Gr7_7_E2_variations.json",
        "Gr7_7_E3_variations.json",
        "Gr7_8_E1_variations.json",
        "Gr7_8_E2_variations.json",
        "Gr7_8_E3_variations.json",
        "Gr7_8_E4_variations.json",
        "Gr7_9_E1_variations.json",
        "Gr7_9_E2_variations.json",
        "Gr7_9_E3_variations.json",
        "Gr7_9_E4_variations.json",
        "Gr7_10_E1_variations.json",
        "Gr7_10_E2_variations.json",
        "Gr7_10_E3_variations.json",
        "Gr7_10_E4_variations.json"
    ]

    # Process each JSON file
    for json_file in json_files:
        json_path = Path(json_file)
        if json_path.exists():
            print(f"\nProcessing {json_file}...")
            try:
                process_json_file(json_path, output_dir)
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
        else:
            print(f"File not found: {json_file}")

if __name__ == "__main__":
    main()