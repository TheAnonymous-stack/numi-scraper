import json
import random
import copy
from math import gcd

def load_templates():
    """Load template questions from parsed_templates.json"""
    with open('parsed_templates.json', 'r') as f:
        data = json.load(f)
    return data.get('Gr6_45_E4', [])

def simplify_fraction(num, den):
    """Simplify a fraction"""
    g = gcd(num, den)
    return num // g, den // g

def generate_restaurant_scenarios():
    """Generate restaurant/food service scenarios"""
    scenarios = []
    
    # Restaurant types and food items
    restaurants = [
        ("Pizza Palace", "pepperoni", "pizzas"),
        ("Taco Town", "extra salsa", "tacos"),
        ("Sushi Station", "wasabi", "orders"),
        ("Sandwich Shop", "extra mayo", "sandwiches"),
        ("Ice Cream Parlor", "chocolate chips", "sundaes"),
        ("Coffee Corner", "whipped cream", "lattes"),
        ("Donut Den", "sprinkles", "donuts"),
        ("Pasta Place", "extra cheese", "dishes"),
        ("BBQ Barn", "hot sauce", "meals"),
        ("Smoothie Spot", "protein powder", "smoothies"),
        ("Bagel Bay", "cream cheese", "bagels"),
        ("Waffle House", "maple syrup", "waffles"),
        ("Noodle Nook", "extra spice", "bowls"),
        ("Burger Haven", "cheese", "burgers"),
        ("Chicken Coop", "buffalo sauce", "wings")
    ]
    
    # Pop culture themed restaurants
    anime_restaurants = [
        ("Ichiraku Ramen", "extra naruto", "bowls"),  # Naruto reference
        ("Baratie Restaurant", "special sauce", "dishes"),  # One Piece
        ("Yukihira Diner", "secret spice", "meals"),  # Food Wars
        ("Kame House Cafe", "senzu topping", "orders"),  # Dragon Ball
        ("UA Cafeteria", "hero sauce", "lunches"),  # My Hero Academia
        ("Soul Society Sushi", "hollow pepper", "rolls"),  # Bleach
        ("Fairy Tail Tavern", "magic seasoning", "plates"),  # Fairy Tail
        ("Demon Slayer Deli", "breathing spice", "bentos"),  # Demon Slayer
        ("Titan's Table", "wall rose herbs", "servings"),  # Attack on Titan
        ("Hunter x Hunter Grill", "nen sauce", "skewers")  # Hunter x Hunter
    ]
    
    # Game themed restaurants
    game_restaurants = [
        ("Mushroom Kingdom Pizza", "fire flower topping", "pizzas"),  # Mario
        ("Hyrule Kitchen", "lon lon cream", "dishes"),  # Zelda
        ("Pallet Town Diner", "rare candy sprinkles", "meals"),  # Pokemon
        ("Minecraft Cafe", "redstone dust", "orders"),  # Minecraft
        ("Overwatch Canteen", "health pack sauce", "meals"),  # Overwatch
        ("Fortnite Food Truck", "shield potion glaze", "orders"),  # Fortnite
        ("Among Us Cafeteria", "sus sauce", "plates"),  # Among Us
        ("Valorant Bistro", "radianite seasoning", "dishes"),  # Valorant
        ("League Lunch", "mana potion dressing", "meals"),  # League of Legends
        ("Genshin Gourmet", "primogem spice", "dishes")  # Genshin Impact
    ]
    
    all_restaurants = restaurants + anime_restaurants + game_restaurants
    
    for restaurant, topping, food_item in all_restaurants:
        scenarios.append({
            'location': restaurant,
            'item': topping,
            'food': food_item
        })
    
    return scenarios

def generate_activity_scenarios():
    """Generate various activity-based experimental probability scenarios"""
    scenarios = []
    
    # Sports scenarios
    sports = [
        ("basketball court", "made a three-pointer", "players", "shots"),
        ("soccer field", "scored a goal", "players", "penalty kicks"),
        ("baseball diamond", "hit a home run", "batters", "at-bats"),
        ("tennis court", "served an ace", "players", "serves"),
        ("bowling alley", "got a strike", "bowlers", "frames"),
        ("golf course", "made a birdie", "golfers", "holes"),
        ("volleyball court", "made a spike", "players", "attempts"),
        ("cricket pitch", "hit a six", "batsmen", "balls"),
        ("pool hall", "sank the 8-ball", "players", "games"),
        ("dart board", "hit the bullseye", "players", "throws")
    ]
    
    # Gaming scenarios
    gaming = [
        ("arcade", "won a prize", "players", "games"),
        ("casino", "won at slots", "gamblers", "spins"),
        ("game show", "won a prize", "contestants", "rounds"),
        ("lottery booth", "won something", "tickets", "drawings"),
        ("raffle", "won a prize", "entries", "draws"),
        ("carnival game", "won a stuffed animal", "players", "attempts"),
        ("escape room", "escaped in time", "teams", "attempts"),
        ("trivia night", "answered correctly", "teams", "questions"),
        ("bingo hall", "got bingo", "cards", "games"),
        ("pokemon go raid", "caught the legendary", "trainers", "raids")
    ]
    
    # School/test scenarios
    school = [
        ("math quiz", "got an A", "students", "quizzes"),
        ("spelling bee", "spelled correctly", "contestants", "words"),
        ("science fair", "won an award", "projects", "entries"),
        ("art contest", "placed in top 3", "submissions", "entries"),
        ("debate tournament", "won their round", "teams", "debates"),
        ("coding competition", "solved the problem", "programmers", "attempts"),
        ("chess tournament", "won their match", "players", "games"),
        ("music recital", "got a standing ovation", "performers", "performances"),
        ("drama audition", "got the part", "actors", "auditions"),
        ("robotics competition", "completed the task", "teams", "runs")
    ]
    
    all_activities = sports + gaming + school
    
    for location, outcome, subjects, trials in all_activities:
        scenarios.append({
            'location': location,
            'outcome': outcome,
            'subjects': subjects,
            'trials': trials
        })
    
    return scenarios

def generate_weather_scenarios():
    """Generate weather-based experimental probability scenarios"""
    scenarios = [
        ("weather station", "it rained", "days", "days"),
        ("beach resort", "was sunny", "days", "vacation days"),
        ("ski lodge", "it snowed", "days", "winter days"),
        ("tornado alley", "had a warning", "days", "storm season days"),
        ("tropical island", "had perfect weather", "days", "tourist days"),
        ("mountain peak", "was foggy", "mornings", "observations"),
        ("desert camp", "reached 100°F", "days", "summer days"),
        ("coastal town", "had high tide", "times", "tide cycles"),
        ("weather balloon", "detected turbulence", "flights", "launches"),
        ("storm chaser van", "saw a tornado", "trips", "chase days")
    ]
    
    return scenarios

def generate_experimental_data():
    """Generate realistic experimental probability data"""
    # Generate favorable/total pairs that create reasonable fractions
    fractions = [
        (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
        (2, 3), (2, 5), (3, 4), (3, 5), (4, 5),
        (1, 8), (3, 8), (5, 8), (7, 8),
        (1, 10), (3, 10), (7, 10), (9, 10)
    ]
    
    # Scale up to reasonable sample sizes
    scales = [6, 8, 10, 12, 15, 16, 18, 20, 24, 25, 30, 32, 36, 40]
    
    data_pairs = []
    for num, den in fractions:
        for scale in scales:
            favorable = num * scale
            total = den * scale
            if 5 <= favorable <= 50 and 10 <= total <= 100:
                data_pairs.append((favorable, total))
    
    return data_pairs

def generate_variation(template, var_num, total_templates):
    """Generate a single variation based on template type"""
    variation = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{var_num}"
    
    # Choose scenario type
    scenario_type = random.choice(['restaurant', 'activity', 'weather'])
    
    if scenario_type == 'restaurant':
        restaurant_scenarios = generate_restaurant_scenarios()
        scenario = random.choice(restaurant_scenarios)
        
        # Generate experimental data
        data_pairs = generate_experimental_data()
        favorable_past, total_past = random.choice(data_pairs)
        
        # Generate prediction data - use a multiple of the denominator for clean division
        prob_num, prob_den = simplify_fraction(favorable_past, total_past)
        multipliers = [1, 2, 3, 4, 5, 6, 7, 8]
        multiplier = random.choice(multipliers)
        total_future = prob_den * multiplier
        
        # Ensure reasonable future sample size
        if total_future < 10:
            total_future *= random.choice([2, 3, 4])
        if total_future > 50:
            total_future = prob_den * random.choice([1, 2, 3])
        
        expected = (prob_num * total_future) // prob_den
        
        question_text = f"At {scenario['location']}, {favorable_past} of the last {total_past} customers wanted {scenario['item']} on their {scenario['food']}. "
        question_text += f"Considering this data, how many of the next {total_future} customers would you expect to want {scenario['item']}?\n___ customers"
        
    elif scenario_type == 'activity':
        activity_scenarios = generate_activity_scenarios()
        scenario = random.choice(activity_scenarios)
        
        # Generate experimental data
        data_pairs = generate_experimental_data()
        favorable_past, total_past = random.choice(data_pairs)
        
        # Generate prediction data
        prob_num, prob_den = simplify_fraction(favorable_past, total_past)
        multipliers = [1, 2, 3, 4, 5, 6, 7, 8]
        multiplier = random.choice(multipliers)
        total_future = prob_den * multiplier
        
        # Ensure reasonable future sample size
        if total_future < 10:
            total_future *= random.choice([2, 3, 4])
        if total_future > 50:
            total_future = prob_den * random.choice([1, 2, 3])
        
        expected = (prob_num * total_future) // prob_den
        
        question_text = f"At the {scenario['location']}, {favorable_past} of the last {total_past} {scenario['subjects']} {scenario['outcome']}. "
        question_text += f"Based on this data, how many of the next {total_future} {scenario['trials']} would you expect to have the same outcome?\n___ {scenario['trials']}"
        
    else:  # weather
        weather_scenarios = generate_weather_scenarios()
        scenario = random.choice(weather_scenarios)
        location, outcome, subjects, trials = scenario
        
        # Generate experimental data
        data_pairs = generate_experimental_data()
        favorable_past, total_past = random.choice(data_pairs)
        
        # Generate prediction data
        prob_num, prob_den = simplify_fraction(favorable_past, total_past)
        multipliers = [1, 2, 3, 4, 5, 6, 7, 8]
        multiplier = random.choice(multipliers)
        total_future = prob_den * multiplier
        
        # Ensure reasonable future sample size
        if total_future < 10:
            total_future *= random.choice([2, 3, 4])
        if total_future > 50:
            total_future = prob_den * random.choice([1, 2, 3])
        
        expected = (prob_num * total_future) // prob_den
        
        question_text = f"At the {location}, {favorable_past} of the last {total_past} {subjects} {outcome}. "
        question_text += f"Based on this pattern, how many of the next {total_future} {trials} would you expect {outcome}?\n___ {trials}"
    
    variation['question_text'] = question_text
    variation['correct_answers'] = [str(expected)]
    
    # Update solution
    variation['solution'] = [
        ["1/6", "Remember, the experimental probability is the number of times an event occurs out of the total number of trials."],
        ["2/6", f"First write the experimental probability as a fraction in simplest form.\n" +
                f"P(event) \n= $\\frac{{\\text{{favorable}}}}{{\\text{{total}}}}$\n" +
                f"= $\\frac{{{favorable_past}}}{{{total_past}}}$\n" +
                (f"= $\\frac{{{prob_num}}}{{{prob_den}}}$" if (prob_num, prob_den) != (favorable_past, total_past) else "") +
                f".\nThe experimental probability is $\\frac{{{prob_num}}}{{{prob_den}}}$"],
        ["3/6", "We can predict the outcome of the second set of trials by assuming that the ratio will be the same as in the first set of trials. " +
                "Write a proportion by setting the two ratios equal to each other, then solve."],
        ["4/6", f"$\\frac{{{prob_num}}}{{{prob_den}}} = \\frac{{n}}{{{total_future}}}$"],
        ["5/6", f"$\\frac{{{prob_num}}}{{{prob_den}}}({prob_den} \\cdot {total_future // prob_den}) = \\frac{{n}}{{{total_future}}}({prob_den} \\cdot {total_future // prob_den})  \\quad \\text{{Multiply both sides by }} ({prob_den} \\cdot {total_future // prob_den})$\n" +
                f"${prob_num} \\times {total_future // prob_den} = {prob_den if prob_den > 1 else ''}n \\quad \\text{{Simplify}}$\n" +
                f"${expected} = {prob_den if prob_den > 1 else ''}n \\quad \\text{{Simplify}}$" +
                (f"\n${expected // prob_den} = n \\quad \\text{{Divide both sides by {prob_den}}}$" if prob_den > 1 else "")],
        ["6/6", f"You would expect {expected} of the next {total_future} to have the desired outcome."]
    ]
    
    return variation

def main():
    """Main function to generate all variations"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_45_E4")
        return
    
    print(f"Found {len(templates)} template(s) for Gr6_45_E4")
    
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
    output_file = 'Gr6_45_E4_variations.json'
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