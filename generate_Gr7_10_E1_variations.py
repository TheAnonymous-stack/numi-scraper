import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_10_E1 (add-integers-using-counters)"""

    # Load template
    with open('Gr7_10_E1_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    variations = []
    variation_num = 2

    # Define possible integer pairs to add
    integer_pairs = [
        (-1, 1), (-2, 2), (-3, 3), (-4, 4),  # Zero results
        (-3, 1), (-4, 2), (-5, 3), (-2, -1),  # Negative results
        (2, 1), (3, 2), (1, 3), (2, 2),  # Positive results
        (-3, -1), (-2, -2), (-1, -3),  # Negative + Negative
        (1, 0), (-1, 0), (0, 2), (0, -2)  # With zero
    ]

    # Answer choices mapping
    def get_choices_for_sum(sum_val):
        if sum_val == 0:
            return [
                ("Shows four red circles with minus signs, representing -4", "A"),
                ("Empty/blank space representing 0 (no counters)", "B"),
                ("Shows two red circles with minus signs, representing -2", "C"),
                ("Shows one yellow circle with a plus sign, representing +1", "D")
            ]
        elif sum_val < 0:
            abs_val = abs(sum_val)
            return [
                (f"Shows {abs_val + 1} red circles with minus signs, representing {sum_val - 1}", "A"),
                (f"Shows {abs_val} red circles with minus signs, representing {sum_val}", "B"),
                (f"Shows {abs_val - 1 if abs_val > 1 else 1} yellow circle{'s' if abs_val - 1 != 1 else ''} with plus sign{'s' if abs_val - 1 != 1 else ''}, representing +{abs_val - 1 if abs_val > 1 else 1}", "C"),
                ("Empty/blank space representing 0 (no counters)", "D")
            ]
        else:  # sum_val > 0
            return [
                (f"Shows {sum_val + 1} yellow circles with plus signs, representing +{sum_val + 1}", "A"),
                (f"Shows {sum_val} yellow circle{'s' if sum_val != 1 else ''} with plus sign{'s' if sum_val != 1 else ''}, representing +{sum_val}", "B"),
                (f"Shows {sum_val - 1 if sum_val > 1 else 1} red circle{'s' if sum_val - 1 != 1 else ''} with minus sign{'s' if sum_val - 1 != 1 else ''}, representing -{sum_val - 1 if sum_val > 1 else 1}", "C"),
                ("Empty/blank space representing 0 (no counters)", "D")
            ]

    # Generate 50 variations
    used_pairs = set()
    while len(variations) < 50:
        # Select random integer pair
        num1, num2 = random.choice(integer_pairs)

        # Avoid exact duplicates
        if (num1, num2) in used_pairs:
            # Try with different values
            num1 = random.randint(-5, 5)
            num2 = random.randint(-5, 5)
            if (num1, num2) in used_pairs:
                continue

        used_pairs.add((num1, num2))
        sum_val = num1 + num2

        # Create variation
        variation = copy.deepcopy(template)

        # Update question text
        sign1 = "" if num1 < 0 else "+"
        sign2 = "+" if num2 >= 0 else ""
        variation["question_text"] = f"Use counters to add {sign1}{num1} {sign2} {num2}.\n\nWhich picture shows the sum?\n"

        # Update image tags
        variation["image_tag"] = f"Gr7_10_1_{variation_num}"
        variation["image_choice_tags"] = [
            f"Gr7_10_1_{variation_num}_A",
            f"Gr7_10_1_{variation_num}_B",
            f"Gr7_10_1_{variation_num}_C",
            f"Gr7_10_1_{variation_num}_D"
        ]

        # Generate choice descriptions and find correct answer
        choices = get_choices_for_sum(sum_val)
        variation["image_choice_tags_backend_description"] = [choice[0] for choice in choices]

        # Determine correct answer based on sum
        if sum_val == 0:
            correct = "B" if "0 (no counters)" in choices[1][0] else "D"
        else:
            for i, (desc, letter) in enumerate(choices):
                if f"representing {'+' if sum_val > 0 else ''}{sum_val}" in desc:
                    correct = letter
                    break

        variation["correct_answers"] = [correct]

        # Update backend description
        variation["backend_description"] = f"Shows a visual representation for adding {num1} {sign2} {num2} using counter symbols. Multiple choice options display different combinations of positive and negative counters."

        # Update solution image tags
        variation["solution_image_tag"] = [
            [
                "2/6",
                f"Gr7_10_1_{variation_num}_step_2",
                f"Shows {'a' if abs(num1) == 1 else abs(num1)} {'red circle' if abs(num1) == 1 else 'red circles'} with {'a minus sign' if abs(num1) == 1 else 'minus signs'}, representing {num1} as the starting value." if num1 < 0 else f"Shows {'a' if num1 == 1 else num1} yellow circle{'' if num1 == 1 else 's'} with {'a plus sign' if num1 == 1 else 'plus signs'}, representing {sign1}{num1} as the starting value."
            ],
            [
                "3/6",
                f"Gr7_10_1_{variation_num}_step_3",
                f"Shows the combination of counters representing {num1} and {num2}."
            ],
            [
                "4/6",
                f"Gr7_10_1_{variation_num}_step_4",
                "Demonstrates the cancellation concept: positive and negative counters form 'zero pairs' that cancel each other out." if (num1 < 0 and num2 > 0) or (num1 > 0 and num2 < 0) else f"Shows combining the counters to get the final result."
            ]
        ]

        # Update solution
        variation["solution"] = [
            [
                "1/6",
                f"We are adding {sign1}{num1} {sign2} {num2} using counters."
            ],
            [
                "2/6",
                f"Start with {abs(num1)} {'negative' if num1 < 0 else 'positive'} counter{'s' if abs(num1) != 1 else ''} to represent {sign1}{num1}."
            ],
            [
                "3/6",
                f"Now add {abs(num2)} {'negative' if num2 < 0 else 'positive'} counter{'s' if abs(num2) != 1 else ''} to represent {sign2}{num2}."
            ],
            [
                "4/6",
                "A positive counter and a negative counter cancel each other out." if (num1 < 0 and num2 > 0) or (num1 > 0 and num2 < 0) else f"Combine the counters together."
            ],
            [
                "5/6",
                f"{'No counters are left after canceling out the pairs.' if sum_val == 0 else str(abs(sum_val)) + ' ' + ('negative' if sum_val < 0 else 'positive') + ' counter' + ('s' if abs(sum_val) != 1 else '') + ' remain' + ('s' if abs(sum_val) == 1 else '') + '.'}"
            ],
            [
                "6/6",
                f"So {sign1}{num1} {sign2} {num2} = {sum_val}.\n\n{'The option with no counters is correct.' if sum_val == 0 else 'The option showing ' + str(abs(sum_val)) + ' ' + ('negative' if sum_val < 0 else 'positive') + ' counter' + ('s' if abs(sum_val) != 1 else '') + ' is correct.'}"
            ]
        ]

        # Update question number
        variation["question_number"] = f"1_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_10_E1 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_10_E1")

if __name__ == "__main__":
    generate_variations()