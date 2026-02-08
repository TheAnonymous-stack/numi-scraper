import json
import os
import re
from fractions import Fraction

def fix_gr7_16_formatting():
    """Fix Gr7_16_E1 and E2 formatting - keep both add and subtract, just fix LaTeX and text"""

    files_to_process = [
        ('Gr7_16_E1_variations.json', 'Gr7_16_E1'),
        ('Gr7_16_E2_variations.json', 'Gr7_16_E2')
    ]

    for source_file, tag in files_to_process:
        if not os.path.exists(source_file):
            print(f"Source file not found: {source_file}")
            continue

        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\nFixing {source_file} with {len(data['quizzes'])} questions...")

        is_word_problem = 'E2' in tag

        for idx, question in enumerate(data['quizzes'], 1):
            q_text = question['question_text']

            # Determine if it's addition or subtraction from the original question
            # Look for keywords or operators
            has_plus = '+' in q_text or 'total' in q_text.lower() or 'altogether' in q_text.lower() or 'combined' in q_text.lower() or 'Add' in q_text or 'Calculate:' in q_text
            has_minus = '-' in q_text or 'difference' in q_text.lower() or 'Subtract' in q_text or 'more than' in q_text.lower() or 'less than' in q_text.lower()

            # Extract fractions
            fractions_plain = re.findall(r'\$(\d+)/(\d+)\$', q_text)
            fractions_latex = re.findall(r'\$\\frac\{(\d+)\}\{(\d+)\}\$', q_text)
            whole_nums = re.findall(r'\$(\d+)\$', q_text)

            if len(fractions_plain) >= 2:
                num1, den1 = map(int, fractions_plain[0])
                num2, den2 = map(int, fractions_plain[1])
            elif len(fractions_latex) >= 2:
                num1, den1 = map(int, fractions_latex[0])
                num2, den2 = map(int, fractions_latex[1])
            elif len(fractions_plain) == 1 and len(whole_nums) >= 1:
                # Mixed: whole number and fraction
                # Find which comes first
                whole_match = re.search(r'\$(\d+)\$ (cups|=)', q_text)
                frac_match = re.search(r'\$(\d+)/(\d+)\$', q_text)

                if whole_match and frac_match:
                    if whole_match.start() < frac_match.start():
                        num1 = int(whole_match.group(1))
                        den1 = 1
                        num2, den2 = map(int, frac_match.groups())
                    else:
                        num1, den1 = map(int, frac_match.groups())
                        num2 = int(whole_match.group(1))
                        den2 = 1
                else:
                    print(f"Could not parse question {idx}")
                    continue
            elif len(whole_nums) >= 2:
                # Two whole numbers
                num1 = int(whole_nums[0])
                den1 = 1
                num2 = int(whole_nums[1])
                den2 = 1
            else:
                print(f"Could not parse question {idx}")
                continue

            # Determine operator
            if has_minus and not has_plus:
                operator = '-'
                operation = 'Subtract'
            else:
                operator = '+'
                operation = 'Add'

            # Calculate result
            frac1 = Fraction(num1, den1)
            frac2 = Fraction(num2, den2)

            if operator == '+':
                result = frac1 + frac2
            else:
                result = frac1 - frac2

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

            # Build proper question text
            if is_word_problem:
                # For E2, keep the word problem but fix LaTeX and duplicate text
                # Replace $a/b$ with $\frac{a}{b}$
                q_text = re.sub(r'\$(\d+)/(\d+)\$', lambda m: f'$\\\\frac{{{m.group(1)}}}{{{m.group(2)}}}$', q_text)
                # Replace standalone $a$ followed by "cups" with $\frac{a}{1}$
                q_text = re.sub(r'\$(\d+)\$ cups', r'$\\frac{\1}{1}$ cups', q_text)

                # Remove duplicate text
                q_text = q_text.replace('Express your answer in simplest form. Write your answer in simplest terms.', 'Write your answer in simplest terms.')
                q_text = q_text.replace('Express your answer in simplest form.', 'Write your answer in simplest terms.')

                # Ensure proper ending
                if '$\\\\\\\\[1em]$' not in q_text:
                    q_text = q_text.replace('Write your answer in simplest terms.', 'Write your answer in simplest terms. $\\\\\\\\[1em]$')
                if not q_text.endswith('_/_ '):
                    if '\\n\\n_/_ ' not in q_text:
                        q_text = q_text.rstrip() + '\\n\\n_/_ '

                question['question_text'] = q_text

                # Set skill for word problems
                if operator == '+':
                    question['skills'] = 'add-fractions-with-unlike-denominators-word-problems'
                else:
                    question['skills'] = 'subtract-fractions-with-unlike-denominators-word-problems'
            else:
                # For E1, rebuild with proper format
                question['question_text'] = f"{operation}.\n\n$\\frac{{{num1}}}{{{den1}}} {operator} \\frac{{{num2}}}{{{den2}}}$ = ?. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

                # Set skill for non-word problems
                if operator == '+':
                    question['skills'] = 'add-fractions-with-unlike-denominators'
                else:
                    question['skills'] = 'subtract-fractions-with-unlike-denominators'

            # Update question type and correct answers based on result
            if result.denominator == 1:
                # Whole number result = Multiple fill in the blank with denominator 1
                question['question_type'] = 'Multiple fill in the blank'
                question['correct_answers'] = [str(result.numerator), '1']
            else:
                # Fraction result = Multiple fill in the blank
                question['question_type'] = 'Multiple fill in the blank'
                question['correct_answers'] = [str(result.numerator), str(result.denominator)]

            # Update solution steps
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

            print(f"  Question {idx}: {num1}/{den1} {operator} {num2}/{den2} = {result.numerator}/{result.denominator}")

        # Write both files
        output_files = [
            source_file,
            os.path.join('edited_by_tag', tag, f'{tag}_edited.json')
        ]

        for output_file in output_files:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Fixed {output_file}")

        print(f"\nSuccessfully fixed {source_file}!")

if __name__ == "__main__":
    fix_gr7_16_formatting()
