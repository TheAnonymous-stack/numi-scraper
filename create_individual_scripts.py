import json
import os

# Template for individual generation scripts
SCRIPT_TEMPLATE = '''import json
import random
import copy
from fractions import Fraction
from decimal import Decimal
from math import gcd

# Pop culture themes for word problems
POP_CULTURE_THEMES = {{
    'anime': {{
        'characters': ['Naruto', 'Goku', 'Luffy', 'Ichigo', 'Eren', 'Levi', 'Mikasa', 'Tanjiro', 'Nezuko',
                      'Deku', 'Bakugo', 'Todoroki', 'Gojo', 'Yuji', 'Megumi', 'Nobara', 'Anya', 'Loid'],
        'activities': ['training', 'mission', 'quest', 'battle preparation', 'technique practice',
                      'chakra control exercise', 'devil fruit training', 'titan elimination practice']
    }},
    'gaming': {{
        'characters': ['Mario', 'Luigi', 'Link', 'Zelda', 'Master Chief', 'Kratos', 'Ellie', 'Joel',
                      'Cloud', 'Sephiroth', 'Sonic', 'Pikachu', 'Steve', 'Alex'],
        'activities': ['speedrun', 'raid', 'dungeon', 'boss fight', 'level completion', 'achievement hunt',
                      'resource gathering', 'crafting session']
    }},
    'tv_shows': {{
        'characters': ['Walter White', 'Jesse', 'Eleven', 'Mike Wheeler', 'Dustin', 'Rick', 'Morty',
                      'Sheldon', 'Leonard', 'Penny', 'Joey', 'Chandler', 'Ross', 'Rachel'],
        'activities': ['experiment', 'investigation', 'project', 'homework', 'research', 'presentation',
                      'study session', 'lab work']
    }},
    'movies': {{
        'characters': ['Tony Stark', 'Peter Parker', 'Thor', 'Black Widow', 'Captain America', 'Harry Potter',
                      'Hermione', 'Ron', 'Luke Skywalker', 'Rey', 'Kylo Ren', 'Batman', 'Wonder Woman'],
        'activities': ['training exercise', 'mission briefing', 'spell practice', 'potion brewing',
                      'lightsaber training', 'suit upgrade', 'web-slinging practice']
    }}
}}

def load_templates():
    """Load templates for tag {tag}"""
    with open('C:/Users/kapil/numi-scraper/file_fixed.json', 'r') as f:
        all_templates = json.load(f)

    # Filter for specific tag
    return [t for t in all_templates if t.get('tag') == '{tag}']

def generate_variations():
    """Generate 50 variations for {tag}"""
    templates = load_templates()

    if not templates:
        print("No templates found for tag {tag}")
        return []

    variations = []
    template = templates[0]  # Use first template as base
    base_num = template.get('question_number', '1_1').split('_')[0]

    for i in range(2, 52):  # Generate 50 variations (2-51)
        var = copy.deepcopy(template)
        var['question_number'] = f"{{base_num}}_{{i}}"

        # Custom generation logic based on skills
        skills = template.get('skills', '')

        {custom_logic}

        variations.append(var)

    return variations

def save_variations(variations):
    """Save variations to JSON file"""
    filename = 'C:/Users/kapil/numi-scraper/{tag} variations.json'
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Generated {{len(variations)}} variations for {tag}")
    print(f"Saved to: {{filename}}")

if __name__ == "__main__":
    variations = generate_variations()
    if variations:
        save_variations(variations)
'''

def get_custom_logic(skills):
    """Get custom generation logic based on skills type"""

    if skills == 'compare-fractions-word-problems':
        return '''# Generate word problem with pop culture theme
        theme = random.choice(list(POP_CULTURE_THEMES.keys()))
        chars = random.sample(POP_CULTURE_THEMES[theme]['characters'], 2)
        activity = random.choice(POP_CULTURE_THEMES[theme]['activities'])

        # Generate random fractions
        d1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20])
        d2 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20])
        n1 = random.randint(1, d1-1)
        n2 = random.randint(1, d2-1)

        var['question_text'] = f"So far, {chars[0]} has completed $\\\\frac{{{n1}}}{{{d1}}}$ of their {activity}. {chars[1]} has finished $\\\\frac{{{n2}}}{{{d2}}}$ of their {activity}.\\\\n\\\\nWho has finished a greater fraction of their {activity}?"
        var['choices'] = chars

        # Calculate correct answer
        val1 = n1 / d1
        val2 = n2 / d2
        var['correct_answers'] = ["A" if val1 > val2 else "B"]

        # Update solution
        perc1 = val1 * 100
        perc2 = val2 * 100
        var['solution'] = [
            ["1/5", f"First convert {chars[0]}'s fraction to decimal. Then convert the decimal into a percentage."],
            ["2/5", f"Now convert {chars[1]}'s fraction into a percentage using the same steps."],
            ["3/5", "Now compare the percentages. Compare the whole-number parts."],
            ["4/5", f"{int(perc1)} {'is greater than' if perc1 > perc2 else 'is less than'} {int(perc2)}, so {perc1:.3f}% {'>' if perc1 > perc2 else '<'} {perc2:.3f}%"],
            ["5/5", f"Therefore, {chars[0] if perc1 > perc2 else chars[1]} completed a greater fraction of their {activity}."]
        ]

        # Update image tags
        if 'solution_image_tag' in var:
            for img in var['solution_image_tag']:
                img[1] = img[1].replace('_1_', f'_{i}_')'''

    elif skills == 'compare-mixed-numbers-and-improper-fractions':
        return '''# Generate mixed number comparison
        w1 = random.randint(1, 10)
        w2 = random.randint(1, 10)
        d1 = random.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
        d2 = random.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
        n1 = random.randint(1, d1-1)
        n2 = random.randint(1, d2-1)

        # Update image tag
        if 'image_tag' in var:
            var['image_tag'] = var['image_tag'].replace('_1', f'_{i}')

        var['backend_description'] = f"Shows the comparison between mixed numbers {w1} {n1}/{d1} and {w2} {n2}/{d2} using visual representations and mathematical symbols."

        # Calculate correct answer
        val1 = w1 + n1/d1
        val2 = w2 + n2/d2
        if val1 > val2:
            var['correct_answers'] = ["A"]  # ">"
        elif val1 < val2:
            var['correct_answers'] = ["B"]  # "<"
        else:
            var['correct_answers'] = ["C"]  # "="

        # Update solution image tags
        if 'solution_image_tag' in var:
            for img in var['solution_image_tag']:
                img[1] = img[1].replace('_1_', f'_{i}_')'''

    elif skills == 'put-a-mix-of-decimals-fractions-and-mixed-numbers-in-order':
        return '''# Generate ordering problem
        items = []
        for _ in range(4):
            choice = random.choice(['fraction', 'decimal', 'mixed'])
            if choice == 'fraction':
                d = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
                n = random.randint(1, d*2)
                items.append(f"{n}/{d}")
            elif choice == 'decimal':
                items.append(str(round(random.uniform(0.1, 2.5), 2)))
            else:
                w = random.randint(0, 2)
                d = random.choice([2, 3, 4, 5, 6, 8])
                n = random.randint(1, d-1)
                if w == 0:
                    items.append(f"{n}/{d}")
                else:
                    items.append(f"{w} {n}/{d}")

        var['choices'] = items

        # Calculate correct order
        def to_decimal(item):
            if ' ' in item:  # Mixed number
                parts = item.split()
                whole = int(parts[0])
                frac_parts = parts[1].split('/')
                return whole + int(frac_parts[0]) / int(frac_parts[1])
            elif '/' in item:  # Fraction
                parts = item.split('/')
                return int(parts[0]) / int(parts[1])
            else:  # Decimal
                return float(item)

        sorted_items = sorted(items, key=to_decimal)
        var['correct_answers'] = sorted_items'''

    elif skills == 'identify-rational-numbers':
        return '''# Generate rational number identification
        choices = [
            ('fraction', random.randint(1, 20), random.randint(2, 20)),
            ('decimal', round(random.uniform(-10, 10), 3)),
            ('integer', random.randint(-100, 100)),
            ('mixed', random.randint(1, 10), random.randint(1, 9), random.randint(2, 10)),
            ('sqrt_perfect', random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])),
            ('negative_fraction', random.randint(1, 15), random.randint(2, 15))
        ]

        choice_type, *values = random.choice(choices)

        if choice_type == 'fraction':
            var['question_text'] = f"Is $\\\\frac{{{values[0]}}}{{{values[1]}}}$ a rational number?"
        elif choice_type == 'decimal':
            var['question_text'] = f"Is {values[0]} a rational number?"
        elif choice_type == 'integer':
            var['question_text'] = f"Is {values[0]} a rational number?"
        elif choice_type == 'mixed':
            var['question_text'] = f"Is ${values[0]} \\\\frac{{{values[1]}}}{{{values[2]}}}$ a rational number?"
        elif choice_type == 'sqrt_perfect':
            var['question_text'] = f"Is $\\\\sqrt{{{values[0]}}}$ a rational number?"
        elif choice_type == 'negative_fraction':
            var['question_text'] = f"Is $-\\\\frac{{{values[0]}}}{{{values[1]}}}$ a rational number?"

        var['correct_answers'] = ["A"]  # All these are rational

        # Update solution image tag
        if 'solution_image_tag' in var:
            for img in var['solution_image_tag']:
                img[1] = img[1].replace('_1_', f'_{i}_')'''

    elif skills == 'equivalent-fractions':
        return '''# Generate equivalent fractions problem
        n1 = random.randint(1, 12)
        d1 = random.randint(2, 15)

        # Find a factor or multiple
        if random.choice([True, False]):
            # Simplify
            g = gcd(n1, d1)
            if g > 1:
                n2 = n1 // g
                d2 = d1 // g
            else:
                # Multiply
                factor = random.randint(2, 5)
                n2 = n1 * factor
                d2 = d1 * factor
                n1, d1, n2, d2 = n2, d2, n1, d1  # Swap
        else:
            # Multiply
            factor = random.randint(2, 5)
            n2 = n1 * factor
            d2 = d1 * factor

        var['question_text'] = f"Type the missing number that makes these fractions equal:\\\\n"

        # Update image tag
        if 'image_tag' in var:
            var['image_tag'] = var['image_tag'].replace('_1', f'_{i}')

        var['backend_description'] = f"Shows an equation with {n1}/{d1} equals a fraction with denominator {d2} and an unknown numerator represented by an empty box."
        var['correct_answers'] = [[str(n2)], [f"{n2}.0"], [f"{n2}.00"]]

        # Update solution
        operation = 'divide' if d2 < d1 else 'multiply'
        factor = d1//d2 if d2 < d1 else d2//d1
        var['solution'] = [
            ["1/3", f"We are given the fraction $\\\\frac{{{n1}}}{{{d1}}}$ and asked to find an equivalent fraction with a denominator of {d2}."],
            ["2/3", f"To find the missing numerator, {operation} both the numerator and denominator of $\\\\frac{{{n1}}}{{{d1}}}$ by the same number. Since {d1} {'÷' if d2 < d1 else '×'} {abs(factor)} = {d2}, {operation} the numerator by {abs(factor)} as well: {n1} {'÷' if d2 < d1 else '×'} {abs(factor)} = {n2}."],
            ["3/3", f"So, $\\\\frac{{{n1}}}{{{d1}}}$ is equivalent to $\\\\frac{{{n2}}}{{{d2}}}$."]
        ]'''

    elif skills == 'write-fractions-in-lowest-terms':
        return '''# Generate fraction simplification
        factor = random.randint(2, 12)
        n_simple = random.randint(1, 10)
        d_simple = random.randint(n_simple+1, 15)

        # Make sure they're coprime
        while gcd(n_simple, d_simple) > 1:
            n_simple = random.randint(1, 10)
            d_simple = random.randint(n_simple+1, 15)

        n = n_simple * factor
        d = d_simple * factor

        var['question_text'] = f"Write $\\\\frac{{{n}}}{{{d}}}$ in lowest terms.\\\\n\\\\n"
        var['correct_answers'] = [f"{n_simple}/{d_simple}"]

        # Update solution
        var['solution'] = [
            ["1/3", f"Find the largest number that divides both the numerator and the denominator. The largest number that divides both {n} and {d} is {factor}."],
            ["2/3", f"Divide the numerator and denominator by {factor}.\\\\nNumerator: {n} ÷ {factor} = {n_simple}\\\\nDenominator: {d} ÷ {factor} = {d_simple}"],
            ["3/3", f"$\\\\frac{{{n}}}{{{d}}}$ written in lowest terms is $\\\\frac{{{n_simple}}}{{{d_simple}}}$."]
        ]'''

    elif skills == 'round-decimals':
        return '''# Generate decimal rounding
        whole = random.randint(1, 999)
        decimal_places = random.randint(1, 3)
        decimal_part = random.randint(1, 10**decimal_places - 1)

        decimal_str = f"{whole}.{str(decimal_part).zfill(decimal_places)}"
        decimal_val = float(decimal_str)

        var['question_text'] = f"What is {decimal_str} rounded to the nearest whole number?\\\\n\\\\n"

        # Calculate rounded value
        rounded_val = round(decimal_val)
        var['correct_answers'] = [[str(rounded_val)], [f"{rounded_val}.0"], [f"{rounded_val}.00"]]

        # Update solution
        first_decimal = int(decimal_str.split('.')[1][0])
        var['solution'] = [
            ["1/4", f"First, find the digit in the ones place. This is the digit you want to round. \\\\n\\\\nIn this case it is the {whole % 10} in {decimal_str}."],
            ["2/4", f"When rounding, we will either round down to {whole} or round up to {whole + 1}. This decision will depend on the number in the tenths place ({first_decimal})."],
            ["3/4", f"Since {first_decimal} is {'less than' if first_decimal < 5 else 'greater than or equal to'} 5 we must round {'down' if first_decimal < 5 else 'up'}. Remove all digits right of the ones place."],
            ["4/4", f"The final answer is {rounded_val}."]
        ]'''

    else:
        # Default logic for other skills
        return '''# Default variation logic - update numeric values
        # This is a placeholder - implement specific logic for this skill type
        pass'''

def main():
    """Load templates and create individual scripts"""
    with open('C:/Users/kapil/numi-scraper/file_fixed.json', 'r') as f:
        templates = json.load(f)

    # Group by tag
    tags = {}
    for template in templates:
        tag = template.get('tag', 'NO_TAG')
        if tag == 'NO_TAG':
            continue

        if tag not in tags:
            tags[tag] = []
        tags[tag].append(template)

    print(f"Found {len(tags)} unique tags")

    # Create script for each tag
    for tag, tag_templates in tags.items():
        # Get the skills from the first template
        skills = tag_templates[0].get('skills', '')

        # Get custom logic for this skill type
        custom_logic = get_custom_logic(skills)

        # Create the script
        script_content = SCRIPT_TEMPLATE.format(
            tag=tag,
            custom_logic=custom_logic
        )

        # Save the script
        script_name = f"C:/Users/kapil/numi-scraper/generate_{tag}_variations.py"
        with open(script_name, 'w') as f:
            f.write(script_content)

        print(f"Created script: generate_{tag}_variations.py")

if __name__ == "__main__":
    main()