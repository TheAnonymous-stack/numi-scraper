import json
import random
import copy

def load_templates():
    """Load template questions from file2.json"""
    with open('file2.json', 'r') as f:
        data = json.load(f)
    
    # Filter for Gr6_55_E2 questions
    templates = [q for q in data if q.get('tag') == 'Gr6_55_E2']
    return templates

def get_interest_scenarios():
    """Generate diverse simple interest scenarios with pop culture themes"""
    scenarios = [
        # Gaming savings
        ("Alex", "save for a PS5 Pro", 400, 4, 1),
        ("Nova", "buy a gaming PC", 800, 3, 2),
        ("Pixel", "get VR equipment", 600, 5, 1),
        ("Quest", "buy Nintendo games", 200, 6, 1),
        ("Arcade", "build a gaming setup", 1000, 4, 2),
        
        # Anime/manga collection
        ("Sakura", "buy manga volumes", 150, 8, 1),
        ("Hiro", "get anime figures", 300, 5, 2),
        ("Yuki", "attend anime convention", 250, 10, 1),
        ("Ren", "buy cosplay materials", 450, 4, 1),
        ("Kai", "collect trading cards", 180, 6, 2),
        
        # Music and instruments
        ("Melody", "buy a keyboard", 550, 3, 1),
        ("Jazz", "get recording equipment", 750, 4, 2),
        ("Rhythm", "buy concert tickets", 320, 5, 1),
        ("Beat", "get DJ equipment", 900, 2, 3),
        ("Harmony", "buy a guitar", 480, 6, 1),
        
        # Sports equipment
        ("Jordan", "buy basketball gear", 280, 5, 1),
        ("Serena", "get tennis equipment", 420, 4, 1),
        ("Tiger", "buy golf clubs", 650, 3, 2),
        ("Bolt", "get running shoes", 160, 8, 1),
        ("Ace", "buy baseball equipment", 380, 5, 2),
        
        # Tech gadgets
        ("Binary", "buy a smartphone", 700, 4, 1),
        ("Cyber", "get a tablet", 450, 5, 2),
        ("Data", "buy a smartwatch", 350, 6, 1),
        ("Cloud", "get wireless earbuds", 250, 8, 1),
        ("Matrix", "buy a drone", 580, 3, 2),
        
        # Art supplies
        ("Canvas", "buy art supplies", 220, 5, 1),
        ("Palette", "get a drawing tablet", 480, 4, 2),
        ("Sketch", "buy paint sets", 180, 10, 1),
        ("Color", "get crafting materials", 320, 6, 1),
        ("Design", "buy a camera", 850, 3, 2),
        
        # Books and education
        ("Scholar", "buy textbooks", 240, 5, 1),
        ("Wisdom", "get online courses", 380, 4, 2),
        ("Knowledge", "buy e-reader", 200, 8, 1),
        ("Study", "get language software", 150, 12, 1),
        ("Learn", "buy educational games", 120, 10, 2),
        
        # Fashion and clothing
        ("Style", "buy designer shoes", 420, 5, 1),
        ("Trend", "get new wardrobe", 680, 3, 2),
        ("Vogue", "buy accessories", 280, 6, 1),
        ("Chic", "get a designer bag", 550, 4, 1),
        ("Fashion", "buy jewelry", 380, 8, 2),
        
        # Travel and experiences
        ("Explorer", "save for a trip", 1200, 2, 2),
        ("Journey", "buy camping gear", 450, 5, 1),
        ("Adventure", "get scuba equipment", 780, 3, 2),
        ("Wanderer", "buy travel accessories", 320, 6, 1),
        ("Nomad", "save for vacation", 950, 4, 1)
    ]
    return scenarios

def create_interest_variation(template, variation_num):
    """Create a variation for simple interest questions"""
    variation = copy.deepcopy(template)
    
    # Update question_number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{variation_num}"
    
    # Get random scenario
    scenarios = get_interest_scenarios()
    name, purpose, principal, rate, time = random.choice(scenarios)
    
    # Add some variation to the numbers
    principal_options = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 
                         120, 150, 180, 200, 250, 300, 350, 400, 450, 500, 600, 
                         700, 800, 900, 1000, 1200, 1500]
    
    rate_options = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]
    time_options = [1, 2, 3, 4, 5]
    
    # Select random values
    principal = random.choice(principal_options)
    rate = random.choice(rate_options)
    time = random.choice(time_options)
    
    # Calculate interest
    interest = principal * (rate / 100) * time
    total = principal + interest
    
    # Format the answer (handle decimal places)
    if interest == int(interest):
        interest_str = str(int(interest))
        total_str = str(int(total))
    else:
        interest_str = f"{interest:.2f}"
        total_str = f"{total:.2f}"
    
    # Create question text
    variation['question_text'] = (
        f"{name} has ${principal} in a savings account. "
        f"The interest rate is {rate}% per year and is not compounded. "
        f"How much will {name} have in total in {time} year{'s' if time > 1 else ''}?\n"
        f"Use the formula $i = prt$, where $i$ is the interest earned, "
        f"$p$ is the principal (starting amount), $r$ is the interest rate expressed as a decimal, "
        f"and $t$ is the time in years.\n$___"
    )
    
    # Set correct answers (accept different decimal formats)
    correct_answers = [total_str]
    if '.' in total_str:
        # Add variations with different decimal places
        if total_str.endswith('0'):
            correct_answers.append(total_str[:-1])  # Remove trailing 0
        if total_str.endswith('.00'):
            correct_answers.append(total_str[:-3])  # Remove .00
    else:
        # Add decimal versions
        correct_answers.append(f"{total_str}.0")
        correct_answers.append(f"{total_str}.00")
    
    variation['correct_answers'] = correct_answers
    
    # Generate solution steps
    solution = [
        ["1/4", f"Write the rate as a decimal.\n{rate}% = {rate/100}"],
        ["2/4", f"Calculate the interest earned.\n$i = prt$\n= {principal} × {rate/100} × {time}\n= {interest_str}"],
        ["3/4", f"Find the total amount by adding the interest to the principal.\n{interest_str} + {principal} = {total_str}"],
        ["4/4", f"The total amount will be ${total_str}"]
    ]
    
    variation['solution'] = solution
    
    return variation

def generate_variations():
    """Generate all variations for Gr6_55_E2"""
    templates = load_templates()
    variations = []
    
    # We have 1 template question, need 51 total (including template)
    # So we need 50 additional variations
    variations_needed = 50
    
    # Generate variations
    for i in range(variations_needed):
        variation = create_interest_variation(templates[0], i + 2)  # Start at 2 since template is 2_1
        variations.append(variation)
    
    # Save variations to file
    with open('Gr6_55_E2_variations.json', 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_55_E2")
    print(f"Total questions (including template): {len(templates) + len(variations)}")

if __name__ == "__main__":
    generate_variations()