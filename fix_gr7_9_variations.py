import json
import random

def generate_gr7_9_e2_variations():
    """Generate varied distributive property questions for Gr7_9_E2"""

    with open('Gr7_9_E2_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Different expressions to simplify using distributive property
    expressions = [
        ("3(5t + 2)", "15t + 6"),
        ("4(3x + 5)", "12x + 20"),
        ("2(7y + 3)", "14y + 6"),
        ("5(2m + 4)", "10m + 20"),
        ("6(3n + 1)", "18n + 6"),
        ("7(2p + 3)", "14p + 21"),
        ("3(4q + 6)", "12q + 18"),
        ("8(2r + 1)", "16r + 8"),
        ("4(5s - 3)", "20s - 12"),
        ("2(6t - 4)", "12t - 8"),
        ("5(3u - 2)", "15u - 10"),
        ("3(7v - 5)", "21v - 15"),
        ("6(2w - 1)", "12w - 6"),
        ("4(4x - 2)", "16x - 8"),
        ("7(3y - 4)", "21y - 28"),
        ("2(8z + 5)", "16z + 10"),
        ("9(2a + 3)", "18a + 27"),
        ("3(6b + 4)", "18b + 12"),
        ("5(4c + 2)", "20c + 10"),
        ("8(3d + 2)", "24d + 16"),
        ("2(9e + 7)", "18e + 14"),
        ("4(2f + 8)", "8f + 32"),
        ("6(5g + 1)", "30g + 6"),
        ("3(8h + 7)", "24h + 21"),
        ("7(4j + 2)", "28j + 14"),
        ("5(5k + 3)", "25k + 15"),
        ("2(10m + 3)", "20m + 6"),
        ("4(6n + 5)", "24n + 20"),
        ("3(9p + 2)", "27p + 6"),
        ("8(4q + 3)", "32q + 24"),
    ]

    for i in range(51):
        expr, answer = expressions[i % len(expressions)]

        # Remove parentheses for display
        expr_display = expr.replace("(", "(").replace(")", ")")

        question = {
            "skills": "multiply-using-the-distributive-property",
            "question_text": f"Simplify the expression:\n\n${expr_display} = $ ____\n\n",
            "question_type": "Fill in the blank",
            "correct_answers": [answer.replace(" ", "")],  # Remove spaces for answer matching
            "solution": [
                ["1/3", f"To simplify the expression {expr}, apply the distributive property."],
                ["2/3", f"Multiply the number outside by each term inside the parentheses."],
                ["3/3", f"So, {expr} = {answer}."]
            ],
            "tag": "Gr7_9_E2",
            "question_number": f"2_{i+1}",
            "solution_image_tag": []
        }
        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_9_E2_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied distributive property questions for Gr7_9_E2")

def generate_gr7_9_e3_variations():
    """Generate varied equation solving questions for Gr7_9_E3"""

    with open('Gr7_9_E3_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Different equations using properties
    equations = [
        ("q + 60 = 60 + 76", "q", "76"),
        ("x + 45 = 45 + 82", "x", "82"),
        ("y + 32 = 32 + 91", "y", "91"),
        ("z + 58 = 58 + 47", "z", "47"),
        ("a + 73 = 73 + 65", "a", "65"),
        ("b + 29 = 29 + 84", "b", "84"),
        ("c + 51 = 51 + 39", "c", "39"),
        ("d + 67 = 67 + 72", "d", "72"),
        ("15 + e = 43 + 15", "e", "43"),
        ("24 + f = 68 + 24", "f", "68"),
        ("37 + g = 55 + 37", "g", "55"),
        ("42 + h = 79 + 42", "h", "79"),
        ("56 + j = 88 + 56", "j", "88"),
        ("k × 8 = 8 × 12", "k", "12"),
        ("m × 5 = 5 × 17", "m", "17"),
        ("n × 9 = 9 × 23", "n", "23"),
        ("p × 7 = 7 × 31", "p", "31"),
        ("q × 6 = 6 × 25", "q", "25"),
        ("4 × r = 19 × 4", "r", "19"),
        ("3 × s = 28 × 3", "s", "28"),
        ("11 × t = 15 × 11", "t", "15"),
        ("(u + 5) + 7 = u + (5 + 7)", "u", "any number"),
        ("(v + 8) + 12 = v + (8 + 12)", "v", "any number"),
        ("(w + 3) + 9 = w + (3 + 9)", "w", "any number"),
        ("(x + 6) × 4 = (5 + 6) × 4", "x", "5"),
        ("(y + 9) × 3 = (7 + 9) × 3", "y", "7"),
        ("(z + 4) × 8 = (11 + 4) × 8", "z", "11"),
        ("a + 0 = 45", "a", "45"),
        ("b + 0 = 67", "b", "67"),
        ("c × 1 = 89", "c", "89"),
        ("d × 1 = 34", "d", "34"),
    ]

    for i in range(51):
        equation, var, answer = equations[i % len(equations)]

        # Determine the property being used
        if "+" in equation and "0" not in equation:
            if "any number" in answer:
                property_used = "associative property of addition"
            else:
                property_used = "commutative property of addition"
        elif "×" in equation and "1" not in equation:
            property_used = "commutative property of multiplication"
        elif "+ 0" in equation:
            property_used = "identity property of addition"
        elif "× 1" in equation:
            property_used = "identity property of multiplication"
        else:
            property_used = "commutative property"

        question = {
            "skills": "solve-equations-using-properties",
            "question_text": f"What value of {var} makes this equation true?\n\nHint: Use properties of operations.\n\n${equation}$\n\n${var} = $ ____\n",
            "question_type": "Fill in the blank",
            "correct_answers": [answer] if answer != "any number" else ["0"],  # Use 0 as example for "any number"
            "solution": [
                ["1/3", f"We are given the equation: {equation}."],
                ["2/3", f"Use the {property_used}."],
                ["3/3", f"Therefore, {var} = {answer}."]
            ],
            "tag": "Gr7_9_E3",
            "question_number": f"3_{i+1}",
            "solution_image_tag": []
        }
        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_9_E3_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied equation solving questions for Gr7_9_E3")

def generate_gr7_9_e4_variations():
    """Generate varied equivalent expression questions for Gr7_9_E4"""

    with open('Gr7_9_E4_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Different expressions to simplify
    simplifications = [
        ("1 + 8s + 3", "8s + 4"),
        ("2 + 5x + 7", "5x + 9"),
        ("4 + 3y + 6", "3y + 10"),
        ("5 + 7z + 8", "7z + 13"),
        ("3 + 4a + 9", "4a + 12"),
        ("6 + 2b + 11", "2b + 17"),
        ("8 + 9c + 4", "9c + 12"),
        ("7 + 6d + 5", "6d + 12"),
        ("2x + 3x", "5x"),
        ("4y + 7y", "11y"),
        ("5z + 3z", "8z"),
        ("8a + 2a", "10a"),
        ("6b + 9b", "15b"),
        ("3c + 4c", "7c"),
        ("7d + 5d", "12d"),
        ("9e + e", "10e"),
        ("3 + 2x + 5 + 4x", "6x + 8"),
        ("7 + 5y + 2 + 3y", "8y + 9"),
        ("4 + 6z + 8 + z", "7z + 12"),
        ("1 + 3a + 9 + 7a", "10a + 10"),
        ("5 + 8b + 3 + 2b", "10b + 8"),
        ("6 + 4c + 7 + 5c", "9c + 13"),
        ("2 + 9d + 4 + d", "10d + 6"),
        ("8 + 3e + 1 + 6e", "9e + 9"),
        ("3(x + 2)", "3x + 6"),
        ("4(y + 5)", "4y + 20"),
        ("2(z + 7)", "2z + 14"),
        ("5(a + 3)", "5a + 15"),
        ("6(b + 4)", "6b + 24"),
        ("7(c + 1)", "7c + 7"),
        ("8(d + 2)", "8d + 16"),
        ("9(e + 3)", "9e + 27"),
        ("2(3x + 4)", "6x + 8"),
        ("3(2y + 5)", "6y + 15"),
        ("4(5z + 1)", "20z + 4"),
        ("5(2a + 6)", "10a + 30"),
        ("2x + 3 + 4x + 7", "6x + 10"),
        ("5y + 8 + 2y + 3", "7y + 11"),
        ("3z + 4 + 6z + 5", "9z + 9"),
        ("7a + 2 + a + 8", "8a + 10"),
        ("4b + 6 + 5b + 1", "9b + 7"),
        ("8c + 3 + 2c + 9", "10c + 12"),
        ("6d + 5 + 3d + 4", "9d + 9"),
        ("x + 7 + 9x + 2", "10x + 9"),
        ("3m + 2m + 7", "5m + 7"),
        ("4n + 6n + 3", "10n + 3"),
        ("5p + p + 8", "6p + 8"),
        ("7q + 3q + 5", "10q + 5"),
        ("2r + 8r + 9", "10r + 9"),
        ("9s + s + 4", "10s + 4"),
        ("6t + 4t + 2", "10t + 2")
    ]

    for i in range(51):
        expr, simplified = simplifications[i % len(simplifications)]

        question = {
            "skills": "write-equivalent-expressions-using-properties",
            "question_text": f"Simplify the expression by combining like terms:\n\n${expr} = $ ____\n\n",
            "question_type": "Fill in the blank",
            "correct_answers": [simplified.replace(" ", "")],  # Remove spaces
            "solution": [
                ["1/3", f"Given expression: {expr}"],
                ["2/3", "Combine like terms using the commutative and associative properties."],
                ["3/3", f"Simplified expression: {simplified}"]
            ],
            "tag": "Gr7_9_E4",
            "question_number": f"4_{i+1}",
            "solution_image_tag": []
        }
        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_9_E4_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied equivalent expression questions for Gr7_9_E4")

# Run all three generators
generate_gr7_9_e2_variations()
generate_gr7_9_e3_variations()
generate_gr7_9_e4_variations()

print("\nSuccessfully generated variations for all three Gr7_9 exercises!")