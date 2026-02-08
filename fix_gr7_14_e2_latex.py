import json
import os

def fix_gr7_14_e2():
    """Fix Gr7_14_E2: Fix LaTeX rendering and remove duplicate instruction text"""

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

            # Fix the LaTeX: Replace $\\\\\\\\[1em]$ with $\\\\[1em]$
            # The issue is 4 backslashes (\\\\\\\\) should be 2 backslashes (\\\\)
            q_text = q_text.replace('$\\\\\\\\[1em]$', '$\\\\[1em]$')

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

        print(f"Fixed {filepath}")

if __name__ == "__main__":
    fix_gr7_14_e2()
    print("\nAll Gr7_14_E2 files fixed!")
    print("- Fixed LaTeX rendering (reduced backslashes)")
    print("- Removed duplicate instruction text")
