import json
import re
import os

def fix_gr7_7_e4_latex():
    """Fix Gr7_7_E4: Fix broken LaTeX with extra $ signs in parentheses"""
    print("\n" + "=" * 60)
    print("Fixing Gr7_7_E4 LaTeX formatting...")
    print("=" * 60)

    filename = 'Gr7_7_E4_variations.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for idx, question in enumerate(data['quizzes'], 1):
        q_text = question['question_text']
        original = q_text

        # Fix patterns like $($\frac{3}{4}$ - $\frac{1}{6}$) + \frac{1}{4}
        # Should be: $(\frac{3}{4} - \frac{1}{6}) + \frac{1}{4}$

        # Pattern 1: $($\frac -> $(\frac (remove $ after opening paren)
        q_text = re.sub(r'\$\(\$\\frac', r'$(\\frac', q_text)

        # Pattern 2: \frac{x}{y}$) -> \frac{x}{y}) (remove $ before closing paren)
        q_text = re.sub(r'(\\frac\{\d+\}\{\d+\})\$\)', r'\1)', q_text)

        # Pattern 3: $$\frac -> $\frac (double $ at start)
        q_text = re.sub(r'\$\$\\frac', r'$\\frac', q_text)

        # Pattern 4: Fix $ - $ to just - within expressions
        q_text = re.sub(r'\$\s*-\s*\$', r' - ', q_text)

        if q_text != original:
            question['question_text'] = q_text
            fixed_count += 1
            print(f"  Question {idx}: Fixed LaTeX formatting")

    # Save files
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    output_dir = "edited_by_tag/Gr7_7_E4"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/Gr7_7_E4_edited.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n  Total questions fixed: {fixed_count}")
    print(f"  Saved to: {output_file}")
    return fixed_count

# Run the fix
total_fixed = fix_gr7_7_e4_latex()

print("\n" + "=" * 60)
print(f"All LaTeX formatting issues fixed!")
print("=" * 60)
