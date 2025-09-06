import json
import random
import copy

def load_templates():
    """Load template questions from the fixed JSON file"""
    with open('file_fixed.json', 'r') as f:
        data = json.load(f)
    return [q for q in data if q.get('tag') == 'Gr6_49_E1']

def generate_conversion_variations():
    """Generate diverse metric unit conversion problems"""
    variations = []
    
    # Define conversion types with their relationships
    conversions = [
        # Volume conversions (millilitres to/from litres)
        {'from': 'litres', 'to': 'millilitres', 'factor': 1000, 'values': [2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 20, 25, 0.5, 1.5, 2.5, 3.5, 4.5, 7.5, 0.25, 0.75]},
        {'from': 'millilitres', 'to': 'litres', 'factor': 0.001, 'values': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 500, 1500, 2500, 3500, 4500, 250, 750, 1250, 1750]},
        
        # Mass conversions (grams to/from kilograms)
        {'from': 'kilograms', 'to': 'grams', 'factor': 1000, 'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0.5, 1.5, 2.5, 3.5, 0.25, 0.75, 1.25, 1.75]},
        {'from': 'grams', 'to': 'kilograms', 'factor': 0.001, 'values': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 500, 1500, 2500, 3500, 4500, 250, 750]},
        
        # Length conversions (millimetres to/from centimetres)
        {'from': 'centimetres', 'to': 'millimetres', 'factor': 10, 'values': [2, 3, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100]},
        {'from': 'millimetres', 'to': 'centimetres', 'factor': 0.1, 'values': [10, 20, 30, 50, 60, 70, 80, 90, 100, 120, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]},
        
        # Length conversions (centimetres to/from metres)
        {'from': 'metres', 'to': 'centimetres', 'factor': 100, 'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0.5, 1.5, 2.5, 3.5, 0.25, 0.75, 1.25, 1.75]},
        {'from': 'centimetres', 'to': 'metres', 'factor': 0.01, 'values': [100, 200, 300, 400, 500, 600, 700, 800, 900, 50, 150, 250, 350, 450, 25, 75, 125, 175]},
        
        # Length conversions (metres to/from kilometres)
        {'from': 'kilometres', 'to': 'metres', 'factor': 1000, 'values': [1, 2, 3, 4, 5, 0.5, 1.5, 2.5, 0.25, 0.75]},
        {'from': 'metres', 'to': 'kilometres', 'factor': 0.001, 'values': [1000, 2000, 3000, 4000, 5000, 500, 1500, 2500, 250, 750]}
    ]
    
    # Generate variations ensuring diversity
    used_combinations = set()
    
    for conv_type in conversions:
        for value in conv_type['values']:
            combo = (conv_type['from'], conv_type['to'], value)
            if combo not in used_combinations and len(variations) < 48:
                used_combinations.add(combo)
                
                result = value * conv_type['factor']
                # Format result nicely (remove unnecessary decimals)
                if result == int(result):
                    result = int(result)
                
                variations.append({
                    'from_unit': conv_type['from'],
                    'to_unit': conv_type['to'],
                    'from_value': value,
                    'to_value': result,
                    'factor': conv_type['factor']
                })
    
    # Shuffle for variety
    random.shuffle(variations)
    return variations[:48]  # Return exactly 48 variations

def get_conversion_explanation(from_unit, to_unit, factor):
    """Get the conversion relationship explanation"""
    relationships = {
        ('litres', 'millilitres'): "1 litre = 1000 millilitres",
        ('millilitres', 'litres'): "1 litre = 1000 millilitres",
        ('kilograms', 'grams'): "1 kilogram = 1000 grams",
        ('grams', 'kilograms'): "1 kilogram = 1000 grams",
        ('centimetres', 'millimetres'): "1 centimetre = 10 millimetres",
        ('millimetres', 'centimetres'): "1 centimetre = 10 millimetres",
        ('metres', 'centimetres'): "1 metre = 100 centimetres",
        ('centimetres', 'metres'): "1 metre = 100 centimetres",
        ('kilometres', 'metres'): "1 kilometre = 1000 metres",
        ('metres', 'kilometres'): "1 kilometre = 1000 metres"
    }
    return relationships.get((from_unit, to_unit), f"1 {from_unit[:-1]} = {int(1/factor) if factor < 1 else int(factor)} {to_unit}")

def create_variation(templates, variation_data, variation_num):
    """Create a single variation from a randomly selected template"""
    # Randomly select a template
    template = random.choice(templates)
    new_q = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    new_q['question_number'] = f"{template_num}_{variation_num}"
    
    # Update question text
    from_unit = variation_data['from_unit']
    to_unit = variation_data['to_unit']
    from_value = variation_data['from_value']
    to_value = variation_data['to_value']
    
    # Format values nicely
    from_str = str(int(from_value)) if from_value == int(from_value) else str(from_value)
    to_str = str(int(to_value)) if to_value == int(to_value) else str(to_value)
    
    # Randomly decide direction of conversion in question
    if random.choice([True, False]):
        new_q['question_text'] = f"Convert:\n___ {to_unit} = {from_str} {from_unit}"
        new_q['correct_answers'] = [to_str]
        asking_for = to_unit
        given = f"{from_str} {from_unit}"
    else:
        new_q['question_text'] = f"Convert:\n{to_str} {to_unit} = ___ {from_unit}"
        new_q['correct_answers'] = [from_str]
        asking_for = from_unit
        given = f"{to_str} {to_unit}"
    
    # Update solution based on conversion type
    relationship = get_conversion_explanation(from_unit, to_unit, variation_data['factor'])
    
    if variation_data['factor'] > 1:  # Converting to smaller unit (multiply)
        operation = "Multiply"
        calc_factor = int(variation_data['factor'])
        if asking_for == to_unit:
            calc = f"${from_str} \\times {calc_factor} = {to_str}$"
            explanation = f"There are {to_str} {to_unit} in {from_str} {from_unit}."
        else:
            calc = f"${to_str} \\div {calc_factor} = {from_str}$"
            explanation = f"{to_str} {to_unit} equals {from_str} {from_unit}."
    else:  # Converting to larger unit (divide)
        operation = "Divide"
        calc_factor = int(1 / variation_data['factor'])
        if asking_for == to_unit:
            calc = f"${from_str} \\div {calc_factor} = {to_str}$"
            explanation = f"{from_str} {from_unit} equals {to_str} {to_unit}."
        else:
            calc = f"${to_str} \\times {calc_factor} = {from_str}$"
            explanation = f"There are {from_str} {from_unit} in {to_str} {to_unit}."
    
    # Build solution steps
    new_q['solution'] = [
        [
            "1/4",
            relationship
        ],
        [
            "2/4",
            f"Find out how many {asking_for} are {'in' if 'litre' in asking_for or 'gram' in asking_for else 'equivalent to'} {given}."
        ],
        [
            "3/4",
            f"{operation}: \n{calc}. {explanation}"
        ],
        [
            "4/4",
            f"{new_q['correct_answers'][0]} {asking_for} = {given}." if new_q['question_text'].startswith('Convert:\n___') else f"{given} = {new_q['correct_answers'][0]} {asking_for}."
        ]
    ]
    
    return new_q

def main():
    """Generate all variations for Gr6_49_E1"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_49_E1")
        return
    
    print(f"Found {len(templates)} templates for Gr6_49_E1")
    
    # Generate variation data
    variation_data = generate_conversion_variations()
    
    # Create all variations
    variations = []
    for i, var_data in enumerate(variation_data, start=4):  # Start from 4 since we have 3 templates
        variation = create_variation(templates, var_data, i)
        variations.append(variation)
    
    # Save variations to JSON file
    output_file = 'Gr6_49_E1_variations.json'
    with open(output_file, 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_49_E1")
    print(f"Saved to {output_file}")
    print(f"Total questions (including {len(templates)} templates): {len(variations) + len(templates)}")

if __name__ == "__main__":
    main()