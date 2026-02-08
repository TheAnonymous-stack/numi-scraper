import json
import os

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
                sol_text = sol_text.replace('\\n', '\n')
                sol_step[1] = sol_text

        print(f"  Fixed question {idx}")

    # Save the main file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {filename}")

    return data

# Fix E2
print("=" * 60)
print("Processing Gr7_20_E2...")
print("=" * 60)

data = fix_latex_in_file('Gr7_20_E2_variations.json')
with open('edited_by_tag/Gr7_20_E2/Gr7_20_E2_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Saved: edited_by_tag/Gr7_20_E2/Gr7_20_E2_edited.json")
print("Completed fixing Gr7_20_E2!")

# Fix E3
print("\n" + "=" * 60)
print("Processing Gr7_20_E3...")
print("=" * 60)

data = fix_latex_in_file('Gr7_20_E3_variations.json')
with open('edited_by_tag/Gr7_20_E3/Gr7_20_E3_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Saved: edited_by_tag/Gr7_20_E3/Gr7_20_E3_edited.json")
print("Completed fixing Gr7_20_E3!")

print("\n" + "=" * 60)
print("All files fixed!")
print("=" * 60)
