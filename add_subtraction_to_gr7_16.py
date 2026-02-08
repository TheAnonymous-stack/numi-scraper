import json
import os
import re
from fractions import Fraction

def add_subtraction_questions():
    """Convert half of the questions to subtraction for Gr7_16_E1 and E2"""

    files_to_process = [
        ('Gr7_16_E1_variations.json', 'Gr7_16_E1', False),
        ('Gr7_16_E2_variations.json', 'Gr7_16_E2', True)
    ]

    for source_file, tag, is_word_problem in files_to_process:
        if not os.path.exists(source_file):
            print(f"Source file not found: {source_file}")
            continue

        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\nProcessing {source_file} with {len(data['quizzes'])} questions...")

        add_count = 0
        subtract_count = 0

        for idx, question in enumerate(data['quizzes'], 1):
            q_text = question['question_text']

            # Convert every other question (even numbered) to subtraction
            should_be_subtraction = (idx % 2 == 0)

            # Extract fractions from question text
            # When reading from JSON, \\frac becomes a single backslash
            fractions = re.findall(r'\$\\\\frac\{(\d+)\}\{(\d+)\}\$', q_text)

            if len(fractions) < 2:
                print(f"Could not find 2 fractions in question {idx}")
                continue

            num1, den1 = map(int, fractions[0])
            num2, den2 = map(int, fractions[1])

            # Create Fraction objects
            frac1 = Fraction(num1, den1)
            frac2 = Fraction(num2, den2)

            # Determine operation and calculate result
            if should_be_subtraction:
                # Make sure frac1 > frac2 to avoid negative results for most cases
                # If frac2 > frac1, swap them
                if frac2 > frac1:
                    num1, den1, num2, den2 = num2, den2, num1, den1
                    frac1, frac2 = frac2, frac1

                operator = '-'
                operation = 'Subtract'
                result = frac1 - frac2
                subtract_count += 1
            else:
                operator = '+'
                operation = 'Add'
                result = frac1 + frac2
                add_count += 1

            # Find LCD
            from math import gcd
            lcd = (den1 * den2) // gcd(den1, den2)

            # Convert fractions to common denominator
            new_num1 = num1 * (lcd // den1)
            new_num2 = num2 * (lcd // den2)

            if operator == '+':
                result_num = new_num1 + new_num2
            else:
                result_num = new_num1 - new_num2

            # Build question text
            if is_word_problem:
                # For word problems, modify the text to reflect the operation
                if should_be_subtraction:
                    # Change "What's the total?" to "What's the difference?"
                    q_text = re.sub(r"What's the total\?", "What's the difference?", q_text)
                    q_text = re.sub(r"altogether\?", "difference?", q_text)
                else:
                    # Ensure it says "total" for addition
                    q_text = re.sub(r"What's the difference\?", "What's the total?", q_text)

                # Update the fractions in the text
                # Replace the two fractions with possibly swapped ones
                frac_pattern = r'\$\\\\frac\{\d+\}\{\d+\}\$'
                fracs_in_text = re.findall(frac_pattern, q_text)
                if len(fracs_in_text) >= 2:
                    q_text = q_text.replace(fracs_in_text[0], f'$\\frac{{{num1}}}{{{den1}}}$', 1)
                    q_text = q_text.replace(fracs_in_text[1], f'$\\frac{{{num2}}}{{{den2}}}$', 1)

                question['question_text'] = q_text
            else:
                # For non-word problems
                question['question_text'] = f"{operation}.\n\n$\\frac{{{num1}}}{{{den1}}} {operator} \\frac{{{num2}}}{{{den2}}}$ = ?. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

            # Update skill
            if is_word_problem:
                if operator == '+':
                    question['skills'] = 'add-fractions-with-unlike-denominators-word-problems'
                else:
                    question['skills'] = 'subtract-fractions-with-unlike-denominators-word-problems'
            else:
                if operator == '+':
                    question['skills'] = 'add-fractions-with-unlike-denominators'
                else:
                    question['skills'] = 'subtract-fractions-with-unlike-denominators'

            # Update correct answers
            if result.denominator == 1:
                question['correct_answers'] = [str(result.numerator), '1']
            else:
                question['correct_answers'] = [str(result.numerator), str(result.denominator)]

            question['question_type'] = 'Multiple fill in the blank'

            # Update solution
            if operator == '+':
                question['solution'] = [
                    [
                        "1/4",
                        f"We are adding $\\frac{{{num1}}}{{{den1}}} + \\frac{{{num2}}}{{{den2}}}$. Since the denominators are different, we need to find a common denominator."
                    ],
                    [
                        "2/4",
                        f"The least common denominator of {den1} and {den2} is {lcd}. Rewrite the fractions using a denominator of {lcd}."
                    ],
                    [
                        "3/4",
                        f"So, $\\frac{{{num1}}}{{{den1}}} + \\frac{{{num2}}}{{{den2}}}$ is the same as $\\frac{{{new_num1}}}{{{lcd}}} + \\frac{{{new_num2}}}{{{lcd}}}$.\n\nNow add: $\\frac{{{new_num1}}}{{{lcd}}} + \\frac{{{new_num2}}}{{{lcd}}} = \\frac{{{result_num}}}{{{lcd}}}$"
                    ],
                    [
                        "4/4",
                        f"Therefore, $\\frac{{{num1}}}{{{den1}}} + \\frac{{{num2}}}{{{den2}}} = {result.numerator}/{result.denominator}$." if result.denominator != 1 else f"Therefore, $\\frac{{{num1}}}{{{den1}}} + \\frac{{{num2}}}{{{den2}}} = {result.numerator}$."
                    ]
                ]
            else:
                question['solution'] = [
                    [
                        "1/4",
                        f"We are subtracting $\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}}$. Since the denominators are different, we need to find a common denominator."
                    ],
                    [
                        "2/4",
                        f"The least common denominator of {den1} and {den2} is {lcd}. Rewrite the fractions using a denominator of {lcd}."
                    ],
                    [
                        "3/4",
                        f"So, $\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}}$ is the same as $\\frac{{{new_num1}}}{{{lcd}}} - \\frac{{{new_num2}}}{{{lcd}}}$.\n\nNow subtract: $\\frac{{{new_num1}}}{{{lcd}}} - \\frac{{{new_num2}}}{{{lcd}}} = \\frac{{{result_num}}}{{{lcd}}}$"
                    ],
                    [
                        "4/4",
                        f"Therefore, $\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}} = {result.numerator}/{result.denominator}$." if result.denominator != 1 else f"Therefore, $\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}} = {result.numerator}$."
                    ]
                ]

            print(f"  Question {idx}: {operation} - {num1}/{den1} {operator} {num2}/{den2} = {result.numerator}/{result.denominator}")

        print(f"\nFixed {source_file}:")
        print(f"  - Add: {add_count} questions")
        print(f"  - Subtract: {subtract_count} questions")

        # Write both files
        output_files = [
            source_file,
            os.path.join('edited_by_tag', tag, f'{tag}_edited.json')
        ]

        for output_file in output_files:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Fixed {output_file}")

if __name__ == "__main__":
    add_subtraction_questions()
