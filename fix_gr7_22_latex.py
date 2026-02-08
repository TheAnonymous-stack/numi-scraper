import json
import re
import os

def convert_fraction_to_latex(match):
    """Convert $a/b$ format to $\frac{a}{b}$ format"""
    num = match.group(1)
    den = match.group(2)
    return f'$\\frac{{{num}}}{{{den}}}$'

def fix_latex_in_file(filename):
    print(f"\nFixing LaTeX in {filename}...")

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for idx, question in enumerate(data['quizzes'], 1):
        # Fix question_text
        q_text = question['question_text']

        # Convert $a/b$ format to $\frac{a}{b}$ format
        q_text = re.sub(r'\$(\d+)/(\d+)\$', convert_fraction_to_latex, q_text)

        # Fix excessive backslashes in \[1em]
        q_text = q_text.replace('\\\\\\\\[1em]', '\\\\[1em]')

        # Fix any \n that got escaped
        q_text = q_text.replace('\\n', '\n')

        question['question_text'] = q_text

        # Fix solution text
        for sol_step in question.get('solution', []):
            if len(sol_step) >= 2:
                sol_text = sol_step[1]
                # Solutions should already have \frac format, just fix escaping
                sol_text = sol_text.replace('\\\\frac', '\\frac')
                sol_text = sol_text.replace('\\n', '\n')
                sol_step[1] = sol_text

        print(f"  Fixed question {idx}")

    # Save the main file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {filename}")

    return data

# Process Gr7_22_E1
print("=" * 60)
print("Processing Gr7_22_E1...")
print("=" * 60)

data = fix_latex_in_file('Gr7_22_E1_variations.json')
with open('edited_by_tag/Gr7_22_E1/Gr7_22_E1_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Saved: edited_by_tag/Gr7_22_E1/Gr7_22_E1_edited.json")
print("Completed fixing Gr7_22_E1!")

print("\n" + "=" * 60)
print("All files fixed!")
print("=" * 60)
