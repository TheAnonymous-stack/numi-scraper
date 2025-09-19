import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_8_E4 (multi-step-word-problems)"""

    # Load template
    with open('Gr7_8_E4_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    # Restaurant scenarios with pop culture themes
    restaurants = ["anime cafe", "K-pop themed restaurant", "Marvel Diner", "Pokemon Cafe",
                  "Gaming Lounge", "Star Wars Cantina", "Hogwarts Kitchen", "Studio Ghibli Cafe"]

    # Names from pop culture
    names_pairs = [
        ("Rob", "Joey"), ("Naruto", "Sasuke"), ("Harry", "Ron"), ("Peter", "MJ"),
        ("Ash", "Misty"), ("Eren", "Mikasa"), ("Luke", "Leia"), ("Tony", "Steve"),
        ("Deku", "Bakugo"), ("Goku", "Vegeta"), ("Hermione", "Luna"), ("Thor", "Loki")
    ]

    # Food items
    food_items = [
        ("spinach salad", 6.60, 8.50), ("tuna sandwich", 6.55, 9.25), ("chicken wrap", 7.20, 10.50),
        ("veggie burger", 8.40, 11.00), ("caesar salad", 7.95, 10.25), ("grilled cheese", 5.50, 7.80),
        ("fish tacos", 9.85, 12.50), ("pasta bowl", 10.20, 13.75), ("pizza slice", 4.50, 6.25),
        ("ramen bowl", 11.50, 14.00), ("sushi roll", 8.75, 12.00), ("bento box", 12.30, 15.50)
    ]

    drinks = [
        ("lemonade", 1.60, 3.50), ("iced tea", 2.20, 3.75), ("soda", 2.50, 4.00),
        ("smoothie", 4.80, 6.50), ("coffee", 2.85, 4.25), ("juice", 3.20, 5.00),
        ("milkshake", 5.50, 7.25), ("bubble tea", 4.95, 6.80)
    ]

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Select random elements
        name1, name2 = random.choice(names_pairs)
        restaurant = random.choice(restaurants)

        # Select 2 food items and 1-2 drinks
        selected_foods = random.sample(food_items, 2)
        selected_drink = random.choice(drinks)
        drink_count = random.choice([2, 3])  # Number of drinks

        # Generate prices (using min and max ranges)
        food1_price = round(random.uniform(selected_foods[0][1], selected_foods[0][2]), 2)
        food2_price = round(random.uniform(selected_foods[1][1], selected_foods[1][2]), 2)
        drink_price = round(random.uniform(selected_drink[1], selected_drink[2]), 2)

        # Calculate totals
        food_cost = food1_price + food2_price + (drink_price * drink_count)
        tax = round(random.uniform(0.50, 3.00), 2)
        total_with_tax = round(food_cost + tax, 2)

        # Amount paid (ensure change is reasonable)
        paid_amounts = [20.00, 25.00, 30.00, 40.00, 50.00]
        valid_amounts = [amt for amt in paid_amounts if amt > total_with_tax]
        if not valid_amounts:
            continue
        amount_paid = random.choice(valid_amounts)
        change = round(amount_paid - total_with_tax, 2)

        # Create variation
        variation = copy.deepcopy(template)

        # Update question text
        article = "an" if restaurant[0].lower() in ['a', 'e', 'i', 'o', 'u'] else "a"
        variation["question_text"] = f"{name1} and {name2} went to lunch at {article} {restaurant}. They ordered a {selected_foods[0][0]} for {food1_price:.2f} dollars, a {selected_foods[1][0]} for {food2_price:.2f} dollars, and {drink_count} glasses of {selected_drink[0]} for {drink_price:.2f} dollars each. The tax was {tax:.2f} dollars. They gave the waiter {amount_paid:.2f} dollars.\n\nHow much change should they have received?\n"

        # Update correct answers
        change_str = f"{change:.2f}".rstrip('0').rstrip('.')
        answers = [[change_str]]
        if '.' in change_str:
            if len(change_str.split('.')[1]) == 1:
                answers.append([f"{change:.1f}"])
            answers.append([f"{change:.2f}"])
        else:
            answers.extend([[f"{change:.1f}"], [f"{change:.2f}"]])

        variation["correct_answers"] = answers

        # Update solution image tag
        variation["solution_image_tag"] = [
            [
                "3/3",
                f"Gr7_8_4_{variation_num}_step_3",
                f"Shows the complete solution with three steps clearly labeled. Step 1 calculates food cost ({food_cost:.2f} dollars), Step 2 adds tax ({total_with_tax:.2f} dollars), and Step 3 finds the change from {amount_paid:.2f} dollars ({change:.2f} dollars)."
            ]
        ]

        # Update solution
        if drink_count == 2:
            drink_calc = f"{food1_price:.2f} + {food2_price:.2f} + {drink_price:.2f} + {drink_price:.2f}"
        else:
            drink_calc = f"{food1_price:.2f} + {food2_price:.2f} + " + " + ".join([f"{drink_price:.2f}"] * drink_count)

        variation["solution"] = [
            [
                "1/3",
                f"First, find the cost of the food.\n\n{drink_calc} = {food_cost:.2f} dollars."
            ],
            [
                "2/3",
                f"Now find the total cost including the tax.\n\n{food_cost:.2f} + {tax:.2f} = {total_with_tax:.2f} dollars"
            ],
            [
                "3/3",
                f"Subtract the total cost including the tax from the amount they paid to find the change:\n\n{amount_paid:.2f} − {total_with_tax:.2f} = {change:.2f} dollars.\n"
            ]
        ]

        # Update question number
        variation["question_number"] = f"4_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_8_E4 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_8_E4")

if __name__ == "__main__":
    generate_variations()