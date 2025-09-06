import json
import random
import copy

def load_templates():
    """Load template questions from parsed_templates.json"""
    with open('parsed_templates.json', 'r') as f:
        data = json.load(f)
    return data.get('Gr6_45_E2', [])

def generate_die_variations():
    """Generate variations for dice probability questions"""
    variations = []
    
    # Different dice configurations
    dice_configs = [
        (4, "4-sided"),   # D4
        (6, "6-sided"),   # Standard die
        (8, "8-sided"),   # D8
        (10, "10-sided"), # D10
        (12, "12-sided"), # D12
        (20, "20-sided")  # D20
    ]
    
    # Different probability scenarios
    scenarios = [
        ("not even", lambda n: [i for i in range(1, n+1) if i % 2 != 0]),
        ("not odd", lambda n: [i for i in range(1, n+1) if i % 2 == 0]),
        ("not a multiple of 3", lambda n: [i for i in range(1, n+1) if i % 3 != 0]),
        ("not greater than {mid}", lambda n: [i for i in range(1, n+1) if i <= n//2]),
        ("not less than {mid}", lambda n: [i for i in range(1, n+1) if i >= (n//2 + 1)]),
        ("not prime", lambda n: [i for i in range(1, n+1) if not is_prime(i)]),
    ]
    
    # Pop culture themes for word problems
    themes = [
        "In a game of Dungeons & Dragons",
        "While playing Monopoly",
        "In a Pokemon battle simulation",
        "During a Mario Party mini-game",
        "In a Naruto-themed board game",
        "While playing Yu-Gi-Oh dice game",
        "In a Harry Potter wizard's duel",
        "During a One Piece adventure game",
        "In a Minecraft probability challenge",
        "While playing Attack on Titan strategy game"
    ]
    
    return dice_configs, scenarios, themes

def generate_card_variations():
    """Generate variations for card probability questions"""
    # Different card sets
    card_sets = [
        (list(range(1, 5)), "1, 2, 3, and 4"),
        (list(range(2, 10)), "2, 3, 4, 5, 6, 7, 8, and 9"),
        (list(range(1, 9)), "1, 2, 3, 4, 5, 6, 7, and 8"),
        (list(range(3, 11)), "3, 4, 5, 6, 7, 8, 9, and 10"),
        (list(range(1, 13)), "1 through 12"),
        (list(range(5, 13)), "5, 6, 7, 8, 9, 10, 11, and 12"),
        (list(range(1, 7)), "1, 2, 3, 4, 5, and 6"),
        (list(range(2, 8)), "2, 3, 4, 5, 6, and 7"),
        (list(range(4, 12)), "4, 5, 6, 7, 8, 9, 10, and 11"),
        (list(range(1, 11)), "1 through 10")
    ]
    
    return card_sets

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def format_percentage(decimal):
    """Convert decimal to percentage string"""
    percentage = int(decimal * 100)
    return f"{percentage}%"

def format_fraction(numerator, denominator):
    """Format and simplify fraction"""
    from math import gcd
    g = gcd(numerator, denominator)
    return f"{numerator//g}/{denominator//g}"

def generate_variation(template, var_num, total_templates):
    """Generate a single variation based on template type"""
    variation = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{var_num}"
    
    # Update image tag if present
    if 'image_tag' in variation:
        old_tag = variation['image_tag']
        parts = old_tag.split('_')
        if len(parts) >= 4:
            parts[3] = str(var_num)
            variation['image_tag'] = '_'.join(parts)
    
    # Update solution image tags if present
    if 'solution_image_tag' in variation:
        for step in variation['solution_image_tag']:
            if len(step) > 1:
                old_tag = step[1]
                parts = old_tag.split('_')
                if len(parts) >= 4:
                    # Extract the step number from the tag
                    step_suffix = parts[-1] if parts[-1].startswith('step_') else ''
                    parts[3] = str(var_num)
                    if step_suffix:
                        parts[-1] = step_suffix
                    step[1] = '_'.join(parts)
    
    if template['question_type'] == "Multiple Choice Question with Single Answer":
        # Die probability variation
        dice_configs, scenarios, themes = generate_die_variations()
        
        # Pick random configuration
        die_size, die_name = random.choice(dice_configs)
        scenario_text, scenario_func = random.choice(scenarios)
        theme = random.choice(themes)
        
        # Handle special scenario text formatting
        if "{mid}" in scenario_text:
            scenario_text = scenario_text.format(mid=die_size//2)
        
        # Calculate probability
        favorable = scenario_func(die_size)
        prob_favorable = len(favorable) / die_size
        
        # Generate question text with theme
        if random.random() < 0.3:  # 30% chance to use theme
            variation['question_text'] = f"{theme}, you roll a {die_name} die.\nWhat is P({scenario_text})?"
        else:
            variation['question_text'] = f"You roll a {die_name} die.\nWhat is P({scenario_text})?"
        
        # Generate choices with correct answer
        correct_percentage = format_percentage(prob_favorable)
        wrong_percentages = []
        
        # Generate plausible wrong answers
        for _ in range(3):
            wrong_prob = random.choice([0.1, 0.2, 0.25, 0.3, 0.33, 0.4, 0.5, 0.6, 0.67, 0.7, 0.75, 0.8, 0.9])
            wrong_perc = format_percentage(wrong_prob)
            if wrong_perc != correct_percentage and wrong_perc not in wrong_percentages:
                wrong_percentages.append(wrong_perc)
        
        # Ensure we have 3 unique wrong answers
        while len(wrong_percentages) < 3:
            wrong_prob = random.uniform(0.1, 0.9)
            wrong_perc = format_percentage(wrong_prob)
            if wrong_perc != correct_percentage and wrong_perc not in wrong_percentages:
                wrong_percentages.append(wrong_perc)
        
        # Randomly place correct answer
        choices = wrong_percentages[:3]
        correct_position = random.randint(0, 3)
        choices.insert(correct_position, correct_percentage)
        variation['choices'] = choices
        variation['correct_answers'] = [chr(65 + correct_position)]  # A, B, C, or D
        
        # Update solution
        complement_favorable = [i for i in range(1, die_size+1) if i not in favorable]
        prob_complement = len(complement_favorable) / die_size
        
        variation['solution'] = [
            ["1/5", "Remember, P(not A) = 1 - P(A)"],
            ["2/5", f"Find P({scenario_text.replace('not ', '')}). The die has {die_size} sides, numbered 1 through {die_size}. "
                     f"The favorable outcomes are {', '.join(map(str, complement_favorable[:5]))}{'...' if len(complement_favorable) > 5 else ''}. "
                     f"There are {len(complement_favorable)} favorable outcomes.\n"
                     f"$P({scenario_text.replace('not ', '')}) = \\frac{{{len(complement_favorable)}}}{{{die_size}}}$"],
            ["3/5", f"Now find P({scenario_text})."],
            ["4/5", f"P({scenario_text})\n=1 - P({scenario_text.replace('not ', '')})\n"
                    f"=1 - $\\frac{{{len(complement_favorable)}}}{{{die_size}}}$\n"
                    f"=$\\frac{{{len(favorable)}}}{{{die_size}}}$"],
            ["5/5", f"Write your answer as a decimal. Then convert your answer to a percentage.\n"
                    f"$\\frac{{{len(favorable)}}}{{{die_size}}} = {prob_favorable:.1f} = {correct_percentage}$\n"
                    f"P({scenario_text}) = {correct_percentage}."]
        ]
        
    else:  # Fill in the blank (card variation)
        card_sets = generate_card_variations()
        cards, cards_text = random.choice(card_sets)
        
        # Generate probability scenario
        scenario_type = random.choice(["not even", "not odd", "not a multiple of 3", "not greater than", "not less than"])
        
        if scenario_type == "not greater than":
            threshold = cards[len(cards)//2]
            favorable = [c for c in cards if c > threshold]
            scenario_text = f"not greater than {threshold}"
        elif scenario_type == "not less than":
            threshold = cards[len(cards)//2]
            favorable = [c for c in cards if c < threshold]
            scenario_text = f"not less than {threshold}"
        elif scenario_type == "not even":
            favorable = [c for c in cards if c % 2 != 0]
            scenario_text = "not even"
        elif scenario_type == "not odd":
            favorable = [c for c in cards if c % 2 == 0]
            scenario_text = "not odd"
        else:  # not a multiple of 3
            favorable = [c for c in cards if c % 3 != 0]
            scenario_text = "not a multiple of 3"
        
        prob = len(favorable) / len(cards)
        
        # Format as decimal
        if prob == 0.5:
            answer = "0.5"
        elif prob == 0.25:
            answer = "0.25"
        elif prob == 0.75:
            answer = "0.75"
        else:
            answer = f"{prob:.2f}" if prob != int(prob) else str(int(prob))
        
        variation['question_text'] = f"You pick a card at random.\nWhat is P({scenario_text})?\nWrite your answer as a decimal.\n __"
        variation['correct_answers'] = [answer]
        
        # Update backend description if image tag exists
        if 'backend_description' in variation:
            variation['backend_description'] = f"This image shows {len(cards)} green cards arranged in rows. The cards show the numbers {cards_text}."
        
        # Update solution
        complement_favorable = [c for c in cards if c not in favorable]
        variation['solution'] = [
            ["1/5", "Remember, P(not A) = 1 - P(A)"],
            ["2/5", f"Find P({scenario_text.replace('not ', '')}). There are {len(cards)} cards, numbered {cards_text}. "
                    f"The favorable outcomes are {', '.join(map(str, complement_favorable[:8]))}. "
                    f"There are {len(complement_favorable)} favorable outcomes.\n"
                    f"$P({scenario_text.replace('not ', '')}) = \\frac{{{len(complement_favorable)}}}{{{len(cards)}}}$"],
            ["3/5", f"Now find P({scenario_text})."],
            ["4/5", f"P({scenario_text})\n=1 - P({scenario_text.replace('not ', '')})\n"
                    f"=1 - $\\frac{{{len(complement_favorable)}}}{{{len(cards)}}}$\n"
                    f"=$\\frac{{{len(favorable)}}}{{{len(cards)}}}$"],
            ["5/5", f"Write your answer as a decimal.\n"
                    f"$\\frac{{{len(favorable)}}}{{{len(cards)}}} = {answer}$\n"
                    f"P({scenario_text}) = {answer}."]
        ]
    
    return variation

def main():
    """Main function to generate all variations"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_45_E2")
        return
    
    print(f"Found {len(templates)} templates for Gr6_45_E2")
    
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
    output_file = 'Gr6_45_E2_variations.json'
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