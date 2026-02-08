import json
import re

def fix_mixed_number_question_format(question):
    """
    Fix questions with mixed number answers (3 correct_answers)
    to match the Gr7_5_E3 format with ending: = _ _/_
    """
    changes_made = False

    # Check if this is a "Multiple fill in the blank" with 3 answers (mixed number format)
    if question.get('question_type') == 'Multiple fill in the blank':
        correct_answers = question.get('correct_answers', [])

        # If there are exactly 3 answers, it's a mixed number answer
        if len(correct_answers) == 3:
            q_text = question['question_text']

            # Check if it needs fixing (doesn't already have the correct ending)
            if '= _ _/_' not in q_text:
                # Remove various old endings like "= ? Answer as a mixed fraction Express your answer in simplest form."
                q_text = re.sub(r'\s*=\s*\?\s*.*$', '', q_text)

                # Add the standard ending for mixed number answers
                q_text = q_text.strip() + ' = _ _/_'

                question['question_text'] = q_text
                changes_made = True

        # If there are exactly 2 answers, it's a simple fraction answer (numerator/denominator)
        elif len(correct_answers) == 2:
            q_text = question['question_text']

            # Check if it already has the correct ending
            if '$\\\\\\\\[1em]$\\n\\n_/_ ' not in q_text:
                # This should already be handled by the previous script
                # But let's make sure it has the right format
                if not q_text.endswith('$\\\\[1em]$\\n\\n_/_ '):
                    # Remove old endings
                    q_text = re.sub(r'\s*=\s*\?\s*.*$', '', q_text)

                    # Add the standard ending for simple fraction answers
                    q_text = q_text.strip() + ' = ? Write your answer in simplest terms. $\\\\[1em]$\\n\\n_/_ '

                    question['question_text'] = q_text
                    changes_made = True

    return changes_made

# Fix Gr7_17_E1_edited.json
print("Fixing Gr7_17_E1_edited.json to match Gr7_5_E3 format...")
with open('edited_by_tag/Gr7_17_E1/Gr7_17_E1_edited.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0
for question in data['quizzes']:
    if fix_mixed_number_question_format(question):
        fixed_count += 1
        num_answers = len(question.get('correct_answers', []))
        print(f"  Fixed question {question.get('question_number', 'unknown')} ({num_answers} answers)")

with open('edited_by_tag/Gr7_17_E1/Gr7_17_E1_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nTotal questions fixed: {fixed_count}")
