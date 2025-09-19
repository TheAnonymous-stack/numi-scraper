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
    """Load templates for tag Gr7_3_E5"""
    with open('C:/Users/kapil/numi-scraper/file_fixed.json', 'r') as f:
        all_templates = json.load(f)

    # Filter for specific tag
    return [t for t in all_templates if t.get('tag') == 'Gr7_3_E5']

def generate_variations():
    """Generate 50 variations for Gr7_3_E5"""
    templates = load_templates()

    if not templates:
        print("No templates found for tag Gr7_3_E5")
        return []

    variations = []
    template = templates[0]  # Use first template as base
    base_num = template.get('question_number', '1_1').split('_')[0]

    for i in range(2, 52):  # Generate 50 variations (2-51)
        var = copy.deepcopy(template)
        var['question_number'] = f"{base_num}_{i}"

        # Custom generation logic based on skills
        skills = template.get('skills', '')

        # Generate ordering problem
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
        var['correct_answers'] = sorted_items

        variations.append(var)

    return variations

def save_variations(variations):
    """Save variations to JSON file"""
    filename = 'C:/Users/kapil/numi-scraper/Gr7_3_E5 variations.json'
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Generated {len(variations)} variations for Gr7_3_E5")
    print(f"Saved to: {filename}")

if __name__ == "__main__":
    variations = generate_variations()
    if variations:
        save_variations(variations)
