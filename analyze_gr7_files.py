import json
import os
import glob
from collections import defaultdict

# Get all Grade 7 JSON files
files = glob.glob('Gr7_*_E*_variations.json')

# Sort files numerically
def extract_numbers(filename):
    parts = filename.replace('.json', '').replace('Gr7_', '').replace('_variations', '').split('_')
    week = int(parts[0]) if parts[0].isdigit() else 999
    exercise = int(parts[1].replace('E', '')) if len(parts) > 1 and parts[1].startswith('E') else 0
    return (week, exercise)

files.sort(key=extract_numbers)

print(f'Total Grade 7 JSON files found: {len(files)}')
print('='*80)

# Analyze each file
files_with_image_tags = []
files_with_format_issues = []
error_files = []

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        has_image_tag = False
        has_format_issue = False
        format_issue_details = []

        # Handle different JSON structures
        variations = []
        if isinstance(data, dict) and 'quizzes' in data:
            variations = data['quizzes']
        elif isinstance(data, list):
            variations = data
        else:
            continue

        # Check all variations for structure
        if variations and len(variations) > 0:
            # Check first few variations
            for idx, var in enumerate(variations[:5] if len(variations) >= 5 else variations):
                if not isinstance(var, dict):
                    continue

                # Check for image tags
                if 'image_tag' in var or 'solution_image_tag' in var:
                    has_image_tag = True

                # Check for answer format issues
                answer = None
                if 'correct_answer' in var:
                    answer = var['correct_answer']
                elif 'correct_answers' in var:
                    answer = var['correct_answers']

                if answer is not None:
                    question_text = var.get('question_text', '').lower() if 'question_text' in var else ''

                    # Check if answer is a list (nested format)
                    if isinstance(answer, list):
                        has_format_issue = True
                        if 'Nested list answer format' not in format_issue_details:
                            format_issue_details.append('Nested list answer format')

                    # Check for mixed number vs improper fraction inconsistency
                    elif isinstance(answer, str):
                        has_fraction = '/' in answer
                        has_mixed = ' ' in answer and '/' in answer

                        # Check if question specifies format
                        specifies_mixed = 'mixed' in question_text or 'mixed number' in question_text
                        specifies_improper = 'improper' in question_text
                        specifies_decimal = 'decimal' in question_text
                        specifies_fraction = ('fraction' in question_text or 'simplest form' in question_text) and not specifies_mixed
                        specifies_format = any([specifies_mixed, specifies_improper, specifies_decimal, specifies_fraction])

                        if has_fraction and not specifies_format:
                            if has_mixed and 'Mixed number format not specified' not in format_issue_details:
                                format_issue_details.append('Mixed number format not specified')
                            elif not has_mixed and 'Fraction format not specified' not in format_issue_details:
                                format_issue_details.append('Fraction format not specified')

                        # Check for decimal answers without specification
                        if '.' in answer and answer.replace('.', '').replace('-', '').isdigit():
                            if not specifies_decimal and 'Decimal format not specified' not in format_issue_details:
                                format_issue_details.append('Decimal format not specified')

            if has_image_tag:
                files_with_image_tags.append(file)

            if format_issue_details:
                files_with_format_issues.append((file, format_issue_details))

    except json.JSONDecodeError as e:
        error_files.append((file, f'JSON decode error: {str(e)}'))
    except Exception as e:
        error_files.append((file, f'Error: {str(e)}'))

# Report findings
print('\n' + '='*80)
print(f'FILES WITH IMAGE TAGS (no actual images exist): {len(files_with_image_tags)}')
print('-'*80)
if files_with_image_tags:
    for i, file in enumerate(files_with_image_tags[:30], 1):
        print(f'  {i:3}. {file}')
    if len(files_with_image_tags) > 30:
        print(f'  ... and {len(files_with_image_tags) - 30} more files')

print('\n' + '='*80)
print(f'FILES WITH ANSWER FORMAT ISSUES: {len(files_with_format_issues)}')
print('-'*80)
if files_with_format_issues:
    for i, (file, issues) in enumerate(files_with_format_issues[:20], 1):
        issue_str = ', '.join(issues)
        print(f'  {i:3}. {file}')
        print(f'       Issues: {issue_str}')
    if len(files_with_format_issues) > 20:
        print(f'  ... and {len(files_with_format_issues) - 20} more files')

if error_files:
    print('\n' + '='*80)
    print(f'FILES WITH ERRORS: {len(error_files)}')
    print('-'*80)
    for file, error in error_files[:10]:
        print(f'  - {file}: {error}')
    if len(error_files) > 10:
        print(f'  ... and {len(error_files) - 10} more files')

# Summary statistics
print('\n' + '='*80)
print('SUMMARY:')
print('-'*80)
print(f'Total files analyzed: {len(files)}')
print(f'Files with image tags: {len(files_with_image_tags)} ({len(files_with_image_tags)*100//len(files) if files else 0}%)')
print(f'Files with format issues: {len(files_with_format_issues)} ({len(files_with_format_issues)*100//len(files) if files else 0}%)')
print(f'Files with errors: {len(error_files)} ({len(error_files)*100//len(files) if files else 0}%)')

# Breakdown of format issues
if files_with_format_issues:
    issue_counts = defaultdict(int)
    for _, issues in files_with_format_issues:
        for issue in issues:
            issue_counts[issue] += 1

    print('\nFormat Issue Breakdown:')
    for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
        print(f'  - {issue}: {count} files')