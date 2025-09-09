import json
import random

def generate_gr6_14_e2_variations():
    """Generate 51 variations for Gr6_14_E2 - Multiply whole numbers"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        # Mix of 2-digit x 2-digit, 3-digit x 2-digit, and 3-digit x 3-digit
        if i <= 20:
            # 2-digit x 2-digit
            num1 = random.randint(12, 99)
            num2 = random.randint(12, 99)
        elif i <= 35:
            # 3-digit x 2-digit
            num1 = random.randint(101, 999)
            num2 = random.randint(12, 99)
        else:
            # 3-digit x 3-digit
            num1 = random.randint(101, 999)
            num2 = random.randint(101, 999)
        
        product = num1 * num2
        
        question = {
            "skills": "multiply-whole-numbers",
            "question_text": f"Multiply. ${num1} \\\\times {num2}$ =_",
            "tag": "Gr6_14_E2",
            "question_number": f"2_{i}",
            "question_type": "Fill in the blank",
            "correct_answers": [
                str(product)
            ],
            "solution": [
                [
                    "1/6",
                    f"Set up the multiplication problem vertically with {num1} on top and {num2} below."
                ],
                [
                    "2/6",
                    f"Multiply {num1} by the ones digit of {num2} ({num2 % 10}):"
                ],
                [
                    "3/6",
                    f"${num1} \\\\times {num2 % 10} = {num1 * (num2 % 10)}$"
                ],
                [
                    "4/6",
                    f"Multiply {num1} by the tens digit of {num2} ({num2 // 10 % 10}), remembering to shift one place to the left:"
                ],
                [
                    "5/6",
                    f"${num1} \\\\times {num2 // 10 % 10}0 = {num1 * (num2 // 10 % 10) * 10}$"
                ] if num2 >= 10 else [
                    "4/6",
                    f"Since {num2} is a single digit, we're done with multiplication."
                ],
                [
                    "6/6",
                    f"Add the partial products: ${num1 * (num2 % 10)} + {num1 * (num2 // 10 % 10) * 10} = {product}$"
                ] if num2 >= 10 else [
                    "5/6",
                    f"The product is {product}."
                ]
            ] if num2 < 100 else [
                [
                    "1/7",
                    f"Set up the multiplication problem vertically with {num1} on top and {num2} below."
                ],
                [
                    "2/7",
                    f"Multiply {num1} by the ones digit of {num2} ({num2 % 10}):"
                ],
                [
                    "3/7",
                    f"${num1} \\\\times {num2 % 10} = {num1 * (num2 % 10)}$"
                ],
                [
                    "4/7",
                    f"Multiply {num1} by the tens digit of {num2} ({num2 // 10 % 10}), shifting one place:"
                ],
                [
                    "5/7",
                    f"${num1} \\\\times {num2 // 10 % 10}0 = {num1 * (num2 // 10 % 10) * 10}$"
                ],
                [
                    "6/7",
                    f"Multiply {num1} by the hundreds digit of {num2} ({num2 // 100}), shifting two places:"
                ],
                [
                    "7/7",
                    f"Add all partial products to get {product}."
                ]
            ],
            "has_alternate_answers": False
        }
        
        variations.append(question)
    
    # Save to JSON file
    output = {"quizzes": variations}
    
    with open('Gr6_14_E2_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_14_E2")

if __name__ == "__main__":
    generate_gr6_14_e2_variations()