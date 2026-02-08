import json
import os

def fix_gr7_14_e2():
    """Fix Gr7_14_E2: Remove the broken = ____$ part and format like other Gr7 files"""

    # Fix both the source file and edited file
    files_to_fix = [
        'Gr7_14_E2_variations.json',
        os.path.join('edited_by_tag', 'Gr7_14_E2', 'Gr7_14_E2_edited.json')
    ]

    for filepath in files_to_fix:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for question in data['quizzes']:
            q_text = question['question_text']

            # Remove the broken = ____$ part completely
            # Replace patterns like "= \\_\\_\\_\\_$." with just ""
            q_text = q_text.replace(' = \\_\\_\\_\\_$.', '.')
            q_text = q_text.replace(' = \\_\\_\\_\\_$', '')

            # The format should be like other Gr7 files:
            # "Operation.\n\n$\frac{a}{b} + \frac{c}{d}$. Write your answer in simplest terms. $\\[1em]$\n\n_/_ "

            question['question_text'] = q_text

        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Fixed {filepath}")

if __name__ == "__main__":
    fix_gr7_14_e2()
    print("\nAll Gr7_14_E2 files fixed!")
    print("- Removed broken = ____$ formatting")
    print("- Now matches other Grade 7 file formats")
