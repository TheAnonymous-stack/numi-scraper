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

# Fix Gr7_17_E1
print("Fixing Gr7_17_E1...")
with open('Gr7_17_E1_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_17 = 0
for question in data['quizzes']:
    original = question['question_text']
    fixed = fix_latex_format(original)
    if fixed != original:
        question['question_text'] = fixed
        fixed_17 += 1

with open('Gr7_17_E1_variations.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Fixed {fixed_17} questions in Gr7_17_E1")

# Gr7_21_E1 and Gr7_21_E2 already have correct format, but let's verify
print("\nChecking Gr7_21_E1...")
with open('Gr7_21_E1_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_21_1 = 0
for question in data['quizzes']:
    original = question['question_text']
    fixed = fix_latex_format(original)
    if fixed != original:
        question['question_text'] = fixed
        fixed_21_1 += 1

if fixed_21_1 > 0:
    with open('Gr7_21_E1_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Fixed {fixed_21_1} questions in Gr7_21_E1")
else:
    print("No fixes needed for Gr7_21_E1")

print("\nChecking Gr7_21_E2...")
with open('Gr7_21_E2_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_21_2 = 0
for question in data['quizzes']:
    original = question['question_text']
    fixed = fix_latex_format(original)
    if fixed != original:
        question['question_text'] = fixed
        fixed_21_2 += 1

if fixed_21_2 > 0:
    with open('Gr7_21_E2_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Fixed {fixed_21_2} questions in Gr7_21_E2")
else:
    print("No fixes needed for Gr7_21_E2")

print("\n" + "="*60)
print(f"Total fixes: Gr7_17_E1: {fixed_17}, Gr7_21_E1: {fixed_21_1}, Gr7_21_E2: {fixed_21_2}")
print("="*60)
