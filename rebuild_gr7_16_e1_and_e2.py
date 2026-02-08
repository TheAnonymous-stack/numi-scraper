import json
import os
import re
from fractions import Fraction

def rebuild_gr7_16_files():
    """Rebuild Gr7_16_E1 and Gr7_16_E2 with proper formatting"""

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

        print(f"\nRebuilding {source_file} with {len(data['quizzes'])} questions...")

        for idx, question in enumerate(data['quizzes'], 1):
            q_text = question['question_text']

            # Extract fractions from question text
            # Pattern 1: $\frac{a}{b} + \frac{c}{d}$
            match = re.search(r'\$\\frac\{(\d+)\}\{(\d+)\}\s*([+\-])\s*\\frac\{(\d+)\}\{(\d+)\}\$', q_text)

            if match:
                # Already proper fractions
                num1, den1, operator, num2, den2 = match.groups()
                num1, den1, num2, den2 = int(num1), int(den1), int(num2), int(den2)
            else:
                # Pattern 2: $a/b$ + $c/d$
                match = re.search(r'\$(\d+)/(\d+)\$\s*([+\-])\s*\$(\d+)/(\d+)\$', q_text)
                if match:
                    num1, den1, operator, num2, den2 = match.groups()
                    num1, den1, num2, den2 = int(num1), int(den1), int(num2), int(den2)
                else:
                    # Pattern 3: $a$ + $b/c$ or $a/b$ + $c$
                    match = re.search(r'\$(\d+)\$\s*([+\-])\s*\$(\d+)/(\d+)\$', q_text)
                    if match:
                        num1 = int(match.group(1))
                        den1 = 1
                        operator = match.group(2)
                        num2 = int(match.group(3))
                        den2 = int(match.group(4))
                    else:
                        match = re.search(r'\$(\d+)/(\d+)\$\s*([+\-])\s*\$(\d+)\$', q_text)
                        if match:
                            num1 = int(match.group(1))
                            den1 = int(match.group(2))
                            operator = match.group(3)
                            num2 = int(match.group(4))
                            den2 = 1
                        else:
                            # Pattern 4: $a$ + $b$
                            match = re.search(r'\$(\d+)\$\s*([+\-])\s*\$(\d+)\$', q_text)
                            if match:
                                num1 = int(match.group(1))
                                den1 = 1
                                operator = match.group(2)
                                num2 = int(match.group(3))
                                den2 = 1
                            else:
                                print(f"Could not parse question {idx}: {q_text[:80]}...")
                                continue

            # Create fractions
            frac1 = Fraction(num1, den1)
            frac2 = Fraction(num2, den2)

            # Calculate result based on operator
            if operator == '+':
                result = frac1 + frac2
                operation = 'Add'
            else:  # operator == '-'
                result = frac1 - frac2
                operation = 'Subtract'

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

            # Update question text to proper format
            question['question_text'] = f"{operation}.\n\n$\\frac{{{num1}}}{{{den1}}} {operator} \\frac{{{num2}}}{{{den2}}}$ = ?. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

            # Update skill based on operation
            if operator == '+':
                question['skills'] = 'add-fractions-with-unlike-denominators'
            else:
                question['skills'] = 'subtract-fractions-with-unlike-denominators'

            # Update question type and correct answers based on result
            if result.denominator == 1:
                # Whole number result = Fill in the blank
                question['question_type'] = 'Fill in the blank'
                question['correct_answers'] = [str(result.numerator)]
            else:
                # Fraction result = Multiple fill in the blank
                question['question_type'] = 'Multiple fill in the blank'
                if result.numerator < 0:
                    question['correct_answers'] = [str(result.numerator), str(result.denominator)]
                else:
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

            print(f"  Question {idx}: {num1}/{den1} {operator} {num2}/{den2} = {result.numerator}/{result.denominator if result.denominator != 1 else ''}")

        # Write both files
        output_files = [
            source_file,
            os.path.join('edited_by_tag', tag, f'{tag}_edited.json')
        ]

        for output_file in output_files:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Rebuilt {output_file}")

        print(f"\nSuccessfully rebuilt {source_file}!")

if __name__ == "__main__":
    rebuild_gr7_16_files()
