import json
import random
from fractions import Fraction

def generate_gr6_16_e3_variations():
    """Generate 51 variations for Gr6_16_E3 - Add and subtract fractions with unlike denominators"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        # Generate fractions with different denominators
        denominators = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
        
        if i <= 25:
            # Addition problems
            denom1 = random.choice(denominators)
            denom2 = random.choice([d for d in denominators if d != denom1])
            num1 = random.randint(1, denom1 - 1)
            num2 = random.randint(1, denom2 - 1)
            
            # Calculate LCD and sum
            from math import gcd
            lcd = (denom1 * denom2) // gcd(denom1, denom2)
            
            # Convert to common denominator
            new_num1 = num1 * (lcd // denom1)
            new_num2 = num2 * (lcd // denom2)
            sum_num = new_num1 + new_num2
            
            # Simplify if possible
            common_factor = gcd(sum_num, lcd)
            final_num = sum_num // common_factor
            final_denom = lcd // common_factor
            
            operation = "+"
            operation_word = "Add"
            
            question_text = f"{operation_word}. $\\\\frac{{{num1}}}{{{denom1}}} {operation} \\\\frac{{{num2}}}{{{denom2}}}$ = Write your answer in simplest form.=_"
            
            if final_denom == 1:
                correct_answer = str(final_num)
            else:
                correct_answer = f"{final_num}/{final_denom}"
            
            solution = [
                [
                    "1/6",
                    f"Find the least common denominator (LCD) of {denom1} and {denom2}."
                ],
                [
                    "2/6",
                    f"The LCD is {lcd}."
                ],
                [
                    "3/6",
                    f"Convert both fractions to have denominator {lcd}:"
                ],
                [
                    "4/6",
                    f"$\\\\frac{{{num1}}}{{{denom1}}} = \\\\frac{{{new_num1}}}{{{lcd}}}$ and $\\\\frac{{{num2}}}{{{denom2}}} = \\\\frac{{{new_num2}}}{{{lcd}}}$"
                ],
                [
                    "5/6",
                    f"Add the fractions: $\\\\frac{{{new_num1}}}{{{lcd}}} + \\\\frac{{{new_num2}}}{{{lcd}}} = \\\\frac{{{sum_num}}}{{{lcd}}}$"
                ],
                [
                    "6/6",
                    f"Simplify: $\\\\frac{{{sum_num}}}{{{lcd}}} = \\\\frac{{{final_num}}}{{{final_denom}}}$" if final_denom != 1 else f"Simplify: $\\\\frac{{{sum_num}}}{{{lcd}}} = {final_num}$"
                ]
            ]
            
        else:
            # Subtraction problems
            denom1 = random.choice(denominators)
            denom2 = random.choice([d for d in denominators if d != denom1])
            
            # Ensure we can subtract (positive result)
            from math import gcd
            lcd = (denom1 * denom2) // gcd(denom1, denom2)
            
            # Generate numbers ensuring first is larger when converted
            num1 = random.randint(denom1//2, denom1 - 1)
            max_num2 = min(denom2 - 1, (num1 * lcd // denom1 - 1) * denom2 // lcd)
            if max_num2 < 1:
                num2 = 1
                num1 = denom1 - 1  # Make num1 larger
            else:
                num2 = random.randint(1, max(1, max_num2))
            
            # Convert to common denominator
            new_num1 = num1 * (lcd // denom1)
            new_num2 = num2 * (lcd // denom2)
            
            # Ensure positive result
            if new_num1 < new_num2:
                num1, num2 = num2, num1
                denom1, denom2 = denom2, denom1
                new_num1 = num1 * (lcd // denom1)
                new_num2 = num2 * (lcd // denom2)
            
            diff_num = new_num1 - new_num2
            
            # Simplify if possible
            if diff_num == 0:
                final_num = 0
                final_denom = 1
            else:
                common_factor = gcd(diff_num, lcd)
                final_num = diff_num // common_factor
                final_denom = lcd // common_factor
            
            operation = "-"
            operation_word = "Subtract"
            
            question_text = f"{operation_word}. $\\\\frac{{{num1}}}{{{denom1}}} {operation} \\\\frac{{{num2}}}{{{denom2}}}$ = Write your answer in simplest form.=_"
            
            if final_denom == 1:
                correct_answer = str(final_num)
            else:
                correct_answer = f"{final_num}/{final_denom}"
            
            solution = [
                [
                    "1/6",
                    f"Find the least common denominator (LCD) of {denom1} and {denom2}."
                ],
                [
                    "2/6",
                    f"The LCD is {lcd}."
                ],
                [
                    "3/6",
                    f"Convert both fractions to have denominator {lcd}:"
                ],
                [
                    "4/6",
                    f"$\\\\frac{{{num1}}}{{{denom1}}} = \\\\frac{{{new_num1}}}{{{lcd}}}$ and $\\\\frac{{{num2}}}{{{denom2}}} = \\\\frac{{{new_num2}}}{{{lcd}}}$"
                ],
                [
                    "5/6",
                    f"Subtract the fractions: $\\\\frac{{{new_num1}}}{{{lcd}}} - \\\\frac{{{new_num2}}}{{{lcd}}} = \\\\frac{{{diff_num}}}{{{lcd}}}$"
                ],
                [
                    "6/6",
                    f"Simplify: $\\\\frac{{{diff_num}}}{{{lcd}}} = \\\\frac{{{final_num}}}{{{final_denom}}}$" if final_denom != 1 and final_num != 0 else f"The answer is {final_num}."
                ]
            ]
        
        question = {
            "skills": "add-and-subtract-fractions-with-unlike-denominators",
            "question_text": question_text,
            "tag": "Gr6_16_E3",
            "question_number": f"3_{i}",
            "question_type": "Fill in the blank",
            "correct_answers": [
                correct_answer
            ],
            "solution": solution,
            "has_alternate_answers": False
        }
        
        variations.append(question)
    
    # Save to JSON file
    output = {"quizzes": variations}
    
    with open('Gr6_16_E3_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_16_E3")

if __name__ == "__main__":
    generate_gr6_16_e3_variations()