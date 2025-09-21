import json
import random
import copy

def generate_equivalent_fraction_variations():
    """Generate 51 variations of equivalent fraction problems"""

    # Template structure
    template = {
        "skills": "equivalent-fractions",
        "question_text": "Type the missing number that makes these fractions equal:\n",
        "question_type": "Fill in the blank",
        "has_alternative_answers": True,
        "tag": "Gr7_5_E1",
        "solution_image_tag": []
    }

    variations = []

    # Generate 51 variations
    for i in range(1, 52):
        variation = copy.deepcopy(template)
        variation["question_number"] = f"1_{i}"
        variation["image_tag"] = f"Gr7_5_1_{i}"

        # Randomly decide if we're finding missing numerator or denominator
        find_numerator = random.choice([True, False])

        if find_numerator:
            # Generate a fraction and find equivalent with missing numerator
            if i <= 17:  # Simple fractions
                # Use simple fractions for first third
                numerator = random.randint(1, 10)
                denominator = random.randint(2, 12)
                # Ensure fraction can be reduced or expanded
                factor = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])

                if random.choice([True, False]):  # Expand
                    given_num = numerator
                    given_den = denominator
                    target_den = denominator * factor
                    answer = numerator * factor

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with denominator {target_den} and an unknown numerator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a denominator of {target_den}."],
                        ["2/3", f"To find the missing numerator, we need to determine what to multiply {given_den} by to get {target_den}. Since {given_den} × {factor} = {target_den}, we multiply the numerator by the same factor: {given_num} × {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{answer}}}{{{target_den}}}$."]
                    ]
                else:  # Reduce
                    given_num = numerator * factor
                    given_den = denominator * factor
                    target_den = denominator
                    answer = numerator

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with denominator {target_den} and an unknown numerator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a denominator of {target_den}."],
                        ["2/3", f"To find the missing numerator, divide both the numerator and denominator of $\\frac{{{given_num}}}{{{given_den}}}$ by the same number. Since {given_den} ÷ {factor} = {target_den}, divide the numerator by {factor} as well: {given_num} ÷ {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{answer}}}{{{target_den}}}$."]
                    ]

            elif i <= 34:  # Medium complexity
                numerator = random.randint(2, 20)
                denominator = random.randint(3, 30)
                factor = random.choice([2, 3, 4, 5, 6, 7, 8])

                if random.choice([True, False]):  # Expand
                    given_num = numerator
                    given_den = denominator
                    target_den = denominator * factor
                    answer = numerator * factor

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with denominator {target_den} and an unknown numerator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a denominator of {target_den}."],
                        ["2/3", f"To find the missing numerator, we need to determine what to multiply {given_den} by to get {target_den}. Since {given_den} × {factor} = {target_den}, we multiply the numerator by the same factor: {given_num} × {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{answer}}}{{{target_den}}}$."]
                    ]
                else:  # Reduce
                    given_num = numerator * factor
                    given_den = denominator * factor
                    target_den = denominator
                    answer = numerator

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with denominator {target_den} and an unknown numerator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a denominator of {target_den}."],
                        ["2/3", f"To find the missing numerator, divide both the numerator and denominator of $\\frac{{{given_num}}}{{{given_den}}}$ by the same number. Since {given_den} ÷ {factor} = {target_den}, divide the numerator by {factor} as well: {given_num} ÷ {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{answer}}}{{{target_den}}}$."]
                    ]

            else:  # More complex/improper fractions
                numerator = random.randint(3, 15)
                denominator = random.randint(2, 12)
                factor = random.choice([2, 3, 4, 5, 6, 7, 8, 9])

                if random.choice([True, False]):  # Expand
                    given_num = numerator
                    given_den = denominator
                    target_den = denominator * factor
                    answer = numerator * factor

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with denominator {target_den} and an unknown numerator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a denominator of {target_den}."],
                        ["2/3", f"To find the missing numerator, we need to determine what to multiply {given_den} by to get {target_den}. Since {given_den} × {factor} = {target_den}, we multiply the numerator by the same factor: {given_num} × {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{answer}}}{{{target_den}}}$."]
                    ]
                else:  # Reduce
                    given_num = numerator * factor
                    given_den = denominator * factor
                    target_den = denominator
                    answer = numerator

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with denominator {target_den} and an unknown numerator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a denominator of {target_den}."],
                        ["2/3", f"To find the missing numerator, divide both the numerator and denominator of $\\frac{{{given_num}}}{{{given_den}}}$ by the same number. Since {given_den} ÷ {factor} = {target_den}, divide the numerator by {factor} as well: {given_num} ÷ {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{answer}}}{{{target_den}}}$."]
                    ]

        else:
            # Generate a fraction and find equivalent with missing denominator
            if i <= 17:  # Simple fractions
                numerator = random.randint(1, 10)
                denominator = random.randint(2, 12)
                factor = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])

                if random.choice([True, False]):  # Expand
                    given_num = numerator
                    given_den = denominator
                    target_num = numerator * factor
                    answer = denominator * factor

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with numerator {target_num} and an unknown denominator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a numerator of {target_num}."],
                        ["2/3", f"To find the missing denominator, we need to determine what to multiply {given_num} by to get {target_num}. Since {given_num} × {factor} = {target_num}, we multiply the denominator by the same factor: {given_den} × {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{target_num}}}{{{answer}}}$."]
                    ]
                else:  # Reduce
                    given_num = numerator * factor
                    given_den = denominator * factor
                    target_num = numerator
                    answer = denominator

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with numerator {target_num} and an unknown denominator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a numerator of {target_num}."],
                        ["2/3", f"To find the missing denominator, divide both the numerator and denominator of $\\frac{{{given_num}}}{{{given_den}}}$ by the same number. Since {given_num} ÷ {factor} = {target_num}, divide the denominator by {factor} as well: {given_den} ÷ {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{target_num}}}{{{answer}}}$."]
                    ]

            elif i <= 34:  # Medium complexity
                numerator = random.randint(2, 20)
                denominator = random.randint(3, 30)
                factor = random.choice([2, 3, 4, 5, 6, 7, 8])

                if random.choice([True, False]):  # Expand
                    given_num = numerator
                    given_den = denominator
                    target_num = numerator * factor
                    answer = denominator * factor

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with numerator {target_num} and an unknown denominator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a numerator of {target_num}."],
                        ["2/3", f"To find the missing denominator, we need to determine what to multiply {given_num} by to get {target_num}. Since {given_num} × {factor} = {target_num}, we multiply the denominator by the same factor: {given_den} × {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{target_num}}}{{{answer}}}$."]
                    ]
                else:  # Reduce
                    given_num = numerator * factor
                    given_den = denominator * factor
                    target_num = numerator
                    answer = denominator

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with numerator {target_num} and an unknown denominator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a numerator of {target_num}."],
                        ["2/3", f"To find the missing denominator, divide both the numerator and denominator of $\\frac{{{given_num}}}{{{given_den}}}$ by the same number. Since {given_num} ÷ {factor} = {target_num}, divide the denominator by {factor} as well: {given_den} ÷ {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{target_num}}}{{{answer}}}$."]
                    ]

            else:  # More complex/improper fractions
                numerator = random.randint(3, 15)
                denominator = random.randint(2, 12)
                factor = random.choice([2, 3, 4, 5, 6, 7, 8, 9])

                if random.choice([True, False]):  # Expand
                    given_num = numerator
                    given_den = denominator
                    target_num = numerator * factor
                    answer = denominator * factor

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with numerator {target_num} and an unknown denominator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a numerator of {target_num}."],
                        ["2/3", f"To find the missing denominator, we need to determine what to multiply {given_num} by to get {target_num}. Since {given_num} × {factor} = {target_num}, we multiply the denominator by the same factor: {given_den} × {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{target_num}}}{{{answer}}}$."]
                    ]
                else:  # Reduce
                    given_num = numerator * factor
                    given_den = denominator * factor
                    target_num = numerator
                    answer = denominator

                    variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with numerator {target_num} and an unknown denominator represented by an empty box."

                    variation["solution"] = [
                        ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a numerator of {target_num}."],
                        ["2/3", f"To find the missing denominator, divide both the numerator and denominator of $\\frac{{{given_num}}}{{{given_den}}}$ by the same number. Since {given_num} ÷ {factor} = {target_num}, divide the denominator by {factor} as well: {given_den} ÷ {factor} = {answer}."],
                        ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{target_num}}}{{{answer}}}$."]
                    ]

        # Add correct answers in multiple formats
        variation["correct_answers"] = [
            [str(answer)],
            [f"{answer}.0"],
            [f"{answer}.00"]
        ]

        variations.append(variation)

    # Create specific variations based on the existing pattern
    # Override some variations with specific examples to ensure variety

    # Variation 1: 20/16 = ?/4 (answer: 5)
    variations[0] = create_specific_variation(1, 20, 16, None, 4, 5, True)

    # Variation 2: 9/10 = 36/? (answer: 40)
    variations[1] = create_specific_variation(2, 9, 10, 36, None, 40, False)

    # Variation 3: 14/18 = 7/? (answer: 9)
    variations[2] = create_specific_variation(3, 14, 18, 7, None, 9, False)

    # Variation 4: 7/2 = ?/8 (answer: 28)
    variations[3] = create_specific_variation(4, 7, 2, None, 8, 28, True)

    # Variation 5: 6/24 = 1/? (answer: 4)
    variations[4] = create_specific_variation(5, 6, 24, 1, None, 4, False)

    # Variation 10: 4/40 = 1/? (answer: 10)
    variations[9] = create_specific_variation(10, 4, 40, 1, None, 10, False)

    # Variation 16: 1/3 = ?/6 (answer: 2)
    variations[15] = create_specific_variation(16, 1, 3, None, 6, 2, True)

    # Variation 22: 6/36 = 1/? (answer: 6)
    variations[21] = create_specific_variation(22, 6, 36, 1, None, 6, False)

    # Variation 25: 5/20 = ?/4 (answer: 1)
    variations[24] = create_specific_variation(25, 5, 20, None, 4, 1, True)

    # Variation 27: 1/2 = ?/14 (answer: 7)
    variations[26] = create_specific_variation(27, 1, 2, None, 14, 7, True)

    # Variation 34: 2/6 = 1/? (answer: 3)
    variations[33] = create_specific_variation(34, 2, 6, 1, None, 3, False)

    # Variation 36: 5/15 = ?/3 (answer: 1)
    variations[35] = create_specific_variation(36, 5, 15, None, 3, 1, True)

    return variations

def create_specific_variation(num, given_num, given_den, target_num, target_den, answer, find_numerator):
    """Create a specific variation with given values"""
    variation = {
        "skills": "equivalent-fractions",
        "question_text": "Type the missing number that makes these fractions equal:\n",
        "question_type": "Fill in the blank",
        "has_alternative_answers": True,
        "tag": "Gr7_5_E1",
        "solution_image_tag": [],
        "question_number": f"1_{num}",
        "image_tag": f"Gr7_5_1_{num}",
        "correct_answers": [
            [str(answer)],
            [f"{answer}.0"],
            [f"{answer}.00"]
        ]
    }

    if find_numerator:
        variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with denominator {target_den} and an unknown numerator represented by an empty box."

        # Determine if this is expansion or reduction
        if given_den < target_den:  # Expansion
            factor = target_den // given_den
            variation["solution"] = [
                ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a denominator of {target_den}."],
                ["2/3", f"To find the missing numerator, we need to determine what to multiply {given_den} by to get {target_den}. Since {given_den} × {factor} = {target_den}, we multiply the numerator by the same factor: {given_num} × {factor} = {answer}."],
                ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{answer}}}{{{target_den}}}$."]
            ]
        else:  # Reduction
            factor = given_den // target_den
            variation["solution"] = [
                ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a denominator of {target_den}."],
                ["2/3", f"To find the missing numerator, divide both the numerator and denominator of $\\frac{{{given_num}}}{{{given_den}}}$ by the same number. Since {given_den} ÷ {factor} = {target_den}, divide the numerator by {factor} as well: {given_num} ÷ {factor} = {answer}."],
                ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{answer}}}{{{target_den}}}$."]
            ]
    else:
        variation["backend_description"] = f"Shows an equation with {given_num}/{given_den} equals a fraction with numerator {target_num} and an unknown denominator represented by an empty box."

        # Determine if this is expansion or reduction
        if given_num < target_num:  # Expansion
            factor = target_num // given_num
            variation["solution"] = [
                ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a numerator of {target_num}."],
                ["2/3", f"To find the missing denominator, we need to determine what to multiply {given_num} by to get {target_num}. Since {given_num} × {factor} = {target_num}, we multiply the denominator by the same factor: {given_den} × {factor} = {answer}."],
                ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{target_num}}}{{{answer}}}$."]
            ]
        else:  # Reduction
            factor = given_num // target_num
            variation["solution"] = [
                ["1/3", f"We are given the fraction $\\frac{{{given_num}}}{{{given_den}}}$ and asked to find an equivalent fraction with a numerator of {target_num}."],
                ["2/3", f"To find the missing denominator, divide both the numerator and denominator of $\\frac{{{given_num}}}{{{given_den}}}$ by the same number. Since {given_num} ÷ {factor} = {target_num}, divide the denominator by {factor} as well: {given_den} ÷ {factor} = {answer}."],
                ["3/3", f"So, $\\frac{{{given_num}}}{{{given_den}}}$ is equivalent to $\\frac{{{target_num}}}{{{answer}}}$."]
            ]

    return variation

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)

    # Generate variations
    variations = generate_equivalent_fraction_variations()

    # Create the output structure
    output = {
        "quizzes": variations
    }

    # Save to file
    with open("Gr7_5_E1_variations.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {len(variations)} variations and saved to Gr7_5_E1_variations.json")