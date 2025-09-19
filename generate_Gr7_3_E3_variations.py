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
    """Load templates for tag Gr7_3_E3"""
    with open('C:/Users/kapil/numi-scraper/file_fixed.json', 'r') as f:
        all_templates = json.load(f)

    # Filter for specific tag
    return [t for t in all_templates if t.get('tag') == 'Gr7_3_E3']

def generate_variations():
    """Generate 50 variations for Gr7_3_E3"""
    templates = load_templates()

    if not templates:
        print("No templates found for tag Gr7_3_E3")
        return []

    variations = []
    template = templates[0]  # Use first template as base
    base_num = template.get('question_number', '1_1').split('_')[0]

    for i in range(2, 52):  # Generate 50 variations (2-51)
        var = copy.deepcopy(template)
        var['question_number'] = f"{base_num}_{i}"

        # Custom generation logic based on skills
        skills = template.get('skills', '')

        # Generate word problem with pop culture theme
        theme = random.choice(list(POP_CULTURE_THEMES.keys()))
        chars = random.sample(POP_CULTURE_THEMES[theme]['characters'], 2)
        activity = random.choice(POP_CULTURE_THEMES[theme]['activities'])

        # Generate random fractions
        d1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20])
        d2 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20])
        n1 = random.randint(1, d1-1)
        n2 = random.randint(1, d2-1)

        var['question_text'] = f"So far, {chars[0]} has completed $\\frac{{{n1}}}{{{d1}}}$ of their {activity}. {chars[1]} has finished $\\frac{{{n2}}}{{{d2}}}$ of their {activity}.\\n\\nWho has finished a greater fraction of their {activity}?"
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
                img[1] = img[1].replace('_1_', f'_{i}_')

        variations.append(var)

    return variations

def save_variations(variations):
    """Save variations to JSON file"""
    filename = 'C:/Users/kapil/numi-scraper/Gr7_3_E3 variations.json'
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Generated {len(variations)} variations for Gr7_3_E3")
    print(f"Saved to: {filename}")

if __name__ == "__main__":
    variations = generate_variations()
    if variations:
        save_variations(variations)
