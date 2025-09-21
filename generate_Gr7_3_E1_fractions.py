import json
import random
from fractions import Fraction

def generate_fraction_addition_problems():
    """Generate 51 fraction addition problems for Grade 7"""

    quizzes = []

    # Problem categories for variety
    # 1. Same denominators (easier) - problems 1-15
    # 2. Different denominators with one multiple of another - problems 16-30
    # 3. Different denominators requiring LCM - problems 31-51

    problem_count = 1

    # Category 1: Same denominators (15 problems)
    denominators = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]
    for i in range(15):
        denom = random.choice(denominators)
        num1 = random.randint(1, denom - 1)
        num2 = random.randint(1, denom - 1)

        # Create the problem
        question_text = f"Calculate: $\\frac{{{num1}}}{{{denom}}} + \\frac{{{num2}}}{{{denom}}}$ = ?"

        # Calculate answer
        result = Fraction(num1, denom) + Fraction(num2, denom)

        # Format answer as simplified fraction
        if result.denominator == 1:
            answer = str(result.numerator)
        else:
            answer = f"{result.numerator}/{result.denominator}"

        # Create solution explanation
        sum_numerator = num1 + num2
        solution_text = (
            f"When adding fractions with the same denominator, we add the numerators "
            f"and keep the denominator the same.\n\n"
            f"$\\frac{{{num1}}}{{{denom}}} + \\frac{{{num2}}}{{{denom}}} = \\frac{{{num1} + {num2}}}{{{denom}}} = \\frac{{{sum_numerator}}}{{{denom}}}$"
        )

        if sum_numerator != result.numerator:  # If simplification occurred
            solution_text += f"\n\nSimplifying: $\\frac{{{sum_numerator}}}{{{denom}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}$"

        if result.denominator == 1:
            solution_text += f" = ${result.numerator}$"

        quiz = {
            "skills": "add-fractions",
            "question_text": question_text,
            "question_type": "Fill in the blank",
            "correct_answers": [answer],
            "solution": solution_text,
            "tag": "Gr7_3_E1",
            "question_number": f"1_{problem_count}"
        }

        quizzes.append(quiz)
        problem_count += 1

    # Category 2: Different denominators where one is multiple of another (15 problems)
    pairs = [(2, 4), (2, 6), (2, 8), (3, 6), (3, 9), (3, 12), (4, 8), (4, 12), (5, 10), (5, 15)]

    for i in range(15):
        denom1, denom2 = random.choice(pairs)
        if random.random() > 0.5:
            denom1, denom2 = denom2, denom1

        num1 = random.randint(1, denom1 - 1)
        num2 = random.randint(1, denom2 - 1)

        question_text = f"Calculate: $\\frac{{{num1}}}{{{denom1}}} + \\frac{{{num2}}}{{{denom2}}}$ = ?"

        # Calculate answer
        result = Fraction(num1, denom1) + Fraction(num2, denom2)

        # Format answer
        if result.denominator == 1:
            answer = str(result.numerator)
        else:
            answer = f"{result.numerator}/{result.denominator}"

        # Find LCD (which is max of denom1 and denom2 in this case)
        lcd = max(denom1, denom2)

        # Convert fractions
        new_num1 = num1 * (lcd // denom1)
        new_num2 = num2 * (lcd // denom2)
        sum_numerator = new_num1 + new_num2

        solution_text = (
            f"To add fractions with different denominators, we first find the LCD (Least Common Denominator).\n\n"
            f"The LCD of {denom1} and {denom2} is {lcd}.\n\n"
            f"Converting to equivalent fractions:\n"
            f"$\\frac{{{num1}}}{{{denom1}}} = \\frac{{{num1} \\times {lcd // denom1}}}{{{denom1} \\times {lcd // denom1}}} = \\frac{{{new_num1}}}{{{lcd}}}$\n\n"
            f"$\\frac{{{num2}}}{{{denom2}}} = \\frac{{{num2} \\times {lcd // denom2}}}{{{denom2} \\times {lcd // denom2}}} = \\frac{{{new_num2}}}{{{lcd}}}$\n\n"
            f"Now we can add: $\\frac{{{new_num1}}}{{{lcd}}} + \\frac{{{new_num2}}}{{{lcd}}} = \\frac{{{sum_numerator}}}{{{lcd}}}$"
        )

        if sum_numerator != result.numerator or lcd != result.denominator:
            solution_text += f"\n\nSimplifying: $\\frac{{{sum_numerator}}}{{{lcd}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}$"

        if result.denominator == 1:
            solution_text += f" = ${result.numerator}$"

        quiz = {
            "skills": "add-fractions",
            "question_text": question_text,
            "question_type": "Fill in the blank",
            "correct_answers": [answer],
            "solution": solution_text,
            "tag": "Gr7_3_E1",
            "question_number": f"1_{problem_count}"
        }

        quizzes.append(quiz)
        problem_count += 1

    # Category 3: Different denominators requiring LCM calculation (21 problems)
    denominator_pairs = [
        (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7), (7, 8),
        (3, 7), (3, 8), (4, 9), (5, 8), (6, 8), (7, 9), (8, 9),
        (5, 12), (7, 12), (8, 12), (9, 10), (7, 10), (9, 12)
    ]

    for i in range(21):
        denom1, denom2 = random.choice(denominator_pairs)
        if random.random() > 0.5:
            denom1, denom2 = denom2, denom1

        num1 = random.randint(1, min(denom1 - 1, 7))  # Keep numerators reasonable
        num2 = random.randint(1, min(denom2 - 1, 7))

        question_text = f"Calculate: $\\frac{{{num1}}}{{{denom1}}} + \\frac{{{num2}}}{{{denom2}}}$ = ?"

        # Calculate answer
        result = Fraction(num1, denom1) + Fraction(num2, denom2)

        # Format answer
        if result.denominator == 1:
            answer = str(result.numerator)
        else:
            answer = f"{result.numerator}/{result.denominator}"

        # Find LCD
        from math import gcd
        lcd = (denom1 * denom2) // gcd(denom1, denom2)

        # Convert fractions
        new_num1 = num1 * (lcd // denom1)
        new_num2 = num2 * (lcd // denom2)
        sum_numerator = new_num1 + new_num2

        solution_text = (
            f"To add fractions with different denominators, we need to find the LCD.\n\n"
            f"Finding the LCD of {denom1} and {denom2}:\n"
            f"Multiples of {denom1}: {denom1}, {denom1*2}, {denom1*3}, ...\n"
            f"Multiples of {denom2}: {denom2}, {denom2*2}, {denom2*3}, ...\n"
            f"LCD = {lcd}\n\n"
            f"Converting to equivalent fractions:\n"
            f"$\\frac{{{num1}}}{{{denom1}}} = \\frac{{{num1} \\times {lcd // denom1}}}{{{denom1} \\times {lcd // denom1}}} = \\frac{{{new_num1}}}{{{lcd}}}$\n\n"
            f"$\\frac{{{num2}}}{{{denom2}}} = \\frac{{{num2} \\times {lcd // denom2}}}{{{denom2} \\times {lcd // denom2}}} = \\frac{{{new_num2}}}{{{lcd}}}$\n\n"
            f"Adding: $\\frac{{{new_num1}}}{{{lcd}}} + \\frac{{{new_num2}}}{{{lcd}}} = \\frac{{{new_num1} + {new_num2}}}{{{lcd}}} = \\frac{{{sum_numerator}}}{{{lcd}}}$"
        )

        if sum_numerator != result.numerator or lcd != result.denominator:
            gcd_val = gcd(sum_numerator, lcd)
            if gcd_val > 1:
                solution_text += (
                    f"\n\nSimplifying by dividing by GCD({sum_numerator}, {lcd}) = {gcd_val}:\n"
                    f"$\\frac{{{sum_numerator}}}{{{lcd}}} = \\frac{{{sum_numerator} ÷ {gcd_val}}}{{{lcd} ÷ {gcd_val}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}$"
                )

        if result.denominator == 1:
            solution_text += f" = ${result.numerator}$"

        quiz = {
            "skills": "add-fractions",
            "question_text": question_text,
            "question_type": "Fill in the blank",
            "correct_answers": [answer],
            "solution": solution_text,
            "tag": "Gr7_3_E1",
            "question_number": f"1_{problem_count}"
        }

        quizzes.append(quiz)
        problem_count += 1

    return {"quizzes": quizzes}

if __name__ == "__main__":
    # Generate the problems
    data = generate_fraction_addition_problems()

    # Save to JSON file
    with open("C:\\Users\\kapil\\numi-scraper\\Gr7_3_E1_variations.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated {len(data['quizzes'])} fraction addition problems")
    print("File saved to: C:\\Users\\kapil\\numi-scraper\\Gr7_3_E1_variations.json")