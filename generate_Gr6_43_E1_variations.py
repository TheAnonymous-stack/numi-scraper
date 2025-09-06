import json
import random
import copy

def load_templates():
    """Load template questions from the fixed JSON file"""
    with open('file_fixed.json', 'r') as f:
        data = json.load(f)
    return [q for q in data if q.get('tag') == 'Gr6_43_E1']

def get_pop_culture_themes():
    """Get diverse pop culture and trending themes"""
    return [
        # Anime themes
        {'theme': 'Naruto', 'items': ['ninja headbands', 'kunai knives', 'ramen bowls', 'chakra scrolls', 'shuriken stars']},
        {'theme': 'One Piece', 'items': ['devil fruits', 'treasure maps', 'pirate flags', 'wanted posters', 'log poses']},
        {'theme': 'Dragon Ball', 'items': ['dragon balls', 'senzu beans', 'power scouters', 'capsules', 'training weights']},
        {'theme': 'Pokemon', 'items': ['pokeballs', 'rare candies', 'gym badges', 'potions', 'trading cards']},
        {'theme': 'My Hero Academia', 'items': ['hero costumes', 'quirk enhancers', 'support items', 'hero licenses', 'training gear']},
        
        # TV Series
        {'theme': 'Stranger Things', 'items': ['Eggo waffles', 'walkie-talkies', 'D&D dice sets', 'Christmas lights', 'cassette tapes']},
        {'theme': 'Wednesday', 'items': ['black dresses', 'typewriter ribbons', 'cello strings', 'mystery novels', 'dark lipsticks']},
        {'theme': 'The Last of Us', 'items': ['survival kits', 'medical supplies', 'canned goods', 'flashlight batteries', 'water bottles']},
        
        # Gaming
        {'theme': 'Minecraft', 'items': ['diamond blocks', 'enchanted books', 'golden apples', 'redstone dust', 'emerald ore']},
        {'theme': 'Fortnite', 'items': ['V-bucks cards', 'shield potions', 'building materials', 'ammo boxes', 'loot llamas']},
        {'theme': 'Among Us', 'items': ['spacesuits', 'emergency buttons', 'task cards', 'vent covers', 'crew badges']},
        
        # Movies
        {'theme': 'Marvel', 'items': ['infinity stones', 'vibranium shields', 'arc reactors', 'web shooters', 'hero masks']},
        {'theme': 'Harry Potter', 'items': ['chocolate frogs', 'spell books', 'wands', 'house scarves', 'butterbeer bottles']},
        {'theme': 'Star Wars', 'items': ['lightsabers', 'holocrons', 'droid parts', 'kyber crystals', 'rebel medals']},
        
        # Music/K-pop
        {'theme': 'BTS', 'items': ['albums', 'light sticks', 'photo cards', 'concert tickets', 'merchandise bags']},
        {'theme': 'Taylor Swift', 'items': ['friendship bracelets', 'vinyl records', 'concert confetti', 'tour posters', 'guitar picks']},
        
        # Food/Beverages
        {'theme': 'Starbucks', 'items': ['seasonal cups', 'cake pops', 'frappuccinos', 'breakfast sandwiches', 'coffee beans']},
        {'theme': 'Bubble Tea', 'items': ['tapioca pearls', 'flavored syrups', 'wide straws', 'tea leaves', 'milk powders']},
        
        # Social Media
        {'theme': 'TikTok', 'items': ['ring lights', 'phone tripods', 'microphones', 'green screens', 'editing apps']},
        {'theme': 'YouTube', 'items': ['play buttons', 'camera lenses', 'subscriber plaques', 'merch boxes', 'streaming gear']},
        
        # Sports
        {'theme': 'FIFA', 'items': ['soccer balls', 'team jerseys', 'shin guards', 'cleats', 'goalkeeper gloves']},
        {'theme': 'NBA', 'items': ['basketballs', 'team jerseys', 'sneakers', 'headbands', 'trading cards']}
    ]

def get_character_names():
    """Get diverse character names"""
    return [
        # Traditional names
        'Alex', 'Sam', 'Jordan', 'Casey', 'Morgan', 'Taylor', 'Riley', 'Avery', 'Quinn', 'Cameron',
        'Jamie', 'Drew', 'Blake', 'Hayden', 'Parker', 'Sage', 'River', 'Sky',
        
        # Cultural names
        'Yuki', 'Kai', 'Ren', 'Sora', 'Hiro', 'Luna', 'Nova', 'Zara', 'Aria', 'Leo',
        'Maya', 'Ava', 'Ethan', 'Olivia', 'Liam', 'Emma', 'Noah', 'Sophia',
        
        # Pop culture inspired
        'Eleven', 'Neo', 'Trinity', 'Hermione', 'Draco', 'Levi', 'Mikasa', 'Eren', 'Naruto', 'Sasuke',
        'Goku', 'Vegeta', 'Luffy', 'Zoro', 'Ash', 'Misty', 'Brock', 'Link', 'Zelda', 'Mario'
    ]

def get_business_contexts():
    """Get diverse business contexts"""
    return [
        'online shop', 'craft business', 'bakery', 'food truck', 'art studio',
        'gaming cafe', 'bookstore', 'toy store', 'comic shop', 'music store',
        'pet shop', 'flower shop', 'jewelry business', 'clothing boutique', 'tech repair shop',
        'tutoring service', 'photography studio', 'dance studio', 'gym', 'spa',
        'coffee shop', 'ice cream parlor', 'pizza place', 'sushi restaurant', 'taco stand',
        'vintage store', 'record shop', 'skateboard shop', 'bike shop', 'sports equipment store'
    ]

def get_hobby_contexts():
    """Get diverse hobby contexts"""
    return [
        'cosplay convention', 'anime club', 'robotics team', 'debate club', 'drama production',
        'school band', 'art exhibition', 'science fair', 'coding competition', 'chess tournament',
        'esports team', 'book club', 'photography club', 'cooking class', 'dance recital',
        'martial arts tournament', 'skateboarding competition', 'rock climbing', 'parkour training',
        'streaming setup', 'podcast recording', 'YouTube channel', 'TikTok content', 'Instagram shop'
    ]

def generate_problem_variations():
    """Generate diverse multi-step metric conversion word problems"""
    variations = []
    themes = get_pop_culture_themes()
    names = get_character_names()
    businesses = get_business_contexts()
    hobbies = get_hobby_contexts()
    
    # Problem type 1: Mass conversions (grams to kilograms)
    for i in range(16):
        theme = random.choice(themes)
        name = random.choice(names)
        business = random.choice(businesses)
        item = random.choice(theme['items'])
        
        num_items = random.choice([8, 10, 12, 15, 16, 18, 20, 24, 25, 30])
        weight_per_item = random.choice([80, 100, 120, 125, 150, 160, 175, 180, 200, 225, 240, 250])
        total_grams = num_items * weight_per_item
        total_kg = total_grams / 1000
        
        variations.append({
            'type': 'mass_multiply',
            'context': f"{name} is packing orders for their {theme['theme']}-themed {business}. One customer ordered {num_items} {item}. If each item weighs {weight_per_item} grams",
            'question': "how many kilograms will this order weigh?",
            'unit': 'kilograms',
            'num_items': num_items,
            'weight_per': weight_per_item,
            'total_grams': total_grams,
            'answer': str(total_kg)
        })
    
    # Problem type 2: Length conversions (scale models)
    for i in range(16):
        name = random.choice(names)
        hobby = random.choice(hobbies)
        
        structures = [
            ('Tokyo Tower', 333), ('Empire State Building', 381), ('Eiffel Tower', 300),
            ('Statue of Liberty', 93), ('Big Ben', 96), ('Space Needle', 184),
            ('CN Tower', 553), ('Burj Khalifa', 828), ('Golden Gate Bridge', 227),
            ('Mount Rushmore', 18), ('Christ the Redeemer', 38), ('Leaning Tower of Pisa', 56)
        ]
        
        structure, actual_height = random.choice(structures)
        scale = random.choice([100, 200, 250, 300, 400, 500, 600, 750, 800, 1000])
        model_metres = actual_height / scale
        model_mm = model_metres * 1000
        
        variations.append({
            'type': 'scale_model',
            'context': f"{name} is making a scale model of the {structure} for their {hobby}. The model is {scale} times smaller than the actual structure, which is {actual_height} metres tall",
            'question': "How many millimetres tall is the model?",
            'unit': 'millimetres',
            'actual_height': actual_height,
            'scale': scale,
            'model_metres': model_metres,
            'answer': str(int(model_mm))
        })
    
    # Problem type 3: Volume conversions (remaining amount)
    for i in range(16):
        name = random.choice(names)
        theme = random.choice(themes)
        
        contexts = [
            'painting their room {}-themed',
            'creating {} artwork',
            'decorating for a {} party',
            'making {} costumes',
            'crafting {} props',
            'designing {} merchandise'
        ]
        
        context = random.choice(contexts).format(theme['theme'])
        needed_ml = random.choice([600, 700, 750, 800, 850, 900, 650, 550, 450, 350])
        bought_litres = random.choice([1, 1.5, 2])
        bought_ml = bought_litres * 1000
        remaining = bought_ml - needed_ml
        
        colors = ['blue', 'red', 'green', 'purple', 'black', 'silver', 'gold', 'pink', 'orange', 'teal']
        color = random.choice(colors)
        
        variations.append({
            'type': 'volume_subtract',
            'context': f"{name} is {context}. They estimate needing {needed_ml} millilitres of {color} paint, but the store only sells paint in litres. If {name} buys {bought_litres} {'litre' if bought_litres == 1 else 'litres'} of paint",
            'question': "how many millilitres will be left?",
            'unit': 'millilitres',
            'needed': needed_ml,
            'bought_litres': bought_litres,
            'bought_ml': bought_ml,
            'answer': str(remaining)
        })
    
    return variations[:48]  # Return exactly 48 variations

def create_variation(templates, variation_data, variation_num):
    """Create a single variation from a randomly selected template"""
    # Select appropriate template based on problem type
    template = random.choice(templates)
    new_q = copy.deepcopy(template)
    
    # Update question number
    template_num = random.choice(['1', '2', '3'])  # Since we have 3 templates
    new_q['question_number'] = f"{template_num}_{variation_num}"
    
    # Update question text
    new_q['question_text'] = f"{variation_data['context']}, {variation_data['question']}\n___ {variation_data['unit']}"
    
    # Update correct answer
    new_q['correct_answers'] = [variation_data['answer']]
    
    # Update solution based on problem type
    if variation_data['type'] == 'mass_multiply':
        new_q['solution'] = [
            ["1/6", "There are 1000 grams in 1 kilogram."],
            ["2/6", f"Multiply to find how much the customer's order will weigh. The customer ordered {variation_data['num_items']} items. Each item weighs {variation_data['weight_per']} grams."],
            ["3/6", f"${variation_data['num_items']} \\cdot {variation_data['weight_per']} = {variation_data['total_grams']}$"],
            ["4/6", f"The customer's order weighs {variation_data['total_grams']} grams, but the problem asks how many kilograms it weighs. So, find how many kilograms are equal to {variation_data['total_grams']} grams. There are 1000 grams in a kilogram, so divide by 1000."],
            ["5/6", f"${variation_data['total_grams']} \\div 1000 = {variation_data['answer']}$"],
            ["6/6", f"The customer's order weighs {variation_data['answer']} kilograms."]
        ]
    
    elif variation_data['type'] == 'scale_model':
        new_q['solution'] = [
            ["1/6", "There are 1000 millimetres in 1 metre."],
            ["2/6", f"Divide to find how tall the model is. The actual structure is {variation_data['actual_height']} metres tall. The model is {variation_data['scale']} times smaller."],
            ["3/6", f"${variation_data['actual_height']} \\div {variation_data['scale']} = {variation_data['model_metres']}$"],
            ["4/6", f"The model is {variation_data['model_metres']} metres tall, but the problem asks about millimetres. So, find how many millimetres are in {variation_data['model_metres']} metres."],
            ["5/6", f"There are 1000 millimetres in a metre, so multiply by 1000.\n${variation_data['model_metres']} \\times 1000 = {variation_data['answer']}$"],
            ["6/6", f"The model is {variation_data['answer']} millimetres tall."]
        ]
    
    else:  # volume_subtract
        new_q['solution'] = [
            ["1/4", "There are 1000 millilitres in 1 litre."],
            ["2/4", f"Subtract to find how many millilitres of paint will be left. They buy {variation_data['bought_litres']} {'litre' if variation_data['bought_litres'] == 1 else 'litres'} of paint. That is the same as {variation_data['bought_ml']} millilitres. They estimate needing {variation_data['needed']} millilitres."],
            ["3/4", f"${variation_data['bought_ml']} - {variation_data['needed']} = {variation_data['answer']}$"],
            ["4/4", f"They will have {variation_data['answer']} millilitres of paint left."]
        ]
    
    return new_q

def main():
    """Generate all variations for Gr6_43_E1"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_43_E1")
        return
    
    print(f"Found {len(templates)} templates for Gr6_43_E1")
    
    # Generate variation data
    variation_data = generate_problem_variations()
    
    # Create all variations
    variations = []
    for i, var_data in enumerate(variation_data, start=4):  # Start from 4 since we have 3 templates
        variation = create_variation(templates, var_data, i)
        variations.append(variation)
    
    # Save variations to JSON file
    output_file = 'Gr6_43_E1_variations.json'
    with open(output_file, 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_43_E1")
    print(f"Saved to {output_file}")
    print(f"Total questions (including {len(templates)} templates): {len(variations) + len(templates)}")

if __name__ == "__main__":
    main()