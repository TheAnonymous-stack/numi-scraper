import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_8_E3 (multi-step-problems-with-percents)"""

    # Load template
    with open('Gr7_8_E3_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    # Define items and scenarios with pop culture themes
    items = [
        ("beach umbrella", 50), ("gaming headset", 80), ("anime figurine", 120), ("bluetooth speaker", 60),
        ("LED strip lights", 40), ("phone case", 30), ("wireless mouse", 45), ("manga volume", 15),
        ("K-pop album", 35), ("cosplay wig", 25), ("streaming microphone", 75), ("ring light", 55),
        ("tablet stand", 20), ("mechanical keyboard", 90), ("Pokemon plush", 28), ("vinyl record", 32),
        ("skateboard", 65), ("smart watch band", 18), ("portable charger", 38), ("webcam", 48),
        ("gaming chair cushion", 42), ("anime poster", 12), ("Funko Pop figure", 16), ("Nintendo game", 60),
        ("Marvel t-shirt", 22), ("Star Wars mug", 14), ("Harry Potter wand", 36), ("Stranger Things hoodie", 45)
    ]

    # Character names from pop culture
    names = ["Nathan", "Sakura", "Ethan", "Luna", "Alex", "Mia", "Tyler", "Emma", "Liam", "Zoe",
             "Mason", "Ava", "Ryan", "Chloe", "Jake", "Sophie", "Max", "Riley", "Oliver", "Grace"]

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Select random item and name
        item_name, original_price = random.choice(items)
        buyer_name = random.choice(names)

        # Random discount (10% to 60% in increments of 5)
        discount_percent = random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])

        # Random tax (5% to 15%)
        tax_percent = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        # Calculate values
        discount_decimal = discount_percent / 100
        discount_amount = original_price * discount_decimal
        discounted_price = original_price - discount_amount

        tax_decimal = tax_percent / 100
        tax_amount = discounted_price * tax_decimal
        total_price = discounted_price + tax_amount

        # Create variation
        variation = copy.deepcopy(template)

        # Update question text
        article = "an" if item_name[0].lower() in ['a', 'e', 'i', 'o', 'u'] else "a"
        variation["question_text"] = f"{article.capitalize()} {item_name} was originally priced at {original_price} dollars but went on sale for {discount_percent}% off. If {buyer_name} bought the {item_name} and paid {tax_percent}% sales tax, how much did {buyer_name.split()[0] if ' ' in buyer_name else 'they'} pay in total?\n"

        # Update correct answers
        if total_price == int(total_price):
            variation["correct_answers"] = [
                [f"{int(total_price)}"],
                [f"{int(total_price)} dollars"]
            ]
        else:
            variation["correct_answers"] = [
                [f"{total_price:.2f}"],
                [f"{total_price:.2f} dollars"]
            ]

        # Update solution image tags
        variation["solution_image_tag"] = [
            [
                "1/4",
                f"Gr7_8_3_{variation_num}_step_1",
                f"Shows finding the discount price: original price x discount = {original_price} dollars x {discount_decimal:.2f} = {discount_amount:.2f} dollars. Then subtracting from original: {original_price} dollars - {discount_amount:.2f} dollars = {discounted_price:.2f} dollars."
            ],
            [
                "2/4",
                f"Gr7_8_3_{variation_num}_step_2",
                f"Shows calculating the tax: {discounted_price:.2f} dollars x {tax_decimal:.2f} = {tax_amount:.2f} dollars. The {tax_percent}% tax rate is converted to decimal form ({tax_decimal:.2f}) for calculation."
            ],
            [
                "3/4",
                f"Gr7_8_3_{variation_num}_step_3",
                f"Shows the final calculation: discounted price + tax = {discounted_price:.2f} dollars + {tax_amount:.2f} dollars = {total_price:.2f} dollars. This gives the total amount {buyer_name} paid."
            ]
        ]

        # Update solution text
        variation["solution"] = [
            [
                "1/4",
                f"First find the discount price. Write {discount_percent}% as the decimal {discount_decimal:.2f} before using it in the equation."
            ],
            [
                "2/4",
                f"Now find the tax. Write {tax_percent}% as the decimal {tax_decimal:.2f} before using it in the equation."
            ],
            [
                "3/4",
                "Finally, find the total cost."
            ],
            [
                "4/4",
                f"The total for the {item_name} cost was {int(total_price) if total_price == int(total_price) else f'{total_price:.2f}'} dollars."
            ]
        ]

        # Update question number
        variation["question_number"] = f"3_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_8_E3 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_8_E3")

if __name__ == "__main__":
    generate_variations()