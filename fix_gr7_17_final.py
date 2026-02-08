import json
import re

def fix_question_ending(question):
    """
    Fix question text endings based on number of answers:
    - 2 answers (simple fraction): ending should be "= ? Write your answer in simplest terms. $\\\\[1em]$\\n\\n_/_ "
    - 3 answers (mixed number): ending should be "= _ _/_"
    """
    changes_made = False

    if question.get('question_type') == 'Multiple fill in the blank':
        correct_answers = question.get('correct_answers', [])
        q_text = question['question_text']

        if len(correct_answers) == 3:
            # Mixed number answer - should end with "= _ _/_"
            # Remove everything after the equals sign and standardize
            if '= _ _/_' in q_text:
                # Already correct, check if it has extra stuff
                parts = q_text.split('= _ _/_')
                if len(parts) > 1 and parts[1].strip():
                    # Has extra text after the correct ending
                    q_text = parts[0] + '= _ _/_'
                    question['question_text'] = q_text
                    changes_made = True
            else:
                # Needs fixing - remove old ending and add correct one
                q_text = re.sub(r'\s*=\s*.*$', '', q_text)
                q_text = q_text.strip() + ' = _ _/_'
                question['question_text'] = q_text
                changes_made = True

        elif len(correct_answers) == 2:
            # Simple fraction answer - should end with specific format
            correct_ending = ' = ? Write your answer in simplest terms. $\\\\[1em]$\\n\\n_/_ '

            if not q_text.endswith(correct_ending.strip()):
                # Remove old ending
                q_text = re.sub(r'\s*=\s*.*$', '', q_text)
                q_text = q_text.strip() + correct_ending
                question['question_text'] = q_text
                changes_made = True

    return changes_made

# Fix Gr7_17_E1_edited.json
print("Fixing Gr7_17_E1_edited.json final format...")
with open('edited_by_tag/Gr7_17_E1/Gr7_17_E1_edited.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0
for question in data['quizzes']:
    if fix_question_ending(question):
        fixed_count += 1
        num_answers = len(question.get('correct_answers', []))
        answer_type = "mixed number" if num_answers == 3 else "simple fraction"
        print(f"  Fixed question {question.get('question_number', 'unknown')} ({answer_type})")

with open('edited_by_tag/Gr7_17_E1/Gr7_17_E1_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nTotal questions fixed: {fixed_count}")
