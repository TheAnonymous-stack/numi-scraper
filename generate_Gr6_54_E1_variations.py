import json
import random
import copy

def load_templates():
    """Load template questions from file2.json"""
    with open('file2.json', 'r') as f:
        data = json.load(f)
    
    # Filter for Gr6_54_E1 questions
    templates = [q for q in data if q.get('tag') == 'Gr6_54_E1']
    return templates

def get_payment_scenarios():
    """Generate diverse payment scenarios with pop culture themes"""
    scenarios = [
        # Anime themes
        ("anime convention tickets", "attending Comic-Con", "purchasing manga"),
        ("Pokemon cards", "buying rare collectibles", "trading card games"),
        ("gaming console", "buying a PlayStation", "purchasing video games"),
        ("cosplay outfit", "attending an anime expo", "buying costume materials"),
        ("streaming subscription", "Netflix anime series", "monthly entertainment"),
        
        # Pop culture themes
        ("concert tickets", "seeing Taylor Swift", "entertainment events"),
        ("movie tickets", "watching Marvel films", "cinema visits"),
        ("sports equipment", "joining a basketball team", "athletic gear"),
        ("musical instrument", "learning guitar", "music lessons"),
        ("smartphone", "upgrading your iPhone", "tech purchases"),
        
        # Everyday items with modern twist
        ("online course", "learning programming", "education expenses"),
        ("gym membership", "fitness training", "health expenses"),
        ("laptop", "remote work setup", "technology"),
        ("electric scooter", "eco-friendly transport", "transportation"),
        ("smart watch", "fitness tracking", "wearable tech"),
        
        # Food and dining
        ("restaurant bill", "dining at a sushi bar", "food expenses"),
        ("coffee shop purchase", "buying at Starbucks", "beverages"),
        ("food delivery", "ordering from UberEats", "meal services"),
        ("grocery shopping", "weekly food supplies", "household expenses"),
        ("bakery items", "birthday cake order", "special occasions"),
        
        # Services
        ("haircut", "salon visit", "personal grooming"),
        ("pet grooming", "dog spa treatment", "pet care"),
        ("tutoring session", "math help", "education"),
        ("house cleaning", "maid service", "home maintenance"),
        ("lawn care", "gardening service", "property maintenance")
    ]
    return scenarios

def create_payment_method_variation(template, variation_num, scenario):
    """Create a variation for payment method advantages/disadvantages questions"""
    variation = copy.deepcopy(template)
    
    # Update question_number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{variation_num}"
    
    item, context, category = scenario
    
    # Determine payment method and advantage/disadvantage
    payment_methods = ['cash', 'cheque', 'credit card', 'debit card', 'e-transfer', 'mobile payment']
    selected_method = random.choice(payment_methods)
    
    # Randomly choose advantage or disadvantage
    is_advantage = random.choice([True, False])
    
    if is_advantage:
        variation['question_text'] = f"Which of the following is an advantage of using {selected_method} to pay for {item}?"
    else:
        variation['question_text'] = f"Which of the following is a disadvantage of using {selected_method} to pay for {item}?"
    
    # Generate appropriate choices based on payment method
    if selected_method == 'cash':
        if is_advantage:
            correct = "No transaction fees are charged when using cash."
            wrong1 = "Cash payments require an internet connection."
            wrong2 = "Cash transactions take several days to process."
        else:
            correct = "You cannot use cash for online purchases."
            wrong1 = "Cash payments are always tracked by your bank."
            wrong2 = "Cash has built-in fraud protection."
    
    elif selected_method == 'cheque':
        if is_advantage:
            correct = "You have a written record of your payment."
            wrong1 = "Cheques process instantly."
            wrong2 = "You don't need a bank account to write cheques."
        else:
            correct = "The payment takes several days to clear."
            wrong1 = "Cheques are accepted everywhere."
            wrong2 = "There are never any fees for using cheques."
    
    elif selected_method == 'credit card':
        if is_advantage:
            correct = "You can make purchases even without immediate funds."
            wrong1 = "Credit cards never charge interest."
            wrong2 = "Credit cards cannot be lost or stolen."
        else:
            correct = "You may be charged interest if you don't pay on time."
            wrong1 = "Credit cards give you free money."
            wrong2 = "Credit cards are not accepted anywhere."
    
    elif selected_method == 'debit card':
        if is_advantage:
            correct = "Money comes directly from your bank account."
            wrong1 = "Debit cards let you spend more than you have."
            wrong2 = "Debit cards always earn you rewards points."
        else:
            correct = "You need sufficient funds in your account."
            wrong1 = "Debit cards build your credit score."
            wrong2 = "Debit cards offer purchase protection insurance."
    
    elif selected_method == 'e-transfer':
        if is_advantage:
            correct = "The money transfers quickly and securely."
            wrong1 = "E-transfers don't require email or phone numbers."
            wrong2 = "E-transfers work without internet."
        else:
            correct = "There may be fees for sending money."
            wrong1 = "E-transfers can be reversed after completion."
            wrong2 = "E-transfers don't require a bank account."
    
    else:  # mobile payment
        if is_advantage:
            correct = "Payments are quick and contactless."
            wrong1 = "Mobile payments work without a phone."
            wrong2 = "Mobile payments don't require setup."
        else:
            correct = "You need a compatible smartphone."
            wrong1 = "Mobile payments are accepted everywhere."
            wrong2 = "Mobile payments don't require internet."
    
    # Randomize choice order
    choices = [correct, wrong1, wrong2]
    random.shuffle(choices)
    variation['choices'] = choices
    
    # Set correct answer
    correct_index = choices.index(correct)
    variation['correct_answers'] = [chr(65 + correct_index)]  # A, B, or C
    
    # Update solution with explanations
    solution_parts = []
    for i, choice in enumerate(choices):
        step_num = f"{i+1}/{len(choices)}"
        if choice == correct:
            explanation = f"✓ {choice}\nThis is correct. When using {selected_method} for {context}, this is {'an advantage' if is_advantage else 'a disadvantage'}."
        else:
            explanation = f"✗ {choice}\nThis is incorrect. This statement is {'not an advantage' if is_advantage else 'not a disadvantage'} of using {selected_method}."
        solution_parts.append([step_num, explanation])
    
    variation['solution'] = solution_parts
    
    return variation

def generate_variations():
    """Generate all variations for Gr6_54_E1"""
    templates = load_templates()
    scenarios = get_payment_scenarios()
    variations = []
    
    # We have 3 template questions, need 51 total (including templates)
    # So we need 48 additional variations
    variations_needed = 48
    variations_per_template = variations_needed // len(templates)
    extra_variations = variations_needed % len(templates)
    
    for template_idx, template in enumerate(templates):
        num_variations = variations_per_template
        if template_idx < extra_variations:
            num_variations += 1
        
        # Start variation numbering from where templates end
        start_num = 5  # Since we have templates 1_2, 1_3, 1_4
        
        for i in range(num_variations):
            scenario = random.choice(scenarios)
            variation = create_payment_method_variation(
                template, 
                start_num + i + (template_idx * variations_per_template),
                scenario
            )
            variations.append(variation)
    
    # Save variations to file
    with open('Gr6_54_E1_variations.json', 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_54_E1")
    print(f"Total questions (including templates): {len(templates) + len(variations)}")

if __name__ == "__main__":
    generate_variations()