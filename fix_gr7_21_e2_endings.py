import json
import re

def fix_mixed_number_ending(question):
    """
    Fix question text endings for mixed number answers.
    Should end with "= _ _/_" not "Express your answer as a mixed number."
    """
    changes_made = False

    if question.get('question_type') == 'Multiple fill in the blank':
        correct_answers = question.get('correct_answers', [])
        q_text = question['question_text']

        # If there are 3 answers (mixed number format)
        if len(correct_answers) == 3:
            # Check if it needs fixing
            if '= _ _/_' not in q_text:
                # Remove "Express your answer as a mixed number." ending
                q_text = re.sub(r'\s*Express your answer as a mixed number\.\s*$', '', q_text)

                # Add the proper ending for mixed number answers
                q_text = q_text.strip() + ' = _ _/_'

                question['question_text'] = q_text
                changes_made = True

    return changes_made

# Fix Gr7_21_E2_edited.json
print("Fixing all Gr7_21_E2_edited.json question endings...")
with open('edited_by_tag/Gr7_21_E2/Gr7_21_E2_edited.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0
for question in data['quizzes']:
    if fix_mixed_number_ending(question):
        fixed_count += 1
        question_num = question.get('question_number', 'unknown')
        print(f"  Fixed question {question_num}")

with open('edited_by_tag/Gr7_21_E2/Gr7_21_E2_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nTotal questions fixed: {fixed_count}")
print("All questions now end with '= _ _/_' for mixed number answers!")
