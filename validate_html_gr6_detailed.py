import json
import os
from pathlib import Path
import re
from collections import defaultdict

def validate_html_for_exercises():
    """Validate HTML files for Grade 6 math exercises with visual components."""

    exercises = [
        "54_E3", "55_E1", "1_E4", "1_E5", "2_E1", "3_E4", "5_E1", "3_E2",
        "15_E5", "16_E1", "23_E1", "23_E2", "23_E3", "24_E1", "24_E2", "24_E3",
        "28_E3", "33_E1", "33_E2", "34_E3", "35_E1", "36_E1", "42_E4", "43_E2",
        "44_E1", "44_E2", "44_E3", "45_E2", "45_E4", "50_E1", "50_E2", "51_E1",
        "51_E2", "51_E3", "51_E4", "52_E1", "46_E3", "47_E1", "47_E2", "48_E1"
    ]

    base_path = Path("C:/Users/kapil/numi-scraper")
    html_path = base_path / "HTML"

    report = {
        "total_exercises": len(exercises),
        "exercises_with_visuals": [],
        "exercises_without_visuals": [],
        "missing_html_files": [],
        "structure_issues": [],
        "content_mismatches": [],
        "label_issues": [],
        "empty_divs": [],
        "successful_validations": []
    }

    # Track statistics
    stats = defaultdict(int)

    for exercise in exercises:
        json_file = base_path / f"Gr6_{exercise}_variations.json"

        if not json_file.exists():
            print(f"JSON file not found: {json_file}")
            continue

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        exercise_has_visuals = False
        exercise_questions = []

        # Check each variation (use 'quizzes' for Grade 6)
        for variation_idx, variation in enumerate(data.get('quizzes', data.get('variations', []))):
            has_visual = False
            visual_info = []

            # Check for main image_tag
            if variation.get('image_tag'):
                has_visual = True
                visual_info.append({
                    'type': 'main_image',
                    'tag': variation['image_tag'],
                    'description': variation.get('backend_description', ''),
                    'question_number': variation.get('question_number', ''),
                    'variation_idx': variation_idx
                })

            # Check for image_choice_tags
            if variation.get('image_choice_tags'):
                has_visual = True
                descriptions = variation.get('image_choice_tags_backend_description', [])
                for idx, tag in enumerate(variation['image_choice_tags']):
                    desc = descriptions[idx] if idx < len(descriptions) else ''
                    visual_info.append({
                        'type': 'image_choice',
                        'tag': tag,
                        'description': desc,
                        'question_number': variation.get('question_number', ''),
                        'variation_idx': variation_idx,
                        'choice_idx': idx
                    })

            # Check for shape_image_tags
            if variation.get('shape_image_tags'):
                has_visual = True
                for shape_item in variation['shape_image_tags']:
                    if isinstance(shape_item, dict):
                        visual_info.append({
                            'type': 'shape_image',
                            'tag': shape_item.get('tag', ''),
                            'description': shape_item.get('backend_description', ''),
                            'question_number': variation.get('question_number', ''),
                            'variation_idx': variation_idx
                        })

            # Check for solution_image_tag
            if variation.get('solution_image_tag'):
                has_visual = True
                for sol_item in variation['solution_image_tag']:
                    if isinstance(sol_item, list) and len(sol_item) >= 2:
                        tag = sol_item[1] if len(sol_item) > 1 else ''
                        desc = sol_item[2] if len(sol_item) > 2 else ''
                        visual_info.append({
                            'type': 'solution_image',
                            'tag': tag,
                            'description': desc,
                            'question_number': variation.get('question_number', ''),
                            'variation_idx': variation_idx
                        })

            if has_visual:
                exercise_has_visuals = True
                question_number = variation.get('question_number', '')
                if question_number:
                    exercise_questions.append(question_number)

                    # Try both naming conventions
                    html_file = html_path / f"Gr6_{exercise}_{question_number}.html"
                    if not html_file.exists():
                        # Try with space separator
                        html_file = html_path / f"Gr6_{exercise} {question_number}.html"

                    if not html_file.exists():
                        report['missing_html_files'].append({
                            'exercise': f"Gr6_{exercise}",
                            'question_number': question_number,
                            'expected_file': str(html_file),
                            'visual_tags': [v['tag'] for v in visual_info]
                        })
                        stats['missing_files'] += 1
                    else:
                        # Validate HTML content
                        validate_html_content(html_file, visual_info, report, f"Gr6_{exercise}",
                                           question_number, stats)
                        stats['files_checked'] += 1

        if exercise_has_visuals:
            report['exercises_with_visuals'].append({
                'name': f"Gr6_{exercise}",
                'questions': exercise_questions
            })
        else:
            report['exercises_without_visuals'].append(f"Gr6_{exercise}")

    return report, stats

def validate_html_content(html_file, visual_info, report, exercise, question_number, stats):
    """Validate the content of an HTML file against expected visual elements."""

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    file_has_issues = False

    for visual in visual_info:
        tag = visual['tag']
        description = visual['description']

        # Check if div with label exists
        pattern = rf'<div[^>]*\slabel=["\']?{re.escape(tag)}["\']?[^>]*>'
        match = re.search(pattern, html_content, re.IGNORECASE)

        if not match:
            report['label_issues'].append({
                'exercise': exercise,
                'question_number': question_number,
                'file': str(html_file),
                'missing_label': tag,
                'type': visual['type'],
                'expected_description': description
            })
            stats['missing_labels'] += 1
            file_has_issues = True
        else:
            # Check if it has correct class
            div_tag = match.group(0)
            has_visual_element = 'visual-element' in div_tag
            has_item = 'item' in div_tag

            if not (has_visual_element and has_item):
                report['structure_issues'].append({
                    'exercise': exercise,
                    'question_number': question_number,
                    'file': str(html_file),
                    'label': tag,
                    'issue': f'Missing class attributes (has visual-element: {has_visual_element}, has item: {has_item})',
                    'found': div_tag
                })
                stats['structure_issues'] += 1
                file_has_issues = True

            # Extract content between div tags
            content_pattern = rf'<div[^>]*\slabel=["\']?{re.escape(tag)}["\']?[^>]*>(.*?)</div>'
            content_match = re.search(content_pattern, html_content, re.IGNORECASE | re.DOTALL)

            if content_match:
                html_inner = content_match.group(1).strip()

                # Check for empty divs
                if not html_inner:
                    if description:  # Only report if there's supposed to be content
                        report['empty_divs'].append({
                            'exercise': exercise,
                            'question_number': question_number,
                            'file': str(html_file),
                            'label': tag,
                            'type': visual['type'],
                            'expected_description': description[:100] + '...' if len(description) > 100 else description
                        })
                        stats['empty_divs'] += 1
                        file_has_issues = True
                    else:
                        # Empty div with no description is okay
                        stats['labels_found'] += 1
                else:
                    # Has content - mark as successful
                    stats['labels_found'] += 1
                    if not file_has_issues:
                        report['successful_validations'].append({
                            'exercise': exercise,
                            'question_number': question_number,
                            'label': tag
                        })

def print_validation_report(report, stats):
    """Print a comprehensive validation report."""

    print("=" * 80)
    print("GRADE 6 HTML VALIDATION REPORT")
    print("=" * 80)
    print()

    print("OVERVIEW:")
    print("-" * 40)
    print(f"Total exercises checked: {report['total_exercises']}")
    print(f"Exercises with visual components: {len(report['exercises_with_visuals'])}")
    print(f"Exercises without visual components: {len(report['exercises_without_visuals'])}")
    print(f"HTML files checked: {stats['files_checked']}")
    print(f"Total labels validated: {stats['labels_found'] + stats['missing_labels']}")
    print(f"Labels successfully found: {stats['labels_found']}")
    print()

    # Show exercises with visuals
    if report['exercises_with_visuals']:
        print("EXERCISES WITH VISUAL COMPONENTS:")
        print("-" * 40)
        for ex in report['exercises_with_visuals'][:5]:  # Show first 5
            print(f"  {ex['name']}: {len(ex['questions'])} questions")
        if len(report['exercises_with_visuals']) > 5:
            print(f"  ... and {len(report['exercises_with_visuals']) - 5} more exercises")
        print()

    # Report issues
    if report['missing_html_files']:
        print(f"MISSING HTML FILES ({len(report['missing_html_files'])} issues):")
        print("-" * 40)
        # Group by exercise
        missing_by_exercise = defaultdict(list)
        for issue in report['missing_html_files']:
            missing_by_exercise[issue['exercise']].append(issue['question_number'])

        for exercise, questions in list(missing_by_exercise.items())[:3]:  # Show first 3 exercises
            print(f"  {exercise}: Missing {len(questions)} files")
            print(f"    Questions: {', '.join(questions[:5])}", end='')
            if len(questions) > 5:
                print(f" ... and {len(questions) - 5} more")
            else:
                print()
        if len(missing_by_exercise) > 3:
            print(f"  ... and {len(missing_by_exercise) - 3} more exercises with missing files")
        print()

    if report['label_issues']:
        print(f"MISSING LABELS IN HTML ({len(report['label_issues'])} issues):")
        print("-" * 40)
        # Group by type
        missing_by_type = defaultdict(int)
        for issue in report['label_issues']:
            missing_by_type[issue['type']] += 1

        for label_type, count in missing_by_type.items():
            print(f"  {label_type}: {count} missing labels")

        # Show a few examples
        print("\n  Examples:")
        for issue in report['label_issues'][:3]:
            print(f"    {issue['exercise']}, Q{issue['question_number']}: Missing '{issue['missing_label']}'")
        if len(report['label_issues']) > 3:
            print(f"    ... and {len(report['label_issues']) - 3} more missing labels")
        print()

    if report['empty_divs']:
        print(f"EMPTY DIVS WITH EXPECTED CONTENT ({len(report['empty_divs'])} issues):")
        print("-" * 40)
        # Group by type
        empty_by_type = defaultdict(int)
        for issue in report['empty_divs']:
            empty_by_type[issue['type']] += 1

        for div_type, count in empty_by_type.items():
            print(f"  {div_type}: {count} empty divs")

        # Show a few examples
        print("\n  Examples:")
        for issue in report['empty_divs'][:3]:
            print(f"    {issue['exercise']}, Q{issue['question_number']}: Empty div '{issue['label']}'")
            if issue['expected_description']:
                print(f"      Expected: {issue['expected_description'][:50]}...")
        if len(report['empty_divs']) > 3:
            print(f"    ... and {len(report['empty_divs']) - 3} more empty divs")
        print()

    if report['structure_issues']:
        print(f"HTML STRUCTURE ISSUES ({len(report['structure_issues'])} issues):")
        print("-" * 40)
        for issue in report['structure_issues'][:3]:
            print(f"  {issue['exercise']}, Q{issue['question_number']}: {issue['label']}")
            print(f"    Issue: {issue['issue']}")
        if len(report['structure_issues']) > 3:
            print(f"  ... and {len(report['structure_issues']) - 3} more structure issues")
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_issues = (len(report['missing_html_files']) +
                   len(report['label_issues']) +
                   len(report['structure_issues']) +
                   len(report['empty_divs']))

    if total_issues == 0:
        print("All HTML files validated successfully - no issues found!")
    else:
        print(f"Total issues found: {total_issues}")
        print(f"  - Missing HTML files: {len(report['missing_html_files'])}")
        print(f"  - Missing labels: {len(report['label_issues'])}")
        print(f"  - Empty divs with expected content: {len(report['empty_divs'])}")
        print(f"  - Structure issues: {len(report['structure_issues'])}")
        print()

        # Provide recommendations
        print("RECOMMENDATIONS:")
        print("-" * 40)
        if report['missing_html_files']:
            print("1. Generate missing HTML files for exercises that don't have them")
        if report['label_issues']:
            print("2. Add missing div elements with proper labels to existing HTML files")
        if report['empty_divs']:
            print("3. Generate content for empty divs that should have visual elements")
        if report['structure_issues']:
            print("4. Fix class attributes to include 'visual-element item'")
        print()
        print("Report these issues to the math-visual-html-generator agent for correction.")

if __name__ == "__main__":
    report, stats = validate_html_for_exercises()
    print_validation_report(report, stats)