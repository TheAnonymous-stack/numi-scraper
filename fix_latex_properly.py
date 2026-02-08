import json
import re

def fix_latex_in_file(filename):
    print(f"\nFixing LaTeX in {filename}...")

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for idx, question in enumerate(data['quizzes'], 1):
        # Fix question_text
        q_text = question['question_text']
        # Replace all instances of \\frac with \frac (removing extra backslashes)
        q_text = q_text.replace('\\\\frac', '\\frac')
        # Fix the \\[1em] as well
        q_text = q_text.replace('\\\\\\\\[1em]', '\\\\[1em]')
        # Fix any \n that got escaped
        q_text = q_text.replace('\\n', '\n')
        question['question_text'] = q_text

        # Fix solution text
        for sol_step in question.get('solution', []):
            if len(sol_step) >= 2:
                sol_text = sol_step[1]
                sol_text = sol_text.replace('\\\\frac', '\\frac')
                sol_step[1] = sol_text

        print(f"  Fixed question {idx}")

    # Save both files
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {filename}")

    # Also save to edited_by_tag if E1 or E2
    if 'E1' in filename:
        output_file = f"edited_by_tag/Gr7_16_E1/Gr7_16_E1_edited.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved: {output_file}")
    elif 'E2' in filename:
        output_file = f"edited_by_tag/Gr7_16_E2/Gr7_16_E2_edited.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved: {output_file}")

    print(f"Completed fixing {filename}!")

# Fix both files
fix_latex_in_file('Gr7_16_E1_variations.json')
fix_latex_in_file('Gr7_16_E2_variations.json')

print("\n=== All files fixed! ===")
