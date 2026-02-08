import json
import os
from fractions import Fraction

def fix_negative_fractions():
    """Fix negative fraction answers to use Multiple fill in the blank with separate numerator/denominator"""

    # Read the source file
    source_file = 'Gr7_15_E2_variations.json'

    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        return

    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Fixing {len(data['quizzes'])} questions...")

    fixed_count = 0

    for idx, question in enumerate(data['quizzes'], 1):
        correct_ans = question['correct_answers']

        # Check if it's a single answer with a fraction format (e.g., "-11/14", "3/1")
        if len(correct_ans) == 1 and '/' in correct_ans[0]:
            # Parse the fraction
            frac_str = correct_ans[0]
            parts = frac_str.split('/')
            numerator = parts[0]
            denominator = parts[1]

            # Update to Multiple fill in the blank with two answers
            question['question_type'] = 'Multiple fill in the blank'
            question['correct_answers'] = [numerator, denominator]

            print(f"  Fixed question {idx}: {frac_str} -> [{numerator}, {denominator}]")
            fixed_count += 1

        # Also check for whole numbers that should be fractions with denominator 1
        elif len(correct_ans) == 1 and correct_ans[0].lstrip('-').isdigit():
            numerator = correct_ans[0]
            # Only fix if it's not already in the right format
            if numerator != '0':  # Skip division by zero cases
                question['question_type'] = 'Multiple fill in the blank'
                question['correct_answers'] = [numerator, '1']
                print(f"  Fixed question {idx}: {numerator} -> [{numerator}, 1]")
                fixed_count += 1

    # Write both files
    output_files = [
        source_file,
        os.path.join('edited_by_tag', 'Gr7_15_E2', 'Gr7_15_E2_edited.json')
    ]

    for output_file in output_files:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nFixed {output_file}")

    print(f"\nSuccessfully fixed {fixed_count} questions!")

if __name__ == "__main__":
    fix_negative_fractions()
