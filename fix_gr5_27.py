import json
import math
from fractions import Fraction

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def simplify_fraction(num, den):
    """Simplify a fraction to lowest terms"""
    if den == 0:
        return num, den
    g = gcd(int(num), int(den))
    return str(num // g), str(den // g)

def process_gr5_27():
    """Process Gr5_27_edited.json to simplify all fractions"""
    filepath = 'edited_by_tag/Gr5_27/Gr5_27_edited.json'

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data.get('quizzes', [])
    simplified_count = 0

    for question in questions:
        correct_answers = question.get('correct_answers', [])

        # Check if it's the "Multiple fill in the blank" format with numerator/denominator
        if (question.get('question_type') == 'Multiple fill in the blank' and
            len(correct_answers) == 2 and
            isinstance(correct_answers[0], str) and
            isinstance(correct_answers[1], str)):

            try:
                num = int(correct_answers[0])
                den = int(correct_answers[1])

                # Simplify the fraction
                simplified_num, simplified_den = simplify_fraction(num, den)

                # Check if it changed
                if simplified_num != correct_answers[0] or simplified_den != correct_answers[1]:
                    print(f"Question {question.get('question_number', '?')}: {num}/{den} -> {simplified_num}/{simplified_den}")
                    question['correct_answers'] = [simplified_num, simplified_den]
                    simplified_count += 1
            except (ValueError, TypeError):
                # Not numeric, skip
                pass

    # Save the updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nTotal fractions simplified: {simplified_count}")
    print(f"File updated: {filepath}")

if __name__ == '__main__':
    process_gr5_27()
