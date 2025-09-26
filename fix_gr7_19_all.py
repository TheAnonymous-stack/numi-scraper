import json
import random

# Fix Gr7_19_E1 - understanding-exponents
with open('Gr7_19_E1_variations.json', 'r') as f:
    data = json.load(f)

for i, quiz in enumerate(data['quizzes']):
    # Generate varied bases and exponents
    base = random.randint(2, 10)
    exponent = random.randint(2, 5)

    # Create multiplication string
    mult_str = ' × '.join([str(base)] * exponent)

    quiz['question_text'] = f"Write the expression using an exponent.\n\n{mult_str} = ____^{{____}}"
    quiz['question_answer'] = f"{base}^{exponent}"

    # Update solution steps
    quiz['solution'] = [
        ["text", f"Count how many times {base} is multiplied by itself."],
        ["text", f"We have {base} multiplied {exponent} times."],
        ["text", f"This can be written as {base}^{{{exponent}}}."],
        ["text", f"So, {mult_str} = {base}^{{{exponent}}}"]
    ]

with open('Gr7_19_E1_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed Gr7_19_E1_variations.json")

# Fix Gr7_19_E2 - evaluate-powers
with open('Gr7_19_E2_variations.json', 'r') as f:
    data = json.load(f)

for i, quiz in enumerate(data['quizzes']):
    # Generate varied bases and exponents
    base = random.randint(2, 12)
    exponent = random.randint(2, 4)

    # Calculate the answer
    answer = base ** exponent

    quiz['question_text'] = f"Evaluate.\n\n{base}^{{{exponent}}} = ____"
    quiz['question_answer'] = str(answer)

    # Create multiplication string for solution
    mult_str = ' × '.join([str(base)] * exponent)

    # Update solution steps
    quiz['solution'] = [
        ["text", f"{base}^{{{exponent}}} means {base} multiplied by itself {exponent} times."],
        ["text", f"{base}^{{{exponent}}} = {mult_str}"],
        ["text", f"Let's calculate: {mult_str} = {answer}"],
        ["text", f"So, {base}^{{{exponent}}} = {answer}"]
    ]

with open('Gr7_19_E2_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed Gr7_19_E2_variations.json")

# Fix Gr7_19_E3 - solve-equations-with-variable-exponents
with open('Gr7_19_E3_variations.json', 'r') as f:
    data = json.load(f)

# Create a list of base-exponent pairs that give nice results
nice_pairs = [
    (2, 3, 8), (2, 4, 16), (2, 5, 32), (2, 6, 64),
    (3, 2, 9), (3, 3, 27), (3, 4, 81),
    (4, 2, 16), (4, 3, 64),
    (5, 2, 25), (5, 3, 125),
    (6, 2, 36), (7, 2, 49), (8, 2, 64), (9, 2, 81), (10, 2, 100),
    (2, 0, 1), (3, 0, 1), (5, 0, 1), (10, 0, 1),  # Powers of 0
    (1, 5, 1), (1, 10, 1), (1, 15, 1),  # Powers of 1
    (2, 7, 128), (2, 8, 256),
    (3, 5, 243),
    (11, 2, 121), (12, 2, 144)
]

# Shuffle for variety
random.shuffle(nice_pairs)

for i, quiz in enumerate(data['quizzes']):
    # Use pairs cyclically if we run out
    base, exponent, result = nice_pairs[i % len(nice_pairs)]

    quiz['question_text'] = f"Solve for s.\n\n{base}^{{s}} = {result}\n\ns = ____"
    quiz['question_answer'] = str(exponent)

    # Create solution steps based on the problem type
    if exponent == 0:
        quiz['solution'] = [
            ["text", f"We need to find what power of {base} equals {result}."],
            ["text", f"Any number raised to the power of 0 equals 1."],
            ["text", f"{base}^{{0}} = 1"],
            ["text", f"So, s = 0"]
        ]
    elif base == 1:
        quiz['solution'] = [
            ["text", f"We need to find what power of 1 equals 1."],
            ["text", f"1 raised to any power equals 1."],
            ["text", f"1^{{{exponent}}} = 1"],
            ["text", f"So, s = {exponent}"]
        ]
    else:
        # Create multiplication string for smaller exponents
        if exponent <= 4:
            mult_str = ' × '.join([str(base)] * exponent)
            quiz['solution'] = [
                ["text", f"We need to find what power of {base} equals {result}."],
                ["text", f"Let's think: {base}^{{s}} = {result}"],
                ["text", f"{base}^{{{exponent}}} = {mult_str} = {result}"],
                ["text", f"So, s = {exponent}"]
            ]
        else:
            # For larger exponents, build up
            quiz['solution'] = [
                ["text", f"We need to find what power of {base} equals {result}."],
                ["text", f"Let's calculate powers of {base}:"],
                ["text", f"{base}^2 = {base**2}, {base}^3 = {base**3}, ..."],
                ["text", f"{base}^{{{exponent}}} = {result}, so s = {exponent}"]
            ]

with open('Gr7_19_E3_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed Gr7_19_E3_variations.json")
print("All Week 19 files have been fixed with varied problems!")