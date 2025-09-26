import json

# Fix Gr7_19_E1
print("Fixing Gr7_19_E1...")
with open('Gr7_19_E1_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Copy question_answer to correct_answers if question_answer exists
    if 'question_answer' in quiz:
        quiz['correct_answers'] = [quiz['question_answer']]
        del quiz['question_answer']

with open('Gr7_19_E1_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E1_variations.json - {len(data['quizzes'])} entries")

# Fix Gr7_19_E2
print("Fixing Gr7_19_E2...")
with open('Gr7_19_E2_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Copy question_answer to correct_answers if question_answer exists
    if 'question_answer' in quiz:
        quiz['correct_answers'] = [quiz['question_answer']]
        del quiz['question_answer']

with open('Gr7_19_E2_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E2_variations.json - {len(data['quizzes'])} entries")

# Fix Gr7_19_E3
print("Fixing Gr7_19_E3...")
with open('Gr7_19_E3_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Copy question_answer to correct_answers if question_answer exists
    if 'question_answer' in quiz:
        quiz['correct_answers'] = [quiz['question_answer']]
        del quiz['question_answer']

with open('Gr7_19_E3_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E3_variations.json - {len(data['quizzes'])} entries")
print("All three files have been fixed!")