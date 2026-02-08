import json

# Read the file
with open('Gr7_7_E4_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0

for question in data['quizzes']:
    original = question['question_text']
    q_text = original

    # Fix 1: Remove space between whole number and \frac in mixed numbers
    # "$2\\frac{5}{6} + 1 \\frac{1}{8}" → "$2\\frac{5}{6} + 1\\frac{1}{8}"
    import re
    q_text = re.sub(r'(\d+)\s+\\frac', r'\1\\frac', q_text)

    # Fix 2: Remove trailing "= $ " pattern and replace with just "="
    # "$1\\frac{3}{5} \\times \\frac{2}{3} = $ ____" → "$1\\frac{3}{5} \\times \\frac{2}{3} = ____$"
    q_text = re.sub(r'=\s+\$\s+(____)', r'= \1$', q_text)

    if q_text != original:
        question['question_text'] = q_text
        fixed_count += 1

# Write the fixed file
with open('Gr7_7_E4_variations.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✓ Fixed {fixed_count} questions in Gr7_7_E4_variations.json")
print("\nFixed patterns:")
print("1. Removed spaces between whole numbers and \\frac in mixed numbers")
print("2. Fixed dollar sign placement at end of expressions")
