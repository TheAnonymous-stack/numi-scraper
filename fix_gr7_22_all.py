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

        # Convert $a/b$ format to $\frac{a}{b}$ format (only if not already \frac)
        if '\\frac' not in q_text:
            q_text = re.sub(r'\$(\d+)/(\d+)\$', convert_fraction_to_latex, q_text)

        # Fix excessive backslashes if present
        q_text = q_text.replace('\\\\\\\\[1em]', '\\\\[1em]')
        q_text = q_text.replace('\\n', '\n')

        question['question_text'] = q_text

        print(f"  Fixed question {idx}")

    # Save the main file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {filename}")

    return data

# Process E1
print("=" * 60)
print("Processing Gr7_22_E1...")
print("=" * 60)

data = fix_latex_in_file('Gr7_22_E1_variations.json')
with open('edited_by_tag/Gr7_22_E1/Gr7_22_E1_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Saved: edited_by_tag/Gr7_22_E1/Gr7_22_E1_edited.json")
print("Completed fixing Gr7_22_E1!")

# Process E3
print("\n" + "=" * 60)
print("Processing Gr7_22_E3...")
print("=" * 60)

data = fix_latex_in_file('Gr7_22_E3_variations.json')
with open('edited_by_tag/Gr7_22_E3/Gr7_22_E3_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Saved: edited_by_tag/Gr7_22_E3/Gr7_22_E3_edited.json")
print("Completed fixing Gr7_22_E3!")

# Process E4
print("\n" + "=" * 60)
print("Processing Gr7_22_E4...")
print("=" * 60)

data = fix_latex_in_file('Gr7_22_E4_variations.json')
with open('edited_by_tag/Gr7_22_E4/Gr7_22_E4_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Saved: edited_by_tag/Gr7_22_E4/Gr7_22_E4_edited.json")
print("Completed fixing Gr7_22_E4!")

print("\n" + "=" * 60)
print("All files fixed!")
print("=" * 60)
