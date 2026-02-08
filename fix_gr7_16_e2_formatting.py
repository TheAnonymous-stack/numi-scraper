import json
import os
import re
from fractions import Fraction

def fix_gr7_16_e2():
    """Fix Gr7_16_E2 formatting - word problems with proper LaTeX fractions"""

    source_file = 'Gr7_16_E2_variations.json'

    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        return

    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Fixing {len(data['quizzes'])} questions...")

    for idx, question in enumerate(data['quizzes'], 1):
        q_text = question['question_text']

        # Extract context and fractions
        # Pattern: A recipe for X uses $a/b$ cups... Another recipe uses $c/d$ cups. What's the total/difference?

        # First, check if fractions use /  (e.g., $9/4$) or \frac
        fractions_plain = re.findall(r'\$(\d+)/(\d+)\$', q_text)
        fractions_latex = re.findall(r'\$\\frac\{(\d+)\}\{(\d+)\}\$', q_text)

        if len(fractions_plain) >= 2:
            # Convert plain fractions to LaTeX
            num1, den1 = map(int, fractions_plain[0])
            num2, den2 = map(int, fractions_plain[1])

            # Replace $a/b$ with $\frac{a}{b}$
            q_text = re.sub(r'\$(\d+)/(\d+)\$', lambda m: f'$\\\\frac{{{m.group(1)}}}{{{m.group(2)}}}$', q_text, count=2)

        elif len(fractions_latex) >= 2:
            num1, den1 = map(int, fractions_latex[0])
            num2, den2 = map(int, fractions_latex[1])
        else:
            # Try to handle mixed formats (whole number + fraction)
            # Pattern: $a$ cups... $b/c$ cups
            whole_nums = re.findall(r'\$(\d+)\$', q_text)
            fractions = re.findall(r'\$(\d+)/(\d+)\$', q_text)

            if len(whole_nums) >= 1 and len(fractions) >= 1:
                num1 = int(whole_nums[0])
                den1 = 1
                num2, den2 = map(int, fractions[0])

                # Replace first $a$ with $\frac{a}{1}$ if it's followed by "cups"
                q_text = re.sub(r'\$(\d+)\$ cups', r'$\\frac{\1}{1}$ cups', q_text, count=1)
                # Replace $b/c$ with $\frac{b}{c}$
                q_text = re.sub(r'\$(\d+)/(\d+)\$', lambda m: f'$\\\\frac{{{m.group(1)}}}{{{m.group(2)}}}$', q_text, count=1)
            elif len(fractions) >= 2:
                num1, den1 = map(int, fractions[0])
                num2, den2 = map(int, fractions[1])
                q_text = re.sub(r'\$(\d+)/(\d+)\$', lambda m: f'$\\\\frac{{{m.group(1)}}}{{{m.group(2)}}}$', q_text, count=2)
            else:
                print(f"Could not parse question {idx}: {q_text[:80]}...")
                continue

        # Remove duplicate "Express your answer in simplest form. Write your answer in simplest terms."
        # Keep only "Write your answer in simplest terms."
        q_text = q_text.replace('Express your answer in simplest form. Write your answer in simplest terms.', 'Write your answer in simplest terms.')
        q_text = q_text.replace('Express your answer in simplest form.', 'Write your answer in simplest terms.')

        # Ensure proper LaTeX spacing format
        if '$\\\\\\\\[1em]$' not in q_text:
            q_text = q_text.replace('Write your answer in simplest terms.', 'Write your answer in simplest terms. $\\\\\\\\[1em]$')

        # Ensure proper ending with input field
        if not q_text.endswith('_/_ '):
            if q_text.endswith('$\\\\\\\\[1em]$\\n\\n'):
                q_text = q_text + '_/_ '
            elif '_/_ ' in q_text:
                pass  # Already has it
            else:
                q_text = q_text.rstrip() + '\\n\\n_/_ '

        question['question_text'] = q_text

        # Determine operation from question text
        if 'total' in q_text.lower() or 'altogether' in q_text.lower() or 'combined' in q_text.lower():
            question['skills'] = 'add-fractions-with-unlike-denominators-word-problems'
        elif 'difference' in q_text.lower() or 'more' in q_text.lower() or 'less' in q_text.lower():
            question['skills'] = 'subtract-fractions-with-unlike-denominators-word-problems'
        else:
            # Keep existing skill
            pass

        print(f"  Fixed question {idx}")

    # Write both files
    output_files = [
        source_file,
        os.path.join('edited_by_tag', 'Gr7_16_E2', 'Gr7_16_E2_edited.json')
    ]

    for output_file in output_files:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Fixed {output_file}")

    print(f"\nSuccessfully fixed all {len(data['quizzes'])} questions!")

if __name__ == "__main__":
    fix_gr7_16_e2()
