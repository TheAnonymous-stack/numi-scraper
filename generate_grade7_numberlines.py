import json
import re

# Read the JSON file
with open('Gr7_1_E2_variations.json', 'r') as f:
    data = json.load(f)

def extract_numbers(question_text):
    """Extract the two numbers from the question text"""
    # Find all numbers (including negative) in the question text
    matches = re.findall(r'\$(-?\d+)\$', question_text)
    if len(matches) >= 2:
        return int(matches[0]), int(matches[1])
    return None, None

def generate_number_line_html(num1, num2, image_tag):
    """Generate HTML for a number line with two points marked"""

    # Determine the range for the number line
    min_val = min(num1, num2)
    max_val = max(num1, num2)

    # Add some padding to the range
    range_padding = max(10, abs(max_val - min_val) * 0.3)
    line_min = min_val - range_padding
    line_max = max_val + range_padding

    # Determine tick marks (we'll use nice round numbers)
    if line_max - line_min <= 20:
        tick_interval = 5
    elif line_max - line_min <= 50:
        tick_interval = 10
    elif line_max - line_min <= 100:
        tick_interval = 20
    elif line_max - line_min <= 200:
        tick_interval = 25
    else:
        tick_interval = 50

    # Round the min and max to nearest tick interval
    tick_min = int(line_min // tick_interval) * tick_interval
    tick_max = int((line_max // tick_interval + 1)) * tick_interval

    # Generate tick marks
    ticks = []
    current = tick_min
    while current <= tick_max:
        ticks.append(current)
        current += tick_interval

    # Calculate positions (use 600px width for the line)
    line_width = 600
    def get_position(value):
        return 50 + (value - tick_min) * (line_width - 100) / (tick_max - tick_min)

    # Generate tick HTML
    tick_html = ""
    for tick in ticks:
        pos = get_position(tick)
        tick_html += f'''
            <div class="tick" style="left: {pos}px;"></div>
            <div class="tick-label" style="left: {pos}px;">{tick}</div>'''

    # Generate point HTML
    point1_pos = get_position(num1)
    point2_pos = get_position(num2)

    html = f'''<!DOCTYPE html>
<html>
<head>
    <style>
        .item {{
            display: inline-block;
            margin: 20px;
        }}

        .number-line {{
            position: relative;
            width: {line_width}px;
            height: 100px;
        }}

        .line {{
            position: absolute;
            top: 50px;
            left: 30px;
            right: 30px;
            height: 2px;
            background: black;
        }}

        .arrow-left {{
            position: absolute;
            top: 48px;
            left: 22px;
            width: 0;
            height: 0;
            border-top: 4px solid transparent;
            border-bottom: 4px solid transparent;
            border-right: 8px solid black;
        }}

        .arrow-right {{
            position: absolute;
            top: 48px;
            right: 22px;
            width: 0;
            height: 0;
            border-top: 4px solid transparent;
            border-bottom: 4px solid transparent;
            border-left: 8px solid black;
        }}

        .tick {{
            position: absolute;
            top: 45px;
            width: 2px;
            height: 10px;
            background: black;
        }}

        .tick-label {{
            position: absolute;
            top: 60px;
            font-size: 12px;
            transform: translateX(-50%);
            font-family: Arial, sans-serif;
        }}

        .point {{
            position: absolute;
            top: 46px;
            width: 8px;
            height: 8px;
            background: red;
            border-radius: 50%;
            transform: translateX(-50%);
            z-index: 10;
        }}

        .point-label {{
            position: absolute;
            top: 25px;
            font-size: 14px;
            font-weight: bold;
            color: red;
            transform: translateX(-50%);
            font-family: Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <div class="item" label="{image_tag}">
        <div class="number-line">
            <div class="line"></div>
            <div class="arrow-left"></div>
            <div class="arrow-right"></div>
            {tick_html}

            <!-- Points for {num1} and {num2} -->
            <div class="point" style="left: {point1_pos}px;"></div>
            <div class="point-label" style="left: {point1_pos}px;">{num1}</div>

            <div class="point" style="left: {point2_pos}px;"></div>
            <div class="point-label" style="left: {point2_pos}px;">{num2}</div>
        </div>
    </div>
</body>
</html>'''

    return html

# Process each question
for quiz in data['quizzes']:
    question_text = quiz['question_text']
    image_tag = quiz['image_tag']

    # Extract the two numbers
    num1, num2 = extract_numbers(question_text)

    if num1 is not None and num2 is not None:
        # Generate HTML
        html_content = generate_number_line_html(num1, num2, image_tag)

        # Create filename from image_tag
        filename = f"{image_tag}.html"

        # Write HTML file
        with open(filename, 'w') as f:
            f.write(html_content)

        print(f"Created {filename} for numbers {num1} and {num2}")

print(f"\nGenerated {len(data['quizzes'])} HTML files successfully!")