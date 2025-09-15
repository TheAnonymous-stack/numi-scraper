import json
import random

def generate_variations():
    """Generate 51 variations for Gr6_49_E2 - unit conversion word problems"""

    variations = []

    # Original template
    original = {
        "tag": "Gr6_49_E2",
        "question_number": "2_1",
        "question_type": "Fill in the blank",
        "question_text": "Darlene loves to cook with fresh herbs. So, she decides to plant 8 different herbs and keep the small pots on her kitchen windowsill. She starts with a 2-kilogram bag of soil and puts the same amount of soil in each pot. If she uses all of the soil, how many grams does she add to each pot?",
        "correct_answers": ["250"],
        "solution": [
            ["1/5", "You want to find how many grams of soil Darlene adds to each pot."],
            ["2/5", "Darlene starts with 2 kilograms of soil. Note that there are 1000 grams in a kilogram, so multiply 2 kilograms by 1000 to get the amount of soil Darlene starts with in grams."],
            ["3/5", "$2 \\times 1000 = 2000$ grams"],
            ["4/5", "Now we know Darlene has 2000 grams in total and there are 8 pots. To find how many grams of soil go into each pot, we divide the amount of soil by the number of pots."],
            ["5/5", "$2000 \\div 8 = 250$ grams."]
        ],
        "solution_image_tag": []
    }

    variations.append(original)

    # Define contexts for variations with different unit conversions
    contexts = [
        # Kilograms to grams scenarios
        ("baker", "flour", "cake layers", "kilograms", "grams", 1000),
        ("chef", "sugar", "desserts", "kilograms", "grams", 1000),
        ("candy maker", "chocolate", "candy bars", "kilograms", "grams", 1000),
        ("pizza chef", "cheese", "pizzas", "kilograms", "grams", 1000),
        ("scientist", "chemicals", "test tubes", "kilograms", "grams", 1000),
        ("artist", "clay", "sculptures", "kilograms", "grams", 1000),
        ("jeweler", "silver", "rings", "kilograms", "grams", 1000),
        ("gardener", "fertilizer", "flower beds", "kilograms", "grams", 1000),
        ("Pokemon trainer", "Pokeballs", "Pokemon", "kilograms", "grams", 1000),
        ("Minecraft player", "gold", "golden apples", "kilograms", "grams", 1000),

        # Liters to milliliters scenarios
        ("bartender", "juice", "cocktails", "liters", "milliliters", 1000),
        ("nurse", "medicine", "patients", "liters", "milliliters", 1000),
        ("chemist", "solution", "beakers", "liters", "milliliters", 1000),
        ("painter", "paint", "canvases", "liters", "milliliters", 1000),
        ("barista", "milk", "lattes", "liters", "milliliters", 1000),
        ("smoothie maker", "fruit juice", "smoothies", "liters", "milliliters", 1000),
        ("potion master", "magical elixir", "potions", "liters", "milliliters", 1000),
        ("Hermione", "polyjuice potion", "vials", "liters", "milliliters", 1000),

        # Meters to centimeters scenarios
        ("tailor", "fabric", "shirts", "meters", "centimeters", 100),
        ("carpenter", "wood", "shelves", "meters", "centimeters", 100),
        ("decorator", "ribbon", "gift boxes", "meters", "centimeters", 100),
        ("seamstress", "silk", "dresses", "meters", "centimeters", 100),
        ("Spider-Man", "web fluid", "web cartridges", "meters", "centimeters", 100),

        # Kilometers to meters scenarios
        ("runner", "track distance", "laps", "kilometers", "meters", 1000),
        ("cyclist", "route", "segments", "kilometers", "meters", 1000),
        ("Mario", "race track", "checkpoints", "kilometers", "meters", 1000),
        ("Sonic", "speed zones", "loops", "kilometers", "meters", 1000),

        # Hours to minutes scenarios
        ("teacher", "class time", "lessons", "hours", "minutes", 60),
        ("trainer", "workout time", "exercises", "hours", "minutes", 60),
        ("gamer", "gaming time", "matches", "hours", "minutes", 60),
        ("YouTuber", "recording time", "videos", "hours", "minutes", 60),
        ("streamer", "stream time", "segments", "hours", "minutes", 60),
        ("Naruto", "training time", "jutsu practices", "hours", "minutes", 60),

        # Days to hours scenarios
        ("project manager", "work time", "tasks", "days", "hours", 24),
        ("astronaut", "mission time", "experiments", "days", "hours", 24),
        ("Dragon Ball fighter", "training time", "sessions", "days", "hours", 24),

        # Dozens to individual items
        ("baker", "eggs", "cakes", "dozens", "eggs", 12),
        ("florist", "roses", "bouquets", "dozens", "roses", 12),
        ("teacher", "pencils", "students", "dozens", "pencils", 12),
        ("party planner", "balloons", "decorations", "dozens", "balloons", 12),

        # Feet to inches scenarios
        ("construction worker", "rope", "sections", "feet", "inches", 12),
        ("interior designer", "molding", "walls", "feet", "inches", 12),

        # Pounds to ounces scenarios
        ("butcher", "meat", "portions", "pounds", "ounces", 16),
        ("cheese maker", "cheese", "packages", "pounds", "ounces", 16),

        # Gallons to quarts scenarios
        ("farmer", "milk", "containers", "gallons", "quarts", 4),
        ("gas station", "fuel", "vehicles", "gallons", "quarts", 4),

        # Yards to feet scenarios
        ("landscaper", "fencing", "sections", "yards", "feet", 3),
        ("football coach", "field distance", "zones", "yards", "feet", 3),

        # Weeks to days scenarios
        ("vacation planner", "vacation time", "destinations", "weeks", "days", 7),
        ("summer camp", "camp duration", "activities", "weeks", "days", 7),

        # Years to months scenarios
        ("subscription service", "membership", "payment periods", "years", "months", 12),
        ("loan officer", "loan term", "installments", "years", "months", 12)
    ]

    # Generate number combinations
    number_combinations = []

    # For each context, generate appropriate number combinations
    for _, _, _, from_unit, to_unit, conversion_factor in contexts:
        # Generate various starting amounts and division numbers
        for start_amount in range(2, 20):
            for num_divisions in range(2, 25):
                total_small_units = start_amount * conversion_factor
                if total_small_units % num_divisions == 0:
                    result = total_small_units // num_divisions
                    if result > 0 and result < 10000:
                        number_combinations.append((start_amount, num_divisions, conversion_factor, result))

    # Shuffle and select combinations
    random.seed(42)
    random.shuffle(contexts)
    random.shuffle(number_combinations)

    # Generate 50 variations
    for i in range(2, 52):
        context_idx = (i-2) % len(contexts)
        person, material, items, from_unit, to_unit, conversion_factor = contexts[context_idx]

        # Find a suitable number combination for this conversion factor
        suitable_combos = [combo for combo in number_combinations if combo[2] == conversion_factor]
        if suitable_combos:
            combo_idx = (i-2) % len(suitable_combos)
            start_amount, num_divisions, _, result = suitable_combos[combo_idx]
        else:
            # Fallback values
            start_amount = 3
            num_divisions = 6
            result = (start_amount * conversion_factor) // num_divisions

        total_small_units = start_amount * conversion_factor

        # Create story variations
        story_templates = [
            f"{person.capitalize()} is preparing {material} for {num_divisions} {items}. Starting with {start_amount} {from_unit} of {material}, and dividing it equally among all {items}, how many {to_unit} does each {items[:-1] if items.endswith('s') else items} receive?",
            f"{person.capitalize()} has {start_amount} {from_unit} of {material} to distribute evenly among {num_divisions} {items}. How many {to_unit} of {material} will each {items[:-1] if items.endswith('s') else items} get?",
            f"A {person} needs to divide {start_amount} {from_unit} of {material} equally between {num_divisions} {items}. If all the {material} is used, how many {to_unit} go into each {items[:-1] if items.endswith('s') else items}?",
            f"{person.capitalize()} bought {start_amount} {from_unit} of {material} and wants to split it evenly among {num_divisions} {items}. How many {to_unit} will each {items[:-1] if items.endswith('s') else items} contain?"
        ]

        story_idx = (i-2) % len(story_templates)
        question_text = story_templates[story_idx]

        variation = {
            "tag": "Gr6_49_E2",
            "question_number": f"2_{i}",
            "question_type": "Fill in the blank",
            "question_text": question_text,
            "correct_answers": [str(result)],
            "solution": [
                ["1/5", f"You want to find how many {to_unit} of {material} each {items[:-1] if items.endswith('s') else items} receives."],
                ["2/5", f"{person.capitalize()} starts with {start_amount} {from_unit} of {material}. Note that there are {conversion_factor} {to_unit} in a {from_unit[:-1] if from_unit.endswith('s') else from_unit}, so multiply {start_amount} {from_unit} by {conversion_factor} to get the amount of {material} in {to_unit}."],
                ["3/5", f"${start_amount} \\times {conversion_factor} = {total_small_units}$ {to_unit}"],
                ["4/5", f"Now we know there are {total_small_units} {to_unit} in total and there are {num_divisions} {items}. To find how many {to_unit} of {material} go into each {items[:-1] if items.endswith('s') else items}, we divide the amount of {material} by the number of {items}."],
                ["5/5", f"${total_small_units} \\div {num_divisions} = {result}$ {to_unit}."]
            ],
            "solution_image_tag": []
        }

        variations.append(variation)

    return variations

if __name__ == "__main__":
    variations = generate_variations()

    # Save to file
    with open("Gr6_49_E2_variations.json", "w") as f:
        json.dump(variations, f, indent=2)

    print(f"Generated {len(variations)} variations for Gr6_49_E2")
    print(f"Saved to Gr6_49_E2_variations.json")