import json
import os
import re
from fractions import Fraction

def final_fix_gr7_16():
    """Final comprehensive fix for Gr7_16_E1 and E2 - convert all from original format"""

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

            # Extract numbers - look for $a/b$ or $a$ patterns
            frac_pattern = r'\$(\d+)/(\d+)\$'
            whole_pattern = r'\$(\d+)\$'

            fractions = re.findall(frac_pattern, q_text)
            # Remove fractions from whole number search
            temp_text = re.sub(frac_pattern, '', q_text)
            whole_nums = re.findall(whole_pattern, temp_text)

            num1 = num2 = den1 = den2 = None

            if len(fractions) >= 2:
                # Two fractions
                num1, den1 = map(int, fractions[0])
                num2, den2 = map(int, fractions[1])
            elif len(fractions) == 1 and len(whole_nums) >= 1:
                # One fraction and one whole number
                # Determine order by position in original text
                frac_str = f'${fractions[0][0]}/{fractions[0][1]}$'
                whole_str = f'${whole_nums[0]}$'

                if q_text.find(frac_str) < q_text.find(whole_str):
                    num1, den1 = map(int, fractions[0])
                    num2, den2 = int(whole_nums[0]), 1
                else:
                    num1, den1 = int(whole_nums[0]), 1
                    num2, den2 = map(int, fractions[0])
            elif len(whole_nums) >= 2:
                # Two whole numbers
                num1, den1 = int(whole_nums[0]), 1
                num2, den2 = int(whole_nums[1]), 1
            else:
                print(f"Warning: Could not parse question {idx}, skipping...")
                continue

            # Create Fraction objects
            frac1 = Fraction(num1, den1)
            frac2 = Fraction(num2, den2)

            # Determine operation
            if should_be_subtraction:
                # Make sure frac1 >= frac2
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

            result_num = new_num1 + new_num2 if operator == '+' else new_num1 - new_num2

            # Build question text
            if is_word_problem:
                # For word problems, modify the existing text
                # Replace numbers and change question
                new_q_text = q_text

                # Convert fractions to LaTeX format
                new_q_text = re.sub(r'\$(\d+)/(\d+)\$', r'$\\frac{\1}{\2}$', new_q_text)
                new_q_text = re.sub(r'\$(\d+)\$ cups', r'$\\frac{\1}{1}$ cups', new_q_text)

                # Update with correct numbers (in case we swapped for subtraction)
                all_fracs = re.findall(r'\$\\frac\{(\d+)\}\{(\d+)\}\$', new_q_text)
                if len(all_fracs) >= 2:
                    # Replace first fraction
                    new_q_text = re.sub(
                        r'\$\\frac\{\d+\}\{\d+\}\$',
                        f'$\\\\frac{{{num1}}}{{{den1}}}$',
                        new_q_text,
                        count=1
                    )
                    # Replace second fraction
                    new_q_text = re.sub(
                        r'\$\\frac\{\d+\}\{\d+\}\$',
                        f'$\\\\frac{{{num2}}}{{{den2}}}$',
                        new_q_text,
                        count=1
                    )

                # Update question type
                if should_be_subtraction:
                    new_q_text = re.sub(r"What's the total\?", "What's the difference?", new_q_text)
                    new_q_text = re.sub(r"total\?", "difference?", new_q_text)
                else:
                    new_q_text = re.sub(r"What's the difference\?", "What's the total?", new_q_text)
                    new_q_text = re.sub(r"difference\?", "total?", new_q_text)

                # Fix duplicate text and format
                new_q_text = new_q_text.replace('Express your answer in simplest form.', 'Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ ')

                question['question_text'] = new_q_text
            else:
                # For E1 (non-word problems), completely rebuild
                question['question_text'] = f"{operation}.\n\n$\\\\frac{{{num1}}}{{{den1}}} {operator} \\\\frac{{{num2}}}{{{den2}}}$ = ?. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

            # Update skill
            if is_word_problem:
                question['skills'] = f"{operation.lower()}-fractions-with-unlike-denominators-word-problems"
            else:
                question['skills'] = f"{operation.lower()}-fractions-with-unlike-denominators"

            # Update correct answers - always use Multiple fill in the blank format
            question['correct_answers'] = [str(result.numerator), str(result.denominator)]
            question['question_type'] = 'Multiple fill in the blank'

            # Update solution
            question['solution'] = [
                [
                    "1/4",
                    f"We are {operation.lower()}ing $\\\\frac{{{num1}}}{{{den1}}} {operator} \\\\frac{{{num2}}}{{{den2}}}$. Since the denominators are different, we need to find a common denominator."
                ],
                [
                    "2/4",
                    f"The least common denominator of {den1} and {den2} is {lcd}. Rewrite the fractions using a denominator of {lcd}."
                ],
                [
                    "3/4",
                    f"So, $\\\\frac{{{num1}}}{{{den1}}} {operator} \\\\frac{{{num2}}}{{{den2}}}$ is the same as $\\\\frac{{{new_num1}}}{{{lcd}}} {operator} \\\\frac{{{new_num2}}}{{{lcd}}}$.\n\nNow {operation.lower()}: $\\\\frac{{{new_num1}}}{{{lcd}}} {operator} \\\\frac{{{new_num2}}}{{{lcd}}} = \\\\frac{{{result_num}}}{{{lcd}}}$"
                ],
                [
                    "4/4",
                    f"Therefore, $\\\\frac{{{num1}}}{{{den1}}} {operator} \\\\frac{{{num2}}}{{{den2}}} = {result.numerator}/{result.denominator}$." if result.denominator != 1 else f"Therefore, $\\\\frac{{{num1}}}{{{den1}}} {operator} \\\\frac{{{num2}}}{{{den2}}} = {result.numerator}$."
                ]
            ]

            print(f"  Q{idx}: {operation} - {num1}/{den1} {operator} {num2}/{den2} = {result.numerator}/{result.denominator}")

        print(f"\n{source_file} Summary:")
        print(f"  - Add: {add_count} questions")
        print(f"  - Subtract: {subtract_count} questions")
        print(f"  - Total: {add_count + subtract_count} / {len(data['quizzes'])} questions fixed")

        # Write both files
        output_files = [
            source_file,
            os.path.join('edited_by_tag', tag, f'{tag}_edited.json')
        ]

        for output_file in output_files:
            dir_name = os.path.dirname(output_file)
            if dir_name:  # Only create directory if path has a directory component
                os.makedirs(dir_name, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved: {output_file}")

if __name__ == "__main__":
    final_fix_gr7_16()
