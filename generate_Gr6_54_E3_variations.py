import json
import random
import copy

def load_templates():
    """Load template questions from file2.json"""
    with open('file2.json', 'r') as f:
        data = json.load(f)
    
    # Filter for Gr6_54_E3 questions
    templates = [q for q in data if q.get('tag') == 'Gr6_54_E3']
    return templates

def get_budget_scenarios():
    """Generate diverse budget scenarios with pop culture themes"""
    scenarios = [
        # Gaming themed
        ("Kai", [
            ("Tournament winnings", 180),
            ("Streaming donations", 250),
            ("Game testing", 45)
        ], [
            ("Gaming headset", None),
            ("Internet bill", 85),
            ("Energy drinks", 25)
        ]),
        
        # Anime themed
        ("Sakura", [
            ("Manga translation", 200),
            ("Convention booth sales", 320),
            ("Art commissions", 55)
        ], [
            ("Cosplay materials", None),
            ("Convention tickets", 120),
            ("Shipping fees", 30)
        ]),
        
        # Sports themed
        ("Jordan", [
            ("Coaching youth basketball", 240),
            ("Sports camp counselor", 380),
            ("Equipment sales", 30)
        ], [
            ("New basketball shoes", None),
            ("Gym membership", 95),
            ("Protein supplements", 45)
        ]),
        
        # Music themed
        ("Melody", [
            ("Guitar lessons", 280),
            ("Band performance", 150),
            ("Music store job", 95)
        ], [
            ("Recording studio time", None),
            ("Guitar strings", 65),
            ("Concert tickets", 80)
        ]),
        
        # Tech themed
        ("Alex", [
            ("App development", 450),
            ("Tech support", 220),
            ("YouTube revenue", 85)
        ], [
            ("Software subscription", None),
            ("Cloud storage", 120),
            ("Hardware upgrades", 95)
        ]),
        
        # Art themed
        ("Luna", [
            ("Portrait commissions", 340),
            ("Art class teaching", 180),
            ("Gallery sales", 125)
        ], [
            ("Art supplies", None),
            ("Studio rent", 150),
            ("Frame materials", 75)
        ]),
        
        # Food/cooking themed
        ("Chef Marco", [
            ("Catering events", 420),
            ("Cooking classes", 260),
            ("Food blog ads", 45)
        ], [
            ("Kitchen equipment", None),
            ("Ingredient costs", 180),
            ("Food truck permit", 85)
        ]),
        
        # Fashion themed
        ("Zara", [
            ("Fashion blog sponsorship", 380),
            ("Personal styling", 290),
            ("Clothing resale", 55)
        ], [
            ("Fabric and materials", None),
            ("Sewing machine payment", 110),
            ("Fashion magazine subscription", 35)
        ]),
        
        # Pet care themed
        ("Bailey", [
            ("Dog walking", 195),
            ("Pet sitting", 320),
            ("Grooming assistant", 60)
        ], [
            ("Pet supplies", None),
            ("Vet assistant course", 140),
            ("Transportation", 45)
        ]),
        
        # Environmental themed
        ("River", [
            ("Recycling collection", 165),
            ("Community garden sales", 240),
            ("Eco-blog writing", 70)
        ], [
            ("Composting equipment", None),
            ("Seeds and tools", 95),
            ("Environmental conference", 55)
        ])
    ]
    return scenarios

def create_budget_variation(template, variation_num, scenario):
    """Create a variation for budget balancing questions"""
    variation = copy.deepcopy(template)
    
    # Update question_number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{variation_num}"
    
    # Get scenario details
    name, income_items, expense_items = scenario
    
    # Randomize amounts slightly
    income_total = 0
    income_list = []
    for desc, base_amount in income_items:
        amount = base_amount + random.choice([-10, -5, 0, 5, 10])
        income_list.append((desc, amount))
        income_total += amount
    
    # Calculate expenses (leaving one blank for the question)
    expense_total = income_total  # For balanced budget
    known_expenses = 0
    expense_list = []
    
    for i, (desc, _) in enumerate(expense_items):
        if i == 0:  # This will be the blank to fill
            expense_list.append((desc, None))
        else:
            amount = expense_items[i][1] + random.choice([-5, 0, 5])
            expense_list.append((desc, amount))
            known_expenses += amount
    
    # Calculate the answer (amount for the blank item)
    answer = expense_total - known_expenses
    
    # Select month
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    month = random.choice(months)
    
    # Create question text
    variation['question_text'] = (
        f"This table shows {name}'s {month} budget. How much money can {name} spend on "
        f"{expense_list[0][0].lower()} to keep the budget balanced? Complete the table."
    )
    
    # Update image tag
    variation['image_tag'] = f"Gr6_54_3_{variation_num}"
    
    # Create backend description
    income_desc = ", ".join([f"'{desc}: ${amt}'" for desc, amt in income_list])
    expense_desc = ", ".join([
        f"'{desc}{',' if desc != expense_list[0][0] else ': [blank],'}" + 
        (f" '${amt}'" if amt else "") 
        for desc, amt in expense_list
    ])
    
    variation['backend_description'] = (
        f"This image shows a table titled '{name}'s {month} budget.' The table is divided into two main columns: "
        f"the 'Income' column on the left and the 'Expenses' column on the right. "
        f"Under the Income column, there are three sources listed: {income_desc}. "
        f"The Total row at the bottom of this column is currently left blank. "
        f"In the Expenses column, there are three listed items: {expense_desc}. "
        f"The Total row for expenses is also left blank, indicating that the budget still needs to be completed."
    )
    
    # Set correct answers
    variation['correct_answers'] = [str(answer), str(income_total), str(expense_total)]
    
    # Update solution image tags
    variation['solution_image_tag'] = [
        ["3/9", f"Gr6_54_3_{variation_num}_step_3", 
         f"This image shows the same table as in Gr6_54_3_{variation_num}, but with the total income filled in as ${income_total}, "
         f"and the total income of ${income_total} is highlighted in pink."],
        ["4/9", f"Gr6_54_3_{variation_num}_step_4",
         f"This image shows the same table as in Gr6_54_3_{variation_num}_step_3, but with the total expenses filled in as ${expense_total}, "
         f"and the total expenses of ${expense_total} is highlighted in pink."],
        ["9/9", f"Gr6_54_3_{variation_num}_step_9",
         f"This image shows the same table as in Gr6_54_3_{variation_num}_step_4, but with the {expense_list[0][0].lower()} amount "
         f"filled in as ${answer}, and the {expense_list[0][0].lower()} amount of ${answer} is highlighted in pink."]
    ]
    
    # Generate solution steps
    solution = [
        ["1/9", f"First, add to find {name}'s total income."],
        ["2/9", f"${income_list[0][1]} + ${income_list[1][1]} + ${income_list[2][1]} = ${income_total}"],
        ["3/9", f"The total income is ${income_total}. Put this number in the table."],
        ["4/9", f"Next, find the total expenses. In a balanced budget, the total income equals the total expenses. So, put ${expense_total} for the total expenses."],
        ["5/9", f"Finally, find how much money {name} can spend on {expense_list[0][0].lower()}. The expenses need to add up to ${expense_total}."],
        ["6/9", f"Start by adding the known expenses.\n${expense_list[1][1]} + ${expense_list[2][1]} = ${known_expenses}"],
        ["7/9", f"Now, find how much more money can be spent on {expense_list[0][0].lower()}."],
        ["8/9", f"Subtract.\n${expense_total} - ${known_expenses} = ${answer}"],
        ["9/9", f"{name} can spend ${answer} on {expense_list[0][0].lower()} to keep the budget balanced."]
    ]
    
    variation['solution'] = solution
    
    return variation

def generate_variations():
    """Generate all variations for Gr6_54_E3"""
    templates = load_templates()
    scenarios = get_budget_scenarios()
    variations = []
    
    # We have 1 template question, need 51 total (including template)
    # So we need 50 additional variations
    variations_needed = 50
    
    # Generate variations
    for i in range(variations_needed):
        # Cycle through scenarios to ensure variety
        scenario = scenarios[i % len(scenarios)]
        
        # Add some randomization to the scenario
        if i >= len(scenarios):
            # Modify the scenario slightly for additional variations
            name, income, expenses = scenario
            # Add variation to the numbers
            modified_income = [(desc, amt + random.choice([-20, -10, 10, 20])) for desc, amt in income]
            modified_expenses = [(desc, amt + random.choice([-10, -5, 5, 10]) if amt else None) for desc, amt in expenses]
            scenario = (name, modified_income, modified_expenses)
        
        variation = create_budget_variation(templates[0], i + 2, scenario)  # Start at 2 since template is 3_1
        variations.append(variation)
    
    # Save variations to file
    with open('Gr6_54_E3_variations.json', 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_54_E3")
    print(f"Total questions (including template): {len(templates) + len(variations)}")

if __name__ == "__main__":
    generate_variations()