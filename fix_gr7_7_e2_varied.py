import json
import random

def generate_varied_numerical_expressions():
    """Generate varied numerical expressions with decimals for Gr7_7_E2"""

    with open('Gr7_7_E2_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Generate 51 varied numerical expressions
    for i in range(51):
        # Different types of expressions
        expr_type = i % 7

        if expr_type == 0:
            # Addition and multiplication
            nums = [(2.5, 3, 1.8), (3.2, 4, 2.1), (1.5, 5, 3.3), (4.6, 2, 1.7), (2.8, 3, 4.2)]
            n1, n2, n3 = nums[i % len(nums)]
            result = round(n1 * n2 + n3, 2)

            question = {
                "skills": "evaluate-numerical-expressions-involving-decimals",
                "question_text": f"Evaluate the expression.\n\n{n1} × {n2} + {n3} = ____\n\nWrite your answer as a decimal. Do not round.",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/3", f"According to the order of operations, multiply before adding."],
                    ["2/3", f"First multiply: {n1} × {n2} = {n1 * n2}"],
                    ["3/3", f"Then add: {n1 * n2} + {n3} = {result}"]
                ],
                "tag": "Gr7_7_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }

        elif expr_type == 1:
            # Subtraction and division
            nums = [(8.4, 3, 1.5), (12.6, 4, 2.3), (15.5, 5, 1.8), (9.6, 2, 3.2), (18.9, 7, 1.4)]
            n1, n2, n3 = nums[i % len(nums)]
            result = round(n1 / n2 - n3, 2)

            question = {
                "skills": "evaluate-numerical-expressions-involving-decimals",
                "question_text": f"Evaluate the expression.\n\n{n1} ÷ {n2} - {n3} = ____\n\nWrite your answer as a decimal. Do not round.",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/3", f"According to the order of operations, divide before subtracting."],
                    ["2/3", f"First divide: {n1} ÷ {n2} = {round(n1/n2, 2)}"],
                    ["3/3", f"Then subtract: {round(n1/n2, 2)} - {n3} = {result}"]
                ],
                "tag": "Gr7_7_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }

        elif expr_type == 2:
            # Multiple operations with parentheses
            nums = [(2.4, 1.6, 3), (3.5, 2.5, 4), (4.2, 1.8, 5), (5.4, 2.6, 2), (1.8, 3.2, 4)]
            n1, n2, n3 = nums[i % len(nums)]
            result = round((n1 + n2) * n3, 2)

            question = {
                "skills": "evaluate-numerical-expressions-involving-decimals",
                "question_text": f"Evaluate the expression.\n\n({n1} + {n2}) × {n3} = ____\n\nWrite your answer as a decimal. Do not round.",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/3", f"According to the order of operations, evaluate parentheses first."],
                    ["2/3", f"First add inside parentheses: {n1} + {n2} = {round(n1 + n2, 2)}"],
                    ["3/3", f"Then multiply: {round(n1 + n2, 2)} × {n3} = {result}"]
                ],
                "tag": "Gr7_7_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }

        elif expr_type == 3:
            # Division and addition
            nums = [(3.6, 2, 4.7), (8.4, 3, 2.9), (7.5, 5, 3.8), (9.6, 4, 5.3), (12.8, 8, 6.4)]
            n1, n2, n3 = nums[i % len(nums)]
            result = round(n1 / n2 + n3, 2)

            question = {
                "skills": "evaluate-numerical-expressions-involving-decimals",
                "question_text": f"Evaluate the expression.\n\n{n1} ÷ {n2} + {n3} = ____\n\nWrite your answer as a decimal. Do not round.",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/3", f"According to the order of operations, divide before adding."],
                    ["2/3", f"First divide: {n1} ÷ {n2} = {round(n1/n2, 2)}"],
                    ["3/3", f"Then add: {round(n1/n2, 2)} + {n3} = {result}"]
                ],
                "tag": "Gr7_7_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }

        elif expr_type == 4:
            # Multiplication and subtraction
            nums = [(3.5, 2, 5.2), (2.8, 3, 6.4), (4.2, 4, 10.3), (1.5, 6, 3.7), (2.3, 5, 8.5)]
            n1, n2, n3 = nums[i % len(nums)]
            result = round(n1 * n2 - n3, 2)

            question = {
                "skills": "evaluate-numerical-expressions-involving-decimals",
                "question_text": f"Evaluate the expression.\n\n{n1} × {n2} - {n3} = ____\n\nWrite your answer as a decimal. Do not round.",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/3", f"According to the order of operations, multiply before subtracting."],
                    ["2/3", f"First multiply: {n1} × {n2} = {round(n1 * n2, 2)}"],
                    ["3/3", f"Then subtract: {round(n1 * n2, 2)} - {n3} = {result}"]
                ],
                "tag": "Gr7_7_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }

        elif expr_type == 5:
            # Complex expression with three operations
            nums = [(2, 3.6, 1.5, 2.4), (3, 4.5, 2.5, 3.2), (4, 5.2, 1.8, 4.1), (5, 7.5, 3.2, 2.8)]
            n1, n2, n3, n4 = nums[i % len(nums)]
            result = round(n1 * n2 / n3 + n4, 2)

            question = {
                "skills": "evaluate-numerical-expressions-involving-decimals",
                "question_text": f"Evaluate the expression.\n\n{n1} × {n2} ÷ {n3} + {n4} = ____\n\nWrite your answer as a decimal. Do not round.",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/4", f"According to the order of operations, multiply and divide from left to right, then add."],
                    ["2/4", f"First multiply: {n1} × {n2} = {n1 * n2}"],
                    ["3/4", f"Then divide: {n1 * n2} ÷ {n3} = {round(n1 * n2 / n3, 2)}"],
                    ["4/4", f"Finally add: {round(n1 * n2 / n3, 2)} + {n4} = {result}"]
                ],
                "tag": "Gr7_7_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }

        else:
            # Parentheses with division
            nums = [(9.6, 2.4, 2), (12.8, 3.2, 3), (15.6, 5.2, 4), (18.4, 4.6, 5), (21.5, 4.3, 2)]
            n1, n2, n3 = nums[i % len(nums)]
            result = round((n1 - n2) / n3, 2)

            question = {
                "skills": "evaluate-numerical-expressions-involving-decimals",
                "question_text": f"Evaluate the expression.\n\n({n1} - {n2}) ÷ {n3} = ____\n\nWrite your answer as a decimal. Do not round.",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/3", f"According to the order of operations, evaluate parentheses first."],
                    ["2/3", f"First subtract inside parentheses: {n1} - {n2} = {round(n1 - n2, 2)}"],
                    ["3/3", f"Then divide: {round(n1 - n2, 2)} ÷ {n3} = {result}"]
                ],
                "tag": "Gr7_7_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }

        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_7_E2_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied numerical expression questions for Gr7_7_E2")

# Run the fix
generate_varied_numerical_expressions()
print("Fixed Gr7_7_E2 with varied numerical expressions")