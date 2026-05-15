import json
import os

def create_tape_diagram_html(question_number, image_tag, backend_description, exercise_info):
    """Create HTML for tape diagram (Gr6_29_E3)"""

    # Parse the description to extract the ratio information
    # Example: "2 blue rectangular sections" and "5 yellow rectangular sections"

    # Default values
    top_sections = 2
    bottom_sections = 5
    top_label = "Item 1"
    bottom_label = "Item 2"

    # Try to extract details from backend_description
    if "bluegills" in backend_description.lower():
        top_label = "bluegills"
        bottom_label = "sunfish"
    elif "chocolate frogs" in backend_description.lower():
        top_label = "chocolate frogs"
        bottom_label = "Bertie Bott's beans"

    # Extract section counts from description
    import re
    top_match = re.search(r'contains (\d+) \w+ rectangular', backend_description)
    if top_match:
        top_sections = int(top_match.group(1))

    # Find the second number for bottom sections
    numbers = re.findall(r'contains (\d+) \w+ rectangular', backend_description)
    if len(numbers) >= 2:
        bottom_sections = int(numbers[1])

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gr6_29_E3_{question_number}</title>
    <style>
        .item {{
            display: inline-block;
            margin: 20px;
            padding: 10px;
            background: white;
        }}
        .tape-diagram {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            font-family: Arial, sans-serif;
        }}
        .tape-row {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .tape-label {{
            width: 120px;
            text-align: right;
            font-size: 14px;
            color: #333;
        }}
        .tape-sections {{
            display: flex;
            gap: 2px;
        }}
        .tape-section {{
            width: 60px;
            height: 40px;
            border: 2px solid #333;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .blue-section {{
            background-color: #87CEEB;
        }}
        .yellow-section {{
            background-color: #FFD700;
        }}
    </style>
</head>
<body>
    <div class="item" label="Gr6_29_E3_{question_number}">
        <div class="item" label="{image_tag}">
            <div class="tape-diagram">
                <div class="tape-row">
                    <div class="tape-label">{top_label}</div>
                    <div class="tape-sections">
                        {"".join(['<div class="tape-section blue-section"></div>' for _ in range(top_sections)])}
                    </div>
                </div>
                <div class="tape-row">
                    <div class="tape-label">{bottom_label}</div>
                    <div class="tape-sections">
                        {"".join(['<div class="tape-section yellow-section"></div>' for _ in range(bottom_sections)])}
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''

    return html_content

def create_bar_model_html(question_number, image_tag, backend_description, exercise_info):
    """Create HTML for bar model diagram (Gr6_31_E3)"""

    # Extract the total value from the description
    total_value = 100  # default
    match = re.search(r'from 0 to (\d+)', backend_description)
    if match:
        total_value = int(match.group(1))

    # Extract what percentage we're solving for
    question_percent = 20  # default
    match = re.search(r'question mark at the (\d+)%', backend_description)
    if match:
        question_percent = int(match.group(1))

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gr6_31_E3_{question_number}</title>
    <style>
        .item {{
            display: inline-block;
            margin: 20px;
            padding: 10px;
            background: white;
        }}
        .bar-model {{
            font-family: Arial, sans-serif;
            width: 520px;
        }}
        .percentage-bar {{
            display: flex;
            margin-bottom: 5px;
        }}
        .percentage-section {{
            width: 100px;
            height: 50px;
            border: 2px solid #333;
            background: linear-gradient(135deg, #ff69b4, #ba55d3);
            position: relative;
        }}
        .percentage-labels {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            font-size: 14px;
            font-weight: bold;
            padding: 0 2px;
        }}
        .value-bar {{
            display: flex;
            margin-top: 10px;
        }}
        .value-section {{
            width: 100px;
            height: 30px;
            border-bottom: 3px solid #333;
            position: relative;
        }}
        .value-labels {{
            display: flex;
            justify-content: space-between;
            margin-top: 5px;
            font-size: 14px;
            padding: 0 2px;
        }}
        .question-mark {{
            position: absolute;
            top: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 20px;
            font-weight: bold;
            color: #ff0000;
        }}
        .highlight-section {{
            background: rgba(255, 255, 0, 0.3);
        }}
    </style>
</head>
<body>
    <div class="item" label="Gr6_31_E3_{question_number}">
        <div class="item" label="{image_tag}">
            <div class="bar-model">
                <div class="percentage-bar">
                    <div class="percentage-section"></div>
                    <div class="percentage-section"></div>
                    <div class="percentage-section"></div>
                    <div class="percentage-section"></div>
                    <div class="percentage-section"></div>
                </div>
                <div class="percentage-labels">
                    <span>0%</span>
                    <span>20%</span>
                    <span>40%</span>
                    <span>60%</span>
                    <span>80%</span>
                    <span>100%</span>
                </div>
                <div class="value-bar">
                    <div class="value-section{' highlight-section' if question_percent <= 20 else ''}">
                        {f'<span class="question-mark">?</span>' if question_percent == 20 else ''}
                    </div>
                    <div class="value-section{' highlight-section' if 20 < question_percent <= 40 else ''}">
                        {f'<span class="question-mark">?</span>' if question_percent == 40 else ''}
                    </div>
                    <div class="value-section{' highlight-section' if 40 < question_percent <= 60 else ''}">
                        {f'<span class="question-mark">?</span>' if question_percent == 60 else ''}
                    </div>
                    <div class="value-section{' highlight-section' if 60 < question_percent <= 80 else ''}">
                        {f'<span class="question-mark">?</span>' if question_percent == 80 else ''}
                    </div>
                    <div class="value-section{' highlight-section' if 80 < question_percent <= 100 else ''}">
                        {f'<span class="question-mark">?</span>' if question_percent == 100 else ''}
                    </div>
                </div>
                <div class="value-labels">
                    <span>0</span>
                    <span>{int(total_value * 0.2)}</span>
                    <span>{int(total_value * 0.4)}</span>
                    <span>{int(total_value * 0.6)}</span>
                    <span>{int(total_value * 0.8)}</span>
                    <span>{total_value}</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''

    return html_content

# Process Gr6_29_E3_variations.json
print("Processing Gr6_29_E3_variations.json...")
with open('C:\\Users\\kapil\\numi-scraper\\Gr6_29_E3_variations.json', 'r') as f:
    data_29 = json.load(f)

import re
for item in data_29:
    if 'image_tag' in item and item['image_tag']:
        question_number = item['question_number']
        image_tag = item['image_tag']
        backend_description = item.get('backend_description', '')

        html_content = create_tape_diagram_html(
            question_number,
            image_tag,
            backend_description,
            {'week': 29, 'exercise': 3}
        )

        filename = f"C:\\Users\\kapil\\numi-scraper\\HTML\\Gr6_29_E3_{question_number}.html"
        with open(filename, 'w') as f:
            f.write(html_content)
        print(f"Created {filename}")

# Process Gr6_31_E3_variations.json
print("\nProcessing Gr6_31_E3_variations.json...")
with open('C:\\Users\\kapil\\numi-scraper\\Gr6_31_E3_variations.json', 'r') as f:
    data_31 = json.load(f)

for item in data_31:
    if 'image_tag' in item and item['image_tag']:
        question_number = item['question_number']
        image_tag = item['image_tag']
        backend_description = item.get('backend_description', '')

        html_content = create_bar_model_html(
            question_number,
            image_tag,
            backend_description,
            {'week': 31, 'exercise': 3}
        )

        filename = f"C:\\Users\\kapil\\numi-scraper\\HTML\\Gr6_31_E3_{question_number}.html"
        with open(filename, 'w') as f:
            f.write(html_content)
        print(f"Created {filename}")

print("\nAll HTML files have been generated successfully!")