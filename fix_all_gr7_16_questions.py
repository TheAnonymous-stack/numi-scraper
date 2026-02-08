import json
import os
import re
from fractions import Fraction

def fix_all_gr7_16():
    """Fix ALL questions in Gr7_16_E1 and E2 - handle fractions and whole numbers"""

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

        print(f"\nFixing ALL {len(data['quizzes'])} questions in {source_file}...")

        add_count = 0
        subtract_count = 0

        for idx, question in enumerate(data['quizzes'], 1):
            q_text = question['question_text']

            # Convert every other question (even numbered) to subtraction
            should_be_subtraction = (idx % 2 == 0)

            # Extract all numbers from question (both fractions and whole numbers)
            # Look for $\frac{a}{b}$ or $a$ patterns
            frac_matches = re.findall(r'\$\\\\frac\{(\d+)\}\{(\d+)\}\$', q_text)
            whole_matches = re.findall(r'\$(\d+)\$', q_text)

            num1 = num2 = den1 = den2 = None

            if len(frac_matches) >= 2:
                # Two fractions
                num1, den1 = map(int, frac_matches[0])
                num2, den2 = map(int, frac_matches[1])
            elif len(frac_matches) == 1 and len(whole_matches) >= 1:
                # One fraction and one whole number
                # Determine order by position in text
                frac_pos = q_text.find(f'$\\\\frac{{{frac_matches[0][0]}}}{{{frac_matches[0][1]}}}$')
                whole_pos = q_text.find(f'${whole_matches[0]}$')

                if frac_pos < whole_pos:
                    num1, den1 = map(int, frac_matches[0])
                    num2, den2 = int(whole_matches[0]), 1
                else:
                    num1, den1 = int(whole_matches[0]), 1
                    num2, den2 = map(int, frac_matches[0])
            elif len(whole_matches) >= 2:
                # Two whole numbers
                num1, den1 = int(whole_matches[0]), 1
                num2, den2 = int(whole_matches[1]), 1
            else:
                print(f"Could not parse question {idx}: {q_text[:80]}...")
                continue

            # Create Fraction objects
            frac1 = Fraction(num1, den1)
            frac2 = Fraction(num2, den2)

            # Determine operation and calculate result
            if should_be_subtraction:
                # Make sure frac1 >= frac2 to avoid negative results
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
                # For word problems, extract the context and update operation
                # Pattern: "A recipe for X uses $...$ cups... Another recipe uses $...$ cups. What's..."

                # Find the context (everything before the question part)
                if 'uses' in q_text and 'cups' in q_text:
                    # Extract the story part
                    parts = q_text.split('.')
                    context_parts = []

                    for i, part in enumerate(parts):
                        if 'What' in part or 'How' in part:
                            break
                        context_parts.append(part)

                    # Rebuild with correct fractions
                    if len(context_parts) >= 2:
                        # Replace numbers in context
                        new_q_text = q_text

                        # Replace all $\frac{...}$ or $...$  with correct values
                        # First occurrence
                        new_q_text = re.sub(
                            r'\$\\\\frac\{\d+\}\{\d+\}\$ cups',
                            f'$\\\\frac{{{num1}}}{{{den1}}}$ cups',
                            new_q_text,
                            count=1
                        )
                        new_q_text = re.sub(
                            r'\$\d+\$ cups',
                            f'$\\\\frac{{{num1}}}{{{den1}}}$ cups',
                            new_q_text,
                            count=1
                        )

                        # Second occurrence
                        new_q_text = re.sub(
                            r'\$\\\\frac\{\d+\}\{\d+\}\$ cups',
                            f'$\\\\frac{{{num2}}}{{{den2}}}$ cups',
                            new_q_text,
                            count=1
                        )
                        new_q_text = re.sub(
                            r'\$\d+\$ cups',
                            f'$\\\\frac{{{num2}}}{{{den2}}}$ cups',
                            new_q_text,
                            count=1
                        )

                        # Update the question part
                        if should_be_subtraction:
                            new_q_text = re.sub(r"What's the total\?", "What's the difference?", new_q_text)
                            new_q_text = re.sub(r"altogether\?", "difference?", new_q_text)
                        else:
                            new_q_text = re.sub(r"What's the difference\?", "What's the total?", new_q_text)

                        question['question_text'] = new_q_text
                    else:
                        question['question_text'] = q_text
                else:
                    question['question_text'] = q_text
            else:
                # For E1 (non-word problems), rebuild with proper format
                question['question_text'] = f"{operation}.\n\n$\\\\frac{{{num1}}}{{{den1}}} {operator} \\\\frac{{{num2}}}{{{den2}}}$ = ?. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

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
                        f"We are adding $\\\\frac{{{num1}}}{{{den1}}} + \\\\frac{{{num2}}}{{{den2}}}$. Since the denominators are different, we need to find a common denominator."
                    ],
                    [
                        "2/4",
                        f"The least common denominator of {den1} and {den2} is {lcd}. Rewrite the fractions using a denominator of {lcd}."
                    ],
                    [
                        "3/4",
                        f"So, $\\\\frac{{{num1}}}{{{den1}}} + \\\\frac{{{num2}}}{{{den2}}}$ is the same as $\\\\frac{{{new_num1}}}{{{lcd}}} + \\\\frac{{{new_num2}}}{{{lcd}}}$.\n\nNow add: $\\\\frac{{{new_num1}}}{{{lcd}}} + \\\\frac{{{new_num2}}}{{{lcd}}} = \\\\frac{{{result_num}}}{{{lcd}}}$"
                    ],
                    [
                        "4/4",
                        f"Therefore, $\\\\frac{{{num1}}}{{{den1}}} + \\\\frac{{{num2}}}{{{den2}}} = {result.numerator}/{result.denominator}$." if result.denominator != 1 else f"Therefore, $\\\\frac{{{num1}}}{{{den1}}} + \\\\frac{{{num2}}}{{{den2}}} = {result.numerator}$."
                    ]
                ]
            else:
                question['solution'] = [
                    [
                        "1/4",
                        f"We are subtracting $\\\\frac{{{num1}}}{{{den1}}} - \\\\frac{{{num2}}}{{{den2}}}$. Since the denominators are different, we need to find a common denominator."
                    ],
                    [
                        "2/4",
                        f"The least common denominator of {den1} and {den2} is {lcd}. Rewrite the fractions using a denominator of {lcd}."
                    ],
                    [
                        "3/4",
                        f"So, $\\\\frac{{{num1}}}{{{den1}}} - \\\\frac{{{num2}}}{{{den2}}}$ is the same as $\\\\frac{{{new_num1}}}{{{lcd}}} - \\\\frac{{{new_num2}}}{{{lcd}}}$.\n\nNow subtract: $\\\\frac{{{new_num1}}}{{{lcd}}} - \\\\frac{{{new_num2}}}{{{lcd}}} = \\\\frac{{{result_num}}}{{{lcd}}}$"
                    ],
                    [
                        "4/4",
                        f"Therefore, $\\\\frac{{{num1}}}{{{den1}}} - \\\\frac{{{num2}}}{{{den2}}} = {result.numerator}/{result.denominator}$." if result.denominator != 1 else f"Therefore, $\\\\frac{{{num1}}}{{{den1}}} - \\\\frac{{{num2}}}{{{den2}}} = {result.numerator}$."
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
    fix_all_gr7_16()
