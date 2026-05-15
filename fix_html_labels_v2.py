import json
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import sys

def get_expected_labels_from_json(json_file):
    """Extract all expected labels from JSON file"""
    labels = {}  # Map question_number to set of labels for that question

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both formats: direct questions or under 'quizzes' key
    if 'quizzes' in data:
        quizzes = data['quizzes']
    else:
        # Old format where keys are question IDs
        quizzes = []
        for question_id, question_data in data.items():
            question_data['question_number'] = question_id
            quizzes.append(question_data)

    for question_data in quizzes:
        question_num = question_data.get('question_number', '')
        if not question_num:
            continue

        question_labels = set()

        # Main image tag
        if 'image_tag' in question_data and question_data['image_tag']:
            question_labels.add(question_data['image_tag'])

        # Solution image tags
        if 'solution_image_tag' in question_data:
            for item in question_data['solution_image_tag']:
                if isinstance(item, list) and len(item) >= 2:
                    question_labels.add(item[1])  # The tag is the second element

        # Image choice tags
        if 'image_choice_tags' in question_data:
            for tag in question_data['image_choice_tags']:
                question_labels.add(tag)

        # Shape image tags
        if 'shape_image_tags' in question_data:
            for shape in question_data['shape_image_tags']:
                if isinstance(shape, dict) and 'tag' in shape:
                    question_labels.add(shape['tag'])

        labels[question_num] = question_labels

    return labels

def get_html_file_for_question(week, exercise, question):
    """Get HTML file for a specific question"""
    html_file = Path("html") / f"Gr6_{week}_E{exercise}_{question}.html"
    if html_file.exists():
        return html_file
    return None

def wrap_visual_element_with_label(element, label):
    """Wrap a visual element with a div containing the label"""
    wrapper = BeautifulSoup(f'<div class="visual-element item" label="{label}"></div>', 'html.parser')
    wrapper_div = wrapper.find('div')
    element_copy = element.extract()
    wrapper_div.append(element_copy)
    return wrapper_div

def fix_html_file(html_file, expected_labels, question_num):
    """Fix labels in a specific HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Find existing labels
    existing_labels = set()
    elements_with_labels = soup.find_all(attrs={'label': True})
    for elem in elements_with_labels:
        existing_labels.add(elem.get('label'))

    # Find visual elements without label wrappers
    visual_elements = []

    # Find all SVGs
    svgs = soup.find_all('svg')
    for svg in svgs:
        parent = svg.parent
        if not (parent and parent.get('label')):
            visual_elements.append(('svg', svg))

    # Find all canvases
    canvases = soup.find_all('canvas')
    for canvas in canvases:
        parent = canvas.parent
        if not (parent and parent.get('label')):
            visual_elements.append(('canvas', canvas))

    # Find divs with class "item" but no label
    items = soup.find_all('div', class_='item')
    for item in items:
        if not item.get('label'):
            # Check if it contains visual content
            if item.find('svg') or item.find('canvas') or item.find('img'):
                # Already a wrapper, just needs label
                visual_elements.append(('div', item))

    missing_labels = expected_labels - existing_labels

    if not missing_labels and not visual_elements:
        return 0

    labels_added = 0

    # If we have visual elements and missing labels, match them up
    if visual_elements and missing_labels:
        # Sort labels to ensure consistent assignment
        sorted_labels = sorted(list(missing_labels))

        for i, (elem_type, element) in enumerate(visual_elements):
            if i < len(sorted_labels):
                label = sorted_labels[i]

                if elem_type == 'div':
                    # Just add the label to existing div
                    element['label'] = label
                else:
                    # Wrap the element
                    wrapper = wrap_visual_element_with_label(element, label)
                    element.replace_with(wrapper)

                labels_added += 1

    # Save the modified file
    if labels_added > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))

    return labels_added

def fix_exercise_labels(week, exercise):
    """Fix labels for all questions in an exercise"""
    json_file = f"Gr6_{week}_E{exercise}_variations.json"

    if not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        return 0, 0

    # Get expected labels for each question
    labels_by_question = get_expected_labels_from_json(json_file)

    total_labels_added = 0
    files_fixed = 0

    for question_num, expected_labels in labels_by_question.items():
        if not expected_labels:
            continue

        html_file = get_html_file_for_question(week, exercise, question_num)
        if not html_file:
            continue

        labels_added = fix_html_file(html_file, expected_labels, question_num)

        if labels_added > 0:
            print(f"  Fixed {html_file.name}: Added {labels_added} labels")
            total_labels_added += labels_added
            files_fixed += 1

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

    total_files_fixed = 0
    total_labels_added = 0

    print("Fixing critical exercises...")
    for week, exercise in critical_exercises:
        print(f"\nProcessing Gr6_{week}_E{exercise}...")
        files_fixed, labels_added = fix_exercise_labels(week, exercise)
        total_files_fixed += files_fixed
        total_labels_added += labels_added
        print(f"  Summary: {files_fixed} files fixed, {labels_added} labels added")

    print("\n\nFixing additional exercises...")
    for week, exercise in additional_exercises:
        print(f"\nProcessing Gr6_{week}_E{exercise}...")
        files_fixed, labels_added = fix_exercise_labels(week, exercise)
        total_files_fixed += files_fixed
        total_labels_added += labels_added
        if files_fixed > 0:
            print(f"  Summary: {files_fixed} files fixed, {labels_added} labels added")

    print(f"\n\n=== FINAL SUMMARY ===")
    print(f"Total files fixed: {total_files_fixed}")
    print(f"Total labels added: {total_labels_added}")

if __name__ == "__main__":
    main()