import json
import random
from fractions import Fraction

def generate_gr6_18_e2_variations():
    """Generate 51 variations for Gr6_18_E2 - Multiply fractions"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        # Generate two fractions to multiply
        if i <= 20:
            # Simple fractions
            num1 = random.randint(1, 9)
            denom1 = random.randint(2, 10)
            num2 = random.randint(1, 9)
            denom2 = random.randint(2, 10)
        elif i <= 35:
            # Mixed with whole numbers
            if random.choice([True, False]):
                # Whole number × fraction
                num1 = random.randint(2, 12)
                denom1 = 1
                num2 = random.randint(1, 9)
                denom2 = random.randint(2, 10)
            else:
                # Fraction × whole number
                num1 = random.randint(1, 9)
                denom1 = random.randint(2, 10)
                num2 = random.randint(2, 12)
                denom2 = 1
        else:
            # Larger fractions
            num1 = random.randint(1, 15)
            denom1 = random.randint(2, 15)
            num2 = random.randint(1, 15)
            denom2 = random.randint(2, 15)
        
        # Calculate product
        product_num = num1 * num2
        product_denom = denom1 * denom2
        
        # Simplify
        from math import gcd
        common_factor = gcd(product_num, product_denom)
        final_num = product_num // common_factor
        final_denom = product_denom // common_factor
        
        # Format question text
        if denom1 == 1:
            frac1_str = str(num1)
        else:
            frac1_str = f"\\\\frac{{{num1}}}{{{denom1}}}"
        
        if denom2 == 1:
            frac2_str = str(num2)
        else:
            frac2_str = f"\\\\frac{{{num2}}}{{{denom2}}}"
        
        question_text = f"Multiply. ${frac1_str} \\\\times {frac2_str}$ = Write your answer in simplest form.=_"
        
        # Format answer
        if final_denom == 1:
            correct_answer = str(final_num)
        else:
            correct_answer = f"{final_num}/{final_denom}"
        
        # Create solution steps
        solution = [
            [
                "1/5",
                f"Multiply the numerators: ${num1} \\\\times {num2} = {product_num}$"
            ],
            [
                "2/5",
                f"Multiply the denominators: ${denom1} \\\\times {denom2} = {product_denom}$"
            ],
            [
                "3/5",
                f"The product is $\\\\frac{{{product_num}}}{{{product_denom}}}$"
            ],
            [
                "4/5",
                f"Find the GCD of {product_num} and {product_denom}: GCD = {common_factor}"
            ],
            [
                "5/5",
                f"Simplify: $\\\\frac{{{product_num}}}{{{product_denom}}} = \\\\frac{{{final_num}}}{{{final_denom}}}$" if final_denom != 1 else f"Simplify: $\\\\frac{{{product_num}}}{{{product_denom}}} = {final_num}$"
            ]
        ]
        
        question = {
            "skills": "multiply-fractions",
            "question_text": question_text,
            "tag": "Gr6_18_E2",
            "question_number": f"2_{i}",
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
    
    with open('Gr6_18_E2_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_18_E2")

if __name__ == "__main__":
    generate_gr6_18_e2_variations()