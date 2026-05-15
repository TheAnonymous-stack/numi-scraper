import json
import random

def generate_variations():
    """Generate 51 variations for Gr6_31_E3 - bar model percentage problems"""

    variations = []

    # Original template
    original = {
        "tag": "Gr6_31_E3",
        "question_number": "3_1",
        "question_type": "Fill in the blank",
        "question_text": "Nomad's ice cream truck sells 50 kinds of treats. If 20% of them are popsicles, how many kinds of treats are popsicles? Use the following model to help you answer the question.",
        "image_tag": "Gr6_31_3_1",
        "backend_description": "A horizontal bar model diagram showing percentage and numerical representations. The top bar is divided into 5 equal sections with percentage labels: 0%, 20%, 40%, 60%, 80%, and 100%. Below it is a corresponding number line showing values from 0 to 50, with a question mark at the 20% position (which corresponds to the value being solved for). The diagram is colored in purple/pink and is used to help visualize the relationship between percentages and actual quantities.",
        "correct_answers": ["10"],
        "solution": [
            ["1/3", "The whole model represents 50 kinds of treats, and there are 5 equal parts. Divide to find how many kinds of treats each part of the model represents."],
            ["2/3", "$50 \\div 5 = 10$"],
            ["3/3", "Each part represents 10 kinds of treats. Since 20% corresponds to 1 part, 10 kinds of treats are popsicles."]
        ],
        "solution_image_tag": []
    }

    variations.append(original)

    # Define contexts and items for variations
    contexts = [
        ("Marvel comic store", "comics", "Spider-Man issues"),
        ("Pokémon Center", "trading cards", "rare holographic cards"),
        ("Netflix", "shows", "anime series"),
        ("Steam library", "games", "indie games"),
        ("Spotify playlist", "songs", "K-pop tracks"),
        ("YouTube channel", "videos", "gaming streams"),
        ("Disney+", "movies", "Marvel films"),
        ("Hogwarts library", "books", "spellbooks"),
        ("Nintendo eShop", "titles", "Mario games"),
        ("anime convention", "merchandise items", "figurines"),
        ("Minecraft server", "builds", "redstone contraptions"),
        ("Fortnite item shop", "skins", "legendary skins"),
        ("Star Wars collection", "items", "lightsabers"),
        ("bakery", "pastries", "croissants"),
        ("school cafeteria", "menu items", "vegetarian options"),
        ("gym", "equipment pieces", "cardio machines"),
        ("music festival", "performers", "rock bands"),
        ("zoo", "animals", "mammals"),
        ("museum", "artifacts", "ancient Egyptian pieces"),
        ("theme park", "attractions", "roller coasters"),
        ("library", "books", "graphic novels"),
        ("pet store", "animals", "tropical fish"),
        ("flower shop", "flowers", "roses"),
        ("electronics store", "products", "smartphones"),
        ("clothing store", "items", "designer jeans"),
        ("toy store", "toys", "LEGO sets"),
        ("bookstore", "titles", "mystery novels"),
        ("candy shop", "candies", "chocolate bars"),
        ("pizza restaurant", "toppings", "vegetable toppings"),
        ("coffee shop", "drinks", "iced beverages"),
        ("sushi restaurant", "rolls", "vegetarian rolls"),
        ("ice cream parlor", "flavors", "fruit sorbets"),
        ("game arcade", "games", "racing games"),
        ("movie theater", "screens", "IMAX screens"),
        ("sports complex", "facilities", "basketball courts"),
        ("art gallery", "paintings", "abstract works"),
        ("science lab", "experiments", "chemistry experiments"),
        ("computer lab", "computers", "gaming PCs"),
        ("Naruto's ninja academy", "techniques", "shadow clone variations"),
        ("One Piece ship", "treasure maps", "Grand Line maps"),
        ("Dragon Ball training ground", "exercises", "ki control drills"),
        ("Avengers headquarters", "gadgets", "Tony Stark inventions"),
        ("Jedi temple", "holocrons", "Sith artifacts"),
        ("Gotham City store", "items", "Batman merchandise"),
        ("Wakanda tech center", "devices", "vibranium tools"),
        ("Studio Ghibli shop", "products", "Totoro plushies"),
        ("PlayStation Store", "games", "exclusive titles"),
        ("Xbox Game Pass", "games", "RPG games"),
        ("TikTok account", "videos", "dance videos"),
        ("Instagram page", "posts", "travel photos")
    ]

    # Generate percentage and total combinations
    percentage_combinations = []

    # Use percentages that divide evenly into 5 parts (20%, 40%, 60%, 80%)
    percentages = [20, 40, 60, 80]

    # Generate totals that work well with these percentages
    for percentage in percentages:
        for total in [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
                     105, 110, 115, 120, 125, 130, 135, 140, 145, 150]:
            if total % 5 == 0:  # Ensure clean division by 5
                answer = (total * percentage) // 100
                percentage_combinations.append((total, percentage, answer))

    # Shuffle and select 50 combinations
    random.seed(42)
    random.shuffle(percentage_combinations)
    selected_combinations = percentage_combinations[:50]
    random.shuffle(contexts)

    for i in range(2, 52):
        total, percentage, answer = selected_combinations[i-2]
        context_idx = (i-2) % len(contexts)
        place, items, specific_items = contexts[context_idx]

        parts = 5
        value_per_part = total // parts
        parts_for_percentage = percentage // 20

        # Adjust description based on percentage
        max_val = total

        variation = {
            "tag": "Gr6_31_E3",
            "question_number": f"3_{i}",
            "question_type": "Fill in the blank",
            "question_text": f"{place} has {total} {items}. If {percentage}% of them are {specific_items}, how many {items} are {specific_items}? Use the following model to help you answer the question.",
            "image_tag": f"Gr6_31_3_{i}",
            "backend_description": f"A horizontal bar model diagram showing percentage and numerical representations. The top bar is divided into {parts} equal sections with percentage labels: 0%, 20%, 40%, 60%, 80%, and 100%. Below it is a corresponding number line showing values from 0 to {total}, with a question mark at the {percentage}% position (which corresponds to the value being solved for). The diagram is colored in purple/pink and is used to help visualize the relationship between percentages and actual quantities.",
            "correct_answers": [str(answer)],
            "solution": [
                ["1/3", f"The whole model represents {total} {items}, and there are {parts} equal parts. Divide to find how many {items} each part of the model represents."],
                ["2/3", f"${total} \\div {parts} = {value_per_part}$"],
                ["3/3", f"Each part represents {value_per_part} {items}. Since {percentage}% corresponds to {parts_for_percentage} part{'s' if parts_for_percentage > 1 else ''}, {answer} {items} are {specific_items}."]
            ],
            "solution_image_tag": []
        }

        variations.append(variation)

    return variations

if __name__ == "__main__":
    variations = generate_variations()

    # Save to file
    with open("Gr6_31_E3_variations.json", "w") as f:
        json.dump(variations, f, indent=2)

    print(f"Generated {len(variations)} variations for Gr6_31_E3")
    print(f"Saved to Gr6_31_E3_variations.json")