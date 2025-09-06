import json
import random
import copy
from math import gcd

def load_templates():
    """Load template questions from parsed_templates.json"""
    with open('parsed_templates.json', 'r') as f:
        data = json.load(f)
    return data.get('Gr6_45_E3', [])

def simplify_fraction(num, den):
    """Simplify a fraction"""
    g = gcd(num, den)
    return num // g, den // g

def generate_dice_scenarios():
    """Generate various dice rolling scenarios"""
    scenarios = []
    
    # Standard dice
    dice_types = [
        (4, "4-sided die"),
        (6, "6-sided die"),
        (8, "8-sided die"),
        (10, "10-sided die"),
        (12, "12-sided die"),
        (20, "20-sided die")
    ]
    
    # Different targets for rolling
    for sides, die_name in dice_types:
        # Single number targets
        for target in range(1, min(sides + 1, 7)):
            scenarios.append({
                'type': 'die_single',
                'sides': sides,
                'die_name': die_name,
                'target': target,
                'target_text': f"a {target}" if target != 1 else "a one",
                'favorable': 1
            })
        
        # Even/odd targets
        scenarios.append({
            'type': 'die_even',
            'sides': sides,
            'die_name': die_name,
            'target_text': "an even number",
            'favorable': sides // 2
        })
        
        scenarios.append({
            'type': 'die_odd',
            'sides': sides,
            'die_name': die_name,
            'target_text': "an odd number",
            'favorable': (sides + 1) // 2
        })
        
        # Greater than/less than targets
        mid = sides // 2
        scenarios.append({
            'type': 'die_greater',
            'sides': sides,
            'die_name': die_name,
            'target_text': f"greater than {mid}",
            'favorable': sides - mid
        })
    
    return scenarios

def generate_coin_scenarios():
    """Generate coin flipping scenarios"""
    scenarios = []
    
    flip_counts = [2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 50, 100]
    
    for flips in flip_counts:
        scenarios.append({
            'type': 'coin',
            'flips': flips,
            'target': 'heads',
            'favorable': 1,
            'total': 2
        })
        scenarios.append({
            'type': 'coin',
            'flips': flips,
            'target': 'tails',
            'favorable': 1,
            'total': 2
        })
    
    return scenarios

def generate_spinner_scenarios():
    """Generate spinner scenarios"""
    scenarios = []
    
    # Different spinner configurations
    spinner_configs = [
        (3, ["red", "blue", "green"]),
        (4, ["red", "blue", "green", "yellow"]),
        (5, ["red", "blue", "green", "yellow", "purple"]),
        (6, ["red", "blue", "green", "yellow", "purple", "orange"]),
        (8, ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black"])
    ]
    
    for sections, colors in spinner_configs:
        for color in colors[:3]:  # Pick first 3 colors for variety
            scenarios.append({
                'type': 'spinner',
                'sections': sections,
                'colors': colors,
                'target': color,
                'favorable': 1
            })
    
    return scenarios

def generate_card_scenarios():
    """Generate card drawing scenarios"""
    scenarios = []
    
    # Standard deck variations
    deck_configs = [
        (52, 13, 4, "standard deck"),  # Standard 52-card deck
        (36, 9, 4, "36-card deck"),    # Reduced deck
        (32, 8, 4, "32-card deck"),    # Another common variant
    ]
    
    for total, ranks, suits, deck_name in deck_configs:
        # Drawing specific suits
        scenarios.append({
            'type': 'cards_suit',
            'total': total,
            'deck_name': deck_name,
            'target': 'a heart',
            'favorable': ranks
        })
        
        # Drawing specific ranks
        scenarios.append({
            'type': 'cards_rank',
            'total': total,
            'deck_name': deck_name,
            'target': 'an ace',
            'favorable': suits
        })
    
    return scenarios

def generate_pop_culture_context():
    """Generate pop culture themed contexts"""
    contexts = [
        "In a Pokemon battle simulation",
        "During a Yu-Gi-Oh duel",
        "In a Naruto ninja training exercise",
        "While playing a Dragon Ball Z game",
        "In a My Hero Academia probability lesson",
        "During a One Piece treasure hunt",
        "In an Attack on Titan strategy game",
        "While playing Demon Slayer dice game",
        "In a Jujutsu Kaisen cursed technique test",
        "During a Death Note probability puzzle",
        "In a Minecraft redstone randomizer",
        "While playing Among Us with probability rules",
        "In a Fortnite loot box simulation",
        "During a League of Legends champion selection",
        "In a Genshin Impact wish simulator"
    ]
    return random.choice(contexts)

def generate_variation(template, var_num, total_templates):
    """Generate a single variation based on template type"""
    variation = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{var_num}"
    
    if template['question_type'] == "Multiple Choice Question with Single Answer":
        # Generate dice rolling variation
        dice_scenarios = generate_dice_scenarios()
        scenario = random.choice(dice_scenarios)
        
        # Calculate rolls and prediction
        rolls = random.choice([6, 12, 18, 24, 30, 36, 42, 48, 60, scenario['sides']])
        
        # Calculate probability and prediction
        prob_num = scenario['favorable']
        prob_den = scenario['sides']
        prob_num_simplified, prob_den_simplified = simplify_fraction(prob_num, prob_den)
        
        prediction = (prob_num * rolls) // prob_den
        
        # Add context occasionally
        if random.random() < 0.3:
            context = generate_pop_culture_context()
            question_text = f"{context}, if you roll a {scenario['die_name']} {rolls} times, "
        else:
            question_text = f"If you roll a {scenario['die_name']} {rolls} times, "
        
        question_text += f"what is the best prediction possible for the number of times you will roll {scenario['target_text']}?"
        
        variation['question_text'] = question_text
        
        # Generate choices
        correct_answer = prediction
        wrong_answers = []
        
        # Generate plausible wrong answers
        for offset in [-2, -1, 1, 2, 3]:
            wrong = prediction + offset
            if wrong >= 0 and wrong != correct_answer:
                wrong_answers.append(wrong)
        
        # Add some random wrong answers
        while len(wrong_answers) < 5:
            wrong = random.randint(0, rolls)
            if wrong not in wrong_answers and wrong != correct_answer:
                wrong_answers.append(wrong)
        
        # Select 3 wrong answers and place correct answer randomly
        wrong_answers = random.sample(wrong_answers, 3)
        choices = wrong_answers
        correct_position = random.randint(0, 3)
        choices.insert(correct_position, correct_answer)
        
        variation['choices'] = [str(c) for c in choices]
        variation['correct_answers'] = [chr(65 + correct_position)]
        
        # Update solution
        variation['solution'] = [
            ["1/6", "Remember, the probability is the number of favourable outcomes out of the number of possible outcomes."],
            ["2/6", f"There are {scenario['sides']} possible outcomes: {', '.join(map(str, range(1, scenario['sides']+1)))}."],
            ["3/6", f"There {'is' if scenario['favorable'] == 1 else 'are'} {scenario['favorable']} favourable outcome{'s' if scenario['favorable'] > 1 else ''}: {scenario['target_text']}."],
            ["4/6", f"The probability is {prob_num} out of {prob_den}, or $\\frac{{{prob_num}}}{{{prob_den}}}$" + 
                    (f" = $\\frac{{{prob_num_simplified}}}{{{prob_den_simplified}}}$" if prob_num != prob_num_simplified else "") + "."],
            ["5/6", f"Now find $\\frac{{{prob_num_simplified}}}{{{prob_den_simplified}}}$ of {rolls}.\n" +
                    f"$\\frac{{{prob_num_simplified}}}{{{prob_den_simplified}}} \\cdot {rolls} = {prediction}$"],
            ["6/6", f"The best prediction possible is {prediction} out of {rolls} times."]
        ]
        
    else:  # Fill in the blank
        # Generate coin or spinner variation
        if random.random() < 0.6:
            # Coin flip variation
            flips = random.choice([2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 50, 100])
            target = random.choice(["heads", "tails"])
            
            prediction = flips // 2
            
            # Add context occasionally
            if random.random() < 0.3:
                context = generate_pop_culture_context()
                question_text = f"{context}, if you flip a coin {flips} times, "
            else:
                question_text = f"If you flip a coin {flips} times, "
            
            question_text += f"what is the best prediction possible for the number of times it will land on {target}?\n___"
            
            variation['question_text'] = question_text
            variation['correct_answers'] = [str(prediction)]
            
            variation['solution'] = [
                ["1/6", "Remember, the probability is the number of favourable outcomes out of the number of possible outcomes."],
                ["2/6", f"There are 2 possible outcomes: heads or tails."],
                ["3/6", f"There is 1 favourable outcome: {target}."],
                ["4/6", f"The probability is 1 out of 2, or $\\frac{{1}}{{2}}$."],
                ["5/6", f"Now find $\\frac{{1}}{{2}}$ of {flips}. $\\frac{{1}}{{2}} \\times {flips} = {prediction}$"],
                ["6/6", f"The best prediction possible is {prediction} out of {flips} times."]
            ]
        else:
            # Spinner variation
            sections = random.choice([3, 4, 5, 6, 8, 10])
            spins = random.choice([sections, sections*2, sections*3, sections*4, sections*5, sections*10])
            
            colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white", "brown"][:sections]
            target_color = random.choice(colors[:3])
            
            prediction = spins // sections
            
            question_text = f"A spinner has {sections} equal sections colored {', '.join(colors[:-1])}, and {colors[-1]}. "
            question_text += f"If you spin it {spins} times, what is the best prediction for the number of times it will land on {target_color}?\n___"
            
            variation['question_text'] = question_text
            variation['correct_answers'] = [str(prediction)]
            
            variation['solution'] = [
                ["1/6", "Remember, the probability is the number of favourable outcomes out of the number of possible outcomes."],
                ["2/6", f"There are {sections} possible outcomes: {', '.join(colors)}."],
                ["3/6", f"There is 1 favourable outcome: {target_color}."],
                ["4/6", f"The probability is 1 out of {sections}, or $\\frac{{1}}{{{sections}}}$."],
                ["5/6", f"Now find $\\frac{{1}}{{{sections}}}$ of {spins}. $\\frac{{1}}{{{sections}}} \\times {spins} = {prediction}$"],
                ["6/6", f"The best prediction possible is {prediction} out of {spins} times."]
            ]
    
    return variation

def main():
    """Main function to generate all variations"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_45_E3")
        return
    
    print(f"Found {len(templates)} templates for Gr6_45_E3")
    
    # Calculate how many variations we need
    total_needed = 51
    variations_needed = total_needed - len(templates)
    
    print(f"Generating {variations_needed} variations to reach {total_needed} total")
    
    variations = []
    
    # Generate variations
    for i in range(variations_needed):
        # Randomly select a template to base the variation on
        template = random.choice(templates)
        
        # Generate variation number (starting after templates)
        var_num = len(templates) + i + 1
        
        variation = generate_variation(template, var_num, len(templates))
        variations.append(variation)
        
        if (i + 1) % 10 == 0:
            print(f"Generated {i + 1} variations...")
    
    # Save variations to file
    output_file = 'Gr6_45_E3_variations.json'
    with open(output_file, 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"\nSuccessfully generated {len(variations)} variations")
    print(f"Variations saved to {output_file}")
    
    # Verify uniqueness
    question_texts = [v['question_text'] for v in variations]
    unique_questions = len(set(question_texts))
    print(f"Unique question texts: {unique_questions}/{len(variations)}")

if __name__ == "__main__":
    main()