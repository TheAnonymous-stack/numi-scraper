import json
import re
import os

def fix_gr7_7_e4_dollar_signs():
    """Fix Gr7_7_E4: Fix stray $ signs that break LaTeX"""
    print("\n" + "=" * 60)
    print("Fixing Gr7_7_E4 dollar sign issues...")
    print("=" * 60)

    filename = 'Gr7_7_E4_variations.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for idx, question in enumerate(data['quizzes'], 1):
        q_text = question['question_text']
        original = q_text

        # Pattern: $\frac{5}{6} - \frac{1}{3}$ \div 2
        # Should be: $\frac{5}{6} - \frac{1}{3} \div 2$
        # The $ before \div is closing the LaTeX too early

        # Fix: Remove $ that appears before \div or other operators when it's in the middle of an expression
        q_text = re.sub(r'(\\frac\{\d+\}\{\d+\})\$\s+(\\div|\\times|\+|-)', r'\1 \2', q_text)

        if q_text != original:
            question['question_text'] = q_text
            fixed_count += 1
            print(f"  Question {idx}: Fixed dollar sign issue")

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
total_fixed = fix_gr7_7_e4_dollar_signs()

print("\n" + "=" * 60)
print(f"All dollar sign issues fixed!")
print("=" * 60)
