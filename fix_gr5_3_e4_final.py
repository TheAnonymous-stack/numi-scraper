import json
import re

# Read the edited file
print("Reading Gr5_3_E4_edited.json...")
with open('edited_by_tag/Gr5_3_E4/Gr5_3_E4_edited.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['quizzes']

# Fix mixed number questions - remove the repeated fraction before = _ _/_
print("Fixing mixed number question formats...")
fixed_count = 0
for question in questions:
    q_text = question['question_text']

    # Check if this is a mixed number question (3 answers)
    if len(question['correct_answers']) == 3:
        # Remove the fraction display before = _ _/_
        # Pattern: \n$\\frac{X}{Y}$ = _ _/_
        # Replace with: = _ _/_
        new_text = re.sub(r'\\n\$\\\\frac\{(\d+)\}\{(\d+)\}\$ =', ' =', q_text)

        if new_text != q_text:
            question['question_text'] = new_text
            fixed_count += 1

print(f"Fixed {fixed_count} mixed number questions")

# Write back to the file
print("Writing updated file...")
with open('edited_by_tag/Gr5_3_E4/Gr5_3_E4_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nSuccessfully updated Gr5_3_E4_edited.json")

# Print example
print("\nExample fixed mixed number question:")
mixed_example = [q for q in questions if len(q['correct_answers']) == 3][0]
print(f"  Text: {mixed_example['question_text']}")
print(f"  Answers: {mixed_example['correct_answers']}")
