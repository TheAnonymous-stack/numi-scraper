import json
import random
import copy

def load_templates():
    """Load template questions from file2.json"""
    with open('file2.json', 'r') as f:
        data = json.load(f)
    
    # Filter for Gr6_55_E1 questions
    templates = [q for q in data if q.get('tag') == 'Gr6_55_E1']
    return templates

def get_budget_adjustment_scenarios():
    """Generate diverse budget adjustment scenarios with pop culture themes"""
    scenarios = [
        # Gaming themed
        ("Ethan", [
            ("Twitch streaming", 45),
            ("Tournament prize", 30),
            ("Game reviews", 75)
        ], [
            ("Gaming mouse", 40),
            ("Steam games", 55),
            ("Discord Nitro", 70)
        ], [
            ("speedrun another game for prize money", 15),
            ("sell old gaming peripherals", 20),
            ("take on sponsored content", 25),
            ("reduce Steam purchases", 10)
        ]),
        
        # Anime/manga themed
        ("Yuki", [
            ("Manga cafe job", 55),
            ("Cosplay photoshoot", 35),
            ("Fan art sales", 80)
        ], [
            ("Anime figures", 65),
            ("Crunchyroll subscription", 48),
            ("Convention tickets", 75)
        ], [
            ("sell custom keychains at convention", 18),
            ("take more photoshoot bookings", 22),
            ("do character voice acting gigs", 20),
            ("skip one convention this season", 15)
        ]),
        
        # Music themed
        ("Jazz", [
            ("Street performing", 40),
            ("Music lessons given", 65),
            ("Band gig", 55)
        ], [
            ("Guitar picks and strings", 35),
            ("Recording software", 85),
            ("Concert tickets", 60)
        ], [
            ("perform at local coffee shop", 20),
            ("sell beats online", 25),
            ("teach additional students", 30),
            ("use free recording software", 15)
        ]),
        
        # Sports/fitness themed
        ("Maya", [
            ("Yoga instruction", 70),
            ("Fitness blog ads", 25),
            ("Marathon prize", 45)
        ], [
            ("Protein powder", 50),
            ("Gym membership", 65),
            ("Running shoes", 40)
        ], [
            ("lead morning boot camps", 15),
            ("create workout plans to sell", 18),
            ("coach running club", 22),
            ("buy shoes next month", 12)
        ]),
        
        # Art/creative themed
        ("Phoenix", [
            ("Digital commissions", 85),
            ("Art supply store job", 40),
            ("Print sales", 30)
        ], [
            ("iPad Pro payment", 75),
            ("Art supplies", 45),
            ("Online course", 55)
        ], [
            ("take rush commissions", 20),
            ("sell sticker designs", 15),
            ("offer art tutorials", 25),
            ("use library resources", 10)
        ]),
        
        # Tech/coding themed
        ("Binary", [
            ("Freelance coding", 95),
            ("Bug bounty", 50),
            ("Tech tutoring", 35)
        ], [
            ("Cloud hosting", 60),
            ("Development tools", 70),
            ("Tech conference", 65)
        ], [
            ("build websites for local businesses", 15),
            ("contribute to open source for sponsorship", 18),
            ("create coding course", 25),
            ("attend virtual conference instead", 20)
        ]),
        
        # Food/cooking themed
        ("Saffron", [
            ("Bake sale profits", 45),
            ("Recipe blog revenue", 38),
            ("Cooking demos", 62)
        ], [
            ("Kitchen gadgets", 55),
            ("Specialty ingredients", 48),
            ("Cookbook collection", 58)
        ], [
            ("cater small parties", 16),
            ("sell homemade spice blends", 20),
            ("teach cooking classes", 22),
            ("borrow cookbooks from library", 12)
        ]),
        
        # Fashion themed
        ("Vogue", [
            ("Thrift flip sales", 58),
            ("Fashion blog sponsorship", 42),
            ("Personal styling", 70)
        ], [
            ("Fabric and notions", 65),
            ("Fashion week tickets", 80),
            ("Sewing machine repair", 45)
        ], [
            ("alter clothes for clients", 20),
            ("sell vintage finds online", 18),
            ("host style workshops", 25),
            ("watch fashion week online", 15)
        ]),
        
        # Pet care themed
        ("Whiskers", [
            ("Dog walking", 48),
            ("Pet photography", 32),
            ("Pet sitting", 75)
        ], [
            ("Pet supplies inventory", 45),
            ("Grooming course", 68),
            ("Van maintenance", 62)
        ], [
            ("offer overnight pet sitting", 20),
            ("add cat sitting services", 15),
            ("create pet care packages", 18),
            ("postpone grooming course", 25)
        ]),
        
        # Environmental themed
        ("Terra", [
            ("Farmers market booth", 52),
            ("Composting service", 38),
            ("Eco-workshop teaching", 65)
        ], [
            ("Garden supplies", 48),
            ("Electric bike payment", 72),
            ("Sustainability conference", 55)
        ], [
            ("sell seedlings and plants", 20),
            ("expand composting route", 15),
            ("write eco-living ebook", 18),
            ("carpool to conference", 10)
        ])
    ]
    return scenarios

def create_budget_adjustment_variation(template, variation_num, scenario):
    """Create a variation for budget adjustment questions"""
    variation = copy.deepcopy(template)
    
    # Update question_number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{variation_num}"
    
    # Get scenario details
    name, income_items, expense_items, adjustment_options = scenario
    
    # Randomize amounts slightly
    income_list = []
    income_total = 0
    for desc, base_amount in income_items:
        amount = base_amount + random.choice([-5, -3, 0, 3, 5])
        income_list.append((desc, amount))
        income_total += amount
    
    # Make expenses exceed income
    expense_list = []
    expense_total = 0
    for desc, base_amount in expense_items:
        amount = base_amount + random.choice([-3, 0, 3, 5])
        expense_list.append((desc, amount))
        expense_total += amount
    
    # Ensure expenses exceed income
    if expense_total <= income_total:
        difference_needed = random.choice([15, 20, 25, 30])
        # Increase one expense to create imbalance
        expense_list[0] = (expense_list[0][0], expense_list[0][1] + difference_needed)
        expense_total += difference_needed
    
    deficit = expense_total - income_total
    
    # Select month
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    month = random.choice(months)
    
    # Create adjustment options (one correct, three incorrect)
    correct_option = random.choice(adjustment_options)
    correct_desc, correct_amount = correct_option
    
    # Ensure correct amount matches or exceeds deficit
    if correct_amount < deficit:
        correct_amount = deficit
    
    # Create incorrect options
    incorrect_options = []
    
    # Option that's too small
    small_amount = deficit - random.choice([5, 10, 15])
    if small_amount > 0:
        incorrect_options.append((f"earn ${small_amount} from a yard sale", small_amount))
    
    # Option that increases expenses
    incorrect_options.append((f"increase spending on {random.choice(expense_list)[0]} by ${random.choice([10, 15])}", -10))
    
    # Option that reduces income
    incorrect_options.append((f"work fewer hours to reduce income by ${random.choice([5, 10])}", -5))
    
    # Create choices
    choices = [
        correct_desc + f" to earn an extra ${correct_amount}",
        incorrect_options[0][0],
        incorrect_options[1][0],
        incorrect_options[2][0] if len(incorrect_options) > 2 else f"reduce spending on {expense_list[1][0]} by ${deficit//2}"
    ]
    
    # Shuffle and find correct answer
    random.shuffle(choices)
    correct_index = choices.index(correct_desc + f" to earn an extra ${correct_amount}")
    
    # Create question text
    variation['question_text'] = (
        f"This table shows {name}'s {month} budget.\n"
        f"What could {name} do to balance the budget?"
    )
    
    # Update image tag
    variation['image_tag'] = f"Gr6_55_1_{variation_num}"
    
    # Create backend description
    income_desc = ", ".join([f"'{desc}: ${amt}'" for desc, amt in income_list])
    expense_desc = ", ".join([f"'{desc}: ${amt}'" for desc, amt in expense_list])
    
    variation['backend_description'] = (
        f"This image shows a table titled '{name}'s {month} budget.' The table is divided into two main columns: "
        f"the 'Income' column on the left and the 'Expenses' column on the right. "
        f"Under the Income column, there are three sources listed: {income_desc}. "
        f"In the Expenses column, there are three listed items: {expense_desc}."
    )
    
    variation['choices'] = choices
    variation['correct_answers'] = [chr(65 + correct_index)]  # A, B, C, or D
    
    # Update solution image tags
    variation['solution_image_tag'] = [
        ["2/9", f"Gr6_55_1_{variation_num}_step_2",
         f"This image shows a visual breakdown of {name}'s total income for {month} using a horizontal addition equation. "
         f"The expression shows ${income_list[0][1]} + ${income_list[1][1]} + ${income_list[2][1]} = ${income_total}."],
        ["3/9", f"Gr6_55_1_{variation_num}_step_3",
         f"This image shows a visual breakdown of {name}'s total expenses for {month} using a horizontal addition equation. "
         f"The expression shows ${expense_list[0][1]} + ${expense_list[1][1]} + ${expense_list[2][1]} = ${expense_total}."]
    ]
    
    # Generate solution steps
    solution = [
        ["1/9", f"Step 1: Find how much money {name} needs to balance the budget."],
        ["2/9", f"First, add {name}'s sources of income to find the total income."],
        ["3/9", f"Next, add {name}'s expenses to find the total expenses."],
        ["4/9", f"{name}'s expenses are more than the income. Subtract to find the difference."],
        ["5/9", f"${expense_total} - ${income_total} = ${deficit}"],
        ["6/9", f"The difference is ${deficit}, so {name} needs an extra ${deficit} to balance the budget."],
        ["7/9", f"Step 2: Find the answer choice that gives {name} an extra ${deficit}."],
        ["8/9", f"Increasing income by ${correct_amount} will give {name} the extra money needed."],
        ["9/9", f"So, {name} can balance the budget by {correct_desc} to earn ${correct_amount}."]
    ]
    
    variation['solution'] = solution
    
    return variation

def generate_variations():
    """Generate all variations for Gr6_55_E1"""
    templates = load_templates()
    scenarios = get_budget_adjustment_scenarios()
    variations = []
    
    # We have 1 template question, need 51 total (including template)
    # So we need 50 additional variations
    variations_needed = 50
    
    # Generate variations
    for i in range(variations_needed):
        # Cycle through scenarios to ensure variety
        scenario_index = i % len(scenarios)
        scenario = scenarios[scenario_index]
        
        # Add more randomization for repeated scenarios
        if i >= len(scenarios):
            # Modify the scenario for additional variations
            name, income, expenses, adjustments = scenario
            
            # Randomize the amounts more
            factor = 1 + (i // len(scenarios)) * 0.1
            modified_income = [(desc, int(amt * factor) + random.choice([-10, -5, 0, 5, 10])) 
                              for desc, amt in income]
            modified_expenses = [(desc, int(amt * factor) + random.choice([-5, 0, 5, 10, 15])) 
                                for desc, amt in expenses]
            modified_adjustments = [(desc, int(amt * factor) + random.choice([0, 5, 10])) 
                                   for desc, amt in adjustments]
            
            scenario = (name, modified_income, modified_expenses, modified_adjustments)
        
        variation = create_budget_adjustment_variation(templates[0], i + 2, scenario)  # Start at 2 since template is 1_1
        variations.append(variation)
    
    # Save variations to file
    with open('Gr6_55_E1_variations.json', 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_55_E1")
    print(f"Total questions (including template): {len(templates) + len(variations)}")

if __name__ == "__main__":
    generate_variations()