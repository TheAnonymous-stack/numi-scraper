import json
import random

def generate_conversion_questions():
    """Generate proper mixed number to improper fraction conversion questions"""

    with open('Gr7_5_E3_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Generate 51 conversion questions
    for i in range(51):
        if i % 2 == 0:
            # Improper fraction to mixed number
            # Generate random improper fraction
            denominator = random.randint(2, 12)
            numerator = random.randint(denominator + 1, denominator * 5)

            # Calculate mixed number
            whole = numerator // denominator
            remainder = numerator % denominator

            question = {
                "skills": "convert-between-mixed-numbers-and-improper-fractions",
                "question_text": f"Write $\\frac{{{numerator}}}{{{denominator}}}$ as a mixed number.\n$\\frac{{{numerator}}}{{{denominator}}}$ = _ _/_",
                "question_type": "Fill in the blank",
                "correct_answers": [f"{whole} {remainder}/{denominator}"],
                "solution": [
                    [
                        "1/3",
                        f"To convert $\\frac{{{numerator}}}{{{denominator}}}$ to a mixed number, divide the numerator by the denominator."
                    ],
                    [
                        "2/3",
                        f"Divide: {numerator} ÷ {denominator} = {whole} with remainder {remainder}.\n\nThis means $\\frac{{{numerator}}}{{{denominator}}}$ equals {whole} whole parts and {remainder} parts left over."
                    ],
                    [
                        "3/3",
                        f"Write the remainder as a fraction over the original denominator: $\\frac{{{remainder}}}{{{denominator}}}$.\n\nSo, $\\frac{{{numerator}}}{{{denominator}}} = {whole}\\frac{{{remainder}}}{{{denominator}}}$."
                    ]
                ],
                "tag": "Gr7_5_E3",
                "question_number": f"3_{i+1}",
                "solution_image_tag": []
            }
        else:
            # Mixed number to improper fraction
            whole = random.randint(1, 8)
            denominator = random.randint(2, 12)
            numerator_part = random.randint(1, denominator - 1)

            # Calculate improper fraction
            improper_numerator = whole * denominator + numerator_part

            question = {
                "skills": "convert-between-mixed-numbers-and-improper-fractions",
                "question_text": f"Convert ${whole}\\frac{{{numerator_part}}}{{{denominator}}}$ to an improper fraction.\n${whole}\\frac{{{numerator_part}}}{{{denominator}}}$ = _/_",
                "question_type": "Fill in the blank",
                "correct_answers": [f"{improper_numerator}/{denominator}"],
                "solution": [
                    [
                        "1/3",
                        f"To convert ${whole}\\frac{{{numerator_part}}}{{{denominator}}}$ to an improper fraction, multiply the whole number by the denominator and add the numerator."
                    ],
                    [
                        "2/3",
                        f"Calculate: ({whole} × {denominator}) + {numerator_part} = {whole * denominator} + {numerator_part} = {improper_numerator}"
                    ],
                    [
                        "3/3",
                        f"Keep the same denominator. So, ${whole}\\frac{{{numerator_part}}}{{{denominator}}} = \\frac{{{improper_numerator}}}{{{denominator}}}$."
                    ]
                ],
                "tag": "Gr7_5_E3",
                "question_number": f"3_{i+1}",
                "solution_image_tag": []
            }

        questions.append(question)

    # Update the data
    data['quizzes'] = questions

    # Write back to file
    with open('Gr7_5_E3_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(questions)} conversion questions for Gr7_5_E3_variations.json")

# Run the fix
generate_conversion_questions()
print("Fixed Gr7_5_E3_variations.json")