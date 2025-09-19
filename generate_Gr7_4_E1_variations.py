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
    """Load templates for tag Gr7_4_E1"""
    with open('C:/Users/kapil/numi-scraper/file_fixed.json', 'r') as f:
        all_templates = json.load(f)

    # Filter for specific tag
    return [t for t in all_templates if t.get('tag') == 'Gr7_4_E1']

def generate_variations():
    """Generate 50 variations for Gr7_4_E1"""
    templates = load_templates()

    if not templates:
        print("No templates found for tag Gr7_4_E1")
        return []

    variations = []
    template = templates[0]  # Use first template as base
    base_num = template.get('question_number', '1_1').split('_')[0]

    for i in range(2, 52):  # Generate 50 variations (2-51)
        var = copy.deepcopy(template)
        var['question_number'] = f"{base_num}_{i}"

        # Custom generation logic based on skills
        skills = template.get('skills', '')

        # Generate rational number identification
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
            var['question_text'] = f"Is $\\frac{{{values[0]}}}{{{values[1]}}}$ a rational number?"
        elif choice_type == 'decimal':
            var['question_text'] = f"Is {values[0]} a rational number?"
        elif choice_type == 'integer':
            var['question_text'] = f"Is {values[0]} a rational number?"
        elif choice_type == 'mixed':
            var['question_text'] = f"Is ${values[0]} \\frac{{{values[1]}}}{{{values[2]}}}$ a rational number?"
        elif choice_type == 'sqrt_perfect':
            var['question_text'] = f"Is $\\sqrt{{{values[0]}}}$ a rational number?"
        elif choice_type == 'negative_fraction':
            var['question_text'] = f"Is $-\\frac{{{values[0]}}}{{{values[1]}}}$ a rational number?"

        var['correct_answers'] = ["A"]  # All these are rational

        # Update solution image tag
        if 'solution_image_tag' in var:
            for img in var['solution_image_tag']:
                img[1] = img[1].replace('_1_', f'_{i}_')

        variations.append(var)

    return variations

def save_variations(variations):
    """Save variations to JSON file"""
    filename = 'C:/Users/kapil/numi-scraper/Gr7_4_E1 variations.json'
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Generated {len(variations)} variations for Gr7_4_E1")
    print(f"Saved to: {filename}")

if __name__ == "__main__":
    variations = generate_variations()
    if variations:
        save_variations(variations)
