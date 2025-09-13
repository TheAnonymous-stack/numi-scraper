import json
import random
from fractions import Fraction
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b) // gcd(a, b)

def simplify_fraction(numerator, denominator):
    """Simplify a fraction to its lowest terms"""
    g = gcd(abs(numerator), abs(denominator))
    return numerator // g, denominator // g

def generate_fraction_pair():
    """Generate two fractions that will have different denominators and realistic values"""
    # Common denominators for grade 6: 2, 3, 4, 5, 6, 8, 10, 12
    denominators = [2, 3, 4, 5, 6, 8, 10, 12]
    
    # Pick two different denominators
    denom1 = random.choice(denominators)
    denom2 = random.choice([d for d in denominators if d != denom1])
    
    # Generate numerators that make proper fractions (less than 1) or mixed numbers
    num1 = random.randint(1, denom1 - 1)  # Proper fraction
    num2 = random.randint(1, denom2 - 1)  # Proper fraction
    
    return (num1, denom1), (num2, denom2)

def solve_fraction_problem(frac1, frac2, operation):
    """Solve fraction addition or subtraction and return solution steps"""
    num1, denom1 = frac1
    num2, denom2 = frac2
    
    # Find LCD
    lcd = lcm(denom1, denom2)
    
    # Convert to equivalent fractions
    new_num1 = num1 * (lcd // denom1)
    new_num2 = num2 * (lcd // denom2)
    
    # Perform operation
    if operation == "add":
        result_num = new_num1 + new_num2
        op_symbol = "+"
    else:  # subtract
        result_num = new_num1 - new_num2
        op_symbol = "-"
    
    # Simplify result
    simplified_num, simplified_denom = simplify_fraction(result_num, lcd)
    
    return {
        "lcd": lcd,
        "equiv_frac1": (new_num1, lcd),
        "equiv_frac2": (new_num2, lcd),
        "result": (result_num, lcd),
        "simplified": (simplified_num, simplified_denom),
        "operation": op_symbol
    }

def create_word_problem(frac1, frac2, operation, context):
    """Create a word problem based on fractions and context"""
    scenarios = {
        "cooking": [
            ("recipe", "cups", "ingredients"),
            ("baking", "cups", "flour/sugar"),
            ("soup", "liters", "broth"),
            ("sauce", "cups", "liquid")
        ],
        "sports": [
            ("race", "miles", "distance"),
            ("practice", "hours", "time"),
            ("game", "hours", "playing time"),
            ("training", "hours", "workout time")
        ],
        "school": [
            ("homework", "hours", "study time"),
            ("project", "days", "work time"),
            ("reading", "hours", "time"),
            ("test", "hours", "preparation time")
        ],
        "crafts": [
            ("painting", "cups", "paint"),
            ("sewing", "yards", "fabric"),
            ("woodwork", "feet", "wood"),
            ("gardening", "cups", "water")
        ],
        "games": [
            ("puzzle", "hours", "time"),
            ("video game", "hours", "playing time"),
            ("board game", "hours", "game time"),
            ("card game", "hours", "time")
        ]
    }
    
    names = ["Alex", "Maya", "Jordan", "Sam", "Riley", "Casey", "Taylor", "Morgan", 
             "Jamie", "Avery", "Quinn", "Blake", "Sage", "River", "Phoenix"]
    
    scenario_type, unit, item = random.choice(scenarios[context])
    name1 = random.choice(names)
    name2 = random.choice([n for n in names if n != name1])
    
    num1, denom1 = frac1
    num2, denom2 = frac2
    
    if operation == "add":
        if context == "cooking":
            return f"{name1} used $\\frac{{{num1}}}{{{denom1}}}$ {unit} of {item} and {name2} used $\\frac{{{num2}}}{{{denom2}}}$ {unit} of the same {item}. How much {item} did they use in total?"
        elif context == "sports":
            return f"{name1} ran $\\frac{{{num1}}}{{{denom1}}}$ {unit} and {name2} ran $\\frac{{{num2}}}{{{denom2}}}$ {unit}. What is the total distance they ran together?"
        elif context == "school":
            return f"{name1} spent $\\frac{{{num1}}}{{{denom1}}}$ {unit} on {scenario_type} and {name2} spent $\\frac{{{num2}}}{{{denom2}}}$ {unit}. How much time did they spend in total?"
        elif context == "crafts":
            return f"{name1} used $\\frac{{{num1}}}{{{denom1}}}$ {unit} of {item} and {name2} used $\\frac{{{num2}}}{{{denom2}}}$ {unit}. How much {item} did they use altogether?"
        else:  # games
            return f"{name1} played for $\\frac{{{num1}}}{{{denom1}}}$ {unit} and {name2} played for $\\frac{{{num2}}}{{{denom2}}}$ {unit}. What was their total playing time?"
    else:  # subtract
        if context == "cooking":
            return f"{name1} had $\\frac{{{num1}}}{{{denom1}}}$ {unit} of {item} and used $\\frac{{{num2}}}{{{denom2}}}$ {unit}. How much {item} is left?"
        elif context == "sports":
            return f"{name1} planned to run $\\frac{{{num1}}}{{{denom1}}}$ {unit} but only ran $\\frac{{{num2}}}{{{denom2}}}$ {unit}. How much more distance does {name1} need to run?"
        elif context == "school":
            return f"{name1} allocated $\\frac{{{num1}}}{{{denom1}}}$ {unit} for {scenario_type} but only spent $\\frac{{{num2}}}{{{denom2}}}$ {unit}. How much time was saved?"
        elif context == "crafts":
            return f"{name1} bought $\\frac{{{num1}}}{{{denom1}}}$ {unit} of {item} and used $\\frac{{{num2}}}{{{denom2}}}$ {unit}. How much {item} is remaining?"
        else:  # games
            return f"{name1} had $\\frac{{{num1}}}{{{denom1}}}$ {unit} to play and already played for $\\frac{{{num2}}}{{{denom2}}}$ {unit}. How much playing time is left?"

def generate_variations():
    """Generate 50 variations of fraction word problems"""
    variations = []
    contexts = ["cooking", "sports", "school", "crafts", "games"]
    
    for i in range(2, 52):  # Generate variations 3_2 through 3_51
        # Alternate between addition and subtraction
        operation = "add" if i % 2 == 0 else "subtract"
        context = random.choice(contexts)
        
        # Generate fraction pair
        frac1, frac2 = generate_fraction_pair()
        
        # For subtraction, ensure first fraction is larger
        if operation == "subtract":
            # Convert to decimal to compare
            val1 = frac1[0] / frac1[1]
            val2 = frac2[0] / frac2[1]
            if val1 <= val2:
                # Swap or regenerate
                if val2 < 0.9:  # If second fraction is not too large, swap
                    frac1, frac2 = frac2, frac1
                else:
                    # Regenerate first fraction to be larger
                    new_denom = frac1[1]
                    new_num = random.randint(frac2[0] * (new_denom // frac2[1]) + 1, new_denom - 1)
                    frac1 = (new_num, new_denom)
        
        # Solve the problem
        solution_data = solve_fraction_problem(frac1, frac2, operation)
        
        # Create word problem
        question_text = create_word_problem(frac1, frac2, operation, context)
        
        # Format answer
        if solution_data["simplified"][1] == 1:
            answer = str(solution_data["simplified"][0])
        else:
            answer = f"{solution_data['simplified'][0]}/{solution_data['simplified'][1]}"
        
        # Create solution steps
        num1, denom1 = frac1
        num2, denom2 = frac2
        lcd = solution_data["lcd"]
        equiv1 = solution_data["equiv_frac1"]
        equiv2 = solution_data["equiv_frac2"]
        op_symbol = solution_data["operation"]
        result = solution_data["result"]
        simplified = solution_data["simplified"]
        
        solution_steps = [
            [
                "1/4",
                f"To solve this problem, we need to {operation} $\\frac{{{num1}}}{{{denom1}}}$ {op_symbol} $\\frac{{{num2}}}{{{denom2}}}$."
            ],
            [
                "2/4",
                f"Find the least common denominator (LCD) of {denom1} and {denom2}. The LCD is {lcd}."
            ],
            [
                "3/4",
                f"Convert to equivalent fractions: $\\frac{{{num1}}}{{{denom1}}} = \\frac{{{equiv1[0]}}}{{{lcd}}}$ and $\\frac{{{num2}}}{{{denom2}}} = \\frac{{{equiv2[0]}}}{{{lcd}}}$"
            ]
        ]
        
        if simplified[1] == 1:
            solution_steps.append([
                "4/4",
                f"Calculate: $\\frac{{{equiv1[0]}}}{{{lcd}}} {op_symbol} \\frac{{{equiv2[0]}}}{{{lcd}}} = \\frac{{{result[0]}}}{{{lcd}}} = {simplified[0]}$"
            ])
        elif result[0] == simplified[0] and result[1] == simplified[1]:
            solution_steps.append([
                "4/4",
                f"Calculate: $\\frac{{{equiv1[0]}}}{{{lcd}}} {op_symbol} \\frac{{{equiv2[0]}}}{{{lcd}}} = \\frac{{{result[0]}}}{{{lcd}}}$"
            ])
        else:
            solution_steps.append([
                "4/4",
                f"Calculate: $\\frac{{{equiv1[0]}}}{{{lcd}}} {op_symbol} \\frac{{{equiv2[0]}}}{{{lcd}}} = \\frac{{{result[0]}}}{{{lcd}}} = \\frac{{{simplified[0]}}}{{{simplified[1]}}}$"
            ])
        
        variation = {
            "skills": "add-and-subtract-fractions-with-unlike-denominators-word-problems-i",
            "question_text": question_text,
            "tag": "Gr6_19_E3",
            "question_number": f"3_{i}",
            "question_type": "Fill in the blank",
            "correct_answers": [answer],
            "solution": solution_steps,
            "has_alternate_answers": False
        }
        
        variations.append(variation)
        print(f"Generated variation 3_{i}: {operation} problem with answer {answer}")
    
    return variations

def main():
    print("Generating 50 variations for Gr6_19_E3 fraction word problems...")
    
    # Generate variations
    variations = generate_variations()
    
    # Create the output structure
    output = {
        "quizzes": variations
    }
    
    # Save to file
    output_file = "C:\\Users\\kapil\\numi-scraper\\Gr6_19_E3_variations.json"
    
    # Load existing file to preserve the template
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        # Add new variations to existing template
        existing_data["quizzes"].extend(variations)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
        print(f"\nSuccessfully generated and saved 50 variations to {output_file}")
        print(f"Total questions in file: {len(existing_data['quizzes'])}")
        
    except Exception as e:
        print(f"Error updating file: {e}")
        
        # Create new file with just the variations
        with open("Gr6_19_E3_new_variations.json", 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print("Saved variations to new file: Gr6_19_E3_new_variations.json")

if __name__ == "__main__":
    main()