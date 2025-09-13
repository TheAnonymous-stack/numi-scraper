import json
import random

def add_data_to_questions(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Different data sets for mode questions
    data_sets = [
        # Single mode examples
        {
            "context": "The library tracked book genres checked out",
            "data": "Mystery: 12, Romance: 18, Sci-fi: 15, Fantasy: 18, Biography: 10",
            "choices": ["mystery", "romance", "sci-fi", "fantasy", "biography"],
            "answer": [["B"], ["D"]],  # romance and fantasy both 18
            "solution": "Romance and Fantasy were both checked out 18 times, which is more than any other genre. So both are modes."
        },
        {
            "context": "Students voted for their favorite subject",
            "data": "Math: 15, Science: 12, English: 8, History: 10, Art: 15",
            "choices": ["math", "science", "English", "history", "art"],
            "answer": [["A"], ["E"]],  # math and art
            "solution": "Math and Art both received 15 votes, which is more than any other subject. So both are modes."
        },
        {
            "context": "Ice cream shop tracked flavors sold",
            "data": "Strawberry: 4, Mint: 6, Toffee: 4, Chocolate: 8, Vanilla: 8",
            "choices": ["strawberry", "mint", "toffee", "chocolate", "vanilla"],
            "answer": [["D"], ["E"]],  # chocolate and vanilla
            "solution": "Chocolate and Vanilla were both sold 8 times, which is more than any other flavor. So both are modes."
        },
        {
            "context": "Animal shelter tracked pet adoptions",
            "data": "Dogs: 25, Cats: 20, Birds: 8, Rabbits: 12, Fish: 10",
            "choices": ["dogs", "cats", "birds", "rabbits", "fish"],
            "answer": ["A"],  # dogs only
            "solution": "Dogs were adopted 25 times, which is more than any other pet. So dogs is the mode."
        },
        {
            "context": "Cafeteria tracked lunch choices",
            "data": "Pizza: 30, Burger: 22, Salad: 18, Pasta: 30, Sandwich: 15",
            "choices": ["pizza", "burger", "salad", "pasta", "sandwich"],
            "answer": [["A"], ["D"]],  # pizza and pasta
            "solution": "Pizza and Pasta were both chosen 30 times, which is more than any other option. So both are modes."
        },
        {
            "context": "Sports club tracked activity preferences",
            "data": "Basketball: 14, Soccer: 16, Tennis: 11, Swimming: 16, Running: 9",
            "choices": ["basketball", "soccer", "tennis", "swimming", "running"],
            "answer": [["B"], ["D"]],  # soccer and swimming
            "solution": "Soccer and Swimming both had 16 participants, which is more than any other activity. So both are modes."
        },
        {
            "context": "Music store tracked instrument rentals",
            "data": "Guitar: 22, Piano: 18, Drums: 15, Violin: 22, Flute: 12",
            "choices": ["guitar", "piano", "drums", "violin", "flute"],
            "answer": [["A"], ["D"]],  # guitar and violin
            "solution": "Guitar and Violin were both rented 22 times, which is more than any other instrument. So both are modes."
        },
        {
            "context": "Game store tracked board game sales",
            "data": "Chess: 13, Checkers: 17, Monopoly: 20, Scrabble: 17, Risk: 8",
            "choices": ["chess", "checkers", "monopoly", "scrabble", "risk"],
            "answer": ["C"],  # monopoly only
            "solution": "Monopoly was sold 20 times, which is more than any other game. So Monopoly is the mode."
        },
        {
            "context": "Theater tracked movie genre preferences",
            "data": "Action: 28, Comedy: 35, Drama: 24, Horror: 19, Romance: 35",
            "choices": ["action", "comedy", "drama", "horror", "romance"],
            "answer": [["B"], ["E"]],  # comedy and romance
            "solution": "Comedy and Romance were both chosen 35 times, which is more than any other genre. So both are modes."
        },
        {
            "context": "School tracked club memberships",
            "data": "Science: 18, Drama: 24, Art: 20, Chess: 16, Debate: 24",
            "choices": ["science", "drama", "art", "chess", "debate"],
            "answer": [["B"], ["E"]],  # drama and debate
            "solution": "Drama and Debate both have 24 members, which is more than any other club. So both are modes."
        },
        {
            "context": "Bakery tracked pastry sales",
            "data": "Croissant: 32, Donut: 28, Muffin: 32, Bagel: 25, Danish: 20",
            "choices": ["croissant", "donut", "muffin", "bagel", "danish"],
            "answer": [["A"], ["C"]],  # croissant and muffin
            "solution": "Croissant and Muffin were both sold 32 times, which is more than any other pastry. So both are modes."
        },
        {
            "context": "Zoo tracked favorite animal exhibits",
            "data": "Lions: 45, Penguins: 52, Elephants: 38, Monkeys: 52, Giraffes: 40",
            "choices": ["lions", "penguins", "elephants", "monkeys", "giraffes"],
            "answer": [["B"], ["D"]],  # penguins and monkeys
            "solution": "Penguins and Monkeys both had 52 visitors, which is more than any other exhibit. So both are modes."
        },
        {
            "context": "Restaurant tracked dessert orders",
            "data": "Cake: 19, Pie: 23, Ice cream: 26, Pudding: 23, Cookies: 15",
            "choices": ["cake", "pie", "ice cream", "pudding", "cookies"],
            "answer": ["C"],  # ice cream only
            "solution": "Ice cream was ordered 26 times, which is more than any other dessert. So ice cream is the mode."
        },
        {
            "context": "Gym tracked workout class attendance",
            "data": "Yoga: 28, Pilates: 21, Spin: 28, Zumba: 25, Boxing: 18",
            "choices": ["yoga", "pilates", "spin", "zumba", "boxing"],
            "answer": [["A"], ["C"]],  # yoga and spin
            "solution": "Yoga and Spin both had 28 attendees, which is more than any other class. So both are modes."
        },
        {
            "context": "Art class tracked medium preferences",
            "data": "Pencil: 11, Paint: 14, Charcoal: 9, Pastel: 14, Marker: 7",
            "choices": ["pencil", "paint", "charcoal", "pastel", "marker"],
            "answer": [["B"], ["D"]],  # paint and pastel
            "solution": "Paint and Pastel were both chosen by 14 students, which is more than any other medium. So both are modes."
        },
        {
            "context": "Tech store tracked device sales",
            "data": "Laptop: 34, Tablet: 29, Phone: 41, Watch: 22, Headphones: 41",
            "choices": ["laptop", "tablet", "phone", "watch", "headphones"],
            "answer": [["C"], ["E"]],  # phone and headphones
            "solution": "Phone and Headphones were both sold 41 times, which is more than any other device. So both are modes."
        },
        {
            "context": "Park tracked recreational activities",
            "data": "Walking: 55, Jogging: 42, Cycling: 38, Picnic: 55, Sports: 35",
            "choices": ["walking", "jogging", "cycling", "picnic", "sports"],
            "answer": [["A"], ["D"]],  # walking and picnic
            "solution": "Walking and Picnic both had 55 participants, which is more than any other activity. So both are modes."
        },
        {
            "context": "Bookstore tracked genre preferences",
            "data": "Fiction: 48, Non-fiction: 36, Poetry: 22, Comics: 31, Magazines: 48",
            "choices": ["fiction", "non-fiction", "poetry", "comics", "magazines"],
            "answer": [["A"], ["E"]],  # fiction and magazines
            "solution": "Fiction and Magazines were both chosen 48 times, which is more than any other category. So both are modes."
        },
        {
            "context": "Coffee shop tracked drink orders",
            "data": "Latte: 62, Cappuccino: 58, Espresso: 45, Mocha: 62, Tea: 38",
            "choices": ["latte", "cappuccino", "espresso", "mocha", "tea"],
            "answer": [["A"], ["D"]],  # latte and mocha
            "solution": "Latte and Mocha were both ordered 62 times, which is more than any other drink. So both are modes."
        },
        {
            "context": "School tracked transportation methods",
            "data": "Bus: 85, Car: 72, Walk: 85, Bike: 45, Carpool: 38",
            "choices": ["bus", "car", "walk", "bike", "carpool"],
            "answer": [["A"], ["C"]],  # bus and walk
            "solution": "Bus and Walk were both used by 85 students, which is more than any other method. So both are modes."
        },
        {
            "context": "Garden center tracked plant sales",
            "data": "Roses: 27, Tulips: 31, Daisies: 24, Sunflowers: 31, Lilies: 19",
            "choices": ["roses", "tulips", "daisies", "sunflowers", "lilies"],
            "answer": [["B"], ["D"]],  # tulips and sunflowers
            "solution": "Tulips and Sunflowers were both sold 31 times, which is more than any other flower. So both are modes."
        },
        {
            "context": "Gaming cafe tracked game preferences",
            "data": "RPG: 16, FPS: 21, Strategy: 18, Sports: 21, Puzzle: 13",
            "choices": ["RPG", "FPS", "strategy", "sports", "puzzle"],
            "answer": [["B"], ["D"]],  # FPS and sports
            "solution": "FPS and Sports games were both played 21 times, which is more than any other genre. So both are modes."
        },
        {
            "context": "Clothing store tracked color preferences",
            "data": "Black: 44, Blue: 37, White: 44, Red: 29, Green: 22",
            "choices": ["black", "blue", "white", "red", "green"],
            "answer": [["A"], ["C"]],  # black and white
            "solution": "Black and White were both chosen 44 times, which is more than any other color. So both are modes."
        },
        {
            "context": "Food truck tracked menu item sales",
            "data": "Tacos: 38, Burritos: 38, Quesadilla: 25, Nachos: 32, Salad: 18",
            "choices": ["tacos", "burritos", "quesadilla", "nachos", "salad"],
            "answer": [["A"], ["B"]],  # tacos and burritos
            "solution": "Tacos and Burritos were both sold 38 times, which is more than any other item. So both are modes."
        },
        {
            "context": "Aquarium tracked favorite sea creatures",
            "data": "Sharks: 29, Dolphins: 36, Turtles: 36, Rays: 24, Jellyfish: 20",
            "choices": ["sharks", "dolphins", "turtles", "rays", "jellyfish"],
            "answer": [["B"], ["C"]],  # dolphins and turtles
            "solution": "Dolphins and Turtles were both chosen by 36 visitors, which is more than any other creature. So both are modes."
        }
    ]
    
    # Create more variations by modifying the numbers
    extended_data_sets = []
    for dataset in data_sets:
        extended_data_sets.append(dataset)
        
        # Create a variation with different numbers but same pattern
        if len(extended_data_sets) < 51:
            new_dataset = dataset.copy()
            # Parse the data string and modify numbers
            data_parts = new_dataset["data"].split(", ")
            new_parts = []
            for part in data_parts:
                label, value = part.split(": ")
                new_value = int(value) + random.randint(5, 15)
                new_parts.append(f"{label}: {new_value}")
            new_dataset["data"] = ", ".join(new_parts)
            extended_data_sets.append(new_dataset)
    
    # Apply to each quiz
    for i, quiz in enumerate(data['quizzes']):
        if i < len(extended_data_sets):
            dataset = extended_data_sets[i]
            
            # Update question text with actual data
            quiz['question_text'] = f"{dataset['context']}.\\n{dataset['data']}\\nPick the mode of this data set. There may be more than one.=_"
            
            # Update choices
            quiz['choices'] = dataset['choices']
            
            # Update correct answers
            quiz['correct_answers'] = dataset['answer']
            
            # Update solution
            quiz['solution'] = [
                ["1/3", "Remember, the mode is the value that occurs most often in a data set."],
                ["2/3", f"Look at the data: {dataset['data']}"],
                ["3/3", dataset['solution']]
            ]
            
            # Remove image-related fields
            if 'image_tag' in quiz:
                del quiz['image_tag']
            if 'backend_description' in quiz:
                del quiz['backend_description']
            if 'solution_image_tag' in quiz:
                del quiz['solution_image_tag']
            
            # Update question type based on whether there's one or multiple modes
            if isinstance(dataset['answer'], list) and len(dataset['answer']) > 1:
                quiz['question_type'] = "Multiple Choice with Multiple Answers"
                quiz['has_alternate_answers'] = True
            else:
                quiz['question_type'] = "Multiple Choice Question with Single Answer"
                quiz['has_alternate_answers'] = False
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added data to question text in {filename}")

# Process the file
add_data_to_questions('Gr6_42_E2_variations.json')