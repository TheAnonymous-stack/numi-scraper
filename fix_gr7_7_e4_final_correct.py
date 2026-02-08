import json

# Read both files
with open('Gr7_7_E4_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('edited_by_tag/Gr7_7_E4/Gr7_7_E4_edited.json', 'r', encoding='utf-8') as f:
    edited_data = json.load(f)

print("Fixing all questions to match the correct format...\n")

for question in data['quizzes']:
    original = question['question_text']
    q_text = original

    # Pattern 1: Simple two-fraction operations
    # Change: $\frac{2}{3} + \frac{1}{4} = _/_
    # To: $\frac{2}{3}$ + $\frac{1}{4}$ = _/_
    import re
    q_text = re.sub(
        r'\$\\frac\{(\d+)\}\{(\d+)\}\s+([+\-]|\\times|\\div)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$\\frac{\1}{\2}$ \3 $\\frac{\4}{\5}$ =',
        q_text
    )

    # Pattern 2: Mixed number operations
    # Change: $2\frac{5}{6} + 1 \frac{1}{8} = _ _/_
    # To: $2\frac{5}{6}$ + $1\frac{1}{8}$ = _ _/_
    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+([+\-]|\\times|\\div)\s+(\d+)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$\1\\frac{\2}{\3}$ \4 $\5\\frac{\6}{\7}$ =',
        q_text
    )

    # Pattern 3: Remove parentheses and fix
    # Change: $(\frac{3}{4} - \frac{1}{6}) + \frac{1}{4} = _/_
    # To: $\frac{3}{4}$ - $\frac{1}{6}$ + $\frac{1}{4}$ = _/_
    q_text = re.sub(
        r'\$\(\\frac\{(\d+)\}\{(\d+)\}\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\)\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$\\frac{\1}{\2}$ \3 $\\frac{\4}{\5}$ \6 $\\frac{\7}{\8}$ =',
        q_text
    )

    # Pattern 4: Division by number
    # Change: $\frac{5}{6} - \frac{1}{3} \div 2 = _/_
    # To: $\frac{5}{6}$ - $\frac{1}{3}$ ÷ 2 = _/_
    q_text = re.sub(
        r'\$\\frac\{(\d+)\}\{(\d+)\}\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\s+\\div\s+(\d+)\s*=',
        r'$\\frac{\1}{\2}$ \3 $\\frac{\4}{\5}$ \\div \6 =',
        q_text
    )

    # Pattern 5: Mixed number with regular fraction (with = $ ____)
    # Change: $1\frac{3}{5} \times \frac{2}{3} = $ ____
    # To: $1\frac{3}{5}$ × $\frac{2}{3}$ = ____
    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+(\\times|\\div)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=\s*\$\s*____',
        r'$\1\\frac{\2}{\3}$ \4 $\\frac{\5}{\6}$ = ____',
        q_text
    )

    # Pattern 6: Two mixed numbers (with = $ ____)
    # Change: $5\frac{1}{4} \div 1 \frac{3}{4} = $ ____
    # To: $5\frac{1}{4}$ ÷ $1\frac{3}{4}$ = ____
    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+(\\div|\\times)\s+(\d+)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=\s*\$\s*____',
        r'$\1\\frac{\2}{\3}$ \4 $\5\\frac{\6}{\7}$ = ____',
        q_text
    )

    if q_text != original:
        question['question_text'] = q_text
        print(f"Fixed Q{question['question_number']}")

# Also fix edited file
for question in edited_data['quizzes']:
    original = question['question_text']
    q_text = original

    q_text = re.sub(
        r'\$\\frac\{(\d+)\}\{(\d+)\}\s+([+\-]|\\times|\\div)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$\\frac{\1}{\2}$ \3 $\\frac{\4}{\5}$ =',
        q_text
    )

    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+([+\-]|\\times|\\div)\s+(\d+)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$\1\\frac{\2}{\3}$ \4 $\5\\frac{\6}{\7}$ =',
        q_text
    )

    q_text = re.sub(
        r'\$\(\\frac\{(\d+)\}\{(\d+)\}\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\)\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$\\frac{\1}{\2}$ \3 $\\frac{\4}{\5}$ \6 $\\frac{\7}{\8}$ =',
        q_text
    )

    q_text = re.sub(
        r'\$\\frac\{(\d+)\}\{(\d+)\}\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\s+\\div\s+(\d+)\s*=',
        r'$\\frac{\1}{\2}$ \3 $\\frac{\4}{\5}$ \\div \6 =',
        q_text
    )

    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+(\\times|\\div)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=\s*\$\s*____',
        r'$\1\\frac{\2}{\3}$ \4 $\\frac{\5}{\6}$ = ____',
        q_text
    )

    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+(\\div|\\times)\s+(\d+)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=\s*\$\s*____',
        r'$\1\\frac{\2}{\3}$ \4 $\5\\frac{\6}{\7}$ = ____',
        q_text
    )

    if q_text != original:
        question['question_text'] = q_text

# Write both files
with open('Gr7_7_E4_variations.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open('edited_by_tag/Gr7_7_E4/Gr7_7_E4_edited.json', 'w', encoding='utf-8') as f:
    json.dump(edited_data, f, indent=2, ensure_ascii=False)

print("\nDone! Fixed both files:")
print("- Gr7_7_E4_variations.json")
print("- edited_by_tag/Gr7_7_E4/Gr7_7_E4_edited.json")
print("\nAll fractions now have separate $...$ delimiters")
print("Removed parentheses from expressions")
