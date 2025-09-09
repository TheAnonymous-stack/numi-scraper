import json
import random

def generate_gr6_40_e2_variations():
    """Generate 51 variations for Gr6_40_E2 - Solve two-step equations"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        if i <= 20:
            # Type 1: ax + b = c
            a = random.randint(2, 10)
            x = random.randint(1, 15)
            b = random.randint(1, 20)
            c = a * x + b
            
            question_text = f"Solve for x. ${a}x + {b} = {c}$ x =_"
            
            solution = [
                [
                    "1/4",
                    f"Subtract {b} from both sides."
                ],
                [
                    "2/4",
                    f"${a}x + {b} - {b} = {c} - {b}$"
                ],
                [
                    "3/4",
                    f"${a}x = {c - b}$\\nDivide both sides by {a}."
                ],
                [
                    "4/4",
                    f"$x = \\\\frac{{{c - b}}}{{{a}}} = {x}$"
                ]
            ]
            
        elif i <= 35:
            # Type 2: ax - b = c
            a = random.randint(2, 10)
            x = random.randint(2, 15)
            b = random.randint(1, 15)
            c = a * x - b
            
            question_text = f"Solve for x. ${a}x - {b} = {c}$ x =_"
            
            solution = [
                [
                    "1/4",
                    f"Add {b} to both sides."
                ],
                [
                    "2/4",
                    f"${a}x - {b} + {b} = {c} + {b}$"
                ],
                [
                    "3/4",
                    f"${a}x = {c + b}$\\nDivide both sides by {a}."
                ],
                [
                    "4/4",
                    f"$x = \\\\frac{{{c + b}}}{{{a}}} = {x}$"
                ]
            ]
            
        else:
            # Type 3: x/a + b = c
            a = random.randint(2, 8)
            b = random.randint(1, 15)
            x_value = random.randint(1, 10) * a  # Ensure integer result
            c = x_value // a + b
            
            question_text = f"Solve for x. $\\\\frac{{x}}{{{a}}} + {b} = {c}$ x =_"
            
            solution = [
                [
                    "1/4",
                    f"Subtract {b} from both sides."
                ],
                [
                    "2/4",
                    f"$\\\\frac{{x}}{{{a}}} + {b} - {b} = {c} - {b}$"
                ],
                [
                    "3/4",
                    f"$\\\\frac{{x}}{{{a}}} = {c - b}$\\nMultiply both sides by {a}."
                ],
                [
                    "4/4",
                    f"$x = {a} \\\\times {c - b} = {x_value}$"
                ]
            ]
            
            x = x_value
        
        question = {
            "skills": "solve-two-step-equations",
            "question_text": question_text,
            "tag": "Gr6_40_E2",
            "question_number": f"2_{i}",
            "question_type": "Fill in the blank",
            "correct_answers": [
                str(x)
            ],
            "solution": solution,
            "has_alternate_answers": False
        }
        
        variations.append(question)
    
    # Save to JSON file
    output = {"quizzes": variations}
    
    with open('Gr6_40_E2_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_40_E2")

if __name__ == "__main__":
    generate_gr6_40_e2_variations()