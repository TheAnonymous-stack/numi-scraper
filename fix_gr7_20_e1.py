import json
from fractions import Fraction

def simplify_fraction(frac_str):
    """Convert a fraction string to its simplest form"""
    if '/' in frac_str:
        parts = frac_str.split('/')
        numerator = int(parts[0])
        denominator = int(parts[1])
        simplified = Fraction(numerator, denominator)
        return f"{simplified.numerator}/{simplified.denominator}"
    return frac_str

# Read the file
with open('Gr7_20_E1_variations.json', 'r') as f:
    data = json.load(f)

# Process each quiz
for quiz in data['quizzes']:
    # Update question text to ask for simplest form
    if "Use the model to solve" in quiz['question_text']:
        quiz['question_text'] = quiz['question_text'].replace(
            "= _",
            "= _ (answer in simplest form)"
        )

    # Fix correct_answers to have only one answer in simplest form
    if 'correct_answers' in quiz and isinstance(quiz['correct_answers'], list):
        if len(quiz['correct_answers']) > 0:
            # Get the first answer (or the simplified one if available)
            first_answer = quiz['correct_answers'][0]

            # Handle nested list structure
            if isinstance(first_answer, list):
                # If there are multiple answers, take the simplified one (usually the second)
                if len(quiz['correct_answers']) > 1 and isinstance(quiz['correct_answers'][1], list):
                    # The second answer is usually the simplified form
                    simplified_answer = quiz['correct_answers'][1][0]
                else:
                    # Otherwise use the first answer and simplify it
                    simplified_answer = simplify_fraction(first_answer[0])
            else:
                # Handle simple string answer
                simplified_answer = simplify_fraction(first_answer)

            # Set correct_answers to a single simplified answer
            quiz['correct_answers'] = [simplified_answer]

# Write the updated data back
with open('Gr7_20_E1_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_20_E1_variations.json - {len(data['quizzes'])} entries updated")
print("- Updated question text to ask for simplest form")
print("- Set correct_answers to single simplified fraction")