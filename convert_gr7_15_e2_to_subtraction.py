import json
import os
import re
from fractions import Fraction

def convert_to_subtraction():
    """Convert all questions in Gr7_15_E2 to subtraction questions"""

    # Read the source file
    source_file = 'Gr7_15_E2_variations.json'

    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        return

    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Converting {len(data['quizzes'])} questions to subtraction...")

    for idx, question in enumerate(data['quizzes'], 1):
        q_text = question['question_text']

        # Extract the fractions from the question
        # Pattern: Operation.\n\n$fraction1 operator fraction2$ = ?
        match = re.search(r'\$\\frac\{(\d+)\}\{(\d+)\}\s*([+\-×\\times]+)\s*\\frac\{(\d+)\}\{(\d+)\}\$', q_text)

        if not match:
            # Try without the operation text prefix
            match = re.search(r'\\frac\{(\d+)\}\{(\d+)\}\s*([+\-×\\times]+)\s*\\frac\{(\d+)\}\{(\d+)\}', q_text)

        if not match:
            print(f"Could not parse question {idx}: {q_text[:80]}...")
            continue

        num1, den1, operator, num2, den2 = match.groups()

        # Convert to integers
        num1, den1, num2, den2 = int(num1), int(den1), int(num2), int(den2)

        # Create fractions
        frac1 = Fraction(num1, den1)
        frac2 = Fraction(num2, den2)

        # Calculate subtraction result (always subtract now)
        result = frac1 - frac2

        # Find LCD
        from math import gcd
        lcd = (den1 * den2) // gcd(den1, den2)

        # Convert fractions to common denominator
        new_num1 = num1 * (lcd // den1)
        new_num2 = num2 * (lcd // den2)
        diff_num = new_num1 - new_num2

        # Update question text to be subtraction
        question['question_text'] = f"Subtract.\n\n$\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}}$ = ?. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

        # Update skill to subtraction
        question['skills'] = 'subtract-fractions-with-unlike-denominators'

        # Update correct answers with the subtraction result
        question['correct_answers'] = [str(abs(result.numerator)), str(result.denominator)]

        # Update solution steps for subtraction
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
                f"So, $\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}}$ is the same as $\\frac{{{new_num1}}}{{{lcd}}} - \\frac{{{new_num2}}}{{{lcd}}}$.\n\nNow subtract: $\\frac{{{new_num1}}}{{{lcd}}} - \\frac{{{new_num2}}}{{{lcd}}} = \\frac{{{diff_num}}}{{{lcd}}}$"
            ],
            [
                "4/4",
                f"Therefore, $\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}} = \\frac{{{diff_num}}}{{{lcd}}} = {abs(result.numerator)}/{result.denominator}$." if diff_num != abs(result.numerator) else f"Therefore, $\\frac{{{num1}}}{{{den1}}} - \\frac{{{num2}}}{{{den2}}} = {abs(result.numerator)}/{result.denominator}$."
            ]
        ]

        print(f"  Question {idx}: {num1}/{den1} - {num2}/{den2} = {abs(result.numerator)}/{result.denominator}")

    # Write both files
    output_files = [
        source_file,
        os.path.join('edited_by_tag', 'Gr7_15_E2', 'Gr7_15_E2_edited.json')
    ]

    for output_file in output_files:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nConverted {output_file}")

    print(f"\nSuccessfully converted all {len(data['quizzes'])} questions to subtraction!")

if __name__ == "__main__":
    convert_to_subtraction()
