import json
import os
from pathlib import Path
import re

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
        "label_issues": []
    }

    for exercise in exercises:
        json_file = base_path / f"Gr6_{exercise}_variations.json"

        if not json_file.exists():
            print(f"JSON file not found: {json_file}")
            continue

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        exercise_has_visuals = False

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
                # Check corresponding HTML file
                question_number = variation.get('question_number', '')
                if question_number:
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
                    else:
                        # Validate HTML content
                        validate_html_content(html_file, visual_info, report, f"Gr6_{exercise}", question_number)

        if exercise_has_visuals:
            report['exercises_with_visuals'].append(f"Gr6_{exercise}")
        else:
            report['exercises_without_visuals'].append(f"Gr6_{exercise}")

    return report

def validate_html_content(html_file, visual_info, report, exercise, question_number):
    """Validate the content of an HTML file against expected visual elements."""

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

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
        else:
            # Check if it has class="visual-element item"
            div_tag = match.group(0)
            if 'class=' not in div_tag or ('visual-element' not in div_tag and 'item' not in div_tag):
                report['structure_issues'].append({
                    'exercise': exercise,
                    'question_number': question_number,
                    'file': str(html_file),
                    'label': tag,
                    'issue': 'Missing or incorrect class attribute (should have "visual-element item")',
                    'found': div_tag
                })

            # Extract content between div tags
            content_pattern = rf'<div[^>]*\slabel=["\']?{re.escape(tag)}["\']?[^>]*>(.*?)</div>'
            content_match = re.search(content_pattern, html_content, re.IGNORECASE | re.DOTALL)

            if content_match and description:
                html_inner = content_match.group(1).strip()
                # Basic validation - checking if key elements from description are present
                # This is a simplified check - would need more sophisticated matching in production
                if len(description) > 20 and len(html_inner) < 10:
                    report['content_mismatches'].append({
                        'exercise': exercise,
                        'question_number': question_number,
                        'file': str(html_file),
                        'label': tag,
                        'expected_description': description[:100] + '...' if len(description) > 100 else description,
                        'html_snippet': html_inner[:100] + '...' if len(html_inner) > 100 else html_inner,
                        'issue': 'HTML content appears too short for the expected description'
                    })

def print_validation_report(report):
    """Print a comprehensive validation report."""

    print("=" * 80)
    print("GRADE 6 HTML VALIDATION REPORT")
    print("=" * 80)
    print()

    print(f"Total exercises checked: {report['total_exercises']}")
    print(f"Exercises with visual components: {len(report['exercises_with_visuals'])}")
    print(f"Exercises without visual components: {len(report['exercises_without_visuals'])}")
    print()

    if report['exercises_without_visuals']:
        print("Exercises without visual components (no HTML validation needed):")
        for ex in report['exercises_without_visuals']:
            print(f"  - {ex}")
        print()

    if report['missing_html_files']:
        print(f"MISSING HTML FILES ({len(report['missing_html_files'])} issues):")
        print("-" * 40)
        for issue in report['missing_html_files']:
            print(f"  Exercise: {issue['exercise']}")
            print(f"  Question: {issue['question_number']}")
            print(f"  Expected file: {issue['expected_file']}")
            print(f"  Missing tags: {', '.join(issue['visual_tags'])}")
            print()

    if report['label_issues']:
        print(f"MISSING LABELS IN HTML ({len(report['label_issues'])} issues):")
        print("-" * 40)
        for issue in report['label_issues']:
            print(f"  Exercise: {issue['exercise']}, Question: {issue['question_number']}")
            print(f"  File: {issue['file']}")
            print(f"  Missing label: {issue['missing_label']}")
            print(f"  Type: {issue['type']}")
            print()

    if report['structure_issues']:
        print(f"HTML STRUCTURE ISSUES ({len(report['structure_issues'])} issues):")
        print("-" * 40)
        for issue in report['structure_issues']:
            print(f"  Exercise: {issue['exercise']}, Question: {issue['question_number']}")
            print(f"  Label: {issue['label']}")
            print(f"  Issue: {issue['issue']}")
            print()

    if report['content_mismatches']:
        print(f"CONTENT MISMATCHES ({len(report['content_mismatches'])} issues):")
        print("-" * 40)
        for issue in report['content_mismatches']:
            print(f"  Exercise: {issue['exercise']}, Question: {issue['question_number']}")
            print(f"  Label: {issue['label']}")
            print(f"  Issue: {issue['issue']}")
            print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_issues = (len(report['missing_html_files']) +
                   len(report['label_issues']) +
                   len(report['structure_issues']) +
                   len(report['content_mismatches']))

    if total_issues == 0:
        print("All HTML files validated successfully - no issues found!")
    else:
        print(f"WARNING: Total issues found: {total_issues}")
        print(f"  - Missing HTML files: {len(report['missing_html_files'])}")
        print(f"  - Missing labels: {len(report['label_issues'])}")
        print(f"  - Structure issues: {len(report['structure_issues'])}")
        print(f"  - Content mismatches: {len(report['content_mismatches'])}")
        print()
        print("Recommendation: Report these issues to the math-visual-html-generator agent for correction.")

if __name__ == "__main__":
    report = validate_html_for_exercises()
    print_validation_report(report)