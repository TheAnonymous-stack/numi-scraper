import json
import re
from fractions import Fraction

def parse_fraction_from_question(question_text):
    """Extract fractions from the question text"""
    # Pattern to match fractions like 5/3, 1/12, etc. or whole numbers
    pattern = r'\$?(\d+/\d+|\d+)\$?\s*×\s*\$?(\d+/\d+|\d+)\$?'
    match = re.search(pattern, question_text)

    if match:
        frac1_str = match.group(1)
        frac2_str = match.group(2)

        # Convert to Fraction objects
        if '/' in frac1_str:
            parts = frac1_str.split('/')
            frac1 = Fraction(int(parts[0]), int(parts[1]))
        else:
            frac1 = Fraction(int(frac1_str), 1)

        if '/' in frac2_str:
            parts = frac2_str.split('/')
            frac2 = Fraction(int(parts[0]), int(parts[1]))
        else:
            frac2 = Fraction(int(frac2_str), 1)

        return frac1, frac2, frac1_str, frac2_str

    return None, None, None, None

def simplify_fraction(frac):
    """Return simplified fraction as a string"""
    if frac.denominator == 1:
        return str(frac.numerator)
    return f"{frac.numerator}/{frac.denominator}"

# Read the file
with open('Gr7_20_E2_variations.json', 'r') as f:
    data = json.load(f)

# Process each quiz
for quiz in data['quizzes']:
    # Parse the fractions from the question
    frac1, frac2, frac1_str, frac2_str = parse_fraction_from_question(quiz['question_text'])

    if frac1 and frac2:
        # Calculate the correct answer
        result = frac1 * frac2

        # Set correct answer in simplest form
        quiz['correct_answers'] = [simplify_fraction(result)]

        # Fix the solution text for each problem
        # Format fractions properly for display
        if '/' in frac1_str:
            parts = frac1_str.split('/')
            frac1_display = f"\\frac{{{parts[0]}}}{{{parts[1]}}}"
        else:
            frac1_display = frac1_str

        if '/' in frac2_str:
            parts = frac2_str.split('/')
            frac2_display = f"\\frac{{{parts[0]}}}{{{parts[1]}}}"
        else:
            frac2_display = frac2_str

        # Update solution text
        quiz['solution'] = [
            [
                "1/4",
                f"We are multiplying two fractions.\\n${frac1_display} \\times {frac2_display}$"
            ],
            [
                "2/4",
                f"First, multiply the numerators.\\n{frac1.numerator} × {frac2.numerator} = {frac1.numerator * frac2.numerator}"
            ],
            [
                "3/4",
                f"Now multiply the denominators:\\n{frac1.denominator} × {frac2.denominator} = {frac1.denominator * frac2.denominator}"
            ],
            [
                "4/4",
                f"So, ${frac1_display} \\times {frac2_display} = \\frac{{{frac1.numerator * frac2.numerator}}}{{{frac1.denominator * frac2.denominator}}}$"
            ]
        ]

        # Add simplification step if needed
        if result.numerator != frac1.numerator * frac2.numerator or result.denominator != frac1.denominator * frac2.denominator:
            quiz['solution'][3][1] += f"\\n\\nSimplified: $\\frac{{{result.numerator}}}{{{result.denominator}}}$"

    # Remove image fields
    if 'image_tag' in quiz:
        del quiz['image_tag']
    if 'backend_description' in quiz:
        del quiz['backend_description']
    if 'solution_image_tag' in quiz:
        del quiz['solution_image_tag']

# Write the updated data back
with open('Gr7_20_E2_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_20_E2_variations.json - {len(data['quizzes'])} entries updated")
print("- Fixed solution text for each problem")
print("- Corrected answers to match actual calculations")
print("- Removed all image fields")