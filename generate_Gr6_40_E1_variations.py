import json
import random

def generate_gr6_40_e1_variations():
    """Generate 51 variations for Gr6_40_E1 - Solve one-step equations"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        if i <= 17:
            # Addition equations: x + a = b
            a = random.randint(2, 50)
            b = random.randint(a + 1, 100)
            x = b - a
            
            question_text = f"Solve for x. $x + {a} = {b}$ x =_"
            
            solution = [
                [
                    "1/3",
                    f"To solve for x, subtract {a} from both sides."
                ],
                [
                    "2/3",
                    f"$x + {a} - {a} = {b} - {a}$"
                ],
                [
                    "3/3",
                    f"$x = {x}$"
                ]
            ]
            
        elif i <= 34:
            # Subtraction equations: x - a = b
            a = random.randint(2, 50)
            b = random.randint(1, 50)
            x = a + b
            
            question_text = f"Solve for x. $x - {a} = {b}$ x =_"
            
            solution = [
                [
                    "1/3",
                    f"To solve for x, add {a} to both sides."
                ],
                [
                    "2/3",
                    f"$x - {a} + {a} = {b} + {a}$"
                ],
                [
                    "3/3",
                    f"$x = {x}$"
                ]
            ]
            
        else:
            # Multiplication equations: ax = b
            a = random.randint(2, 12)
            x = random.randint(1, 20)
            b = a * x
            
            question_text = f"Solve for x. ${a}x = {b}$ x =_"
            
            solution = [
                [
                    "1/3",
                    f"To solve for x, divide both sides by {a}."
                ],
                [
                    "2/3",
                    f"$\\\\frac{{{a}x}}{{{a}}} = \\\\frac{{{b}}}{{{a}}}$"
                ],
                [
                    "3/3",
                    f"$x = {x}$"
                ]
            ]
        
        question = {
            "skills": "solve-one-step-equations",
            "question_text": question_text,
            "tag": "Gr6_40_E1",
            "question_number": f"1_{i}",
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
    
    with open('Gr6_40_E1_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_40_E1")

if __name__ == "__main__":
    generate_gr6_40_e1_variations()