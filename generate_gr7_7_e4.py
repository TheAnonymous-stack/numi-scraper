import json
import random

def generate_fraction_expressions():
    """Generate 51 varied numerical expressions with fractions and mixed numbers for Gr7_7_E4"""

    questions = []

    # Generate 51 varied questions
    for i in range(51):
        question_type = i % 10

        if question_type == 0:
            # Addition of fractions
            fractions = [
                ("2/3", "1/4", "11/12"),
                ("3/5", "2/7", "31/35"),
                ("1/2", "3/8", "7/8"),
                ("5/6", "1/3", "7/6"),
                ("2/9", "4/5", "46/45")
            ]
            f1, f2, answer = fractions[i % len(fractions)]
            n1, d1 = f1.split('/')
            n2, d2 = f2.split('/')

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n$\\frac{{{n1}}}{{{d1}}} + \\frac{{{n2}}}{{{d2}}} = $ ____\n\nWrite your answer as a fraction in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "To add fractions with different denominators, find the LCD."],
                    ["2/3", f"The LCD of {d1} and {d2} is their least common multiple."],
                    ["3/3", f"After finding common denominators and adding: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        elif question_type == 1:
            # Subtraction of fractions
            fractions = [
                ("5/6", "1/4", "7/12"),
                ("3/4", "2/5", "7/20"),
                ("7/8", "1/3", "13/24"),
                ("4/5", "1/6", "19/30"),
                ("5/7", "1/2", "3/14")
            ]
            f1, f2, answer = fractions[i % len(fractions)]
            n1, d1 = f1.split('/')
            n2, d2 = f2.split('/')

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n$\\frac{{{n1}}}{{{d1}}} - \\frac{{{n2}}}{{{d2}}} = $ ____\n\nWrite your answer as a fraction in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "To subtract fractions with different denominators, find the LCD."],
                    ["2/3", f"The LCD of {d1} and {d2} is their least common multiple."],
                    ["3/3", f"After finding common denominators and subtracting: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        elif question_type == 2:
            # Multiplication of fractions
            fractions = [
                ("2/3", "3/4", "1/2"),
                ("3/5", "5/6", "1/2"),
                ("4/7", "7/8", "1/2"),
                ("2/5", "3/8", "3/20"),
                ("5/9", "3/10", "1/6")
            ]
            f1, f2, answer = fractions[i % len(fractions)]
            n1, d1 = f1.split('/')
            n2, d2 = f2.split('/')

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n$\\frac{{{n1}}}{{{d1}}} \\times \\frac{{{n2}}}{{{d2}}} = $ ____\n\nWrite your answer as a fraction in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "To multiply fractions, multiply the numerators and multiply the denominators."],
                    ["2/3", f"$\\frac{{{n1}}}{{{d1}}} \\times \\frac{{{n2}}}{{{d2}}} = \\frac{{{n1} \\times {n2}}}{{{d1} \\times {d2}}}$"],
                    ["3/3", f"Simplify to lowest terms: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        elif question_type == 3:
            # Division of fractions
            fractions = [
                ("3/4", "1/2", "3/2"),
                ("2/5", "3/10", "4/3"),
                ("5/6", "2/3", "5/4"),
                ("7/8", "3/4", "7/6"),
                ("4/9", "2/3", "2/3")
            ]
            f1, f2, answer = fractions[i % len(fractions)]
            n1, d1 = f1.split('/')
            n2, d2 = f2.split('/')

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n$\\frac{{{n1}}}{{{d1}}} \\div \\frac{{{n2}}}{{{d2}}} = $ ____\n\nWrite your answer as a fraction in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "To divide fractions, multiply by the reciprocal of the divisor."],
                    ["2/3", f"$\\frac{{{n1}}}{{{d1}}} \\div \\frac{{{n2}}}{{{d2}}} = \\frac{{{n1}}}{{{d1}}} \\times \\frac{{{d2}}}{{{n2}}}$"],
                    ["3/3", f"Multiply and simplify: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        elif question_type == 4:
            # Mixed number addition
            problems = [
                ("1 1/2", "2 1/3", "3 5/6"),
                ("2 3/4", "1 2/5", "4 3/20"),
                ("3 1/3", "1 3/4", "5 1/12"),
                ("1 2/5", "2 3/7", "3 29/35"),
                ("2 5/6", "1 1/8", "3 23/24")
            ]
            m1, m2, answer = problems[i % len(problems)]

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n${m1.replace(' ', ' ')} + {m2.replace(' ', ' ')} = $ ____\n\nWrite your answer as a mixed number.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "To add mixed numbers, add the whole parts and fraction parts separately."],
                    ["2/3", "Add whole numbers, then add fractions with common denominators."],
                    ["3/3", f"Final answer: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        elif question_type == 5:
            # Mixed number subtraction
            problems = [
                ("3 1/2", "1 1/3", "2 1/6"),
                ("4 3/4", "2 2/5", "2 7/20"),
                ("5 2/3", "2 3/8", "3 7/24"),
                ("3 5/6", "1 1/4", "2 7/12"),
                ("4 1/5", "2 3/7", "1 22/35")
            ]
            m1, m2, answer = problems[i % len(problems)]

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n${m1.replace(' ', ' ')} - {m2.replace(' ', ' ')} = $ ____\n\nWrite your answer as a mixed number.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "To subtract mixed numbers, convert to improper fractions or subtract parts separately."],
                    ["2/3", "Find common denominators for the fraction parts."],
                    ["3/3", f"Final answer: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        elif question_type == 6:
            # Expression with parentheses (addition/subtraction)
            problems = [
                ("(1/2 + 1/3)", "1/4", "7/12"),
                ("(3/4 - 1/6)", "1/3", "11/12"),
                ("(2/3 + 1/5)", "1/4", "31/60"),
                ("(5/6 - 1/4)", "2/5", "59/60"),
                ("(3/8 + 1/6)", "1/3", "7/8")
            ]
            expr, f2, answer = problems[i % len(problems)]

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n${expr} + \\frac{{1}}{{4}} = $ ____\n\nWrite your answer as a fraction in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "According to order of operations, evaluate parentheses first."],
                    ["2/3", "Calculate the expression in parentheses, then perform the final operation."],
                    ["3/3", f"Final answer: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        elif question_type == 7:
            # Multiplication with mixed numbers
            problems = [
                ("1 1/2", "2/3", "1"),
                ("2 1/4", "4/9", "1"),
                ("1 3/5", "5/8", "1"),
                ("2 2/3", "3/8", "1"),
                ("3 1/3", "3/10", "1")
            ]
            m1, f2, answer = problems[i % len(problems)]

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n${m1.replace(' ', ' ')} \\times \\frac{{2}}{{3}} = $ ____\n\nWrite your answer as a fraction or mixed number in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "Convert the mixed number to an improper fraction."],
                    ["2/3", "Multiply the fractions."],
                    ["3/3", f"Simplify to get: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        elif question_type == 8:
            # Complex expression with multiple operations
            problems = [
                ("1/2 × 3/4 + 1/3", "7/12"),
                ("2/3 ÷ 1/2 - 1/4", "13/12"),
                ("3/5 + 1/4 × 2/3", "23/30"),
                ("5/6 - 1/3 ÷ 2", "2/3"),
                ("1/4 + 2/3 × 3/8", "1/2")
            ]
            expr, answer = problems[i % len(problems)]

            expr_formatted = expr.replace('×', '\\times').replace('÷', '\\div')
            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n${expr_formatted} = $ ____\n\nWrite your answer as a fraction in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "According to order of operations, multiply and divide before adding and subtracting."],
                    ["2/3", "Perform multiplication/division first, then addition/subtraction."],
                    ["3/3", f"Final answer: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        else:
            # Division with mixed numbers
            problems = [
                ("2 1/2", "1 1/4", "2"),
                ("3 3/4", "1 1/2", "5/2"),
                ("4 1/3", "1 1/6", "26/7"),
                ("2 2/5", "3/5", "4"),
                ("5 1/4", "1 3/4", "3")
            ]
            m1, m2, answer = problems[i % len(problems)]

            question = {
                "skills": "evaluate-numerical-expressions-involving-fractions-and-mixed-numbers",
                "question_text": f"Evaluate the expression.\n\n${m1.replace(' ', ' ')} \\div {m2.replace(' ', ' ')} = $ ____\n\nWrite your answer as a fraction or whole number in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [answer],
                "solution": [
                    ["1/3", "Convert mixed numbers to improper fractions."],
                    ["2/3", "To divide, multiply by the reciprocal."],
                    ["3/3", f"Simplify to get: {answer}"]
                ],
                "tag": "Gr7_7_E4",
                "question_number": f"4_{i+1}",
                "solution_image_tag": []
            }

        questions.append(question)

    # Create the JSON structure
    data = {
        "quizzes": questions
    }

    # Write to file
    with open('Gr7_7_E4_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(questions)} questions for Gr7_7_E4_variations.json")

# Run the generator
generate_fraction_expressions()
print("Successfully created Gr7_7_E4_variations.json")