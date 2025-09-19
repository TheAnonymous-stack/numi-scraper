import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_8_E2 (unit-prices-find-the-total-price)"""

    # Load template
    with open('Gr7_8_E2_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    # Define food items and prices for variations
    food_items = [
        ("vegetable soup", 0.63), ("tortilla soup", 0.63), ("chicken chili", 0.72), ("lobster bisque", 1.04),
        ("tomato soup", 0.55), ("minestrone", 0.68), ("clam chowder", 0.89), ("french onion soup", 0.75),
        ("mushroom soup", 0.66), ("lentil soup", 0.58), ("split pea soup", 0.61), ("corn chowder", 0.70),
        ("beef stew", 0.82), ("chicken noodle", 0.64), ("potato soup", 0.59), ("seafood bisque", 1.15),
        ("thai curry", 0.88), ("miso soup", 0.71), ("pho broth", 0.76), ("ramen base", 0.79),
        ("gazpacho", 0.65), ("borscht", 0.62), ("gumbo", 0.85), ("consomme", 0.92)
    ]

    variations = []
    variation_num = 2  # Start from 2 since template is 2_1

    # Generate 50 variations
    while len(variations) < 50:
        # Randomly select 4 items
        items = random.sample(food_items, 4)

        # Select one item for the question
        selected_item = random.choice(items)

        # Random quantity (1-5 kg)
        quantity = random.randint(1, 5)

        # Create variation
        variation = copy.deepcopy(template)

        # Update question text
        variation["question_text"] = f"What is the total cost for {quantity} kilogram{'s' if quantity > 1 else ''} of {selected_item[0]}?\n\n Do not round your answer.\n"

        # Calculate answer
        total = selected_item[1] * quantity
        variation["correct_answers"] = [
            [f"{total:.2f}"],
            [f"{total:.2f} dollars"]
        ]

        # Update backend description
        items_desc = ", ".join([f"{item[0]} ({item[1]:.2f} dollars/kg)" for item in items])
        variation["backend_description"] = f"A price list table showing soup prices per kilogram: {items_desc}. The table clearly displays unit prices."

        # Update solution
        if quantity == 1:
            variation["solution"] = [
                [
                    "1/3",
                    f"Find the cost for 1kg of {selected_item[0]}. Multiply the price per kilogram by the number of kilograms."
                ],
                [
                    "2/3",
                    f"{selected_item[1]:.2f} x 1 = {total:.2f} dollars"
                ],
                [
                    "3/3",
                    f"The total cost for 1kg of {selected_item[0]} is {total:.2f} dollars."
                ]
            ]
        else:
            variation["solution"] = [
                [
                    "1/3",
                    f"Find the cost for {quantity}kg of {selected_item[0]}. Multiply the price per kilogram by the number of kilograms."
                ],
                [
                    "2/3",
                    f"{selected_item[1]:.2f} x {quantity} = {total:.2f} dollars"
                ],
                [
                    "3/3",
                    f"The total cost for {quantity}kg of {selected_item[0]} is {total:.2f} dollars."
                ]
            ]

        # Update question number
        variation["question_number"] = f"2_{variation_num}"

        # Update image tag
        variation["image_tag"] = f"Gr7_8_2_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_8_E2 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_8_E2")

if __name__ == "__main__":
    generate_variations()