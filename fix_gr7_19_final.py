import json

# Fix Gr7_19_E1 - understanding-exponents
print("Fixing Gr7_19_E1...")
with open('Gr7_19_E1_variations.json', 'r') as f:
    data = json.load(f)

for quiz in data['quizzes']:
    # Get the correct answer from question_answer field
    if 'question_answer' in quiz:
        correct_answer = quiz['question_answer']
        # Set correct_answers to this value
        quiz['correct_answers'] = [correct_answer]
        # Remove question_answer field
        del quiz['question_answer']

with open('Gr7_19_E1_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E1_variations.json - {len(data['quizzes'])} entries")

# Fix Gr7_19_E2 - evaluate-powers
print("Fixing Gr7_19_E2...")
with open('Gr7_19_E2_variations.json', 'r') as f:
    data = json.load(f)

# E2 already has correct correct_answers field, just need to remove question_answer if it exists
for quiz in data['quizzes']:
    if 'question_answer' in quiz:
        del quiz['question_answer']

with open('Gr7_19_E2_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E2_variations.json - {len(data['quizzes'])} entries")

# Fix Gr7_19_E3 - solve-equations-with-variable-exponents
print("Fixing Gr7_19_E3...")
with open('Gr7_19_E3_variations.json', 'r') as f:
    data = json.load(f)

# E3 already has correct correct_answers field, just need to remove question_answer if it exists
for quiz in data['quizzes']:
    if 'question_answer' in quiz:
        del quiz['question_answer']

with open('Gr7_19_E3_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_19_E3_variations.json - {len(data['quizzes'])} entries")
print("All three files have been fixed!")