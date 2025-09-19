import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_8_E1 (price-lists)"""

    # Load template
    with open('Gr7_8_E1_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]  # Only one template for this tag

    # Define item sets for variations
    hardware_items = [
        ("red thumbtack", 0.12), ("brass clip", 0.52), ("small paintbrush", 0.70),
        ("short steel screw", 0.14), ("roll of electrical tape", 0.60), ("small metal hook", 0.60),
        ("rubber washer", 0.15), ("metal nail", 0.18), ("plastic anchor", 0.25),
        ("wooden dowel", 0.35), ("cable tie", 0.08), ("corner bracket", 0.45),
        ("door stopper", 0.65), ("wall plug", 0.10), ("picture hanger", 0.38),
        ("furniture pad", 0.22), ("drawer knob", 0.85), ("hinge pin", 0.28),
        ("lock washer", 0.16), ("eye hook", 0.42), ("wing nut", 0.20),
        ("spring clip", 0.30), ("toggle bolt", 0.55), ("masonry bit", 0.95),
        ("sanding pad", 0.48), ("wire connector", 0.12), ("pipe clamp", 0.75),
        ("adhesive strip", 0.33), ("magnetic catch", 0.68), ("shelf pin", 0.15)
    ]

    variations = []
    variation_num = 2  # Start from 2 since template is 1_3

    # Generate 50 variations (51 total - 1 template = 50 new)
    while len(variations) < 50:
        # Randomly select 6 items
        items = random.sample(hardware_items, 6)

        # Select two items to buy
        buy_items = random.sample(items, 2)

        # Create variation
        variation = copy.deepcopy(template)

        # Update question text
        variation["question_text"] = f"How much money does Wanda need to buy a {buy_items[0][0]} and a {buy_items[1][0]}?\n\nDo not round.\n"

        # Calculate answer
        total = buy_items[0][1] + buy_items[1][1]
        variation["correct_answers"] = [f"{total:.2f}"]

        # Update backend description
        items_desc = ", ".join([f"{item[0]} ({item[1]:.2f} dollars)" for item in items])
        variation["backend_description"] = f"A price list table showing hardware items: {items_desc}. The table has alternating row colors for easier reading."

        # Update solution
        variation["solution"] = [
            [
                "1/2",
                f"Add the price of a {buy_items[0][0]} and the price of a {buy_items[1][0]}:\n{buy_items[0][1]:.2f} dollars + {buy_items[1][1]:.2f} dollars = {total:.2f} dollars."
            ],
            [
                "2/2",
                f"Wanda needs {total:.2f} dollars to buy a {buy_items[0][0]} and a {buy_items[1][0]}."
            ]
        ]

        # Update question number
        variation["question_number"] = f"1_{variation_num}"

        # Update image tag
        variation["image_tag"] = f"Gr7_8_1_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_8_E1 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_8_E1")

if __name__ == "__main__":
    generate_variations()