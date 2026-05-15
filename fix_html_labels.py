import json
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import sys

def get_expected_labels_from_json(json_file):
    """Extract all expected labels from JSON file"""
    labels = set()

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for question_id, question_data in data.items():
        # Extract base exercise info from filename
        match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', os.path.basename(json_file))
        if not match:
            continue
        week = match.group(1)
        exercise = match.group(2)

        # Main image tag
        if 'image_tag' in question_data and question_data['image_tag']:
            labels.add(question_data['image_tag'])

        # Solution image tags
        if 'solution_image_tag' in question_data:
            for item in question_data['solution_image_tag']:
                if isinstance(item, list) and len(item) >= 2:
                    labels.add(item[1])  # The tag is the second element

        # Image choice tags
        if 'image_choice_tags' in question_data:
            for tag in question_data['image_choice_tags']:
                labels.add(tag)

        # Shape image tags
        if 'shape_image_tags' in question_data:
            for shape in question_data['shape_image_tags']:
                if isinstance(shape, dict) and 'tag' in shape:
                    labels.add(shape['tag'])

    return labels

def get_html_files_for_exercise(week, exercise):
    """Get all HTML files for a specific exercise"""
    pattern = f"Gr6_{week}_E{exercise}_*.html"
    html_dir = Path("html")
    return list(html_dir.glob(pattern))

def analyze_html_file(html_file):
    """Analyze an HTML file and return existing labels and visual elements without labels"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Find all elements with labels
    existing_labels = set()
    elements_with_labels = soup.find_all(attrs={'label': True})
    for elem in elements_with_labels:
        existing_labels.add(elem.get('label'))

    # Find visual elements without label wrappers
    visual_elements_without_labels = []

    # Check SVGs
    svgs = soup.find_all('svg')
    for svg in svgs:
        parent = svg.parent
        if not (parent and parent.get('label')):
            visual_elements_without_labels.append(svg)

    # Check canvases
    canvases = soup.find_all('canvas')
    for canvas in canvases:
        parent = canvas.parent
        if not (parent and parent.get('label')):
            visual_elements_without_labels.append(canvas)

    # Check divs with class "item" but no label
    items = soup.find_all('div', class_='item')
    for item in items:
        if not item.get('label'):
            visual_elements_without_labels.append(item)

    return existing_labels, visual_elements_without_labels, soup

def fix_html_labels(exercise_info):
    """Fix labels for a specific exercise"""
    week, exercise = exercise_info
    json_file = f"Gr6_{week}_E{exercise}_variations.json"

    if not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        return 0, 0

    # Get expected labels from JSON
    expected_labels = get_expected_labels_from_json(json_file)

    # Get HTML files
    html_files = get_html_files_for_exercise(week, exercise)

    total_labels_added = 0
    files_fixed = 0

    for html_file in html_files:
        existing_labels, visual_elements, soup = analyze_html_file(html_file)

        # Find missing labels
        missing_labels = expected_labels - existing_labels

        if missing_labels or visual_elements:
            print(f"\nProcessing {html_file.name}")
            print(f"  Expected labels: {len(expected_labels)}")
            print(f"  Existing labels: {len(existing_labels)}")
            print(f"  Missing labels: {len(missing_labels)}")
            print(f"  Visual elements without labels: {len(visual_elements)}")

            # Here we would add the wrapping logic
            # For now, just count
            if missing_labels:
                files_fixed += 1
                total_labels_added += len(missing_labels)

    return files_fixed, total_labels_added

def main():
    # Critical exercises to fix
    critical_exercises = [
        (54, 3),  # Gr6_54_E3 - Missing 204 labels
        (55, 1),  # Gr6_55_E1 - Missing 204 labels
        (48, 1),  # Gr6_48_E1 - Missing 408 labels
        (23, 1),  # Gr6_23_E1 - Empty divs
        (23, 2),  # Gr6_23_E2 - Empty divs
        (23, 3),  # Gr6_23_E3 - Empty divs
    ]

    # Additional exercises
    additional_exercises = [
        (15, 5), (16, 1), (24, 1), (24, 2), (24, 3), (28, 3),
        (33, 1), (33, 2), (34, 3), (35, 1), (36, 1), (42, 4),
        (43, 2), (44, 1), (44, 2), (44, 3), (45, 2), (45, 4),
        (50, 1), (50, 2), (51, 1), (51, 2), (51, 3), (51, 4),
        (52, 1), (46, 3), (47, 1), (47, 2), (1, 4), (1, 5),
        (2, 1), (3, 4), (5, 1), (3, 2)
    ]

    print("Analyzing critical exercises...")
    for exercise in critical_exercises:
        fix_html_labels(exercise)

    print("\n\nAnalyzing additional exercises...")
    for exercise in additional_exercises:
        fix_html_labels(exercise)

if __name__ == "__main__":
    main()