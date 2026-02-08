import json
import re

def fix_whole_number_answers(question):
    """
    Fix questions that have whole number answers to be consistent with mixed number format.
    A whole number like 7 should be represented as 7 0/1 in the answer blanks.
    But since we're asking for mixed numbers, whole numbers should still use 3-blank format.
    """
    changes_made = False

    # Check if this is a "Fill in the blank" question with 1 answer (whole number)
    if question.get('question_type') == 'Fill in the blank':
        correct_answers = question.get('correct_answers', [])

        # If there's exactly 1 answer and it's a whole number
        if len(correct_answers) == 1:
            whole_number = correct_answers[0]

            # Change to Multiple fill in the blank with 3 answers
            # For a whole number like 7, the mixed number representation is 7 0/1
            question['question_type'] = 'Multiple fill in the blank'
            question['correct_answers'] = [whole_number, "0", "1"]

            # Update question text - change ending to match mixed number format
            q_text = question['question_text']

            # Remove "Express your answer as a mixed number." and add the proper ending
            # The ending should be "= _ _/_" for mixed number answers
            if '= _ _/_' not in q_text:
                # Remove old ending
                q_text = re.sub(r'\s*Express your answer as a mixed number\.\s*$', '', q_text)
                # Add mixed number ending
                q_text = q_text.strip() + ' = _ _/_'
                question['question_text'] = q_text

            # Ensure orderMatter is set
            if 'orderMatter' not in question:
                question['orderMatter'] = True

            # Ensure has_alternate_answers is set
            if 'has_alternate_answers' not in question:
                question['has_alternate_answers'] = True

            changes_made = True

    return changes_made

# Fix Gr7_21_E2_edited.json
print("Fixing Gr7_21_E2_edited.json...")
with open('edited_by_tag/Gr7_21_E2/Gr7_21_E2_edited.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0
for question in data['quizzes']:
    if fix_whole_number_answers(question):
        fixed_count += 1
        question_num = question.get('question_number', 'unknown')
        whole_num = question['correct_answers'][0]
        print(f"  Fixed question {question_num} (whole number {whole_num} -> {whole_num} 0/1)")

with open('edited_by_tag/Gr7_21_E2/Gr7_21_E2_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nTotal questions fixed: {fixed_count}")
