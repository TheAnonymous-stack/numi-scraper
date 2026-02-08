import json
import re

def split_fraction_answer(fraction_str):
    """
    Split a fraction answer like "-37/66" into ["-37", "66"]
    or "47/12" into ["47", "12"]
    """
    if '/' in fraction_str:
        parts = fraction_str.split('/')
        return [parts[0], parts[1]]
    return None

def fix_question_format(question):
    """
    Fix a question to have proper format:
    - Change question_type to "Multiple fill in the blank"
    - Split fraction answers into numerator/denominator
    - Add proper ending to question_text with $\\\\[1em]$\n\n_/_
    """
    changes_made = False

    # Check if this is a "Fill in the blank" question with a fraction answer
    if question.get('question_type') == 'Fill in the blank':
        correct_answers = question.get('correct_answers', [])

        # If there's exactly 1 answer and it contains a '/', it's a fraction
        if len(correct_answers) == 1 and '/' in correct_answers[0]:
            fraction_parts = split_fraction_answer(correct_answers[0])

            if fraction_parts:
                # Update question type
                question['question_type'] = 'Multiple fill in the blank'

                # Update correct answers
                question['correct_answers'] = fraction_parts

                # Update question text to have proper ending
                q_text = question['question_text']

                # Remove various old endings and add the standard one
                # Remove patterns like "= ?" or "= ? Answer as a mixed fraction"
                q_text = re.sub(r'\s*=\s*\?\s*.*$', '', q_text)

                # Add the standard ending
                q_text = q_text.strip() + ' = ? Write your answer in simplest terms. $\\\\[1em]$\n\n_/_ '

                question['question_text'] = q_text

                # Add orderMatter if not present
                if 'orderMatter' not in question:
                    question['orderMatter'] = True

                changes_made = True

    return changes_made

# Fix Gr7_17_E1_edited.json
print("Fixing Gr7_17_E1_edited.json...")
with open('edited_by_tag/Gr7_17_E1/Gr7_17_E1_edited.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0
for question in data['quizzes']:
    if fix_question_format(question):
        fixed_count += 1
        print(f"  Fixed question {question.get('question_number', 'unknown')}")

with open('edited_by_tag/Gr7_17_E1/Gr7_17_E1_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nTotal questions fixed: {fixed_count}")
