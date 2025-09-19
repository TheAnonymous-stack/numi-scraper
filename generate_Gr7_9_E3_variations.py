import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_9_E3 (solve-equations-using-properties)"""

    # Load template
    with open('Gr7_9_E3_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    # Variables to use
    variables = ['q', 'x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'r', 's', 't', 'w']

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Create variation
        variation = copy.deepcopy(template)

        # Random values
        var = random.choice(variables)
        common_value = random.randint(10, 99)
        answer = random.randint(10, 99)

        # Ensure values are different
        while answer == common_value:
            answer = random.randint(10, 99)

        # Update question text
        variation["question_text"] = f"What value of {var} makes this addition sentence true?\n\nHint: Use properties of addition.\n\n${var} + {common_value} = {common_value} + {answer}$\n\n${var} = \\_\\_\\_\\_$\n"

        # Update correct answer
        variation["correct_answers"] = [str(answer)]

        # Update solution
        variation["solution"] = [
            [
                "1/5",
                f"We are given the equation: ${var} + {common_value} = {common_value} + {answer}$."
            ],
            [
                "2/5",
                "Use the commutative property of addition, which tells us that numbers can be added in any order: a + b = b + a."
            ],
            [
                "3/5",
                f"Since ${var} + {common_value}$ must equal ${common_value} + {answer}$, and {common_value} is already matched on both sides, ${var}$ must be equal to {answer}"
            ],
            [
                "4/5",
                f"So, ${var} + {common_value} = {common_value} + {answer}$ becomes ${answer} + {common_value} = {common_value} + {answer}$, which is true."
            ],
            [
                "5/5",
                f"Therefore, ${var} = {answer}$."
            ]
        ]

        # Update question number
        variation["question_number"] = f"3_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_9_E3 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_9_E3")

if __name__ == "__main__":
    generate_variations()