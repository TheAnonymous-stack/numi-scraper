import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_9_E1 (properties-of-addition-and-multiplication)"""

    # Load template
    with open('Gr7_9_E1_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Create variation
        variation = copy.deepcopy(template)

        # Randomly decide which property to show
        show_associative = random.choice([True, False])

        if show_associative:
            # Generate associative property example
            a = random.randint(2, 15)
            b = random.randint(2, 15)
            c = random.randint(2, 15)

            variation["question_text"] = f"Which property of multiplication is shown?\n\n${a} \\times ({b} \\times {c}) = ({a} \\times {b}) \\times {c}$"
            variation["correct_answers"] = ["A"]  # associative is option A

            variation["solution"] = [
                [
                    "1/2",
                    f"The equation ${a} \\times ({b} \\times {c}) = ({a} \\times {b}) \\times {c}$ shows a change in grouping."
                ],
                [
                    "2/2",
                    "This is the associative property of multiplication, which states that the way factors are grouped does not change the product."
                ]
            ]
        else:
            # Generate commutative property example
            a = random.randint(2, 15)
            b = random.randint(2, 15)

            variation["question_text"] = f"Which property of multiplication is shown?\n\n${a} \\times {b} = {b} \\times {a}$"
            variation["correct_answers"] = ["B"]  # commutative is option B

            variation["solution"] = [
                [
                    "1/2",
                    f"The equation ${a} \\times {b} = {b} \\times {a}$ shows a change in the order of factors."
                ],
                [
                    "2/2",
                    "This is the commutative property of multiplication, which states that the order of factors does not change the product."
                ]
            ]

        # Randomly rotate answer choices sometimes
        if random.choice([True, False]):
            variation["choices"] = ["commutative", "associative"]
            if show_associative:
                variation["correct_answers"] = ["B"]
            else:
                variation["correct_answers"] = ["A"]

        # Update question number
        variation["question_number"] = f"1_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_9_E1 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_9_E1")

if __name__ == "__main__":
    generate_variations()