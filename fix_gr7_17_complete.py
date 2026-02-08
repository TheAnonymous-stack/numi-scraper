import json
import re

def fix_latex_format(text):
    """Fix LaTeX formatting to match the standard: separate $ for each fraction"""

    # Pattern 1: Fix simple fractions like "$4 1/6$" to "$4\\frac{1}{6}$"
    # Match: $NUMBER SPACE NUMBER/NUMBER$
    text = re.sub(r'\$(\d+)\s+(\d+)/(\d+)\$', r'$\1\\frac{\2}{\3}$', text)

    # Pattern 2: Fix "$NUMBER NUMBER/NUMBER$" (no space) to "$NUMBER\\frac{NUMBER}{NUMBER}$"
    text = re.sub(r'\$(\d+)(\d+)/(\d+)\$', r'$\1\\frac{\2}{\3}$', text)

    return text

# Fix main Gr7_17_E1_variations.json
print("Fixing Gr7_17_E1_variations.json...")
with open('Gr7_17_E1_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_main = 0
for question in data['quizzes']:
    original = question['question_text']
    fixed = fix_latex_format(original)
    if fixed != original:
        question['question_text'] = fixed
        fixed_main += 1

with open('Gr7_17_E1_variations.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Fixed {fixed_main} questions in Gr7_17_E1_variations.json")

# Fix edited Gr7_17_E1_edited.json
print("\nFixing Gr7_17_E1_edited.json...")
with open('edited_by_tag/Gr7_17_E1/Gr7_17_E1_edited.json', 'r', encoding='utf-8') as f:
    data_edited = json.load(f)

fixed_edited = 0
for question in data_edited['quizzes']:
    original = question['question_text']
    fixed = fix_latex_format(original)
    if fixed != original:
        question['question_text'] = fixed
        fixed_edited += 1

with open('edited_by_tag/Gr7_17_E1/Gr7_17_E1_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data_edited, f, indent=2, ensure_ascii=False)

print(f"Fixed {fixed_edited} questions in Gr7_17_E1_edited.json")

print("\n" + "="*60)
print(f"Total fixes - Main: {fixed_main}, Edited: {fixed_edited}")
print("="*60)
