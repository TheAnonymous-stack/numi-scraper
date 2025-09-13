import json
import random

def fix_professions(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # List of varied professions/roles with their items
    professions = [
        ("baker", "specializes in", "custom wedding cakes"),
        ("blacksmith", "forges", "decorative swords"),
        ("carpenter", "builds", "custom furniture pieces"),
        ("jeweler", "creates", "diamond rings"),
        ("tailor", "sews", "designer suits"),
        ("potter", "shapes", "ceramic vases"),
        ("glassblower", "crafts", "stained glass windows"),
        ("watchmaker", "assembles", "luxury watches"),
        ("sculptor", "carves", "marble statues"),
        ("weaver", "produces", "tapestries"),
        ("chocolatier", "makes", "gourmet chocolates"),
        ("florist", "arranges", "wedding bouquets"),
        ("cobbler", "handcrafts", "leather boots"),
        ("perfumer", "blends", "signature fragrances"),
        ("bookbinder", "creates", "leather journals"),
        ("candlemaker", "produces", "scented candles"),
        ("toymaker", "builds", "wooden toys"),
        ("architect", "designs", "house blueprints"),
        ("illustrator", "draws", "book illustrations"),
        ("calligrapher", "writes", "wedding invitations"),
        ("seamstress", "creates", "ball gowns"),
        ("mechanic", "restores", "classic cars"),
        ("chef", "prepares", "gourmet meals"),
        ("artist", "paints", "portraits"),
        ("musician", "composes", "symphonies"),
        ("programmer", "develops", "mobile apps"),
        ("designer", "creates", "logos"),
        ("landscaper", "designs", "garden layouts"),
        ("barista", "crafts", "specialty coffees"),
        ("pastry chef", "bakes", "croissants"),
        ("electrician", "installs", "solar panels"),
        ("plumber", "fixes", "water systems"),
        ("roofer", "installs", "tile roofs"),
        ("mason", "builds", "stone walls"),
        ("upholsterer", "restores", "antique chairs"),
        ("engraver", "etches", "crystal awards"),
        ("brewer", "ferments", "craft beers"),
        ("distiller", "produces", "artisan spirits"),
        ("cheese maker", "ages", "specialty cheeses"),
        ("butcher", "prepares", "gourmet cuts"),
        ("fishmonger", "prepares", "sushi-grade fish"),
        ("herbalist", "blends", "healing teas"),
        ("cosmetologist", "creates", "beauty products"),
        ("hairstylist", "styles", "wedding hairdos"),
        ("makeup artist", "designs", "special effects"),
        ("tattoo artist", "creates", "custom tattoos"),
        ("photographer", "shoots", "wedding albums"),
        ("videographer", "films", "documentaries"),
        ("animator", "creates", "cartoon episodes"),
        ("web developer", "builds", "websites"),
        ("game developer", "creates", "video games")
    ]
    
    # Make sure we have enough professions
    while len(professions) < len(data['quizzes']):
        professions.extend(professions)
    
    # Shuffle for variety
    random.seed(42)
    random.shuffle(professions)
    
    for i, quiz in enumerate(data['quizzes']):
        if i < len(professions):
            profession, verb, item = professions[i]
            
            # Get the character name from the original text
            original_text = quiz['question_text']
            name = original_text.split(' is a')[0]
            
            # Extract the numbers from original text
            import re
            numbers = re.findall(r'\d+', original_text)
            if len(numbers) >= 3:
                first_qty = numbers[0]
                time_taken = numbers[1]
                second_qty = numbers[2]
                
                # Create new question text
                if random.random() < 0.5:
                    # Version 1: profession who verb item
                    new_text = f"{name} is a {profession} who {verb} {item}. The last order was for {first_qty} {item}, and it took {time_taken} weeks to complete them. A new order comes in for {second_qty} {item}. If the work continues at the same rate, how many weeks will it take {name} to complete the {item}?=_"
                else:
                    # Version 2: works as a profession
                    new_text = f"{name} works as a {profession} creating {item}. Recently, {name} completed {first_qty} {item} in {time_taken} weeks. Now there's an order for {second_qty} {item}. Working at the same pace, how many weeks will {name} need to finish the {item}?=_"
                
                quiz['question_text'] = new_text
                
                # Update the solution text to match
                if 'solution' in quiz and len(quiz['solution']) >= 3:
                    # Calculate rate
                    rate = int(time_taken) / int(first_qty)
                    rate_str = str(int(rate)) if rate.is_integer() else str(rate)
                    total_time = int(float(rate) * int(second_qty))
                    
                    quiz['solution'][0][1] = f"First, find {name}'s rate per item. {name} made {first_qty} {item} in {time_taken} weeks, so each item takes ${time_taken} \\div {first_qty} = {rate_str}$ weeks."
                    quiz['solution'][1][1] = f"Now find how long it takes to make {second_qty} {item}. Since each item takes {rate_str} weeks, multiply: ${rate_str} \\times {second_qty} = {total_time}$ weeks."
                    quiz['solution'][2][1] = f"Therefore, it will take {name} {total_time} weeks to complete {second_qty} {item}."
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Process the file
fix_professions('Gr6_30_E3_variations.json')
print("Fixed professions in Gr6_30_E3_variations.json")