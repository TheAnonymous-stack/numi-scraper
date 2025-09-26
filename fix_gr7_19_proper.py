import json
import random

# Fix Gr7_19_E1 - understanding-exponents
print("Fixing Gr7_19_E1...")
with open('Gr7_19_E1_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Parse the current messed up question to extract base and exponent
    question = quiz['question_text']
    if "×" in question:
        parts = question.split("=")[0].strip()
        parts = parts.replace("Write the expression using an exponent.\n\n", "")
        numbers = parts.split("×")
        base = numbers[0].strip()
        exponent = len(numbers)

        # Fix the fields properly
        quiz['question_text'] = f"Write the expression using an exponent.\n\n{parts} = ____^{{____}}"
        quiz['correct_answers'] = [f"{base}^{exponent}"]

        # Remove question_answer field if it exists
        if 'question_answer' in quiz:
            del quiz['question_answer']

        # Fix solution steps
        quiz['solution'] = [
            ["text", f"Count how many times {base} is multiplied by itself."],
            ["text", f"We have {base} multiplied {exponent} times."],
            ["text", f"This can be written as {base}^{{{exponent}}}."],
            ["text", f"So, {parts} = {base}^{{{exponent}}}"]
        ]

with open('Gr7_19_E1_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed Gr7_19_E1_variations.json")

# Fix Gr7_19_E2 - evaluate-powers
print("Fixing Gr7_19_E2...")
with open('Gr7_19_E2_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Extract base and exponent from question
    question = quiz['question_text']
    import re
    match = re.search(r'(\d+)\^{(\d+)}', question)
    if match:
        base = int(match.group(1))
        exponent = int(match.group(2))

        # Calculate correct answer
        answer = base ** exponent

        # Fix the fields properly
        quiz['question_text'] = f"Evaluate.\n\n{base}^{{{exponent}}} = ____"
        quiz['correct_answers'] = [str(answer)]

        # Remove question_answer field if it exists
        if 'question_answer' in quiz:
            del quiz['question_answer']

        # Fix solution steps
        mult_str = ' × '.join([str(base)] * exponent)
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
print("Fixing Gr7_19_E3...")
with open('Gr7_19_E3_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Extract base and result from question
    question = quiz['question_text']
    match = re.search(r'(\d+)\^{s}\s*=\s*(\d+)', question)
    if match:
        base = int(match.group(1))
        result = int(match.group(2))

        # Calculate the exponent
        if result == 1:
            if base == 1:
                exponent = 1  # Could be any exponent, but we'll use 1
            else:
                exponent = 0  # Any non-1 number^0 = 1
        else:
            # Find the correct exponent
            exponent = 0
            temp = 1
            while temp < result and exponent < 20:
                exponent += 1
                temp = base ** exponent
                if temp == result:
                    break

        # Fix the fields properly
        quiz['question_text'] = f"Solve for s.\n\n{base}^{{s}} = {result}\n\ns = ____"
        quiz['correct_answers'] = [str(exponent)]

        # Remove question_answer field if it exists
        if 'question_answer' in quiz:
            del quiz['question_answer']

        # Fix solution based on problem type
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
            if exponent <= 4:
                mult_str = ' × '.join([str(base)] * exponent)
                quiz['solution'] = [
                    ["text", f"We need to find what power of {base} equals {result}."],
                    ["text", f"Let's think: {base}^{{s}} = {result}"],
                    ["text", f"{base}^{{{exponent}}} = {mult_str} = {result}"],
                    ["text", f"So, s = {exponent}"]
                ]
            else:
                quiz['solution'] = [
                    ["text", f"We need to find what power of {base} equals {result}."],
                    ["text", f"Let's calculate powers of {base}:"],
                    ["text", f"{base}^2 = {base**2}, {base}^3 = {base**3}, ..."],
                    ["text", f"{base}^{{{exponent}}} = {result}, so s = {exponent}"]
                ]

with open('Gr7_19_E3_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed Gr7_19_E3_variations.json")
print("All three files have been properly fixed!")