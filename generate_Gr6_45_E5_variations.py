import json
import random
import copy
from math import gcd
from fractions import Fraction

def load_templates():
    """Load template questions from parsed_templates.json"""
    with open('parsed_templates.json', 'r') as f:
        data = json.load(f)
    return data.get('Gr6_45_E5', [])

def simplify_fraction(num, den):
    """Simplify a fraction"""
    g = gcd(num, den)
    return num // g, den // g

def generate_game_show_scenarios():
    """Generate game show and contest scenarios"""
    scenarios = [
        "game show",
        "quiz competition",
        "talent show",
        "lottery drawing",
        "raffle",
        "spelling bee",
        "trivia contest",
        "math competition",
        "science fair",
        "art contest",
        "cooking competition",
        "dance competition",
        "singing contest",
        "debate tournament",
        "chess tournament"
    ]
    
    # Add pop culture themed contests
    anime_contests = [
        "Chunin exam",  # Naruto
        "Hunter exam",  # Hunter x Hunter
        "UA Sports Festival",  # My Hero Academia
        "Grand Magic Games",  # Fairy Tail
        "Demon Slayer trial",  # Demon Slayer
        "Soul Reaper test",  # Bleach
        "Dragon Ball tournament",  # Dragon Ball
        "Pokemon battle",  # Pokemon
        "Duel Monsters tournament",  # Yu-Gi-Oh
        "Food Wars competition"  # Food Wars
    ]
    
    # Add video game themed contests
    game_contests = [
        "Fortnite tournament",
        "Minecraft building contest",
        "Among Us championship",
        "League of Legends match",
        "Overwatch competition",
        "Valorant tournament",
        "Rocket League championship",
        "Call of Duty tournament",
        "Super Smash Bros tournament",
        "Mario Kart race"
    ]
    
    return scenarios + anime_contests + game_contests

def generate_sports_scenarios():
    """Generate sports-related experimental probability scenarios"""
    scenarios = [
        ("basketball players", "made a free throw"),
        ("soccer players", "scored a penalty kick"),
        ("baseball players", "got a hit"),
        ("tennis players", "won their serve"),
        ("golfers", "made par"),
        ("bowlers", "got a strike"),
        ("volleyball players", "made their serve"),
        ("hockey players", "scored on a penalty shot"),
        ("football players", "completed a pass"),
        ("swimmers", "qualified for finals"),
        ("runners", "beat their personal best"),
        ("cyclists", "finished the race"),
        ("gymnasts", "stuck their landing"),
        ("wrestlers", "won their match"),
        ("boxers", "won by knockout")
    ]
    
    return scenarios

def generate_student_scenarios():
    """Generate student/academic scenarios"""
    scenarios = [
        ("students", "passed the test"),
        ("students", "got an A"),
        ("students", "turned in homework on time"),
        ("students", "made the honor roll"),
        ("students", "perfect attendance"),
        ("teams", "won their debate"),
        ("projects", "received funding"),
        ("essays", "were selected for publication"),
        ("presentations", "got a standing ovation"),
        ("experiments", "succeeded"),
        ("students", "solved the bonus problem"),
        ("groups", "finished their project early"),
        ("students", "earned extra credit"),
        ("participants", "completed the challenge"),
        ("students", "answered correctly")
    ]
    
    return scenarios

def generate_customer_scenarios():
    """Generate customer/business scenarios"""
    scenarios = [
        ("customers", "bought something"),
        ("shoppers", "used a coupon"),
        ("visitors", "signed up for membership"),
        ("customers", "left a 5-star review"),
        ("diners", "ordered dessert"),
        ("moviegoers", "bought popcorn"),
        ("passengers", "upgraded their seat"),
        ("subscribers", "renewed their subscription"),
        ("users", "clicked the ad"),
        ("players", "made an in-app purchase"),
        ("viewers", "liked the video"),
        ("listeners", "downloaded the song"),
        ("readers", "finished the article"),
        ("attendees", "stayed until the end"),
        ("participants", "completed the survey")
    ]
    
    return scenarios

def generate_experimental_data():
    """Generate realistic experimental probability data"""
    # Generate favorable/total pairs that create clean fractions
    data_options = []
    
    # Simple fractions with small totals
    for total in [5, 10, 12, 15, 20, 25, 30, 40, 50]:
        for favorable in range(1, total):
            # Create fractions that simplify nicely
            num, den = simplify_fraction(favorable, total)
            if den <= 10:  # Keep denominators manageable
                data_options.append((favorable, total, num, den))
    
    return data_options

def format_fraction_answer(num, den):
    """Format fraction as answer string"""
    if num == den:
        return "1"
    else:
        return f"{num}/{den}"

def generate_variation(template, var_num, total_templates):
    """Generate a single variation based on template type"""
    variation = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{var_num}"
    
    # Choose scenario type
    scenario_type = random.choice(['contest', 'sports', 'student', 'customer'])
    
    if scenario_type == 'contest':
        contests = generate_game_show_scenarios()
        contest = random.choice(contests)
        
        # Generate data
        data_options = generate_experimental_data()
        favorable, total, num_simple, den_simple = random.choice(data_options)
        
        question_text = f"Of the last {total} contestants on a {contest}, {favorable} won a prize. "
        question_text += f"What is the experimental probability that the next contestant will win a prize?\n"
        question_text += "Write your answer as a fraction or whole number.\n"
        question_text += "P(win) = ___"
        
        answer = format_fraction_answer(num_simple, den_simple)
        
        solution = [
            ["1/4", "Remember, the experimental probability is the number of times an event occurs out of the total number of trials."],
            ["2/4", "Write the experimental probability as a fraction in simplest form."],
            ["3/4", f"P(win) = $\\frac{{\\text{{wins}}}}{{\\text{{total}}}}$ = $\\frac{{{favorable}}}{{{total}}}$" +
                    (f"=$\\frac{{{num_simple}}}{{{den_simple}}}$" if (favorable, total) != (num_simple, den_simple) else "")],
            ["4/4", f"So, P(win) = $\\frac{{{num_simple}}}{{{den_simple}}}$"]
        ]
        
    elif scenario_type == 'sports':
        sports = generate_sports_scenarios()
        subjects, outcome = random.choice(sports)
        
        # Generate data
        data_options = generate_experimental_data()
        favorable, total, num_simple, den_simple = random.choice(data_options)
        
        question_text = f"Of the last {total} {subjects}, {favorable} {outcome}. "
        question_text += f"What is the experimental probability that the next player will {outcome.replace('made', 'make').replace('got', 'get').replace('won', 'win').replace('scored', 'score').replace('completed', 'complete').replace('qualified', 'qualify').replace('stuck', 'stick').replace('beat', 'beat').replace('finished', 'finish')}?\n"
        question_text += "Write your answer as a fraction or whole number.\n"
        question_text += "P(success) = ___"
        
        answer = format_fraction_answer(num_simple, den_simple)
        
        solution = [
            ["1/4", "Remember, the experimental probability is the number of times an event occurs out of the total number of trials."],
            ["2/4", "Write the experimental probability as a fraction in simplest form."],
            ["3/4", f"P(success) = $\\frac{{\\text{{successes}}}}{{\\text{{total}}}}$ = $\\frac{{{favorable}}}{{{total}}}$" +
                    (f"=$\\frac{{{num_simple}}}{{{den_simple}}}$" if (favorable, total) != (num_simple, den_simple) else "")],
            ["4/4", f"So, P(success) = $\\frac{{{num_simple}}}{{{den_simple}}}$"]
        ]
        
    elif scenario_type == 'student':
        students = generate_student_scenarios()
        subjects, outcome = random.choice(students)
        
        # Generate data
        data_options = generate_experimental_data()
        favorable, total, num_simple, den_simple = random.choice(data_options)
        
        question_text = f"Of the last {total} {subjects}, {favorable} {outcome}. "
        question_text += f"What is the experimental probability that the next will have the same result?\n"
        question_text += "Write your answer as a fraction or whole number.\n"
        question_text += "P(event) = ___"
        
        answer = format_fraction_answer(num_simple, den_simple)
        
        solution = [
            ["1/4", "Remember, the experimental probability is the number of times an event occurs out of the total number of trials."],
            ["2/4", "Write the experimental probability as a fraction in simplest form."],
            ["3/4", f"P(event) = $\\frac{{\\text{{favorable}}}}{{\\text{{total}}}}$ = $\\frac{{{favorable}}}{{{total}}}$" +
                    (f"=$\\frac{{{num_simple}}}{{{den_simple}}}$" if (favorable, total) != (num_simple, den_simple) else "")],
            ["4/4", f"So, P(event) = $\\frac{{{num_simple}}}{{{den_simple}}}$"]
        ]
        
    else:  # customer
        customers = generate_customer_scenarios()
        subjects, outcome = random.choice(customers)
        
        # Generate data
        data_options = generate_experimental_data()
        favorable, total, num_simple, den_simple = random.choice(data_options)
        
        question_text = f"Of the last {total} {subjects}, {favorable} {outcome}. "
        question_text += f"What is the experimental probability that the next will do the same?\n"
        question_text += "Write your answer as a fraction or whole number.\n"
        question_text += "P(outcome) = ___"
        
        answer = format_fraction_answer(num_simple, den_simple)
        
        solution = [
            ["1/4", "Remember, the experimental probability is the number of times an event occurs out of the total number of trials."],
            ["2/4", "Write the experimental probability as a fraction in simplest form."],
            ["3/4", f"P(outcome) = $\\frac{{\\text{{favorable}}}}{{\\text{{total}}}}$ = $\\frac{{{favorable}}}{{{total}}}$" +
                    (f"=$\\frac{{{num_simple}}}{{{den_simple}}}$" if (favorable, total) != (num_simple, den_simple) else "")],
            ["4/4", f"So, P(outcome) = $\\frac{{{num_simple}}}{{{den_simple}}}$"]
        ]
    
    variation['question_text'] = question_text
    variation['correct_answers'] = [answer]
    variation['solution'] = solution
    
    return variation

def main():
    """Main function to generate all variations"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_45_E5")
        return
    
    print(f"Found {len(templates)} template(s) for Gr6_45_E5")
    
    # Calculate how many variations we need
    total_needed = 51
    variations_needed = total_needed - len(templates)
    
    print(f"Generating {variations_needed} variations to reach {total_needed} total")
    
    variations = []
    
    # Generate variations
    for i in range(variations_needed):
        # Use the single template as base
        template = templates[0]
        
        # Generate variation number (starting after templates)
        var_num = len(templates) + i + 1
        
        variation = generate_variation(template, var_num, len(templates))
        variations.append(variation)
        
        if (i + 1) % 10 == 0:
            print(f"Generated {i + 1} variations...")
    
    # Save variations to file
    output_file = 'Gr6_45_E5_variations.json'
    with open(output_file, 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"\nSuccessfully generated {len(variations)} variations")
    print(f"Variations saved to {output_file}")
    
    # Verify uniqueness
    question_texts = [v['question_text'] for v in variations]
    unique_questions = len(set(question_texts))
    print(f"Unique question texts: {unique_questions}/{len(variations)}")

if __name__ == "__main__":
    main()