import json
import random

def generate_gr6_15_e2_variations():
    """Generate 51 variations for Gr6_15_E2 - Add and subtract decimals"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        # Generate random decimal numbers
        if i <= 17:
            # Addition problems
            num1 = round(random.uniform(0.1, 99.99), 2)
            num2 = round(random.uniform(0.1, 99.99), 2)
            result = round(num1 + num2, 2)
            operation = "+"
            operation_word = "Add"
        elif i <= 34:
            # Subtraction problems (ensure positive result)
            num1 = round(random.uniform(10.0, 99.99), 2)
            num2 = round(random.uniform(0.1, num1 - 0.1), 2)
            result = round(num1 - num2, 2)
            operation = "-"
            operation_word = "Subtract"
        else:
            # Mixed addition with 3 decimals places
            num1 = round(random.uniform(0.001, 99.999), 3)
            num2 = round(random.uniform(0.001, 99.999), 3)
            result = round(num1 + num2, 3)
            operation = "+"
            operation_word = "Add"
        
        question = {
            "skills": "add-and-subtract-decimals",
            "question_text": f"{operation_word}. ${num1} {operation} {num2}$ =_",
            "tag": "Gr6_15_E2",
            "question_number": f"2_{i}",
            "question_type": "Fill in the blank",
            "correct_answers": [
                str(result)
            ],
            "solution": [
                [
                    "1/5",
                    f"Line up the decimal points vertically."
                ],
                [
                    "2/5",
                    f"{'Add' if operation == '+' else 'Subtract'} starting from the rightmost digit."
                ],
                [
                    "3/5",
                    f"${num1} {operation} {num2} = {result}$"
                ],
                [
                    "4/5",
                    f"Remember to place the decimal point in the same position in your answer."
                ],
                [
                    "5/5",
                    f"The {'sum' if operation == '+' else 'difference'} is {result}."
                ]
            ],
            "has_alternate_answers": False
        }
        
        variations.append(question)
    
    # Save to JSON file
    output = {"quizzes": variations}
    
    with open('Gr6_15_E2_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_15_E2")

if __name__ == "__main__":
    generate_gr6_15_e2_variations()