import json
import re
import os

def fix_gr7_13_e1():
    """Fix Gr7_13_E1: convert fractions to LaTeX and remove duplicate instruction text"""
    filepath = os.path.join('edited_by_tag', 'Gr7_13_E1', 'Gr7_13_E1_edited.json')

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for question in data['quizzes']:
        q_text = question['question_text']

        # Convert fractions like $6/7$ to LaTeX format $\frac{6}{7}$
        # Match patterns like $1/5$ or $11/9$
        q_text = re.sub(r'\$(\d+)/(\d+)\$', r'$\\frac{\1}{\2}$', q_text)

        # Remove duplicate instruction text
        # Replace "Express your answer in simplest form. Write your answer in simplest terms."
        # with just "Write your answer in simplest terms."
        q_text = q_text.replace(
            'Express your answer in simplest form. Write your answer in simplest terms.',
            'Write your answer in simplest terms.'
        )

        # Also handle case where only "Express your answer in simplest form." appears
        if 'Write your answer in simplest terms.' not in q_text:
            q_text = q_text.replace(
                'Express your answer in simplest form.',
                'Write your answer in simplest terms.'
            )

        question['question_text'] = q_text

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Fixed Gr7_13_E1_edited.json")
    print("- Converted fractions to LaTeX format")
    print("- Removed duplicate instruction text")

if __name__ == "__main__":
    fix_gr7_13_e1()
