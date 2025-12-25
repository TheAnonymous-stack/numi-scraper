import json
import os
import re
from pathlib import Path

# Read the Turkish JSON file
with open('scaled_questions_turkish.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build mapping: html_filename -> (tag, question_number)
html_to_question = {}

for quiz in data['quizzes']:
    tag = quiz['tag']
    question_number = quiz['question_number']

    if 'solution_image_tag' in quiz:
        for solution_img in quiz['solution_image_tag']:
            if len(solution_img) >= 2:
                html_filename = solution_img[1]
                html_to_question[html_filename] = (tag, question_number)

print(f"Found {len(html_to_question)} HTML file mappings")

# Translation dictionary
translations = {
    'Long side': 'Uzun kenar',
    'Short side': 'Kısa kenar',
    'Area': 'Alan',
    'Difference': 'Fark',
    'Perimeter': 'Çevre',
    'long side': 'uzun kenar',
    'short side': 'kısa kenar',
    '(long side × short side)': '(uzun kenar × kısa kenar)',
    '(long side x short side)': '(uzun kenar x kısa kenar)',
}

# Get all HTML files in html/ directory
html_dir = Path('html')
html_files = list(html_dir.glob('*.html'))

print(f"Found {len(html_files)} HTML files to process")

# Process each HTML file
processed = 0
for html_file in html_files:
    filename_without_ext = html_file.stem  # e.g., Gr56_2_1_step_2

    # Read the file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get tag and question_number from mapping
    if filename_without_ext in html_to_question:
        tag, question_number = html_to_question[filename_without_ext]
        # Extract step number from filename
        step_match = re.search(r'_(step_\d+)', filename_without_ext)
        if step_match:
            step = step_match.group(1)
            label = f"{tag}_{question_number}_{step}"
        else:
            label = f"{tag}_{question_number}"
    else:
        # If not in mapping, derive from filename
        # e.g., Gr56_1_3_step_3 -> tag: Gr56_1, question_number needs to be inferred
        parts = filename_without_ext.split('_')
        if len(parts) >= 4 and parts[-2] == 'step':
            # Format: Gr56_1_3_step_3
            tag_parts = parts[:-2]  # ['Gr56', '1']
            tag = '_'.join(tag_parts)  # 'Gr56_1'
            number = parts[-3]  # '3'
            step = f"step_{parts[-1]}"  # 'step_3'

            # For Gr56_1_X, we need to find the question_number
            # Check if this HTML is referenced in any question with this tag
            found = False
            for quiz in data['quizzes']:
                if quiz['tag'] == tag:
                    if 'solution_image_tag' in quiz:
                        for solution_img in quiz['solution_image_tag']:
                            if len(solution_img) >= 2 and solution_img[1] == filename_without_ext:
                                question_number = quiz['question_number']
                                label = f"{tag}_{question_number}_{step}"
                                found = True
                                break
                if found:
                    break

            if not found:
                # Fallback: use the number from filename as question_number
                label = f"{tag}_{number}_{step}"
        else:
            print(f"Warning: Could not parse filename {filename_without_ext}")
            continue

    # Translate English text to Turkish
    translated_content = content
    for english, turkish in translations.items():
        translated_content = translated_content.replace(english, turkish)

    # Check if already wrapped in div with label
    if '<div class="item"' not in translated_content:
        # Find the body content to wrap
        body_match = re.search(r'<body>(.*?)</body>', translated_content, re.DOTALL)
        if body_match:
            body_content = body_match.group(1).strip()
            # Wrap in div with label
            new_body_content = f'    <div class="item" label="{label}">\n{body_content}\n    </div>'
            translated_content = translated_content.replace(
                f'<body>{body_match.group(1)}</body>',
                f'<body>\n{new_body_content}\n</body>'
            )
    else:
        # Update existing label if different
        translated_content = re.sub(
            r'<div class="item" label="[^"]*"',
            f'<div class="item" label="{label}"',
            translated_content
        )

    # Write the updated content back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)

    processed += 1
    print(f"Processed {html_file.name} -> label: {label}")

print(f"\nTotal processed: {processed} files")
