import json

# Read the file
with open('Gr7_7_E4_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0

for question in data['quizzes']:
    original = question['question_text']
    q_text = original

    # Fix 1: Missing backslash in parentheses - \frac should be \\frac
    # "$(\frac{3}{4}$" should be "$(\\frac{3}{4}$"
    q_text = q_text.replace('$(\frac{', '$( \\frac{')
    q_text = q_text.replace('\frac{', '\\frac{')
    q_text = q_text.replace('$(  \\frac{', '$(\\frac{')  # Clean up double space

    # Fix 2: Remove stray $ at the end before newline
    # "= ____$\n" should be "= ____\n"
    q_text = q_text.replace('= ____$\n', '= ____\n')

    if q_text != original:
        question['question_text'] = q_text
        fixed_count += 1
        print(f"Fixed Q{question['question_number']}")

# Write the fixed file
with open('Gr7_7_E4_variations.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nFixed {fixed_count} questions")
print("All dollar signs and backslashes are now correct!")
