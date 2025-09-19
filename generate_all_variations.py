import json
import random
import copy
from fractions import Fraction

def load_templates():
    """Load all template questions from the original file"""
    with open(r'C:\Users\kapil\numi-scraper\file.json', 'r') as f:
        content = f.read().strip().rstrip(',')
        content = '[' + content + ']'
        data = json.loads(content)
    return data

def generate_gr7_12_e3_variations(templates):
    """Generate word problem variations with pop culture themes"""
    variations = []

    # Pop culture themes
    themes = [
        ("Spider-Man", "web fluid cartridges", "saved from crime fighting"),
        ("Harry Potter", "galleons", "earned from selling potions"),
        ("Minecraft", "diamonds", "mined from caves"),
        ("Pokemon", "Pokeballs", "won from battles"),
        ("Among Us", "coins", "earned from completing tasks"),
        ("Fortnite", "V-Bucks", "earned from Victory Royales"),
        ("Naruto", "ryo", "earned from ninja missions"),
        ("One Piece", "berries", "found in treasure"),
        ("Dragon Ball", "zeni", "won from tournaments"),
        ("Attack on Titan", "coins", "earned from titan eliminations"),
        ("My Hero Academia", "yen", "received from hero work"),
        ("Demon Slayer", "coins", "earned from demon hunting"),
        ("Jujutsu Kaisen", "points", "gained from curse exorcisms"),
        ("Star Wars", "credits", "earned from bounty hunting"),
        ("Marvel", "units", "collected from missions"),
        ("DC Comics", "dollars", "saved from crime fighting"),
        ("Zelda", "rupees", "found in dungeons"),
        ("Mario", "coins", "collected in levels"),
        ("Sonic", "rings", "gathered while running"),
        ("Roblox", "Robux", "earned from games"),
        ("Genshin Impact", "primogems", "collected from quests"),
        ("League of Legends", "blue essence", "earned from matches"),
        ("Valorant", "radianite points", "won from ranked games"),
        ("Apex Legends", "crafting materials", "found in supply bins"),
        ("Call of Duty", "CoD points", "earned from missions"),
    ]

    # Generate 49 variations (3_3 through 3_51 for each template)
    for i in range(3, 52):
        template_idx = random.randint(0, 1)  # Choose between the two templates
        template = templates[template_idx]
        var = copy.deepcopy(template)

        # Select theme
        theme_idx = (i - 3) % len(themes)
        character, currency, action = themes[theme_idx]

        # Generate random numbers
        if template_idx == 0:  # Deposit template
            starting = random.randint(100, 1000)
            amount = random.randint(50, 500)
            final = starting + amount

            var['question_text'] = f"{character} deposited {amount} {currency} they {action}. If {character}'s bank account started out with a balance of {starting} {currency}, which integer represents the final balance?"

            # Rotate correct answer position
            correct_positions = ['A', 'B', 'C', 'D']
            correct_pos = correct_positions[i % 4]

            # Generate choices
            choices = [str(final)]
            distractors = [str(starting), str(amount), str(abs(starting - amount))]
            random.shuffle(distractors)

            all_choices = []
            distractor_idx = 0
            for pos in ['A', 'B', 'C', 'D']:
                if pos == correct_pos:
                    all_choices.append(str(final))
                else:
                    all_choices.append(distractors[distractor_idx])
                    distractor_idx += 1

            var['choices'] = all_choices
            var['correct_answers'] = [correct_pos]

            var['solution'] = [
                ["1/3", f"Add {character}'s starting balance ({starting} {currency}) plus the amount deposited ({amount} {currency}) to find the final balance"],
                ["2/3", f"{starting} {currency} + {amount} {currency} = {final} {currency}"],
                ["3/3", f"{character}'s final balance is {final} {currency}. So, option {correct_pos} is correct."]
            ]
        else:  # Spending template
            starting = random.randint(1000, 20000)
            spent = random.randint(500, starting)
            final = starting - spent

            items = ["legendary weapon", "rare artifact", "special upgrade", "exclusive skin", "power-up", "mystical item"]
            item = random.choice(items)

            var['question_text'] = f"According to their bank statement, {character} spent {spent} {currency} on a {item}. If {character}'s bank account started out with a balance of {starting} {currency}, which integer represents the final balance?"

            # Rotate correct answer position
            correct_positions = ['A', 'B', 'C', 'D']
            correct_pos = correct_positions[i % 4]

            # Generate choices
            choices = [str(final)]
            distractors = [str(starting), str(spent), str(starting + spent)]
            random.shuffle(distractors)

            all_choices = []
            distractor_idx = 0
            for pos in ['A', 'B', 'C', 'D']:
                if pos == correct_pos:
                    all_choices.append(str(final))
                else:
                    all_choices.append(distractors[distractor_idx])
                    distractor_idx += 1

            var['choices'] = all_choices
            var['correct_answers'] = [correct_pos]

            var['solution'] = [
                ["1/3", f"Subtract the amount spent ({spent} {currency}) from {character}'s starting balance ({starting} {currency}) to find the final balance"],
                ["2/3", f"{starting} {currency} - {spent} {currency} = {final} {currency}"],
                ["3/3", f"{character}'s final balance is {final} {currency}. So, option {correct_pos} is correct."]
            ]

        var['question_number'] = f"{template_idx + 1}_{i}"
        variations.append(var)

    return variations

def generate_fraction_variations(templates, tag, num_new=49):
    """Generate variations for fraction addition/subtraction problems"""
    variations = []

    # Define common denominators for each tag type
    if "13" in tag:  # Like denominators
        denominators = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    else:  # Unlike denominators
        denominator_pairs = [(2, 4), (3, 6), (4, 8), (3, 9), (5, 10),
                            (2, 6), (3, 12), (4, 12), (5, 15), (6, 12)]

    template_count = len(templates)
    variations_per_template = num_new // template_count + 1

    variation_num = 3  # Start numbering from 3

    for template_idx, template in enumerate(templates):
        for _ in range(variations_per_template):
            if len(variations) >= num_new:
                break

            var = copy.deepcopy(template)

            if "word-problems" in template.get('skills', ''):
                # Word problem variations with pop culture
                themes = [
                    ("Hogwarts", "students", "received O.W.L.s", "received N.E.W.T.s"),
                    ("Avengers", "heroes", "joined the team", "went on missions"),
                    ("Pokemon gym", "trainers", "earned badges", "caught legendaries"),
                    ("Jedi Temple", "padawans", "passed trials", "became knights"),
                    ("UA High School", "students", "got provisional licenses", "became pro heroes"),
                ]

                theme = random.choice(themes)

                if "13" in tag:  # Like denominators
                    denom = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
                    num1 = random.randint(1, denom - 1)
                    num2 = random.randint(1, denom - 1)

                    if "add" in template.get('skills', ''):
                        result = Fraction(num1 + num2, denom)
                        var['question_text'] = f"In {theme[0]}, $\\frac{{{num1}}}{{{denom}}}$ of the {theme[1]} {theme[2]} and $\\frac{{{num2}}}{{{denom}}}$ {theme[3]}. What fraction of the {theme[1]} achieved either accomplishment?\\n\\nWrite your answer as a fraction or as a whole or mixed number.\\n\\n"
                    else:  # Subtraction word problem
                        if num1 > num2:
                            result = Fraction(num1 - num2, denom)
                            var['question_text'] = f"At a competition, contestant A completed $\\frac{{{num1}}}{{{denom}}}$ of the challenge while contestant B finished just $\\frac{{{num2}}}{{{denom}}}$ of it.\\n\\nHow much more did contestant A complete than contestant B?\\n\\nWrite your answer as a fraction or as a whole or mixed number.\\n\\n"
                        else:
                            num1, num2 = num2, num1
                            result = Fraction(num1 - num2, denom)
                            var['question_text'] = f"At a competition, contestant A completed $\\frac{{{num1}}}{{{denom}}}$ of the challenge while contestant B finished just $\\frac{{{num2}}}{{{denom}}}$ of it.\\n\\nHow much more did contestant A complete than contestant B?\\n\\nWrite your answer as a fraction or as a whole or mixed number.\\n\\n"
                else:  # Unlike denominators word problems
                    d1, d2 = random.choice(denominator_pairs)
                    num1 = random.randint(1, d1 - 1)
                    num2 = random.randint(1, d2 - 1)

                    if "add" in template.get('skills', ''):
                        result = Fraction(num1, d1) + Fraction(num2, d2)
                    else:
                        result = abs(Fraction(num1, d1) - Fraction(num2, d2))

                    var['question_text'] = f"A hero used $\\frac{{{num1}}}{{{d1}}}$ of their energy for the first attack and $\\frac{{{num2}}}{{{d2}}}$ for the second. How much total energy was used?\\n\\nWrite your answer as a fraction or as a whole or mixed number.\\n\\n"

                # Format result
                if result.denominator == 1:
                    var['correct_answers'] = [str(result.numerator)]
                else:
                    var['correct_answers'] = [f"{result.numerator}/{result.denominator}"]

                # Update solution
                var['solution'][0][1] = var['solution'][0][1].replace("1/5", f"{num1}/{denom if '13' in tag else d1}")
                var['solution'][0][1] = var['solution'][0][1].replace("3/5", f"{num2}/{denom if '13' in tag else d2}")

            else:  # Regular fraction problems
                if "13" in tag:  # Like denominators
                    denom = random.choice(denominators)
                    num1 = random.randint(1, denom - 1)
                    num2 = random.randint(1, denom - 1)

                    if "add" in template.get('skills', ''):
                        var['question_text'] = "Add.\\n"
                        var['image_tag'] = f"Gr7_{tag.split('_')[1]}_{template_idx + 1}_{variation_num}"
                        var['backend_description'] = f"Shows the addition of {num1}/{denom} + {num2}/{denom} with an empty box for the answer."
                        result = Fraction(num1 + num2, denom)
                    else:
                        if num1 < num2:
                            num1, num2 = num2, num1
                        var['question_text'] = "Subtract.\\n"
                        var['image_tag'] = f"Gr7_{tag.split('_')[1]}_{template_idx + 1}_{variation_num}"
                        var['backend_description'] = f"Shows the subtraction of {num1}/{denom} - {num2}/{denom} with an empty box for the answer."
                        result = Fraction(num1 - num2, denom)

                    # Update solution
                    var['solution'] = [
                        ["1/2", f"Since the denominators are the same, just {'add' if 'add' in template.get('skills', '') else 'subtract'} the numerators: {num1} {'+'if 'add' in template.get('skills', '') else '-'} {num2} = {result.numerator}."],
                        ["2/2", f"So, $\\frac{{{num1}}}{{{denom}}} {'+'if 'add' in template.get('skills', '') else '-'} \\frac{{{num2}}}{{{denom}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}$."]
                    ]
                else:  # Unlike denominators
                    d1, d2 = random.choice(denominator_pairs)
                    num1 = random.randint(1, d1 - 1)
                    num2 = random.randint(1, d2 - 1)

                    if "add" in template.get('skills', ''):
                        result = Fraction(num1, d1) + Fraction(num2, d2)
                        operation = "+"
                    else:
                        if Fraction(num1, d1) < Fraction(num2, d2):
                            num1, d1, num2, d2 = num2, d2, num1, d1
                        result = Fraction(num1, d1) - Fraction(num2, d2)
                        operation = "-"

                    var['image_tag'] = f"Gr7_{tag.split('_')[1]}_{template_idx + 1}_{variation_num}"
                    var['backend_description'] = f"Shows the {'addition' if operation == '+' else 'subtraction'} problem {num1}/{d1} {operation} {num2}/{d2} with an empty box for the answer."

                # Format result
                if result.denominator == 1:
                    var['correct_answers'] = [str(result.numerator)]
                else:
                    var['correct_answers'] = [f"{result.numerator}/{result.denominator}"]

            var['question_number'] = f"{template_idx + 1}_{variation_num}"
            variations.append(var)
            variation_num += 1

    return variations[:num_new]

def save_variations(variations, tag):
    """Save variations to JSON file"""
    filename = f"{tag} variations.json"
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Saved {len(variations)} variations to {filename}")

def main():
    # Load all templates
    all_templates = load_templates()

    # Process each tag group
    tag_groups = {}
    for q in all_templates:
        if 'tag' in q:
            tag = q['tag']
            if tag not in tag_groups:
                tag_groups[tag] = []
            tag_groups[tag].append(q)

    # Generate variations for each tag
    for tag, templates in tag_groups.items():
        print(f"\nProcessing {tag} with {len(templates)} template(s)")

        # Calculate how many new variations needed
        total_needed = 51
        num_new = total_needed - len(templates)

        if tag == "Gr7_12_E3":
            variations = generate_gr7_12_e3_variations(templates)
        elif tag.startswith("Gr7_13") or tag.startswith("Gr7_14") or tag.startswith("Gr7_15") or tag.startswith("Gr7_16"):
            variations = generate_fraction_variations(templates, tag, num_new)
        else:
            # Skip tags already handled by individual scripts
            if tag in ["Gr7_12_E1", "Gr7_12_E2"]:
                print(f"Skipping {tag} - already has dedicated script")
                continue
            else:
                print(f"Skipping {tag} - needs custom implementation")
                continue

        save_variations(variations, tag)

if __name__ == "__main__":
    main()