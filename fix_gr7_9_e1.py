import json
import random

def generate_gr7_9_e1_variations():
    """Generate varied property of operations questions for Gr7_9_E1"""

    with open('Gr7_9_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Different examples for each property
    examples = [
        # Associative property of multiplication
        {"expr": "3 × (4 × 5) = (3 × 4) × 5", "property": "associative", "operation": "multiplication"},
        {"expr": "2 × (6 × 8) = (2 × 6) × 8", "property": "associative", "operation": "multiplication"},
        {"expr": "(5 × 7) × 3 = 5 × (7 × 3)", "property": "associative", "operation": "multiplication"},
        {"expr": "4 × (9 × 2) = (4 × 9) × 2", "property": "associative", "operation": "multiplication"},
        {"expr": "(8 × 3) × 6 = 8 × (3 × 6)", "property": "associative", "operation": "multiplication"},

        # Commutative property of multiplication
        {"expr": "7 × 9 = 9 × 7", "property": "commutative", "operation": "multiplication"},
        {"expr": "5 × 8 = 8 × 5", "property": "commutative", "operation": "multiplication"},
        {"expr": "3 × 11 = 11 × 3", "property": "commutative", "operation": "multiplication"},
        {"expr": "6 × 4 = 4 × 6", "property": "commutative", "operation": "multiplication"},
        {"expr": "12 × 2 = 2 × 12", "property": "commutative", "operation": "multiplication"},

        # Associative property of addition
        {"expr": "(4 + 5) + 6 = 4 + (5 + 6)", "property": "associative", "operation": "addition"},
        {"expr": "7 + (8 + 9) = (7 + 8) + 9", "property": "associative", "operation": "addition"},
        {"expr": "(12 + 3) + 5 = 12 + (3 + 5)", "property": "associative", "operation": "addition"},
        {"expr": "10 + (15 + 20) = (10 + 15) + 20", "property": "associative", "operation": "addition"},
        {"expr": "(25 + 30) + 45 = 25 + (30 + 45)", "property": "associative", "operation": "addition"},

        # Commutative property of addition
        {"expr": "8 + 15 = 15 + 8", "property": "commutative", "operation": "addition"},
        {"expr": "23 + 17 = 17 + 23", "property": "commutative", "operation": "addition"},
        {"expr": "45 + 32 = 32 + 45", "property": "commutative", "operation": "addition"},
        {"expr": "19 + 26 = 26 + 19", "property": "commutative", "operation": "addition"},
        {"expr": "38 + 14 = 14 + 38", "property": "commutative", "operation": "addition"},

        # Distributive property
        {"expr": "3 × (4 + 5) = 3 × 4 + 3 × 5", "property": "distributive", "operation": "multiplication"},
        {"expr": "6 × (2 + 7) = 6 × 2 + 6 × 7", "property": "distributive", "operation": "multiplication"},
        {"expr": "5 × (8 + 3) = 5 × 8 + 5 × 3", "property": "distributive", "operation": "multiplication"},
        {"expr": "4 × (9 + 6) = 4 × 9 + 4 × 6", "property": "distributive", "operation": "multiplication"},
        {"expr": "7 × (5 + 2) = 7 × 5 + 7 × 2", "property": "distributive", "operation": "multiplication"},

        # Identity property of multiplication
        {"expr": "8 × 1 = 8", "property": "identity", "operation": "multiplication"},
        {"expr": "1 × 15 = 15", "property": "identity", "operation": "multiplication"},
        {"expr": "23 × 1 = 23", "property": "identity", "operation": "multiplication"},
        {"expr": "1 × 47 = 47", "property": "identity", "operation": "multiplication"},

        # Identity property of addition
        {"expr": "12 + 0 = 12", "property": "identity", "operation": "addition"},
        {"expr": "0 + 35 = 35", "property": "identity", "operation": "addition"},
        {"expr": "58 + 0 = 58", "property": "identity", "operation": "addition"},
        {"expr": "0 + 94 = 94", "property": "identity", "operation": "addition"},

        # Zero property of multiplication
        {"expr": "7 × 0 = 0", "property": "zero", "operation": "multiplication"},
        {"expr": "0 × 25 = 0", "property": "zero", "operation": "multiplication"},
        {"expr": "43 × 0 = 0", "property": "zero", "operation": "multiplication"},
        {"expr": "0 × 81 = 0", "property": "zero", "operation": "multiplication"},
    ]

    for i in range(51):
        example = examples[i % len(examples)]

        if example["property"] in ["associative", "commutative"]:
            # Multiple choice question
            choices = ["associative", "commutative"] if i % 2 == 0 else ["commutative", "associative"]
            correct_index = choices.index(example["property"])
            correct_answer = "A" if correct_index == 0 else "B"

            if example["property"] == "associative":
                explanation = f"shows a change in grouping. This is the associative property of {example['operation']}, which states that the way {'factors' if example['operation'] == 'multiplication' else 'addends'} are grouped does not change the {'product' if example['operation'] == 'multiplication' else 'sum'}."
            else:
                explanation = f"shows a change in order. This is the commutative property of {example['operation']}, which states that changing the order of {'factors' if example['operation'] == 'multiplication' else 'addends'} does not change the {'product' if example['operation'] == 'multiplication' else 'sum'}."

            question = {
                "skills": "properties-of-addition-and-multiplication",
                "question_text": f"Which property of {example['operation']} is shown?\n\n${example['expr']}$",
                "question_type": "Multiple Choice Question with Single Answer",
                "choices": choices,
                "correct_answers": [correct_answer],
                "solution": [
                    ["1/2", f"The equation {example['expr']} {explanation.split('.')[0]}."],
                    ["2/2", explanation[0].upper() + explanation[1:]]
                ],
                "tag": "Gr7_9_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif example["property"] == "distributive":
            # Fill in the blank for distributive property
            question = {
                "skills": "properties-of-addition-and-multiplication",
                "question_text": f"Use the distributive property to fill in the blank.\n\n${example['expr'].split('=')[0].strip()} = $ ____",
                "question_type": "Fill in the blank",
                "correct_answers": [example['expr'].split('=')[1].strip()],
                "solution": [
                    ["1/2", "Apply the distributive property, which states that a × (b + c) = a × b + a × c."],
                    ["2/2", f"Therefore: {example['expr']}"]
                ],
                "tag": "Gr7_9_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif example["property"] == "identity":
            # True/False for identity property
            question = {
                "skills": "properties-of-addition-and-multiplication",
                "question_text": f"True or False: The equation ${example['expr']}$ shows the identity property of {example['operation']}.",
                "question_type": "Multiple Choice Question with Single Answer",
                "choices": ["True", "False"],
                "correct_answers": ["A"],
                "solution": [
                    ["1/2", f"The identity property of {example['operation']} states that {'any number multiplied by 1 equals itself' if example['operation'] == 'multiplication' else 'any number plus 0 equals itself'}."],
                    ["2/2", f"Since {example['expr']}, this shows the identity property. The answer is True."]
                ],
                "tag": "Gr7_9_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        else:  # zero property
            # Fill in the blank for zero property
            parts = example['expr'].split('=')
            question = {
                "skills": "properties-of-addition-and-multiplication",
                "question_text": f"What property is shown by: ${example['expr']}$?\n\nComplete: This is the ____ property of multiplication.",
                "question_type": "Fill in the blank",
                "correct_answers": ["zero"],
                "solution": [
                    ["1/2", "The zero property of multiplication states that any number multiplied by 0 equals 0."],
                    ["2/2", f"Since {example['expr']}, this demonstrates the zero property."]
                ],
                "tag": "Gr7_9_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_9_E1_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied property questions for Gr7_9_E1")

# Run the generator
generate_gr7_9_e1_variations()
print("Successfully fixed Gr7_9_E1_variations.json")