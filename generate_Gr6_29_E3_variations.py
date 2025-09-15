import json
import random

def generate_variations():
    """Generate 51 variations for Gr6_29_E3 - tape diagram ratio problems"""

    variations = []

    # Original template
    original = {
        "tag": "Gr6_29_E3",
        "question_type": "Fill in the blank",
        "question_text": "Jon's scout troop went fishing yesterday. The scouts caught 2 bluegills for every 5 sunfish. If the scout caught 25 sunfish, how many bluegills did they catch? Use the following model to help you answer the question.",
        "skill": "use-tape-diagrams-to-solve-ratio-word-problems",
        "image_tag": "Gr6_29_3_1",
        "question_number": "3_1",
        "backend_description": "A tape diagram showing a ratio comparison between bluegills and sunfish. The diagram consists of two horizontal bars: the top bar labeled 'bluegills' contains 2 blue rectangular sections, and the bottom bar labeled 'sunfish' contains 5 yellow rectangular sections. This visual model represents the ratio of 2 bluegills to 5 sunfish that the scouts caught while fishing.",
        "correct_answers": ["10"],
        "solution": [
            ["1/5", "The diagram models the ratio in the story. There are 2 boxes for bluegills and 5 boxes for sunfish."],
            ["2/5", "Find how many fish each box in the diagram represents. The scouts caught 25 sunfish, and there are 5 boxes in the diagram for sunfish. So, divide 25 by 5: $25 \\div 5 = 5$"],
            ["3/5", "Each box in the diagram represents 5 fish. There are 2 boxes in the diagram for bluegills. So, multiply to find how many bluegills the scouts caught."],
            ["4/5", "$2 \\times 5 = 10$"],
            ["5/5", "The scouts caught 10 bluegills yesterday."]
        ],
        "solution_image_tag": []
    }

    variations.append(original)

    # Define contexts and items for variations
    contexts = [
        ("marine biologist", "collected", "seahorses", "starfish"),
        ("Pokemon trainer", "caught", "Pikachus", "Charmanders"),
        ("bakery", "sold", "croissants", "bagels"),
        ("library", "checked out", "graphic novels", "chapter books"),
        ("game store", "sold", "Nintendo Switch games", "PlayStation games"),
        ("anime convention", "sold", "manga volumes", "anime DVDs"),
        ("Marvel store", "sold", "Spider-Man comics", "Batman comics"),
        ("Harry Potter shop", "sold", "wands", "spell books"),
        ("zoo", "counted", "penguins", "flamingos"),
        ("farm", "harvested", "tomatoes", "cucumbers"),
        ("candy store", "packaged", "lollipops", "chocolate bars"),
        ("music store", "sold", "guitars", "keyboards"),
        ("sports shop", "sold", "basketballs", "soccer balls"),
        ("Minecraft server", "collected", "diamonds", "emeralds"),
        ("Fortnite match", "found", "shield potions", "medkits"),
        ("Star Wars shop", "sold", "lightsabers", "blasters"),
        ("Disney store", "sold", "Mickey Mouse plushies", "Donald Duck toys"),
        ("pet store", "sold", "hamsters", "guinea pigs"),
        ("flower shop", "arranged", "roses", "tulips"),
        ("ice cream shop", "served", "vanilla cones", "chocolate sundaes"),
        ("sushi restaurant", "prepared", "California rolls", "salmon nigiri"),
        ("pizza place", "delivered", "cheese pizzas", "pepperoni pizzas"),
        ("coffee shop", "served", "lattes", "cappuccinos"),
        ("Naruto's ramen shop", "served", "miso ramen bowls", "shoyu ramen bowls"),
        ("One Piece crew", "collected", "treasure chests", "gold coins"),
        ("Dragon Ball tournament", "counted", "senzu beans", "power capsules"),
        ("Avengers mission", "collected", "vibranium samples", "arc reactors"),
        ("Hogwarts", "distributed", "chocolate frogs", "Bertie Bott's beans"),
        ("Jurassic Park", "counted", "velociraptors", "triceratops"),
        ("NASA mission", "collected", "moon rocks", "Mars samples"),
        ("archaeological dig", "found", "pottery shards", "arrowheads"),
        ("treasure hunt", "discovered", "silver coins", "gold doubloons"),
        ("chemistry lab", "prepared", "test tubes", "beakers"),
        ("art studio", "created", "oil paintings", "watercolors"),
        ("construction site", "used", "hammers", "screwdrivers"),
        ("Zelda's adventure", "collected", "rupees", "heart pieces"),
        ("Mario's quest", "collected", "coins", "stars"),
        ("toy factory", "produced", "action figures", "board games"),
        ("movie theater", "sold", "popcorn buckets", "soda cups"),
        ("gym", "counted", "dumbbells", "resistance bands"),
        ("school cafeteria", "served", "sandwiches", "salads"),
        ("clothing store", "sold", "t-shirts", "jeans"),
        ("electronics store", "sold", "smartphones", "tablets"),
        ("bookstore", "sold", "fiction books", "non-fiction books"),
        ("garden center", "sold", "rose bushes", "oak trees"),
        ("aquarium", "housed", "clownfish", "angelfish"),
        ("museum", "displayed", "fossils", "minerals"),
        ("theme park", "sold", "fast passes", "regular tickets"),
        ("circus", "featured", "acrobats", "clowns")
    ]

    # Generate unique ratio combinations
    ratio_combinations = []
    for first in range(2, 10):
        for second in range(3, 15):
            if first != second and (first, second) not in ratio_combinations:
                # Calculate a multiple that gives reasonable numbers
                for multiple in range(2, 20):
                    total_second = second * multiple
                    if 10 <= total_second <= 150:
                        ratio_combinations.append((first, second, total_second))

    # Shuffle and select 50 combinations
    random.seed(42)
    random.shuffle(ratio_combinations)
    selected_ratios = ratio_combinations[:50]
    random.shuffle(contexts)

    for i in range(2, 52):
        ratio_first, ratio_second, total_second = selected_ratios[i-2]
        context_idx = (i-2) % len(contexts)
        who, action, item1, item2 = contexts[context_idx]

        total_first = (total_second // ratio_second) * ratio_first
        value_per_box = total_second // ratio_second

        variation = {
            "tag": "Gr6_29_E3",
            "question_type": "Fill in the blank",
            "question_text": f"{who.capitalize()} {action} {ratio_first} {item1} for every {ratio_second} {item2}. If they {action} {total_second} {item2}, how many {item1} did they {action.rstrip('ed')}? Use the following model to help you answer the question.",
            "skill": "use-tape-diagrams-to-solve-ratio-word-problems",
            "image_tag": f"Gr6_29_3_{i}",
            "question_number": f"3_{i}",
            "backend_description": f"A tape diagram showing a ratio comparison between {item1} and {item2}. The diagram consists of two horizontal bars: the top bar labeled '{item1}' contains {ratio_first} blue rectangular sections, and the bottom bar labeled '{item2}' contains {ratio_second} yellow rectangular sections. This visual model represents the ratio of {ratio_first} {item1} to {ratio_second} {item2}.",
            "correct_answers": [str(total_first)],
            "solution": [
                ["1/5", f"The diagram models the ratio in the story. There are {ratio_first} boxes for {item1} and {ratio_second} boxes for {item2}."],
                ["2/5", f"Find how many items each box in the diagram represents. They {action} {total_second} {item2}, and there are {ratio_second} boxes in the diagram for {item2}. So, divide {total_second} by {ratio_second}: ${total_second} \\div {ratio_second} = {value_per_box}$"],
                ["3/5", f"Each box in the diagram represents {value_per_box} items. There are {ratio_first} boxes in the diagram for {item1}. So, multiply to find how many {item1} they {action}."],
                ["4/5", f"${ratio_first} \\times {value_per_box} = {total_first}$"],
                ["5/5", f"They {action} {total_first} {item1}."]
            ],
            "solution_image_tag": []
        }

        variations.append(variation)

    return variations

if __name__ == "__main__":
    variations = generate_variations()

    # Save to file
    with open("Gr6_29_E3_variations.json", "w") as f:
        json.dump(variations, f, indent=2)

    print(f"Generated {len(variations)} variations for Gr6_29_E3")
    print(f"Saved to Gr6_29_E3_variations.json")