import json
import random
import copy

# Load the formatted questions
with open('questions_formatted.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

# Filter questions for this tag
tag = "Gr7_12_E3"
template_questions = [q for q in all_questions if q.get('tag') == tag]

print(f"Found {len(template_questions)} template questions for {tag}")

# Since we have 2 templates, we need 49 new variations
variations_needed = 51 - len(template_questions)
variations = []

# Template 1: Deposit scenario (adding to balance)
# Template 2: Spending scenario (subtracting from balance)

# Pop culture themes for word problems
pop_culture_themes = [
    ("Naruto", "earned from completing ninja missions", "ryo"),
    ("Harry Potter", "received from selling magical potions", "galleons"),
    ("Pokemon", "won from gym battles", "pokedollars"),
    ("Marvel", "received from Tony Stark for superhero work", "dollars"),
    ("Star Wars", "earned from bounty hunting", "credits"),
    ("Dragon Ball", "won from tournament prizes", "zeni"),
    ("One Piece", "found in treasure chests", "berries"),
    ("Attack on Titan", "earned from titan elimination rewards", "coins"),
    ("My Hero Academia", "received from hero agency work", "yen"),
    ("Demon Slayer", "earned from demon slaying missions", "gold"),
    ("Stranger Things", "found in the Upside Down", "dollars"),
    ("The Mandalorian", "earned from guild contracts", "beskar"),
    ("Minecraft", "earned from trading with villagers", "emeralds"),
    ("Fortnite", "won from Victory Royales", "V-bucks"),
    ("Among Us", "collected from completing tasks", "coins"),
    ("Squid Game", "won from surviving games", "won"),
    ("Wednesday", "inherited from the Addams family", "dollars"),
    ("Avatar", "earned from helping the Na'vi", "units"),
    ("SpongeBob", "earned from working at the Krusty Krab", "dollars"),
    ("Rick and Morty", "stolen from alternate dimensions", "schmeckles")
]

spending_themes = [
    ("new jutsu scrolls", "Naruto"),
    ("a Firebolt broomstick", "Harry Potter"),
    ("rare Pokemon cards", "Pokemon"),
    ("vibranium shield upgrades", "Marvel"),
    ("lightsaber crystals", "Star Wars"),
    ("senzu beans", "Dragon Ball"),
    ("Devil Fruit", "One Piece"),
    ("ODM gear maintenance", "Attack on Titan"),
    ("hero costume upgrades", "My Hero Academia"),
    ("nichirin sword polish", "Demon Slayer"),
    ("Eggo waffles", "Stranger Things"),
    ("ship repairs", "The Mandalorian"),
    ("diamond pickaxes", "Minecraft"),
    ("new skins", "Fortnite"),
    ("emergency meeting buttons", "Among Us"),
    ("survival gear", "Squid Game"),
    ("gothic accessories", "Wednesday"),
    ("ikran saddles", "Avatar"),
    ("Krabby Patties", "SpongeBob"),
    ("portal gun batteries", "Rick and Morty")
]

names = ["Sakura", "Hermione", "Ash", "Peter", "Luke", "Goku", "Luffy", "Eren", "Deku", "Tanjiro",
         "Eleven", "Din", "Steve", "Jonesy", "Red", "Gi-hun", "Enid", "Jake", "Patrick", "Morty",
         "Levi", "Nezuko", "Pikachu", "Tony", "Yoda", "Vegeta", "Zoro", "Mikasa", "Bakugo", "Zenitsu"]

for i in range(variations_needed):
    # Randomly choose which template to base the variation on
    template_idx = random.randint(0, 1)
    variation = copy.deepcopy(template_questions[template_idx])

    # Determine which template number this variation is based on
    base_template_num = int(variation['question_number'].split('_')[0])

    # Update question number
    variation_num = i + 3
    variation['question_number'] = f"{base_template_num}_{variation_num}"

    # Select random theme and name
    name = random.choice(names)

    if template_idx == 0:  # Deposit/earning scenario
        theme = random.choice(pop_culture_themes)
        earned = random.randint(50, 5000)
        starting = random.randint(100, 10000)
        final = starting + earned
        currency = theme[2]

        variation['question_text'] = (
            f"{name} deposited {earned} {currency} they made from {theme[1]}. "
            f"If {name}'s bank account started out with a balance of {starting} {currency}, "
            f"which integer represents the final balance?"
        )

        # Generate multiple choice options
        options = [
            final - random.randint(100, 500),
            final + random.randint(100, 500),
            final,
            abs(starting - earned)
        ]
        random.shuffle(options)
        correct_idx = options.index(final)
        correct_letter = ['A', 'B', 'C', 'D'][correct_idx]

        variation['choices'] = [str(opt) for opt in options]
        variation['correct_answers'] = [correct_letter]

        variation['solution'] = [
            ["1/3", f"Add {name}'s starting balance ({starting} {currency}) plus the amount deposited ({earned} {currency}) to find the final balance"],
            ["2/3", f"{starting} {currency} + {earned} {currency} = {final} {currency}"],
            ["3/3", f"{name}'s final balance is {final} {currency}. So, option {correct_letter} is correct."]
        ]

    else:  # Spending scenario
        item_theme = random.choice(spending_themes)
        spent = random.randint(100, 15000)
        starting = random.randint(spent, spent + 10000)  # Ensure enough balance
        final = starting - spent

        variation['question_text'] = (
            f"According to their bank statement, {name} spent {spent} dollars on {item_theme[0]}. "
            f"If {name}'s bank account started out with a balance of {starting} dollars, "
            f"which integer represents the final balance?"
        )

        # Generate multiple choice options
        options = [
            final,
            final + random.randint(100, 1000),
            starting,
            starting + spent
        ]
        random.shuffle(options)
        correct_idx = options.index(final)
        correct_letter = ['A', 'B', 'C', 'D'][correct_idx]

        variation['choices'] = [str(opt) for opt in options]
        variation['correct_answers'] = [correct_letter]

        variation['solution'] = [
            ["1/3", f"Subtract the amount spent ({spent} dollars) from {name}'s starting balance ({starting} dollars) to find the final balance"],
            ["2/3", f"{starting} dollars - {spent} dollars = {final} dollars"],
            ["3/3", f"{name}'s final balance is {final} dollars. So, option {correct_letter} is correct."]
        ]

    variations.append(variation)

# Save variations to file
output_file = f'{tag} variations.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(variations, f, indent=2, ensure_ascii=False)

print(f"Generated {len(variations)} variations and saved to {output_file}")
print(f"Total questions for {tag}: {len(template_questions)} templates + {len(variations)} variations = {len(template_questions) + len(variations)}")