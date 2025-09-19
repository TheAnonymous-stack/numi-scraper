import json
import random
import copy
from fractions import Fraction
from decimal import Decimal
from math import gcd

# Pop culture themes for word problems
POP_CULTURE_THEMES = {
    'anime': {
        'characters': ['Naruto', 'Goku', 'Luffy', 'Ichigo', 'Eren', 'Levi', 'Mikasa', 'Tanjiro', 'Nezuko',
                      'Deku', 'Bakugo', 'Todoroki', 'Gojo', 'Yuji', 'Megumi', 'Nobara', 'Anya', 'Loid'],
        'activities': ['training', 'mission', 'quest', 'battle preparation', 'technique practice',
                      'chakra control exercise', 'devil fruit training', 'titan elimination practice']
    },
    'gaming': {
        'characters': ['Mario', 'Luigi', 'Link', 'Zelda', 'Master Chief', 'Kratos', 'Ellie', 'Joel',
                      'Cloud', 'Sephiroth', 'Sonic', 'Pikachu', 'Steve', 'Alex'],
        'activities': ['speedrun', 'raid', 'dungeon', 'boss fight', 'level completion', 'achievement hunt',
                      'resource gathering', 'crafting session']
    },
    'tv_shows': {
        'characters': ['Walter White', 'Jesse', 'Eleven', 'Mike Wheeler', 'Dustin', 'Rick', 'Morty',
                      'Sheldon', 'Leonard', 'Penny', 'Joey', 'Chandler', 'Ross', 'Rachel'],
        'activities': ['experiment', 'investigation', 'project', 'homework', 'research', 'presentation',
                      'study session', 'lab work']
    },
    'movies': {
        'characters': ['Tony Stark', 'Peter Parker', 'Thor', 'Black Widow', 'Captain America', 'Harry Potter',
                      'Hermione', 'Ron', 'Luke Skywalker', 'Rey', 'Kylo Ren', 'Batman', 'Wonder Woman'],
        'activities': ['training exercise', 'mission briefing', 'spell practice', 'potion brewing',
                      'lightsaber training', 'suit upgrade', 'web-slinging practice']
    }
}

def load_templates():
    """Load templates for tag Gr7_5_E1"""
    with open('C:/Users/kapil/numi-scraper/file_fixed.json', 'r') as f:
        all_templates = json.load(f)

    # Filter for specific tag
    return [t for t in all_templates if t.get('tag') == 'Gr7_5_E1']

def generate_variations():
    """Generate 50 variations for Gr7_5_E1"""
    templates = load_templates()

    if not templates:
        print("No templates found for tag Gr7_5_E1")
        return []

    variations = []
    template = templates[0]  # Use first template as base
    base_num = template.get('question_number', '1_1').split('_')[0]

    for i in range(2, 52):  # Generate 50 variations (2-51)
        var = copy.deepcopy(template)
        var['question_number'] = f"{base_num}_{i}"

        # Custom generation logic based on skills
        skills = template.get('skills', '')

        # Generate equivalent fractions problem
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

        var['question_text'] = f"Type the missing number that makes these fractions equal:\\n"

        # Update image tag
        if 'image_tag' in var:
            var['image_tag'] = var['image_tag'].replace('_1', f'_{i}')

        var['backend_description'] = f"Shows an equation with {n1}/{d1} equals a fraction with denominator {d2} and an unknown numerator represented by an empty box."
        var['correct_answers'] = [[str(n2)], [f"{n2}.0"], [f"{n2}.00"]]

        # Update solution
        operation = 'divide' if d2 < d1 else 'multiply'
        factor = d1//d2 if d2 < d1 else d2//d1
        var['solution'] = [
            ["1/3", f"We are given the fraction $\\frac{{{n1}}}{{{d1}}}$ and asked to find an equivalent fraction with a denominator of {d2}."],
            ["2/3", f"To find the missing numerator, {operation} both the numerator and denominator of $\\frac{{{n1}}}{{{d1}}}$ by the same number. Since {d1} {'÷' if d2 < d1 else '×'} {abs(factor)} = {d2}, {operation} the numerator by {abs(factor)} as well: {n1} {'÷' if d2 < d1 else '×'} {abs(factor)} = {n2}."],
            ["3/3", f"So, $\\frac{{{n1}}}{{{d1}}}$ is equivalent to $\\frac{{{n2}}}{{{d2}}}$."]
        ]

        variations.append(var)

    return variations

def save_variations(variations):
    """Save variations to JSON file"""
    filename = 'C:/Users/kapil/numi-scraper/Gr7_5_E1 variations.json'
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Generated {len(variations)} variations for Gr7_5_E1")
    print(f"Saved to: {filename}")

if __name__ == "__main__":
    variations = generate_variations()
    if variations:
        save_variations(variations)
