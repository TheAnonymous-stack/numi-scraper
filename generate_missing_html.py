import json
import os

def create_html_for_first_question(json_file, html_file):
    """Generate HTML for the first visual question in a JSON file."""

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data.get('quizzes'):
        return False

    first_q = data['quizzes'][0]

    if 'image_tag' not in first_q:
        return False

    image_tag = first_q['image_tag']
    backend_desc = first_q.get('backend_description', 'Visual representation')
    question_num = first_q.get('question_number', '1')

    # Extract exercise info from filename
    parts = os.path.basename(json_file).replace('_variations.json', '').split('_')
    grade = parts[0]
    week = parts[1]
    exercise = parts[2]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{grade}_{week}_{exercise}_1</title>
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
            align-items: flex-start;
        }}
        .item {{
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 5px;
            display: inline-block;
            min-width: 300px;
        }}
        .description {{
            margin-top: 10px;
            font-size: 14px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Main problem visualization -->
        <div class="item" label="{image_tag}">
            <div style="text-align: center; font-size: 18px; padding: 40px; background: #f5f5f5; border-radius: 5px;">
                [Visual Content Placeholder]
            </div>
            <div class="description">
                {backend_desc}
            </div>
        </div>
"""

    # Add solution images if they exist
    if 'solution_image_tag' in first_q and first_q['solution_image_tag']:
        for step in first_q['solution_image_tag']:
            if len(step) >= 3:
                step_tag = step[1]
                step_desc = step[2]
                html_content += f"""
        <div class="item" label="{step_tag}">
            <div style="text-align: center; font-size: 16px; padding: 30px; background: #f9f9f9; border-radius: 5px;">
                [Solution Step Visualization]
            </div>
            <div class="description">
                {step_desc}
            </div>
        </div>
"""

    # Add image choices if they exist
    if 'image_choice_tags' in first_q and first_q['image_choice_tags']:
        descs = first_q.get('image_choice_tags_backend_description', [])
        for i, choice_tag in enumerate(first_q['image_choice_tags']):
            choice_desc = descs[i] if i < len(descs) else 'Choice visualization'
            html_content += f"""
        <div class="item" label="{choice_tag}">
            <div style="text-align: center; font-size: 16px; padding: 30px; background: #f9f9f9; border-radius: 5px;">
                [Choice {chr(65+i)} Visualization]
            </div>
            <div class="description">
                {choice_desc}
            </div>
        </div>
"""

    html_content += """
    </div>
</body>
</html>"""

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return True

# List of files to process
files_to_process = [
    ('Gr7_33_E2_variations.json', 'HTML/Gr7_33_E2_1.html'),
    ('Gr7_33_E3_variations.json', 'HTML/Gr7_33_E3_1.html'),
    ('Gr7_37_E3_variations.json', 'HTML/Gr7_37_E3_1.html'),
    ('Gr7_38_E3_variations.json', 'HTML/Gr7_38_E3_1.html'),
    ('Gr7_38_E4_variations.json', 'HTML/Gr7_38_E4_1.html'),
    ('Gr7_40_E1_variations.json', 'HTML/Gr7_40_E1_1.html'),
    ('Gr7_40_E2_variations.json', 'HTML/Gr7_40_E2_1.html'),
    ('Gr7_41_E2_variations.json', 'HTML/Gr7_41_E2_1.html'),
    ('Gr7_42_E1_variations.json', 'HTML/Gr7_42_E1_1.html'),
    ('Gr7_42_E2_variations.json', 'HTML/Gr7_42_E2_1.html'),
    ('Gr7_42_E3_variations.json', 'HTML/Gr7_42_E3_1.html'),
    ('Gr7_43_E1_variations.json', 'HTML/Gr7_43_E1_1.html'),
    ('Gr7_43_E2_variations.json', 'HTML/Gr7_43_E2_1.html'),
    ('Gr7_43_E3_variations.json', 'HTML/Gr7_43_E3_1.html'),
    ('Gr7_44_E1_variations.json', 'HTML/Gr7_44_E1_1.html'),
    ('Gr7_44_E2_variations.json', 'HTML/Gr7_44_E2_1.html'),
    ('Gr7_45_E1_variations.json', 'HTML/Gr7_45_E1_1.html'),
    ('Gr7_45_E2_variations.json', 'HTML/Gr7_45_E2_1.html'),
    ('Gr7_45_E3_variations.json', 'HTML/Gr7_45_E3_1.html'),
    ('Gr7_45_E4_variations.json', 'HTML/Gr7_45_E4_1.html'),
    ('Gr7_46_E2_variations.json', 'HTML/Gr7_46_E2_1.html'),
    ('Gr7_47_E1_variations.json', 'HTML/Gr7_47_E1_1.html'),
    ('Gr7_47_E3_variations.json', 'HTML/Gr7_47_E3_1.html'),
    ('Gr7_48_E1_variations.json', 'HTML/Gr7_48_E1_1.html'),
    ('Gr7_48_E3_variations.json', 'HTML/Gr7_48_E3_1.html'),
    ('Gr7_49_E1_variations.json', 'HTML/Gr7_49_E1_1.html'),
]

os.chdir('C:/Users/kapil/numi-scraper')

success_count = 0
for json_file, html_file in files_to_process:
    if os.path.exists(json_file):
        if create_html_for_first_question(json_file, html_file):
            print(f"Created: {html_file}")
            success_count += 1
        else:
            print(f"Skipped (no image_tag): {json_file}")
    else:
        print(f"File not found: {json_file}")

print(f"\nTotal files created: {success_count}")