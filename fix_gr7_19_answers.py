import json
import random

# Fix Gr7_19_E1 - understanding-exponents
with open('Gr7_19_E1_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Fix the question_answer to match what's in the question
    # Parse the question to extract base and exponent
    question = quiz['question_text']

    # Extract the repeated multiplication part
    if "×" in question:
        parts = question.split("=")[0].strip()
        numbers = parts.split("×")
        base = numbers[0].strip()
        exponent = len(numbers)

        # Fix question_answer and correct_answers
        answer = f"{base}^{{{exponent}}}"
        quiz['question_answer'] = f"{base}^{exponent}"
        quiz['correct_answers'] = [f"{base}^{exponent}"]

        # Fix solution to match
        quiz['solution'][2][1] = f"This can be written as {base}^{{{exponent}}}."
        quiz['solution'][3][1] = f"So, {parts} = {base}^{{{exponent}}}"

with open('Gr7_19_E1_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed Gr7_19_E1_variations.json")

# Fix Gr7_19_E2 - evaluate-powers
with open('Gr7_19_E2_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Extract base and exponent from question_text
    question = quiz['question_text']
    # Format is "Evaluate.\n\nX^{Y} = ____"
    import re
    match = re.search(r'(\d+)\^{(\d+)}', question)
    if match:
        base = int(match.group(1))
        exponent = int(match.group(2))

        # Calculate correct answer
        answer = base ** exponent

        # Fix question_answer and correct_answers
        quiz['question_answer'] = str(answer)
        quiz['correct_answers'] = [str(answer)]

        # Fix solution steps
        mult_str = ' × '.join([str(base)] * exponent)
        quiz['solution'][0][1] = f"{base}^{{{exponent}}} means {base} multiplied by itself {exponent} times."
        quiz['solution'][1][1] = f"{base}^{{{exponent}}} = {mult_str}"
        quiz['solution'][2][1] = f"Let's calculate: {mult_str} = {answer}"
        quiz['solution'][3][1] = f"So, {base}^{{{exponent}}} = {answer}"

with open('Gr7_19_E2_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed Gr7_19_E2_variations.json")

# Fix Gr7_19_E3 - solve-equations-with-variable-exponents
with open('Gr7_19_E3_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Extract base and result from question_text
    question = quiz['question_text']
    # Format is "Solve for s.\n\nX^{s} = Y\n\ns = ____"
    match = re.search(r'(\d+)\^{s}\s*=\s*(\d+)', question)
    if match:
        base = int(match.group(1))
        result = int(match.group(2))

        # Calculate the exponent
        if result == 1:
            if base == 1:
                exponent = 1  # 1^1 = 1, could be any exponent
            else:
                exponent = 0  # any non-1 number^0 = 1
        else:
            # Find the exponent
            exponent = 0
            temp = 1
            while temp < result and exponent < 20:
                exponent += 1
                temp = base ** exponent
                if temp == result:
                    break

        # Fix question_answer and correct_answers
        quiz['question_answer'] = str(exponent)
        quiz['correct_answers'] = [str(exponent)]

        # Update solution based on the problem type
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
print("All Week 19 files have been fixed with correct answers!")