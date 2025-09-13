import json
import random
from typing import List, Dict, Any

# Define themes for word problems
themes = [
    # Pop culture and entertainment
    {"context": "video game", "item": "coins", "action": "collected", "location": "in the game"},
    {"context": "streaming service", "item": "episodes", "action": "watched", "location": "this month"},
    {"context": "anime convention", "item": "manga volumes", "action": "sold", "location": "at the booth"},
    {"context": "Pokemon trainer", "item": "Pokemon", "action": "caught", "location": "in the region"},
    {"context": "Marvel movie theater", "item": "tickets", "action": "sold", "location": "opening weekend"},
    {"context": "K-pop concert", "item": "fans", "action": "attended", "location": "at the venue"},
    {"context": "Netflix series", "item": "viewers", "action": "watched", "location": "in the first week"},
    {"context": "YouTube channel", "item": "subscribers", "action": "gained", "location": "this year"},
    {"context": "TikTok creator", "item": "followers", "action": "gained", "location": "after going viral"},
    {"context": "Minecraft server", "item": "blocks", "action": "placed", "location": "in the build"},
    
    # School and education
    {"context": "school library", "item": "books", "action": "borrowed", "location": "this semester"},
    {"context": "science fair", "item": "projects", "action": "submitted", "location": "for judging"},
    {"context": "math club", "item": "problems", "action": "solved", "location": "during practice"},
    {"context": "art class", "item": "paintings", "action": "created", "location": "this year"},
    
    # Sports and activities
    {"context": "basketball team", "item": "points", "action": "scored", "location": "in the season"},
    {"context": "soccer club", "item": "goals", "action": "scored", "location": "in the tournament"},
    {"context": "swimming pool", "item": "laps", "action": "completed", "location": "during practice"},
    {"context": "chess tournament", "item": "games", "action": "played", "location": "in the competition"},
    
    # Business and stores
    {"context": "bakery", "item": "cupcakes", "action": "sold", "location": "on Saturday"},
    {"context": "bookstore", "item": "novels", "action": "sold", "location": "during the sale"},
    {"context": "toy store", "item": "toys", "action": "sold", "location": "before holidays"},
    {"context": "candy shop", "item": "chocolates", "action": "sold", "location": "on Valentine's Day"},
    
    # Nature and environment
    {"context": "forest", "item": "trees", "action": "planted", "location": "this spring"},
    {"context": "beach cleanup", "item": "pieces of trash", "action": "collected", "location": "along the shore"},
    {"context": "garden", "item": "flowers", "action": "bloomed", "location": "in the summer"},
    {"context": "farm", "item": "apples", "action": "harvested", "location": "from the orchard"},
]

def generate_subtraction_problem(theme: Dict, num1: int, num2: int, round_place: str) -> Dict:
    """Generate a subtraction estimation problem"""
    
    # Determine rounding values
    if round_place == "ten thousand":
        rounded1 = round(num1, -4)
        rounded2 = round(num2, -4)
        place_value = 10000
    elif round_place == "thousand":
        rounded1 = round(num1, -3)
        rounded2 = round(num2, -3)
        place_value = 1000
    elif round_place == "hundred":
        rounded1 = round(num1, -2)
        rounded2 = round(num2, -2)
        place_value = 100
    else:  # ten
        rounded1 = round(num1, -1)
        rounded2 = round(num2, -1)
        place_value = 10
    
    estimate = rounded1 - rounded2
    wrong_estimate = estimate + random.choice([place_value, place_value*2, -place_value]) * random.choice([1, 2, 5, 10])
    
    # Ensure wrong estimate is positive and different
    if wrong_estimate <= 0 or wrong_estimate == estimate:
        wrong_estimate = estimate + place_value * 10
    
    # Randomize choice order
    if random.random() < 0.5:
        choices = [str(estimate), str(wrong_estimate)]
        correct_answer = "A"
    else:
        choices = [str(wrong_estimate), str(estimate)]
        correct_answer = "B"
    
    question_text = f"The {theme['context']} had {num1} {theme['item']}. They used {num2} {theme['item']} {theme['location']}. About how many {theme['item']} are left? Choose the better estimate."
    
    total_steps = random.choice([5, 6])
    
    solution = [
        ["1/" + str(total_steps), f"Subtract the number of {theme['item']} used from the total.\n{num1} - {num2} = ?"],
        ["2/" + str(total_steps), f"Round each number to the nearest {round_place}."],
        ["3/" + str(total_steps), f"{num1} $\\rightarrow$ {rounded1}\n{num2} $\\rightarrow$ {rounded2}"],
        ["4/" + str(total_steps), f"${num1} - {num2} \\rightarrow {rounded1} - {rounded2} =$?"]
    ]
    
    if total_steps == 6:
        solution.append(["5/" + str(total_steps), f"{rounded1} - {rounded2} = {estimate}"])
        solution.append(["6/" + str(total_steps), f"{estimate:,} is the better estimate."])
    else:
        solution.append(["5/" + str(total_steps), f"${rounded1} - {rounded2} = {estimate}$\n{estimate:,} is the better estimate."])
    
    return {
        "skills": "estimate-sums-and-differences-word-problems",
        "question_text": question_text,
        "tag": "Gr6_14_E4",
        "question_type": "Multiple Choice Question with Single Answer",
        "choices": choices,
        "correct_answers": [correct_answer],
        "solution": solution
    }

def generate_addition_problem(theme: Dict, num1: int, num2: int, round_place: str) -> Dict:
    """Generate an addition estimation problem"""
    
    # Determine rounding values
    if round_place == "ten thousand":
        rounded1 = round(num1, -4)
        rounded2 = round(num2, -4)
        place_value = 10000
    elif round_place == "thousand":
        rounded1 = round(num1, -3)
        rounded2 = round(num2, -3)
        place_value = 1000
    elif round_place == "hundred":
        rounded1 = round(num1, -2)
        rounded2 = round(num2, -2)
        place_value = 100
    else:  # ten
        rounded1 = round(num1, -1)
        rounded2 = round(num2, -1)
        place_value = 10
    
    estimate = rounded1 + rounded2
    wrong_estimate = estimate + random.choice([place_value, place_value*2, -place_value]) * random.choice([1, 2, 5])
    
    # Ensure wrong estimate is positive and different
    if wrong_estimate <= 0 or wrong_estimate == estimate:
        wrong_estimate = estimate + place_value * 5
    
    # Randomize choice order
    if random.random() < 0.5:
        choices = [str(estimate), str(wrong_estimate)]
        correct_answer = "A"
    else:
        choices = [str(wrong_estimate), str(estimate)]
        correct_answer = "B"
    
    question_text = f"A {theme['context']} has {num1} {theme['item']} from last year and gained {num2} more {theme['item']} {theme['location']}. About how many {theme['item']} in total? Choose the better estimate."
    
    total_steps = random.choice([5, 6])
    
    solution = [
        ["1/" + str(total_steps), f"Add the {theme['item']}.\n{num1} + {num2} = ?"],
        ["2/" + str(total_steps), f"Round each number to the nearest {round_place}."],
        ["3/" + str(total_steps), f"{num1} $\\rightarrow$ {rounded1}\n{num2} $\\rightarrow$ {rounded2}"],
        ["4/" + str(total_steps), f"${num1} + {num2} \\rightarrow {rounded1} + {rounded2} = $?"]
    ]
    
    if total_steps == 6:
        solution.append(["5/" + str(total_steps), f"{rounded1} + {rounded2} = {estimate}"])
        solution.append(["6/" + str(total_steps), f"{estimate:,} is the better estimate."])
    else:
        solution.append(["5/" + str(total_steps), f"${rounded1} + {rounded2} = {estimate}$\n{estimate:,} is the better estimate."])
    
    return {
        "skills": "estimate-sums-and-differences-word-problems",
        "question_text": question_text,
        "tag": "Gr6_14_E4",
        "question_type": "Multiple Choice Question with Single Answer",
        "choices": choices,
        "correct_answers": [correct_answer],
        "solution": solution
    }

def generate_variations():
    """Generate 49 variations of the estimation word problems"""
    
    variations = []
    used_combinations = set()
    variation_count = 1
    
    # We need exactly 49 variations (51 total - 2 templates)
    while len(variations) < 49:
        # Randomly choose between addition and subtraction
        operation = random.choice(["addition", "subtraction"])
        
        # Select a random theme
        theme = random.choice(themes)
        
        if operation == "subtraction":
            # Generate numbers for subtraction (larger - smaller)
            # Mix different ranges for variety
            range_choice = random.choice(["large", "medium", "small"])
            
            if range_choice == "large":
                num1 = random.randint(50000, 99999)
                num2 = random.randint(10000, 40000)
                round_place = "ten thousand"
            elif range_choice == "medium":
                num1 = random.randint(5000, 9999)
                num2 = random.randint(1000, 4000)
                round_place = "thousand"
            else:
                num1 = random.randint(500, 999)
                num2 = random.randint(100, 400)
                round_place = "hundred"
            
            # Create unique identifier
            combo = (operation, num1, num2, theme['context'])
            if combo not in used_combinations:
                used_combinations.add(combo)
                problem = generate_subtraction_problem(theme, num1, num2, round_place)
                # Assign question number based on template pattern
                template_num = "4" if variation_count % 2 == 1 else "4"
                problem["question_number"] = f"{template_num}_{variation_count + 2}"  # +2 because we have 2 templates
                variations.append(problem)
                variation_count += 1
        
        else:  # addition
            # Generate numbers for addition
            range_choice = random.choice(["large", "medium", "small"])
            
            if range_choice == "large":
                num1 = random.randint(10000, 50000)
                num2 = random.randint(10000, 50000)
                round_place = "ten thousand"
            elif range_choice == "medium":
                num1 = random.randint(1000, 5000)
                num2 = random.randint(1000, 5000)
                round_place = "thousand"
            else:
                num1 = random.randint(100, 999)
                num2 = random.randint(100, 999)
                round_place = "hundred"
            
            # Create unique identifier
            combo = (operation, num1, num2, theme['context'])
            if combo not in used_combinations:
                used_combinations.add(combo)
                problem = generate_addition_problem(theme, num1, num2, round_place)
                # Assign question number
                template_num = "4" if variation_count % 2 == 1 else "4"
                problem["question_number"] = f"{template_num}_{variation_count + 2}"  # +2 because we have 2 templates
                variations.append(problem)
                variation_count += 1
    
    return variations

def main():
    # Generate variations
    print("Generating 49 variations for Gr6_14_E4...")
    variations = generate_variations()
    
    # Save to JSON file
    output_file = "Gr6_14_E4_variations.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(variations)} variations")
    print(f"Saved to {output_file}")
    
    # Verify total count
    print(f"Total questions (2 templates + {len(variations)} variations) = {2 + len(variations)}")

if __name__ == "__main__":
    main()