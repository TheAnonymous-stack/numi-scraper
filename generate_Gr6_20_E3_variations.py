import json
import random
from fractions import Fraction

def generate_gr6_20_e3_variations():
    """Generate 51 variations for Gr6_20_E3 - Multiply mixed numbers"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        # Generate mixed numbers or whole numbers with fractions
        if i <= 20:
            # Mixed number × whole number
            whole1 = random.randint(1, 5)
            num1 = random.randint(1, 7)
            denom1 = random.randint(2, 8)
            # Ensure proper fraction
            if num1 >= denom1:
                num1 = denom1 - 1
            
            whole2 = random.randint(2, 6)
            
            # Convert to improper fraction
            improper1_num = whole1 * denom1 + num1
            improper1_denom = denom1
            improper2_num = whole2
            improper2_denom = 1
            
            question_text = f"Multiply. ${whole1}\\\\frac{{{num1}}}{{{denom1}}} \\\\times {whole2}$ = Write your answer as a whole or mixed number in simplest form.=_"
            
        elif i <= 35:
            # Mixed number × fraction
            whole1 = random.randint(1, 4)
            num1 = random.randint(1, 5)
            denom1 = random.randint(2, 6)
            if num1 >= denom1:
                num1 = denom1 - 1
            
            num2 = random.randint(1, 5)
            denom2 = random.randint(2, 8)
            if num2 >= denom2:
                num2 = denom2 - 1
            
            # Convert to improper fraction
            improper1_num = whole1 * denom1 + num1
            improper1_denom = denom1
            improper2_num = num2
            improper2_denom = denom2
            
            question_text = f"Multiply. ${whole1}\\\\frac{{{num1}}}{{{denom1}}} \\\\times \\\\frac{{{num2}}}{{{denom2}}}$ = Write your answer as a whole or mixed number in simplest form.=_"
            
        else:
            # Mixed number × mixed number
            whole1 = random.randint(1, 3)
            num1 = random.randint(1, 4)
            denom1 = random.randint(2, 5)
            if num1 >= denom1:
                num1 = denom1 - 1
            
            whole2 = random.randint(1, 3)
            num2 = random.randint(1, 4)
            denom2 = random.randint(2, 5)
            if num2 >= denom2:
                num2 = denom2 - 1
            
            # Convert to improper fractions
            improper1_num = whole1 * denom1 + num1
            improper1_denom = denom1
            improper2_num = whole2 * denom2 + num2
            improper2_denom = denom2
            
            question_text = f"Multiply. ${whole1}\\\\frac{{{num1}}}{{{denom1}}} \\\\times {whole2}\\\\frac{{{num2}}}{{{denom2}}}$ = Write your answer as a whole or mixed number in simplest form.=_"
        
        # Calculate product
        product_num = improper1_num * improper2_num
        product_denom = improper1_denom * improper2_denom
        
        # Simplify
        from math import gcd
        common_factor = gcd(product_num, product_denom)
        final_num = product_num // common_factor
        final_denom = product_denom // common_factor
        
        # Convert to mixed number if needed
        if final_num >= final_denom:
            final_whole = final_num // final_denom
            final_remainder = final_num % final_denom
            if final_remainder == 0:
                correct_answer = str(final_whole)
            else:
                # Simplify the remainder fraction
                gcd_rem = gcd(final_remainder, final_denom)
                final_remainder = final_remainder // gcd_rem
                final_denom = final_denom // gcd_rem
                correct_answer = f"{final_whole} {final_remainder}/{final_denom}"
        else:
            correct_answer = f"{final_num}/{final_denom}"
        
        # Create solution steps
        solution = [
            [
                "1/6",
                f"Convert mixed numbers to improper fractions."
            ],
            [
                "2/6",
                f"$\\\\frac{{{improper1_num}}}{{{improper1_denom}}} \\\\times \\\\frac{{{improper2_num}}}{{{improper2_denom}}}$"
            ],
            [
                "3/6",
                f"Multiply the numerators: ${improper1_num} \\\\times {improper2_num} = {product_num}$"
            ],
            [
                "4/6",
                f"Multiply the denominators: ${improper1_denom} \\\\times {improper2_denom} = {product_denom}$"
            ],
            [
                "5/6",
                f"The product is $\\\\frac{{{product_num}}}{{{product_denom}}}$"
            ],
            [
                "6/6",
                f"Simplify and convert to mixed number: {correct_answer}"
            ]
        ]
        
        question = {
            "skills": "multiply-mixed-numbers",
            "question_text": question_text,
            "tag": "Gr6_20_E3",
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
    
    with open('Gr6_20_E3_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_20_E3")

if __name__ == "__main__":
    generate_gr6_20_e3_variations()