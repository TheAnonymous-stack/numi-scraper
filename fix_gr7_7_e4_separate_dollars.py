import json
import re

# Read the file
with open('Gr7_7_E4_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0

for question in data['quizzes']:
    original = question['question_text']
    q_text = original

    # Pattern 1: Simple fraction operation: $\frac{a}{b} + \frac{c}{d} = _/_
    # Should be: $\frac{a}{b}$ + $\frac{c}{d}$ = _/_
    q_text = re.sub(
        r'\$\\frac\{(\d+)\}\{(\d+)\}\s+([+\-×÷]|\\times|\\div)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$\\frac{\1}{\2}$ \3 $\\frac{\4}{\5}$ =',
        q_text
    )

    # Pattern 2: Mixed number operations: $2\frac{5}{6} + 1\frac{1}{8} = _ _/_
    # Should be: $2\frac{5}{6}$ + $1\frac{1}{8}$ = _ _/_
    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+([+\-×÷]|\\times|\\div)\s+(\d+)\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$\1\\frac{\2}{\3}$ \4 $\5\\frac{\6}{\7}$ =',
        q_text
    )

    # Pattern 3: Mixed number with simple fraction: $1\frac{3}{5} \times \frac{2}{3} = ____$
    # Should be: $1\frac{3}{5}$ × $\frac{2}{3}$ = ____
    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+(\\times|\\div)\s+\\frac\{(\d+)\}\{(\d+)\}\s*=\s*____\$',
        r'$\1\\frac{\2}{\3}$ \4 $\\frac{\5}{\6}$ = ____',
        q_text
    )

    # Pattern 4: Two mixed numbers: $5\frac{1}{4} \div 1\frac{3}{4} = ____$
    # Should be: $5\frac{1}{4}$ ÷ $1\frac{3}{4}$ = ____
    q_text = re.sub(
        r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\s+(\\div|\\times)\s+(\d+)\\frac\{(\d+)\}\{(\d+)\}\s*=\s*____\$',
        r'$\1\\frac{\2}{\3}$ \4 $\5\\frac{\6}{\7}$ = ____',
        q_text
    )

    # Pattern 5: Parentheses: $(\frac{3}{4} - \frac{1}{6}) + \frac{1}{4} = _/_
    # Should be: $(\frac{3}{4}$ - $\frac{1}{6})$ + $\frac{1}{4}$ = _/_
    q_text = re.sub(
        r'\$\(\\frac\{(\d+)\}\{(\d+)\}\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\)\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\s*=',
        r'$(\frac{\1}{\2}$ \3 $\frac{\4}{\5})$ \6 $\frac{\7}{\8}$ =',
        q_text
    )

    # Pattern 6: Division by number: $\frac{5}{6} - \frac{1}{3} \div 2 = _/_
    # Should be: $\frac{5}{6}$ - $\frac{1}{3}$ ÷ 2 = _/_
    q_text = re.sub(
        r'\$\\frac\{(\d+)\}\{(\d+)\}\s+([+\-])\s+\\frac\{(\d+)\}\{(\d+)\}\s+\\div\s+(\d+)\s*=',
        r'$\\frac{\1}{\2}$ \3 $\\frac{\4}{\5}$ \\div \6 =',
        q_text
    )

    if q_text != original:
        question['question_text'] = q_text
        fixed_count += 1
        print(f"Fixed Q{question['question_number']}:")
        print(f"  Before: {original[:80]}")
        print(f"  After:  {q_text[:80]}")
        print()

# Write the fixed file
with open('Gr7_7_E4_variations.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nFixed {fixed_count} questions")
print("Each fraction now has its own $...$ delimiters!")
