import json
import os
import re

def extract_fractions(question_text):
    """Extract the two fractions from the question text"""
    pattern = r'\\frac\{(\d+)\}\{(\d+)\}\s*x\s*\\frac\{(\d+)\}\{(\d+)\}'
    match = re.search(pattern, question_text)
    if match:
        num1, den1, num2, den2 = match.groups()
        return (int(num1), int(den1)), (int(num2), int(den2))
    return None

def create_fraction_model_html(frac1, frac2, image_tag, question_number):
    """Create an HTML file with the fraction multiplication visual model"""
    num1, den1 = frac1
    num2, den2 = frac2

    # Grid dimensions: denominator2 x denominator1
    cols = den2
    rows = den1
    total_parts = cols * rows

    # Calculate shaded areas
    cols_shaded = num2  # numerator2 columns are shaded
    rows_shaded = num1  # numerator1 rows are double-shaded
    double_shaded = num1 * num2  # intersection

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fraction Model {question_number}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .fraction-text {{
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        svg {{
            border: 2px solid #333;
            background: white;
        }}
    </style>
</head>
<body>
    <div class="item" label="{image_tag}">
        <div class="container">
            <div class="fraction-text">
                {num1}/{den1} × {num2}/{den2}
            </div>
            <svg width="300" height="300" viewBox="0 0 300 300">
                <defs>
                    <pattern id="stripes_{question_number}" patternUnits="userSpaceOnUse" width="8" height="8">
                        <path d="M0,8 L8,0" stroke="#8B4789" stroke-width="2"/>
                    </pattern>
                </defs>

                <!-- Grid lines -->
                <g stroke="#ccc" stroke-width="1">'''

    # Add vertical grid lines
    for i in range(1, cols):
        x = i * 300 / cols
        html += f'''
                    <line x1="{x}" y1="0" x2="{x}" y2="300"/>'''

    # Add horizontal grid lines
    for i in range(1, rows):
        y = i * 300 / rows
        html += f'''
                    <line x1="0" y1="{y}" x2="300" y2="{y}"/>'''

    html += '''
                </g>

                <!-- Shaded regions -->'''

    # Shade the first num2 columns in light purple
    if cols_shaded > 0:
        width = cols_shaded * 300 / cols
        html += f'''
                <rect x="0" y="0" width="{width}" height="300" fill="#E6D4F1" opacity="0.7"/>'''

    # Double-shade the intersection (first num2 columns, first num1 rows)
    if double_shaded > 0:
        width = cols_shaded * 300 / cols
        height = rows_shaded * 300 / rows
        html += f'''
                <rect x="0" y="0" width="{width}" height="{height}" fill="url(#stripes_{question_number})" opacity="0.7"/>'''

    # Add border
    html += '''

                <!-- Border -->
                <rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/>
            </svg>

            <div style="text-align: center; margin-top: 20px; font-size: 18px;">
                = {}/{} = <strong>{}/{}</strong>
            </div>
        </div>
    </div>
</body>
</html>'''.format(double_shaded, total_parts,
                  num1*num2//gcd(num1*num2, den1*den2),
                  den1*den2//gcd(num1*num2, den1*den2))

    return html

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def create_step_html(frac1, frac2, image_tag, step_num, question_number):
    """Create HTML for solution step visuals"""
    num1, den1 = frac1
    num2, den2 = frac2

    if step_num == 1:
        # Step 1: Show just the columns
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Step 1 - {question_number}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        svg {{
            border: 2px solid #333;
            background: white;
        }}
    </style>
</head>
<body>
    <div class="item" label="{image_tag}">
        <div class="container">
            <div style="text-align: center; font-size: 20px; margin-bottom: 15px;">
                Step 1: Show {num2}/{den2}
            </div>
            <svg width="300" height="300" viewBox="0 0 300 300">
                <!-- Vertical lines only -->
                <g stroke="#ccc" stroke-width="1">'''

        for i in range(1, den2):
            x = i * 300 / den2
            html += f'''
                    <line x1="{x}" y1="0" x2="{x}" y2="300"/>'''

        # Shade the first num2 columns
        width = num2 * 300 / den2
        html += f'''
                </g>
                <rect x="0" y="0" width="{width}" height="300" fill="#E6D4F1" opacity="0.7"/>
                <rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
        </div>
    </div>
</body>
</html>'''

    else:  # Step 2: Show the full grid with double shading
        html = create_fraction_model_html(frac1, frac2, image_tag, question_number)

    return html

# Read the JSON file
with open('Gr7_20_E1_variations.json', 'r') as f:
    data = json.load(f)

# Create HTML folder if it doesn't exist
os.makedirs('HTML', exist_ok=True)

# Process each quiz
for quiz in data['quizzes']:
    question_text = quiz['question_text']
    question_number = quiz['question_number']

    # Extract fractions
    fractions = extract_fractions(question_text)
    if fractions:
        frac1, frac2 = fractions

        # Create main visual
        if 'image_tag' in quiz:
            image_tag = quiz['image_tag']
            html = create_fraction_model_html(frac1, frac2, image_tag, question_number)

            # Write HTML file
            filename = f"HTML/Gr7_20_E1_{question_number}.html"
            with open(filename, 'w') as f:
                f.write(html)
            print(f"Created {filename}")

        # Create solution step visuals
        if 'solution_image_tag' in quiz:
            for step_info in quiz['solution_image_tag']:
                if len(step_info) >= 2:
                    step_tag = step_info[1]  # e.g., "Gr7_20_1_1_step_1"

                    # Determine step number from tag
                    if 'step_1' in step_tag:
                        step_html = create_step_html(frac1, frac2, step_tag, 1, question_number)
                    else:
                        step_html = create_step_html(frac1, frac2, step_tag, 2, question_number)

                    # Write step HTML file
                    step_filename = f"HTML/{step_tag}.html"
                    with open(step_filename, 'w') as f:
                        f.write(step_html)
                    print(f"Created {step_filename}")

print(f"\nSuccessfully created HTML files for {len(data['quizzes'])} questions in ./HTML folder")