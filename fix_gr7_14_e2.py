import json
import os

def fix_gr7_14_e2():
    """Fix Gr7_14_E2: remove duplicate instruction text"""
    filepath = os.path.join('edited_by_tag', 'Gr7_14_E2', 'Gr7_14_E2_edited.json')

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for question in data['quizzes']:
        q_text = question['question_text']

        # Remove duplicate instruction text
        # Replace "Express your answer in simplest form. Write your answer in simplest terms."
        # with just "Write your answer in simplest terms."
        q_text = q_text.replace(
            'Express your answer in simplest form. Write your answer in simplest terms.',
            'Write your answer in simplest terms.'
        )

        question['question_text'] = q_text

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Fixed Gr7_14_E2_edited.json")
    print("- Removed duplicate instruction text")

if __name__ == "__main__":
    fix_gr7_14_e2()
