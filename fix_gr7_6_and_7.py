import json
import re
import os

def convert_simple_fraction_to_latex(text):
    """Convert simple fractions like 3/4 to LaTeX \\frac{3}{4} but NOT in mixed numbers like $2 5/6$"""
    # First protect mixed number patterns from conversion
    # Pattern: space + digit/digit (as in "2 5/6")
    text = re.sub(r'(\d+\s+)(\d+)/(\d+)', r'\1MIXEDTEMP\2_\3', text)

    # Now convert standalone fractions 3/4 to $\frac{3}{4}$
    text = re.sub(r'(\d+)/(\d+)', r'$\\frac{\1}{\2}$', text)

    # Restore the mixed numbers with proper LaTeX format
    text = re.sub(r'MIXEDTEMP(\d+)_(\d+)', r'\\frac{\1}{\2}', text)

    return text

def fix_gr7_6_e1():
    """Fix Gr7_6_E1: Add _ _/_ format to question_text for mixed number answers"""
    print("\n" + "=" * 60)
    print("Fixing Gr7_6_E1...")
    print("=" * 60)

    filename = 'Gr7_6_E1_variations.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0
    for idx, question in enumerate(data['quizzes'], 1):
        # Check if this has mixed number answers (3 values in correct_answers)
        if (question.get('question_type') == 'Multiple fill in the blank' and
            len(question.get('correct_answers', [])) == 3):

            q_text = question['question_text']

            # Add _ _/_ to the question text if it doesn't have it
            if '_ _/_' not in q_text and '_/_' not in q_text:
                # Replace the ending pattern
                q_text = re.sub(r'\.$', r'. $\\\\[1em]$\n\n_ _/_', q_text)
                question['question_text'] = q_text
                fixed_count += 1
                print(f"  Fixed question {idx}: Added _ _/_ format")

    # Save files
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    output_dir = "edited_by_tag/Gr7_6_E1"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/Gr7_6_E1_edited.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  Fixed {fixed_count} questions")
    print(f"  Saved to: {output_file}")
    return fixed_count

def fix_gr7_7_e4():
    """Fix Gr7_7_E4: Convert simple fractions to LaTeX and add _ _/_ format"""
    print("\n" + "=" * 60)
    print("Fixing Gr7_7_E4...")
    print("=" * 60)

    filename = 'Gr7_7_E4_variations.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_latex = 0
    fixed_format = 0

    for idx, question in enumerate(data['quizzes'], 1):
        q_text = question['question_text']

        # Fix LaTeX in mixed numbers (convert 3/4 to \frac{3}{4} in expressions)
        # Look for patterns like "$2 5/6" and convert to "$2\frac{5}{6}"
        original_text = q_text

        # Pattern for mixed numbers in LaTeX: $2 5/6 -> $2\frac{5}{6}
        q_text = re.sub(r'\$(\d+)\s+(\d+)/(\d+)', r'$\1\\frac{\2}{\3}', q_text)

        # Pattern for standalone fractions without $ around them: (3/4 - 1/6)
        # Convert any remaining fraction pattern outside $ delimiters
        q_text = convert_simple_fraction_to_latex(q_text)

        if q_text != original_text:
            fixed_latex += 1
            print(f"  Question {idx}: Fixed LaTeX formatting")

        # For questions with mixed number answers, add _ _/_ format
        if (question.get('question_type') == 'Multiple fill in the blank' and
            len(question.get('correct_answers', [])) == 3):

            # Add _ _/_ to the question text if it doesn't have it
            if '_ _/_' not in q_text and '= $ ____' in q_text:
                q_text = q_text.replace('= $ ____', '= _ _/_')
                fixed_format += 1
                print(f"  Question {idx}: Added _ _/_ format")

        question['question_text'] = q_text

    # Save files
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    output_dir = "edited_by_tag/Gr7_7_E4"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/Gr7_7_E4_edited.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  Fixed LaTeX in {fixed_latex} questions")
    print(f"  Fixed answer format in {fixed_format} questions")
    print(f"  Saved to: {output_file}")
    return fixed_latex + fixed_format

# Run both fixes
total_fixed = 0
total_fixed += fix_gr7_6_e1()
total_fixed += fix_gr7_7_e4()

print("\n" + "=" * 60)
print(f"Total fixes applied: {total_fixed}")
print("All files processed!")
print("=" * 60)
