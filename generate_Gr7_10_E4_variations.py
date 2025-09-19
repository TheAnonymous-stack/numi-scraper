import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_10_E4 (add-three-or-more-integers)"""

    # Load template
    with open('Gr7_10_E4_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Generate 4 random integers
        nums = []
        for _ in range(4):
            num = random.randint(-12, 12)
            if num != 0:
                nums.append(num)

        # Ensure we have exactly 4 numbers
        while len(nums) < 4:
            num = random.randint(-12, 12)
            if num != 0:
                nums.append(num)

        # Calculate intermediate results
        step1_result = nums[0] + nums[1]
        step2_result = step1_result + nums[2]
        final_result = step2_result + nums[3]

        # Create variation
        variation = copy.deepcopy(template)

        # Format the expression
        expression_parts = []
        for num in nums:
            if num < 0:
                expression_parts.append(f"({num})")
            else:
                expression_parts.append(str(num))

        expression = " + ".join(expression_parts)
        # Clean up the expression
        expression = expression.replace("+ (-", "+ -")

        # Update question text
        variation["question_text"] = f"Add:\n\n${expression} = \\_\\_\\_\\_$\n"

        # Update correct answer
        variation["correct_answers"] = [str(final_result)]

        # Update solution image tags
        variation["solution_image_tag"] = [
            [
                "1/4",
                f"Gr7_10_4_{variation_num}_step_1",
                f"Shows the addition of {nums[0]} + {'(' + str(nums[1]) + ')' if nums[1] < 0 else nums[1]} = {step1_result} in blue text. {'When adding two negative numbers, the result is negative and the absolute values are added.' if nums[0] < 0 and nums[1] < 0 else 'When adding a negative and positive number, subtract the smaller absolute value from the larger and keep the sign of the larger.' if (nums[0] < 0) != (nums[1] < 0) else 'Adding two positive numbers gives a positive result.'}"
            ],
            [
                "2/4",
                f"Gr7_10_4_{variation_num}_step_2",
                f"Shows {step1_result} + {'(' + str(nums[2]) + ')' if nums[2] < 0 else nums[2]} = {step2_result} in purple text. {'When adding a negative and positive number, subtract the smaller absolute value from the larger and keep the sign of the larger.' if (step1_result < 0) != (nums[2] < 0) else 'When adding numbers with the same sign, add their absolute values and keep the sign.'}"
            ],
            [
                "3/4",
                f"Gr7_10_4_{variation_num}_step_3",
                f"Shows {step2_result} + {'(' + str(nums[3]) + ')' if nums[3] < 0 else nums[3]} = {final_result} in blue text. {'Again adding a negative and positive, resulting in ' + str(final_result) if (step2_result < 0) != (nums[3] < 0) else 'Adding numbers with the same sign, resulting in ' + str(final_result)} as the final answer."
            ]
        ]

        # Update solution
        variation["solution"] = [
            [
                "1/4",
                f"First add {nums[0]} and {'(' + str(nums[1]) + ')' if nums[1] < 0 else nums[1]}:\n"
            ],
            [
                "2/4",
                f"Now add {step1_result} and {'(' + str(nums[2]) + ')' if nums[2] < 0 else nums[2]}:\n"
            ],
            [
                "3/4",
                f"Now add {step2_result} and {'(' + str(nums[3]) + ')' if nums[3] < 0 else nums[3]}:\n"
            ],
            [
                "4/4",
                f"The sum is {final_result}."
            ]
        ]

        # Update question number
        variation["question_number"] = f"4_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_10_E4 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_10_E4")

if __name__ == "__main__":
    generate_variations()