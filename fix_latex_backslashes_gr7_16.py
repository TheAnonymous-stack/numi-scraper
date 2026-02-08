import json
import os
import re

def fix_latex_backslashes():
    """Fix LaTeX backslashes in Gr7_16_E1 and E2 - change \\\\ to \\"""

    files_to_process = [
        ('Gr7_16_E1_variations.json', 'Gr7_16_E1'),
        ('Gr7_16_E2_variations.json', 'Gr7_16_E2')
    ]

    for source_file, tag in files_to_process:
        if not os.path.exists(source_file):
            print(f"Source file not found: {source_file}")
            continue

        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\nFixing LaTeX in {len(data['quizzes'])} questions in {source_file}...")

        for idx, question in enumerate(data['quizzes'], 1):
            # Fix question_text
            q_text = question['question_text']

            # Replace \\\\frac with \\frac (4 backslashes to 2)
            q_text = q_text.replace('$\\\\\\\\frac', '$\\\\frac')

            question['question_text'] = q_text

            # Fix solution text
            for sol_step in question.get('solution', []):
                if len(sol_step) >= 2:
                    sol_text = sol_step[1]
                    # Replace \\\\frac with \\frac
                    sol_text = sol_text.replace('\\\\\\\\frac', '\\\\frac')
                    sol_step[1] = sol_text

            print(f"  Fixed question {idx}")

        # Write both files
        output_files = [
            source_file,
            os.path.join('edited_by_tag', tag, f'{tag}_edited.json')
        ]

        for output_file in output_files:
            dir_name = os.path.dirname(output_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved: {output_file}")

        print(f"Completed fixing {source_file}!")

if __name__ == "__main__":
    fix_latex_backslashes()
