import json
import random

def generate_gr7_8_e2_variations():
    """Generate varied unit price questions for Gr7_8_E2"""

    with open('Gr7_8_E2_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Different items and prices per unit
    scenarios = [
        # Food items (per kg)
        {"item": "chicken chili", "price": 0.72, "unit": "kilogram", "quantity": [1, 2, 3, 4, 5]},
        {"item": "vegetable soup", "price": 0.63, "unit": "kilogram", "quantity": [2, 3, 4, 5, 6]},
        {"item": "tortilla soup", "price": 0.63, "unit": "kilogram", "quantity": [3, 4, 5, 6, 7]},
        {"item": "lobster bisque", "price": 1.04, "unit": "kilogram", "quantity": [1, 2, 3, 4, 5]},
        {"item": "tomato soup", "price": 0.85, "unit": "kilogram", "quantity": [2, 3, 4, 5, 6]},

        # Fruits (per pound)
        {"item": "apples", "price": 1.29, "unit": "pound", "quantity": [2, 3, 4, 5, 6]},
        {"item": "oranges", "price": 0.99, "unit": "pound", "quantity": [3, 4, 5, 6, 7]},
        {"item": "bananas", "price": 0.59, "unit": "pound", "quantity": [4, 5, 6, 7, 8]},
        {"item": "grapes", "price": 2.49, "unit": "pound", "quantity": [1, 2, 3, 4, 5]},
        {"item": "strawberries", "price": 3.99, "unit": "pound", "quantity": [1, 2, 3, 4]},

        # School supplies (per item)
        {"item": "notebooks", "price": 2.75, "unit": "item", "quantity": [3, 4, 5, 6, 7]},
        {"item": "pencils", "price": 0.45, "unit": "item", "quantity": [10, 12, 15, 20, 24]},
        {"item": "erasers", "price": 0.89, "unit": "item", "quantity": [4, 5, 6, 8, 10]},
        {"item": "folders", "price": 1.25, "unit": "item", "quantity": [5, 6, 8, 10, 12]},
        {"item": "markers", "price": 3.50, "unit": "box", "quantity": [2, 3, 4, 5, 6]}
    ]

    for i in range(51):
        scenario = scenarios[i % len(scenarios)]
        qty = scenario["quantity"][i % len(scenario["quantity"])]
        total = round(scenario["price"] * qty, 2)

        unit_text = scenario["unit"] + ("s" if qty > 1 and scenario["unit"] != "item" else "")
        if scenario["unit"] == "item":
            unit_text = ""

        question = {
            "skills": "unit-prices-find-the-total-price",
            "question_text": f"What is the total cost for {qty} {unit_text} {'of ' if unit_text else ''}{scenario['item']}?\n\n Do not round your answer.\n",
            "image_tag": f"Gr7_8_2_{i+1}",
            "backend_description": f"A price list table showing prices: {scenario['item']} ({scenario['price']} dollars/{scenario['unit']}). The table clearly displays unit prices.",
            "question_type": "Fill in the blank",
            "has_alternative_answers": True,
            "correct_answers": [
                str(total),
                f"{total} dollars"
            ],
            "solution": [
                ["1/3", f"Find the cost for {qty} {unit_text} {'of ' if unit_text else ''}{scenario['item']}. Multiply the price per {scenario['unit']} by the number of {scenario['unit']}s."],
                ["2/3", f"{scenario['price']} x {qty} = {total} dollars"],
                ["3/3", f"The total cost for {qty} {unit_text} {'of ' if unit_text else ''}{scenario['item']} is {total} dollars."]
            ],
            "tag": "Gr7_8_E2",
            "question_number": f"2_{i+1}",
            "solution_image_tag": []
        }
        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_8_E2_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied unit price questions for Gr7_8_E2")

def generate_gr7_8_e3_variations():
    """Generate varied percent discount and tax questions for Gr7_8_E3"""

    with open('Gr7_8_E3_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Different scenarios with items, original prices, discounts, and tax rates
    scenarios = [
        {"item": "beach umbrella", "price": 50, "discount": 50, "tax": 12},
        {"item": "winter jacket", "price": 80, "discount": 25, "tax": 10},
        {"item": "bicycle", "price": 200, "discount": 30, "tax": 8},
        {"item": "television", "price": 500, "discount": 20, "tax": 9},
        {"item": "laptop", "price": 800, "discount": 15, "tax": 11},
        {"item": "running shoes", "price": 60, "discount": 40, "tax": 7},
        {"item": "backpack", "price": 45, "discount": 35, "tax": 8.5},
        {"item": "watch", "price": 120, "discount": 25, "tax": 9.5},
        {"item": "camera", "price": 350, "discount": 30, "tax": 10.5},
        {"item": "headphones", "price": 90, "discount": 20, "tax": 6},
        {"item": "skateboard", "price": 75, "discount": 45, "tax": 7.5},
        {"item": "tennis racket", "price": 150, "discount": 40, "tax": 8},
        {"item": "gaming console", "price": 400, "discount": 25, "tax": 12},
        {"item": "tablet", "price": 300, "discount": 35, "tax": 9},
        {"item": "desk chair", "price": 180, "discount": 30, "tax": 10}
    ]

    for i in range(51):
        scenario = scenarios[i % len(scenarios)]

        # Calculate discount price
        discount_amount = scenario["price"] * (scenario["discount"] / 100)
        sale_price = scenario["price"] - discount_amount

        # Calculate tax
        tax_amount = sale_price * (scenario["tax"] / 100)

        # Total price
        total = round(sale_price + tax_amount, 2)

        question = {
            "skills": "multi-step-problems-with-percents",
            "question_text": f"A {scenario['item']} was originally priced at {scenario['price']} dollars but went on sale for {scenario['discount']}% off. If you bought the {scenario['item']} and paid {scenario['tax']}% sales tax, how much did you pay in total?\n",
            "question_type": "Fill in the blank",
            "has_alternative_answers": True,
            "correct_answers": [
                str(int(total) if total == int(total) else total),
                f"{int(total) if total == int(total) else total} dollars"
            ],
            "solution_image_tag": [],
            "solution": [
                ["1/4", f"First find the discount price. Write {scenario['discount']}% as the decimal {scenario['discount']/100:.2f} before using it in the equation."],
                ["2/4", f"Discount amount: {scenario['price']} × {scenario['discount']/100:.2f} = {discount_amount:.2f} dollars. Sale price: {scenario['price']} - {discount_amount:.2f} = {sale_price:.2f} dollars."],
                ["3/4", f"Now find the tax. Write {scenario['tax']}% as the decimal {scenario['tax']/100:.2f}. Tax amount: {sale_price:.2f} × {scenario['tax']/100:.2f} = {tax_amount:.2f} dollars."],
                ["4/4", f"Total cost: {sale_price:.2f} + {tax_amount:.2f} = {total} dollars."]
            ],
            "tag": "Gr7_8_E3",
            "question_number": f"3_{i+1}"
        }
        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_8_E3_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied percent discount and tax questions for Gr7_8_E3")

def generate_gr7_8_e4_variations():
    """Generate varied multi-step word problems for Gr7_8_E4"""

    with open('Gr7_8_E4_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Different restaurant/shopping scenarios
    scenarios = [
        {
            "context": "Rob and Joey went to lunch at a cafe",
            "items": [
                ("spinach salad", 6.60),
                ("tuna sandwich", 6.55),
                ("2 glasses of lemonade", 3.20)
            ],
            "tax": 1.65,
            "paid": 20.00
        },
        {
            "context": "Sarah and Mike went to dinner",
            "items": [
                ("pizza", 12.99),
                ("pasta", 9.75),
                ("2 sodas", 4.50)
            ],
            "tax": 2.45,
            "paid": 35.00
        },
        {
            "context": "Amy bought school supplies",
            "items": [
                ("3 notebooks", 8.25),
                ("pack of pens", 4.50),
                ("calculator", 15.99)
            ],
            "tax": 2.30,
            "paid": 35.00
        },
        {
            "context": "Tom and Lisa went to the movies",
            "items": [
                ("2 movie tickets", 24.00),
                ("large popcorn", 7.50),
                ("2 drinks", 6.00)
            ],
            "tax": 3.00,
            "paid": 45.00
        },
        {
            "context": "Emma bought groceries",
            "items": [
                ("milk", 3.99),
                ("bread", 2.50),
                ("dozen eggs", 4.25),
                ("cheese", 5.75)
            ],
            "tax": 1.32,
            "paid": 20.00
        },
        {
            "context": "Jake went to the bookstore",
            "items": [
                ("novel", 14.99),
                ("magazine", 5.50),
                ("bookmark", 2.25)
            ],
            "tax": 1.82,
            "paid": 30.00
        },
        {
            "context": "Maria and Carlos had breakfast",
            "items": [
                ("2 pancake plates", 13.90),
                ("orange juice", 3.50),
                ("coffee", 2.75)
            ],
            "tax": 1.61,
            "paid": 25.00
        },
        {
            "context": "Ben bought sports equipment",
            "items": [
                ("basketball", 22.50),
                ("water bottle", 8.99),
                ("sweatband", 4.25)
            ],
            "tax": 2.86,
            "paid": 40.00
        },
        {
            "context": "Nina went to the craft store",
            "items": [
                ("paint set", 16.75),
                ("brushes", 7.50),
                ("canvas", 12.00)
            ],
            "tax": 2.90,
            "paid": 45.00
        },
        {
            "context": "Alex and Sam bought snacks",
            "items": [
                ("chips", 3.50),
                ("cookies", 4.25),
                ("2 candy bars", 3.00),
                ("soda", 2.00)
            ],
            "tax": 1.02,
            "paid": 15.00
        }
    ]

    for i in range(51):
        scenario = scenarios[i % len(scenarios)]

        # Calculate subtotal
        subtotal = sum(price for _, price in scenario["items"])

        # Add tax
        total_with_tax = round(subtotal + scenario["tax"], 2)

        # Calculate change
        change = round(scenario["paid"] - total_with_tax, 2)

        # Format items list for question text
        items_text = ""
        for j, (item, price) in enumerate(scenario["items"]):
            if j == len(scenario["items"]) - 1 and j > 0:
                items_text += f", and {item} for {price:.2f} dollars"
            elif j == 0:
                items_text += f"{item} for {price:.2f} dollars"
            else:
                items_text += f", {item} for {price:.2f} dollars"

        question = {
            "skills": "multi-step-word-problems",
            "question_text": f"{scenario['context']}. They ordered {items_text}. The tax was {scenario['tax']:.2f} dollars. They gave the cashier {scenario['paid']:.2f} dollars.\n\nHow much change should they have received?\n",
            "question_type": "Fill in the blank",
            "has_alternative_answers": True,
            "correct_answers": [
                str(int(change) if change == int(change) else change),
                f"{change:.1f}",
                f"{change:.2f}"
            ],
            "solution_image_tag": [],
            "solution": [
                ["1/3", f"First, find the cost of the items.\n\n{' + '.join([f'{price:.2f}' for _, price in scenario['items']])} = {subtotal:.2f} dollars."],
                ["2/3", f"Now find the total cost including the tax.\n\n{subtotal:.2f} + {scenario['tax']:.2f} = {total_with_tax:.2f} dollars"],
                ["3/3", f"Subtract the total cost including the tax from the amount they paid to find the change:\n\n{scenario['paid']:.2f} − {total_with_tax:.2f} = {change:.2f} dollars.\n"]
            ],
            "tag": "Gr7_8_E4",
            "question_number": f"4_{i+1}"
        }
        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_8_E4_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied multi-step word problems for Gr7_8_E4")

# Run all three generators
generate_gr7_8_e2_variations()
generate_gr7_8_e3_variations()
generate_gr7_8_e4_variations()
print("\nSuccessfully generated variations for Gr7_8_E2, Gr7_8_E3, and Gr7_8_E4!")