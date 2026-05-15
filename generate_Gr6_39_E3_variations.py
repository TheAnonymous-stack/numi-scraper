import json
import random

def generate_variations():
    """Generate 51 variations for Gr6_39_E3 - simple algebra solve for variable"""

    variations = []

    # Original template
    original = {
        "tag": "Gr6_39_E3",
        "question_number": "3_1",
        "question_type": "Fill in the blank",
        "question_text": "Solve for $m$ where $m + 17 = 93$. $m = ?$",
        "correct_answers": ["76"],
        "solution": [
            ["1/3", "Subtracting 17 from both sides to isolate for $m$."],
            ["2/3", "$m + 17 - 17 = 93 - 17$"],
            ["3/3", "$m = 76$"]
        ],
        "solution_image_tag": []
    }

    variations.append(original)

    # Generate unique number combinations for addition equations
    equation_combinations = []

    # Generate a variety of equations with different patterns
    # Addition equations: variable + number = result
    for addend in range(5, 100):
        for result in range(addend + 10, 200):
            answer = result - addend
            if answer > 0 and answer < 150:
                equation_combinations.append(('add', addend, result, answer))

    # Subtraction equations: variable - number = result
    for subtrahend in range(5, 50):
        for result in range(10, 100):
            answer = result + subtrahend
            if answer > 0 and answer < 150:
                equation_combinations.append(('sub', subtrahend, result, answer))

    # Shuffle and select 50 combinations
    random.seed(42)
    random.shuffle(equation_combinations)
    selected_equations = equation_combinations[:50]

    # Different variable names to use
    variables = ['m', 'n', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'p', 'q', 'r', 's', 't', 'v', 'w']

    for i in range(2, 52):
        eq_type, operand, result, answer = selected_equations[i-2]
        var = variables[(i-2) % len(variables)]

        if eq_type == 'add':
            variation = {
                "tag": "Gr6_39_E3",
                "question_number": f"3_{i}",
                "question_type": "Fill in the blank",
                "question_text": f"Solve for ${var}$ where ${var} + {operand} = {result}$. ${var} = ?$",
                "correct_answers": [str(answer)],
                "solution": [
                    ["1/3", f"Subtracting {operand} from both sides to isolate for ${var}$."],
                    ["2/3", f"${var} + {operand} - {operand} = {result} - {operand}$"],
                    ["3/3", f"${var} = {answer}$"]
                ],
                "solution_image_tag": []
            }
        else:  # subtraction
            variation = {
                "tag": "Gr6_39_E3",
                "question_number": f"3_{i}",
                "question_type": "Fill in the blank",
                "question_text": f"Solve for ${var}$ where ${var} - {operand} = {result}$. ${var} = ?$",
                "correct_answers": [str(answer)],
                "solution": [
                    ["1/3", f"Adding {operand} to both sides to isolate for ${var}$."],
                    ["2/3", f"${var} - {operand} + {operand} = {result} + {operand}$"],
                    ["3/3", f"${var} = {answer}$"]
                ],
                "solution_image_tag": []
            }

        variations.append(variation)

    return variations

if __name__ == "__main__":
    variations = generate_variations()

    # Save to file
    with open("Gr6_39_E3_variations.json", "w") as f:
        json.dump(variations, f, indent=2)

    print(f"Generated {len(variations)} variations for Gr6_39_E3")
    print(f"Saved to Gr6_39_E3_variations.json")