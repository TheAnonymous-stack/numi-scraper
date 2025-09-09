import json
import random

def generate_gr6_13_e3_variations():
    """Generate 51 variations for Gr6_13_E3 - Finding the whole from a percent"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        # Generate random values
        part = random.choice([6, 8, 9, 10, 12, 15, 16, 18, 20, 21, 24, 25, 27, 28, 30, 32, 35, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 70, 72, 75, 80, 81, 84, 90, 96, 100, 108, 120, 125, 135, 144, 150, 160, 180, 200, 225, 240, 250, 270, 300])
        percent = random.choice([10, 15, 20, 25, 30, 40, 50, 60, 75, 80])
        
        # Calculate the whole
        whole = (part * 100) / percent
        
        # Ensure whole is a nice number
        if whole % 1 != 0:
            continue
        whole = int(whole)
        
        question = {
            "skills": "find-the-whole-knowing-a-percent-and-a-part",
            "question_text": f"{part} is {percent}% of what number?=_",
            "tag": "Gr6_13_E3",
            "question_number": f"3_{i}",
            "question_type": "Fill in the blank",
            "correct_answers": [
                str(whole)
            ],
            "solution": [
                [
                    "1/9",
                    f"The part is {part}."
                ],
                [
                    "2/9",
                    f"The percent is {percent}%."
                ],
                [
                    "3/9",
                    "Let w represent the whole."
                ],
                [
                    "4/9",
                    "Write a proportion to solve for w."
                ],
                [
                    "5/9",
                    f"$\\\\frac{{{part}}}{{w}} = \\\\frac{{{percent}}}{{100}}$"
                ],
                [
                    "6/9",
                    f"${percent}w = {part} \\\\cdot 100$"
                ],
                [
                    "7/9",
                    f"${percent}w = {part * 100}$"
                ],
                [
                    "8/9",
                    f"$w = \\\\frac{{{part * 100}}}{{{percent}}} = {whole}$"
                ],
                [
                    "9/9",
                    f"{part} is {percent}% of {whole}."
                ]
            ],
            "has_alternate_answers": False
        }
        
        variations.append(question)
    
    # Ensure we have exactly 51 variations
    while len(variations) < 51:
        i = len(variations) + 1
        # Generate with specific values to ensure clean division
        pairs = [
            (15, 25, 60), (20, 40, 50), (30, 50, 60), (40, 80, 50),
            (45, 75, 60), (60, 30, 200), (75, 50, 150), (90, 60, 150),
            (120, 80, 150), (150, 75, 200), (180, 90, 200), (200, 50, 400)
        ]
        part, percent, whole = random.choice(pairs)
        
        question = {
            "skills": "find-the-whole-knowing-a-percent-and-a-part",
            "question_text": f"{part} is {percent}% of what number?=_",
            "tag": "Gr6_13_E3",
            "question_number": f"3_{i}",
            "question_type": "Fill in the blank",
            "correct_answers": [
                str(whole)
            ],
            "solution": [
                [
                    "1/9",
                    f"The part is {part}."
                ],
                [
                    "2/9",
                    f"The percent is {percent}%."
                ],
                [
                    "3/9",
                    "Let w represent the whole."
                ],
                [
                    "4/9",
                    "Write a proportion to solve for w."
                ],
                [
                    "5/9",
                    f"$\\\\frac{{{part}}}{{w}} = \\\\frac{{{percent}}}{{100}}$"
                ],
                [
                    "6/9",
                    f"${percent}w = {part} \\\\cdot 100$"
                ],
                [
                    "7/9",
                    f"${percent}w = {part * 100}$"
                ],
                [
                    "8/9",
                    f"$w = \\\\frac{{{part * 100}}}{{{percent}}} = {whole}$"
                ],
                [
                    "9/9",
                    f"{part} is {percent}% of {whole}."
                ]
            ],
            "has_alternate_answers": False
        }
        
        variations.append(question)
    
    # Save to JSON file
    output = {"quizzes": variations[:51]}  # Ensure exactly 51
    
    with open('Gr6_13_E3_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_13_E3")

if __name__ == "__main__":
    generate_gr6_13_e3_variations()