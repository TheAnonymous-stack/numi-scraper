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
    """Load templates for tag Gr7_3_E4"""
    with open('C:/Users/kapil/numi-scraper/file_fixed.json', 'r') as f:
        all_templates = json.load(f)

    # Filter for specific tag
    return [t for t in all_templates if t.get('tag') == 'Gr7_3_E4']

def generate_variations():
    """Generate 50 variations for Gr7_3_E4"""
    templates = load_templates()

    if not templates:
        print("No templates found for tag Gr7_3_E4")
        return []

    variations = []
    template = templates[0]  # Use first template as base
    base_num = template.get('question_number', '1_1').split('_')[0]

    for i in range(2, 52):  # Generate 50 variations (2-51)
        var = copy.deepcopy(template)
        var['question_number'] = f"{base_num}_{i}"

        # Custom generation logic based on skills
        skills = template.get('skills', '')

        # Generate mixed number comparison
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
                img[1] = img[1].replace('_1_', f'_{i}_')

        variations.append(var)

    return variations

def save_variations(variations):
    """Save variations to JSON file"""
    filename = 'C:/Users/kapil/numi-scraper/Gr7_3_E4 variations.json'
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Generated {len(variations)} variations for Gr7_3_E4")
    print(f"Saved to: {filename}")

if __name__ == "__main__":
    variations = generate_variations()
    if variations:
        save_variations(variations)
