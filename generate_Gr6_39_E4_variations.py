import json
import random

def generate_variations():
    """Generate 51 variations for Gr6_39_E4 - word problem about learning items"""

    variations = []

    # Original template
    original = {
        "tag": "Gr6_39_E4",
        "question_number": "4_1",
        "question_text": "Before beginning voice lessons, Kaylee already knew how to sing 5 pieces, and she expects to learn 1 new piece during each week of lessons. How many weeks of lessons will Kaylee need before she will be able to sing a total of 46 pieces?",
        "question_type": "Fill in the blank",
        "correct_answers": ["41"],
        "solution": [
            ["1/5", "Extract the key information from the question: Kaylee currently knows 5 songs. She will learn 1 new song per week. We want to find how many more weeks of lessons are needed for Kaylee to know 46 songs in total."],
            ["2/5", "The number of songs Kaylee still needs to learn = The total number of songs Kaylee wants to know - The number of songs Kaylee already knows"],
            ["3/5", "The number of songs Kaylee still needs to learn = $46 - 5$ = $41$ songs"],
            ["4/5", "Number of weeks Kaylee needs = Number of weeks it takes Kaylee to learn a song $\\times$ Number of songs Kaylee still needs to learn"],
            ["5/5", "Number of weeks Kaylee needs = $1 \\times 41$ = $41$ weeks"]
        ],
        "solution_image_tag": []
    }

    variations.append(original)

    # Define contexts for variations
    contexts = [
        ("piano lessons", "Emma", "play", "songs", "song"),
        ("guitar lessons", "Jake", "play", "chords", "chord"),
        ("coding bootcamp", "Alex", "complete", "projects", "project"),
        ("art classes", "Sophie", "paint", "paintings", "painting"),
        ("dance lessons", "Maya", "perform", "routines", "routine"),
        ("karate training", "Ryan", "master", "katas", "kata"),
        ("chess coaching", "Diana", "learn", "openings", "opening"),
        ("magic lessons", "Harry", "perform", "tricks", "trick"),
        ("cooking classes", "Gordon", "prepare", "recipes", "recipe"),
        ("language school", "Carlos", "memorize", "vocabulary words", "word"),
        ("photography course", "Lisa", "edit", "photos", "photo"),
        ("swimming lessons", "Michael", "master", "strokes", "stroke"),
        ("yoga classes", "Priya", "perfect", "poses", "pose"),
        ("pottery workshop", "Clay", "create", "pieces", "piece"),
        ("origami classes", "Yuki", "fold", "designs", "design"),
        ("skateboarding lessons", "Tony", "land", "tricks", "trick"),
        ("basketball training", "LeBron", "master", "plays", "play"),
        ("violin lessons", "Mozart", "play", "concertos", "concerto"),
        ("drums lessons", "Ringo", "learn", "beats", "beat"),
        ("Pokémon training", "Ash", "catch", "Pokémon", "Pokémon"),
        ("Jedi training", "Luke", "master", "Force techniques", "technique"),
        ("ninja academy", "Naruto", "learn", "jutsu", "jutsu"),
        ("wizard school", "Hermione", "master", "spells", "spell"),
        ("superhero training", "Peter", "develop", "web-slinging moves", "move"),
        ("Minecraft tutorials", "Steve", "build", "structures", "structure"),
        ("Fortnite coaching", "Ninja", "master", "building techniques", "technique"),
        ("anime drawing class", "Sakura", "draw", "characters", "character"),
        ("manga workshop", "Goku", "create", "panels", "panel"),
        ("YouTube tutorials", "MrBeast", "produce", "videos", "video"),
        ("TikTok academy", "Charli", "choreograph", "dances", "dance"),
        ("game development", "Mario", "code", "levels", "level"),
        ("robotics club", "Wall-E", "program", "robots", "robot"),
        ("astronomy course", "Neil", "identify", "constellations", "constellation"),
        ("chemistry lab", "Walter", "complete", "experiments", "experiment"),
        ("biology class", "Darwin", "study", "species", "species"),
        ("math tutoring", "Einstein", "solve", "problems", "problem"),
        ("writing workshop", "Shakespeare", "write", "stories", "story"),
        ("debate club", "Lincoln", "prepare", "arguments", "argument"),
        ("theater class", "Hamilton", "memorize", "monologues", "monologue"),
        ("film school", "Spielberg", "direct", "scenes", "scene"),
        ("DJ lessons", "Marshmello", "mix", "tracks", "track"),
        ("beatbox training", "Beatbox", "perform", "rhythms", "rhythm"),
        ("parkour training", "Ezio", "complete", "courses", "course"),
        ("circus school", "Barnum", "perform", "acts", "act"),
        ("ventriloquism class", "Jeff", "master", "routines", "routine"),
        ("stand-up comedy", "Kevin", "write", "jokes", "joke"),
        ("improv classes", "Amy", "create", "scenes", "scene"),
        ("voice acting", "Tara", "record", "characters", "character"),
        ("animation course", "Walt", "animate", "sequences", "sequence")
    ]

    # Generate number combinations
    number_combinations = []
    for already_knows in range(2, 20):
        for rate in [1, 2, 3]:
            for total_target in range(already_knows + 10, already_knows + 100):
                weeks_needed = (total_target - already_knows) // rate
                if weeks_needed * rate == (total_target - already_knows) and weeks_needed > 5 and weeks_needed < 60:
                    number_combinations.append((already_knows, rate, total_target, weeks_needed))

    # Shuffle and select 50 combinations
    random.seed(42)
    random.shuffle(number_combinations)
    selected_combinations = number_combinations[:50]
    random.shuffle(contexts)

    for i in range(2, 52):
        already_knows, rate, total_target, weeks_needed = selected_combinations[i-2]
        context_idx = (i-2) % len(contexts)
        lesson_type, name, verb, items_plural, item_singular = contexts[context_idx]

        items_to_learn = total_target - already_knows

        # Adjust grammar for rate
        rate_text = f"{rate} new {items_plural}" if rate > 1 else f"{rate} new {item_singular}"
        time_period = "week" if rate == 1 else f"week"

        variation = {
            "tag": "Gr6_39_E4",
            "question_number": f"4_{i}",
            "question_text": f"Before beginning {lesson_type}, {name} already knew how to {verb} {already_knows} {items_plural}, and expects to learn {rate_text} during each {time_period} of lessons. How many weeks of lessons will {name} need before being able to {verb} a total of {total_target} {items_plural}?",
            "question_type": "Fill in the blank",
            "correct_answers": [str(weeks_needed)],
            "solution": [
                ["1/5", f"Extract the key information from the question: {name} currently knows {already_knows} {items_plural}. They will learn {rate_text} per week. We want to find how many weeks of lessons are needed for {name} to know {total_target} {items_plural} in total."],
                ["2/5", f"The number of {items_plural} {name} still needs to learn = The total number of {items_plural} {name} wants to know - The number of {items_plural} {name} already knows"],
                ["3/5", f"The number of {items_plural} {name} still needs to learn = ${total_target} - {already_knows}$ = ${items_to_learn}$ {items_plural}"],
                ["4/5", f"Number of weeks {name} needs = Number of {items_plural} {name} still needs to learn $\\div$ Number of {items_plural} learned per week"],
                ["5/5", f"Number of weeks {name} needs = ${items_to_learn} \\div {rate}$ = ${weeks_needed}$ weeks"]
            ],
            "solution_image_tag": []
        }

        variations.append(variation)

    return variations

if __name__ == "__main__":
    variations = generate_variations()

    # Save to file
    with open("Gr6_39_E4_variations.json", "w") as f:
        json.dump(variations, f, indent=2)

    print(f"Generated {len(variations)} variations for Gr6_39_E4")
    print(f"Saved to Gr6_39_E4_variations.json")