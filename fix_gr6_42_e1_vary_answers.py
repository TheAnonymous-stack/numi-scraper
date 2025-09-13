import json

def vary_discrete_continuous_answers(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Examples of discrete variables (countable)
    discrete_examples = [
        ("N is the number of students in a classroom.", "students can be counted"),
        ("X is the number of cars in a parking lot.", "cars can be counted"),
        ("M is the number of books on a shelf.", "books can be counted"),
        ("K is the number of coins in a jar.", "coins can be counted"),
        ("P is the number of pets in a household.", "pets can be counted"),
        ("R is the number of rooms in a house.", "rooms can be counted"),
        ("S is the shoe size of a person.", "shoe sizes come in specific values like 7, 7.5, 8"),
        ("G is the grade level of a student.", "grade levels are distinct values like 1, 2, 3"),
        ("D is the number of days in a month.", "days are countable whole numbers"),
        ("T is the number of trees in a park.", "trees can be counted"),
        ("C is the number of chairs in a room.", "chairs can be counted"),
        ("B is the number of buttons on a shirt.", "buttons can be counted"),
        ("F is the number of fingers on a hand.", "fingers can be counted"),
        ("W is the number of windows in a building.", "windows can be counted"),
        ("L is the number of letters in a word.", "letters can be counted"),
        ("E is the number of eggs in a carton.", "eggs can be counted"),
        ("H is the number of hours worked in a week.", "hours worked are typically counted in whole or half hours"),
        ("V is the number of votes in an election.", "votes can be counted"),
        ("Q is the number of questions on a test.", "questions can be counted"),
        ("Z is the zip code of an address.", "zip codes are specific discrete values"),
        ("A is the age in years of a person.", "age in years is counted in whole numbers"),
        ("I is the ID number of a student.", "ID numbers are discrete values"),
        ("O is the number of oranges in a basket.", "oranges can be counted"),
        ("U is the number of umbrellas sold.", "umbrellas can be counted"),
        ("J is the jersey number of a player.", "jersey numbers are discrete values")
    ]
    
    # Examples of continuous variables (measurable)
    continuous_examples = [
        ("W is the height of a building.", "height can take any value in a range"),
        ("Y is the weight of a package.", "weight can take any value in a range"),
        ("X is the temperature outside.", "temperature can vary continuously"),
        ("T is the time it takes to run a mile.", "time can take any value in a range"),
        ("D is the distance between two cities.", "distance can take any value in a range"),
        ("V is the volume of water in a tank.", "volume can vary continuously"),
        ("S is the speed of a car.", "speed can take any value in a range"),
        ("L is the length of a rope.", "length can take any value in a range"),
        ("A is the area of a room.", "area can take any value in a range"),
        ("P is the pressure in a tire.", "pressure can vary continuously"),
        ("H is the humidity in the air.", "humidity can vary continuously"),
        ("R is the radius of a circle.", "radius can take any value in a range"),
        ("M is the mass of an object.", "mass can take any value in a range"),
        ("E is the electricity usage in kilowatts.", "electricity usage can vary continuously"),
        ("F is the fuel consumption of a car.", "fuel consumption can vary continuously"),
        ("C is the concentration of a solution.", "concentration can vary continuously"),
        ("B is the brightness of a light.", "brightness can vary continuously"),
        ("N is the noise level in decibels.", "noise level can vary continuously"),
        ("G is the growth rate of a plant.", "growth rate can vary continuously"),
        ("I is the intensity of rainfall.", "rainfall intensity can vary continuously"),
        ("O is the oxygen level in blood.", "oxygen level can vary continuously"),
        ("U is the UV index.", "UV index can vary continuously"),
        ("Q is the quantity of paint needed.", "paint quantity can vary continuously"),
        ("K is the kinetic energy of an object.", "kinetic energy can vary continuously"),
        ("Z is the zoom level of a camera.", "zoom can vary continuously"),
        ("J is the juice extracted from oranges in liters.", "juice volume can vary continuously")
    ]
    
    # Create a mixed pattern
    # Pattern: 2 continuous, 1 discrete, repeat (gives roughly 1/3 discrete, 2/3 continuous)
    quiz_index = 0
    discrete_idx = 0
    continuous_idx = 0
    
    # Apply the pattern to the quizzes
    for i, quiz in enumerate(data['quizzes']):
        # Use pattern: every 3rd question is discrete, others are continuous
        if i % 3 == 2 and discrete_idx < len(discrete_examples):  # Every third question is discrete
            example = discrete_examples[discrete_idx]
            quiz['question_text'] = example[0] + "\\nIs the random variable " + example[0][0] + " discrete or continuous?=_"
            quiz['correct_answers'] = ["A"]  # discrete
            quiz['solution'][1][1] = f"This is a discrete random variable because {example[1]}. Discrete variables take countable values."
            discrete_idx += 1
        elif continuous_idx < len(continuous_examples):  # Others are continuous
            example = continuous_examples[continuous_idx]
            quiz['question_text'] = example[0] + "\\nIs the random variable " + example[0][0] + " discrete or continuous?=_"
            quiz['correct_answers'] = ["B"]  # continuous
            quiz['solution'][1][1] = f"This is a continuous random variable because {example[1]}."
            continuous_idx += 1
        else:  # Fallback if we run out of examples
            # Use remaining discrete examples
            if discrete_idx < len(discrete_examples):
                example = discrete_examples[discrete_idx]
                quiz['question_text'] = example[0] + "\\nIs the random variable " + example[0][0] + " discrete or continuous?=_"
                quiz['correct_answers'] = ["A"]  # discrete
                quiz['solution'][1][1] = f"This is a discrete random variable because {example[1]}. Discrete variables take countable values."
                discrete_idx += 1
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Varied discrete/continuous answers in {filename}")

# Process the file
vary_discrete_continuous_answers('Gr6_42_E1_variations.json')