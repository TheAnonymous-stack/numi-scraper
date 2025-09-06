import json
import random
import copy

def load_templates():
    """Load template questions from file2.json"""
    with open('file2.json', 'r') as f:
        data = json.load(f)
    
    # Filter for Gr6_54_E2 questions
    templates = [q for q in data if q.get('tag') == 'Gr6_54_E2']
    return templates

def get_savings_scenarios():
    """Generate diverse savings scenarios with pop culture themes"""
    scenarios = [
        # Gaming and tech
        ("Nintendo Switch", 350, "gaming console"),
        ("VR headset", 450, "virtual reality"),
        ("gaming laptop", 1200, "computer"),
        ("mechanical keyboard", 150, "gaming accessory"),
        ("graphics card", 600, "PC component"),
        
        # Anime and collectibles
        ("limited edition manga set", 280, "anime collection"),
        ("anime figure collection", 420, "collectibles"),
        ("cosplay materials", 380, "costume supplies"),
        ("convention weekend pass", 250, "event tickets"),
        ("rare Pokemon cards", 520, "trading cards"),
        
        # Sports and fitness
        ("mountain bike", 750, "sports equipment"),
        ("skateboard setup", 320, "sports gear"),
        ("tennis racket", 180, "sports equipment"),
        ("gym equipment", 450, "fitness gear"),
        ("running shoes", 160, "athletic wear"),
        
        # Music and arts
        ("electric guitar", 680, "musical instrument"),
        ("digital piano", 850, "musical instrument"),
        ("art supplies set", 220, "creative materials"),
        ("camera equipment", 920, "photography gear"),
        ("DJ controller", 450, "music equipment"),
        
        # Entertainment
        ("concert ticket package", 380, "entertainment"),
        ("theme park season pass", 450, "entertainment"),
        ("streaming service bundle", 240, "subscriptions"),
        ("movie theater gift cards", 200, "entertainment"),
        ("escape room party", 280, "group activity")
    ]
    return scenarios

def create_bank_comparison_variation(template, variation_num, scenario):
    """Create a variation for bank comparison questions"""
    variation = copy.deepcopy(template)
    
    # Update question_number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{variation_num}"
    
    item, base_amount, category = scenario
    
    # Generate random amounts and interest rates
    amount = random.choice([300, 400, 500, 600, 700, 800])
    
    # Create two banks with different interest rates and fees
    bank_names = [
        ("Starlight Bank", "Moonbeam Bank"),
        ("Crystal Bank", "Diamond Bank"),
        ("Thunder Bank", "Lightning Bank"),
        ("Phoenix Bank", "Dragon Bank"),
        ("Cosmic Bank", "Galaxy Bank"),
        ("Ninja Bank", "Samurai Bank"),
        ("Pixel Bank", "Digital Bank"),
        ("Fortune Bank", "Lucky Bank")
    ]
    
    bank1, bank2 = random.choice(bank_names)
    
    # Interest rates per $100
    rate1 = random.choice([2, 3, 4, 5])
    rate2 = random.choice([3, 4, 5, 6])
    
    # Fees
    fee1 = random.choice([0, 2, 4, 5])
    fee2 = random.choice([4, 6, 8, 10])
    
    # Calculate totals
    interest1 = (amount // 100) * rate1
    interest2 = (amount // 100) * rate2
    total1 = amount + interest1 - fee1
    total2 = amount + interest2 - fee2
    
    # Determine which bank is better
    better_bank = bank1 if total1 > total2 else bank2
    
    # Generate question text with theme
    character_names = ["Alex", "Maya", "Jordan", "Sam", "Casey", "Riley", "Morgan", "Avery"]
    character = random.choice(character_names)
    
    variation['question_text'] = (
        f"{character} has ${amount} and wants to deposit the money into a savings account for one year.\n"
        f"{bank1} pays ${rate1} interest each year for every $100 in a savings account.\n"
        f"{bank2} pays ${rate2} interest each year for every $100 in a savings account.\n"
        f"{bank2} charges a ${fee2} yearly fee on savings accounts.\n"
        f"Which bank has the better savings option for {character}?"
    )
    
    variation['choices'] = [bank1, bank2]
    variation['correct_answers'] = ["A" if better_bank == bank1 else "B"]
    
    # Generate solution steps
    solution = [
        ["1/13", f"Find which savings option gives {character} more money after one year."],
        ["2/13", f"Find how much money {character} will have with {bank1}."],
        ["3/13", f"{bank1} pays ${rate1} interest for every hundred dollars in a savings account. {character} has {amount // 100} hundred dollars."],
        ["4/13", f"Multiply ${rate1} by {amount // 100}.\n${rate1} × {amount // 100} = ${interest1}\n{bank1} will pay {character} ${interest1} interest."],
        ["5/13", f"Add ${interest1} interest to the ${amount} {character} has to start.\n${amount} + ${interest1} = ${total1}"],
        ["6/13", f"{character} will have ${total1} after one year if they keep their money at {bank1}."],
        ["7/13", f"Find how much money {character} will have with {bank2}."],
        ["8/13", f"{bank2} pays ${rate2} interest for every hundred dollars in a savings account. {character} has {amount // 100} hundred dollars."],
        ["9/13", f"Multiply ${rate2} by {amount // 100}.\n${rate2} × {amount // 100} = ${interest2}\n{bank2} will pay {character} ${interest2} interest."],
        ["10/13", f"Add ${interest2} interest to the ${amount} {character} has to start.\n${amount} + ${interest2} = ${amount + interest2}"],
        ["11/13", f"Now, subtract the ${fee2} yearly fee that {bank2} charges.\n${amount + interest2} - ${fee2} = ${total2}"],
        ["12/13", f"{character} will have ${total2} after one year if they keep their money at {bank2}."],
        ["13/13", f"Since ${total1 if better_bank == bank1 else total2} is more than ${total2 if better_bank == bank1 else total1}, {better_bank} has the better savings option for {character}."]
    ]
    
    variation['solution'] = solution
    
    return variation

def create_savings_plan_variation(template, variation_num, scenario):
    """Create a variation for savings plan comparison questions"""
    variation = copy.deepcopy(template)
    
    # Update question_number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{variation_num}"
    
    item, target_amount, category = scenario
    
    # Adjust target amount slightly
    target = target_amount + random.choice([-50, -30, -20, 0, 20, 30, 50])
    
    # Generate two savings plans
    weekly_save_a = random.choice([12, 13, 14, 15, 16, 17, 18])
    weeks_a = random.choice([18, 19, 20, 21, 22, 23])
    interest_a = random.choice([1, 2, 3, 4])
    
    weekly_save_b = random.choice([10, 11, 12, 13, 14, 15])
    weeks_b = random.choice([22, 23, 24, 25, 26, 27])
    interest_b = random.choice([3, 4, 5, 6, 7])
    
    # Calculate totals
    total_a = weekly_save_a * weeks_a + interest_a
    total_b = weekly_save_b * weeks_b + interest_b
    
    # Ensure one plan meets the target and one doesn't
    if total_a >= target and total_b >= target:
        # Adjust one to be below target
        if random.choice([True, False]):
            weekly_save_a -= 1
            total_a = weekly_save_a * weeks_a + interest_a
        else:
            weekly_save_b -= 1
            total_b = weekly_save_b * weeks_b + interest_b
    elif total_a < target and total_b < target:
        # Adjust one to be above target
        if random.choice([True, False]):
            weekly_save_a += 1
            total_a = weekly_save_a * weeks_a + interest_a
        else:
            weekly_save_b += 1
            total_b = weekly_save_b * weeks_b + interest_b
    
    correct_plan = "Plan A" if total_a >= target else "Plan B"
    
    # Generate character and brand names
    characters = ["Emma", "Liam", "Sophia", "Noah", "Olivia", "Ethan", "Ava", "Mason"]
    character = random.choice(characters)
    
    brands = ["Super Deluxe", "Ultra Pro", "Mega Elite", "Premium Plus", "Turbo Max", "Power Surge", "Lightning Strike", "Thunder Bolt"]
    brand = random.choice(brands)
    
    variation['question_text'] = (
        f"{character} wants to buy a {brand} {item}, but needs ${target}. They think of two plans to save this money.\n"
        f"Plan A: Save ${weekly_save_a} each week for {weeks_a} weeks. Put the money in a savings account that will pay a total of ${interest_a} in interest.\n"
        f"Plan B: Save ${weekly_save_b} each week for {weeks_b} weeks. Put the money in a savings account that will pay a total of ${interest_b} in interest.\n"
        f"Which plan should {character} follow to save enough money to buy the {item}?"
    )
    
    variation['choices'] = ["Plan A", "Plan B"]
    variation['correct_answers'] = ["A" if correct_plan == "Plan A" else "B"]
    
    # Generate solution
    solution = [
        ["1/10", f"{character} needs ${target} to buy the {item}. Find which plan will save enough money."],
        ["2/10", f"Find how much money {character} will save with Plan A.\nPlan A is to save ${weekly_save_a} each week for {weeks_a} weeks and earn ${interest_a} in interest."],
        ["3/10", f"First, multiply ${weekly_save_a} by {weeks_a}.\n${weekly_save_a} × {weeks_a} = ${weekly_save_a * weeks_a}"],
        ["4/10", f"Then, add ${interest_a} interest.\n${weekly_save_a * weeks_a} + ${interest_a} = ${total_a}"],
        ["5/10", f"{character} will save ${total_a} with Plan A. {'That is enough money' if total_a >= target else 'That is not enough money'} to buy the {item}."],
        ["6/10", f"Find how much money {character} will save with Plan B.\nPlan B is to save ${weekly_save_b} each week for {weeks_b} weeks and earn ${interest_b} in interest."],
        ["7/10", f"First, multiply ${weekly_save_b} by {weeks_b}.\n${weekly_save_b} × {weeks_b} = ${weekly_save_b * weeks_b}"],
        ["8/10", f"Then, add ${interest_b} interest.\n${weekly_save_b * weeks_b} + ${interest_b} = ${total_b}"],
        ["9/10", f"{character} will save ${total_b} with Plan B. {'That is enough money' if total_b >= target else 'That is not enough money'} to buy the {item}."],
        ["10/10", f"{character} should follow {correct_plan}."]
    ]
    
    variation['solution'] = solution
    
    return variation

def create_savings_location_variation(template, variation_num):
    """Create a variation for savings location comparison questions"""
    variation = copy.deepcopy(template)
    
    # Update question_number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{variation_num}"
    
    # Generate job scenarios
    jobs = [
        "tutoring students", "walking dogs", "delivering newspapers", "washing cars",
        "mowing lawns", "babysitting", "selling lemonade", "helping at a bakery",
        "streaming video games", "creating digital art", "editing videos", "coding websites"
    ]
    
    # Generate character names
    characters = ["Zoe", "Marcus", "Isabella", "Jackson", "Mia", "Lucas", "Harper", "Owen"]
    
    character = random.choice(characters)
    job = random.choice(jobs)
    
    # Create variations of advantage/disadvantage statements
    is_advantage = random.choice([True, False])
    
    if is_advantage:
        correct = random.choice([
            "An advantage of keeping the money in a savings account is that it will earn interest.",
            "An advantage of a savings account is that the money is protected by the bank.",
            "An advantage of using a bank is that you have a record of your savings."
        ])
        wrong = random.choice([
            "An advantage of keeping money at home is that it earns interest.",
            "An advantage of keeping money at home is that it's insured against loss."
        ])
    else:
        correct = random.choice([
            "A disadvantage of keeping the money at home is that it could be lost or stolen.",
            "A disadvantage of keeping money at home is that it won't earn interest.",
            "A disadvantage of keeping cash at home is that there's no record of savings."
        ])
        wrong = random.choice([
            "A disadvantage of keeping money in a savings account is that you can't access it.",
            "A disadvantage of a savings account is that the bank will lose your money."
        ])
    
    variation['question_text'] = (
        f"{character} earns money by {job}. They can put their money in a savings account. "
        f"They can also keep it at home. Which of these is true?"
    )
    
    # Set up choices
    if is_advantage:
        choices = [wrong, correct]
    else:
        choices = [wrong, correct]
    
    random.shuffle(choices)
    variation['choices'] = choices
    
    # Set correct answer
    correct_index = choices.index(correct)
    variation['correct_answers'] = [chr(65 + correct_index)]
    
    # Generate solution
    solution = []
    for i, choice in enumerate(choices):
        step_num = f"{i+1}/2"
        if choice == correct:
            explanation = f"✓ {choice}\nThis statement is true and correctly describes {'an advantage' if is_advantage else 'a disadvantage'} of the savings option."
        else:
            explanation = f"✗ {choice}\nThis statement is not true or does not correctly describe the savings option."
        solution.append([step_num, explanation])
    
    variation['solution'] = solution
    
    return variation

def generate_variations():
    """Generate all variations for Gr6_54_E2"""
    templates = load_templates()
    scenarios = get_savings_scenarios()
    variations = []
    
    # We have 4 template questions, need 51 total (including templates)
    # So we need 47 additional variations
    variations_needed = 47
    
    # Categorize templates by type
    bank_comparison_template = templates[0]  # question_number 2_1
    simple_comparison_template = templates[1]  # question_number 2_2
    savings_plan_template = templates[2]  # question_number 2_3
    location_comparison_template = templates[3]  # question_number 2_4
    
    variation_counter = 5  # Start after template questions
    
    # Generate bank comparison variations (15 variations)
    for i in range(15):
        scenario = random.choice(scenarios)
        variation = create_bank_comparison_variation(bank_comparison_template, variation_counter, scenario)
        variations.append(variation)
        variation_counter += 1
    
    # Generate savings plan variations (16 variations)
    for i in range(16):
        scenario = random.choice(scenarios)
        variation = create_savings_plan_variation(savings_plan_template, variation_counter, scenario)
        variations.append(variation)
        variation_counter += 1
    
    # Generate savings location variations (16 variations)
    for i in range(16):
        variation = create_savings_location_variation(location_comparison_template, variation_counter)
        variations.append(variation)
        variation_counter += 1
    
    # Save variations to file
    with open('Gr6_54_E2_variations.json', 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_54_E2")
    print(f"Total questions (including templates): {len(templates) + len(variations)}")

if __name__ == "__main__":
    generate_variations()