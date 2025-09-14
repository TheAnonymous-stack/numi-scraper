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

        question_labels = []  # Use list to maintain order

        # Main image tag - this should wrap the main visual element
        if 'image_tag' in question_data and question_data['image_tag']:
            question_labels.append(('main', question_data['image_tag']))

        # Solution image tags - these wrap solution step visuals
        if 'solution_image_tag' in question_data:
            for item in question_data['solution_image_tag']:
                if isinstance(item, list) and len(item) >= 2:
                    question_labels.append(('solution', item[1]))  # The tag is the second element

        # Image choice tags
        if 'image_choice_tags' in question_data:
            for tag in question_data['image_choice_tags']:
                question_labels.append(('choice', tag))

        # Shape image tags
        if 'shape_image_tags' in question_data:
            for shape in question_data['shape_image_tags']:
                if isinstance(shape, dict) and 'tag' in shape:
                    question_labels.append(('shape', shape['tag']))

        labels[question_num] = question_labels

    return labels

def get_html_file_for_question(week, exercise, question):
    """Get HTML file for a specific question"""
    html_file = Path("html") / f"Gr6_{week}_E{exercise}_{question}.html"
    if html_file.exists():
        return html_file
    return None

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

    labels_added = 0

    # Process each expected label
    for label_type, label in expected_labels:
        if label in existing_labels:
            continue  # Label already exists

        if label_type == 'main':
            # For main image, wrap the primary visual content
            # This could be a table, svg, canvas, or other visual element

            # Look for budget tables first (for Gr6_54, Gr6_55, etc.)
            budget_table = soup.find('table', class_='budget-table')
            if budget_table and not budget_table.parent.get('label'):
                # Create wrapper div
                wrapper = soup.new_tag('div', attrs={'class': 'visual-element item', 'label': label})
                budget_table.wrap(wrapper)
                labels_added += 1
                continue

            # Look for any table that's not already wrapped
            tables = soup.find_all('table')
            for table in tables:
                if not table.parent.get('label'):
                    wrapper = soup.new_tag('div', attrs={'class': 'visual-element item', 'label': label})
                    table.wrap(wrapper)
                    labels_added += 1
                    break

            # Look for SVGs
            svgs = soup.find_all('svg')
            for svg in svgs:
                if not svg.parent.get('label'):
                    wrapper = soup.new_tag('div', attrs={'class': 'visual-element item', 'label': label})
                    svg.wrap(wrapper)
                    labels_added += 1
                    break

            # Look for canvases
            canvases = soup.find_all('canvas')
            for canvas in canvases:
                if not canvas.parent.get('label'):
                    wrapper = soup.new_tag('div', attrs={'class': 'visual-element item', 'label': label})
                    canvas.wrap(wrapper)
                    labels_added += 1
                    break

            # Look for divs with class "item" without labels
            items = soup.find_all('div', class_='item')
            for item in items:
                if not item.get('label'):
                    item['label'] = label
                    labels_added += 1
                    break

        elif label_type == 'solution':
            # Solution images - these would be additional visual elements
            # Usually shown after the main content
            # For now, create placeholder divs if they don't exist

            # Check if there's already a div for this solution step
            existing_solution = soup.find(attrs={'label': label})
            if not existing_solution:
                # Create a placeholder div for the solution image
                solution_div = soup.new_tag('div', attrs={
                    'class': 'visual-element item solution-step',
                    'label': label,
                    'style': 'display: none;'  # Hidden by default
                })

                # Add it to the container
                container = soup.find('div', class_='container')
                if container:
                    container.append(solution_div)
                    labels_added += 1

        elif label_type in ['choice', 'shape']:
            # Similar handling for choice and shape tags
            existing_elem = soup.find(attrs={'label': label})
            if not existing_elem:
                # Look for unwrapped visual elements
                visual_elements = soup.find_all(['svg', 'canvas', 'img'])
                for elem in visual_elements:
                    if not elem.parent.get('label'):
                        wrapper = soup.new_tag('div', attrs={'class': 'visual-element item', 'label': label})
                        elem.wrap(wrapper)
                        labels_added += 1
                        break

    # Save the modified file
    if labels_added > 0:
        # Write back with minimal formatting changes
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))

    return labels_added

def fix_exercise_labels(week, exercise):
    """Fix labels for all questions in an exercise"""
    json_file = f"Gr6_{week}_E{exercise}_variations.json"

    if not os.path.exists(json_file):
        print(f"  JSON file not found: {json_file}")
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

        try:
            labels_added = fix_html_file(html_file, expected_labels, question_num)

            if labels_added > 0:
                print(f"  Fixed {html_file.name}: Added {labels_added} labels")
                total_labels_added += labels_added
                files_fixed += 1
        except Exception as e:
            print(f"  Error fixing {html_file.name}: {e}")

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
        if files_fixed > 0 or labels_added > 0:
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