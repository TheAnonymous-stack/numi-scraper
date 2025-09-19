import json
import random
import copy

def generate_variations():
    # Load the fixed JSON file to get the template
    with open(r'C:\Users\kapil\numi-scraper\file_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # Find the template with tag Gr7_7_E1
    template = None
    for item in data:
        if item.get('tag') == 'Gr7_7_E1':
            template = item
            break

    if not template:
        print("Template for Gr7_7_E1 not found")
        return

    variations = []

    # Pop culture themes for word problems
    themes = [
        ("Harry Potter", "magic powder", "potion"),
        ("Naruto", "ramen seasoning", "special ramen"),
        ("Pokemon", "rare candy dust", "evolution serum"),
        ("Marvel", "vibranium particles", "shield upgrade"),
        ("Star Wars", "kyber crystal dust", "lightsaber"),
        ("Dragon Ball", "senzu bean powder", "healing drink"),
        ("One Piece", "sea salt", "pirate stew"),
        ("Attack on Titan", "titan serum", "experiment"),
        ("My Hero Academia", "quirk enhancer", "training drink"),
        ("Demon Slayer", "wisteria powder", "demon repellent"),
        ("SpongeBob", "secret formula ingredient", "Krabby Patty"),
        ("Minecraft", "redstone dust", "potion"),
        ("Fortnite", "shield powder", "shield potion"),
        ("Among Us", "reactor fuel", "engine repair"),
        ("Zelda", "fairy dust", "health elixir"),
        ("Mario", "fire flower powder", "power-up"),
        ("Sonic", "ring dust", "speed boost"),
        ("Batman", "bat powder", "smoke bomb"),
        ("Spider-Man", "web fluid catalyst", "web shooters"),
        ("Iron Man", "arc reactor particles", "suit upgrade"),
        ("Thor", "Asgardian dust", "weapon enhancement"),
        ("Black Panther", "heart-shaped herb powder", "ceremonial drink"),
        ("Doctor Strange", "mystic powder", "spell"),
        ("Stranger Things", "Upside Down spores", "experiment"),
        ("Rick and Morty", "portal gun particles", "interdimensional travel"),
        ("Avatar", "spirit water essence", "healing potion"),
        ("Frozen", "ice crystal powder", "magic spell"),
        ("Encanto", "miracle powder", "magical gift"),
        ("Moana", "ocean salt", "wayfinding ritual"),
        ("Tangled", "golden flower dust", "healing potion"),
        ("Shrek", "ogre spice", "swamp stew"),
        ("Toy Story", "battery acid crystals", "toy repair"),
        ("Cars", "nitrous oxide powder", "race fuel"),
        ("Finding Nemo", "coral dust", "reef restoration"),
        ("The Incredibles", "super suit fiber", "costume repair"),
        ("Ratatouille", "special seasoning", "signature dish"),
        ("Wall-E", "plant fertilizer", "Earth restoration"),
        ("Up", "helium powder", "balloon mixture"),
        ("Inside Out", "memory dust", "core memory"),
        ("Coco", "marigold powder", "Day of the Dead offering"),
        ("Luca", "sea monster scales", "transformation potion"),
        ("Turning Red", "red panda fur essence", "calming tea"),
        ("Jujutsu Kaisen", "cursed energy powder", "technique enhancement"),
        ("Chainsaw Man", "devil essence", "contract ritual"),
        ("Spy x Family", "spy gadget powder", "smoke screen"),
        ("Mob Psycho", "psychic salt", "exorcism"),
        ("Death Note", "shinigami dust", "death god ritual"),
        ("Tokyo Ghoul", "ghoul suppressant", "medicine"),
        ("Bleach", "spirit particles", "hollow mask"),
        ("Fullmetal Alchemist", "philosopher stone dust", "transmutation")
    ]

    # Generate 50 variations
    for i in range(2, 52):
        variation = copy.deepcopy(template)

        # Select random theme
        character, ingredient, usage = random.choice(themes)

        # Generate random decimal values
        total = round(random.uniform(0.5, 9.9), random.choice([1, 2]))
        used = round(random.uniform(0.01, min(0.99, total * 0.8)), 2)
        remaining = round(total - used, 2)

        # Update question text
        variation['question_text'] = f"{character} had {total} grams of {ingredient}. Then they used {used} grams of the {ingredient} to make some {usage}.\n\nHow much {ingredient} does {character} have left?\n\n"

        # Update correct answer
        variation['correct_answers'] = [str(remaining)]

        # Format values for display in solution
        total_display = f"{total:.2f}" if total != int(total) else str(int(total))
        used_display = f"{used:.2f}" if used != int(used) else str(int(used))
        remaining_display = f"{remaining:.2f}" if remaining != int(remaining) else str(int(remaining))

        # Update solution
        variation['solution'] = [
            [
                "1/2",
                f"To find out how much {ingredient} {character} has left, subtract the amount they used from the total amount:\n"
            ],
            [
                "2/2",
                f"{character} has {remaining} grams of {ingredient} left."
            ]
        ]

        # Update solution image tag
        variation['solution_image_tag'] = [
            [
                "1/2",
                f"Gr7_7_1_1_{i}_step_1",
                f"Shows the subtraction calculation {total_display} - {used_display} = {remaining_display}, with proper decimal alignment. The visual representation helps students see how to subtract decimals."
            ]
        ]

        # Update question number
        variation['question_number'] = f"1_{i}"

        variations.append(variation)

    # Save variations to JSON file
    with open(r'C:\Users\kapil\numi-scraper\Gr7_7_E1 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_7_E1")

if __name__ == "__main__":
    generate_variations()