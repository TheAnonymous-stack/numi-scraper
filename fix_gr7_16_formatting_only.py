import json
import os
import re
from fractions import Fraction

def fix_formatting_only():
    """Fix Gr7_16_E1 and E2 formatting - keep operations as-is, just fix LaTeX and duplicate text"""

    files_to_process = [
        ('Gr7_16_E1_variations.json', 'Gr7_16_E1', False),
        ('Gr7_16_E2_variations.json', 'Gr7_16_E2', True)
    ]

    for source_file, tag, is_word_problem in files_to_process:
        if not os.path.exists(source_file):
            print(f"Source file not found: {source_file}")
            continue

        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\nFixing {source_file} with {len(data['quizzes'])} questions...")

        add_count = 0
        subtract_count = 0

        for idx, question in enumerate(data['quizzes'], 1):
            q_text = question['question_text']
            orig_q_text = q_text

            # Extract fractions and operator from current question text
            # Check if it has + or - operator
            has_subtract = ' - ' in q_text or '−' in q_text or 'difference' in q_text.lower()
            operator = '-' if has_subtract else '+'
            operation = 'Subtract' if has_subtract else 'Add'

            # Convert $a/b$ to $\frac{a}{b}$
            q_text = re.sub(r'\$(\d+)/(\d+)\$', lambda m: f'$\\\\frac{{{m.group(1)}}}{{{m.group(2)}}}$', q_text)

            # Convert standalone $a$ followed by specific patterns to $\frac{a}{1}$
            # But only if it appears in calculation context
            if is_word_problem:
                q_text = re.sub(r'\$(\d+)\$ cups', r'$\\frac{\1}{1}$ cups', q_text)

            # Remove "Express your answer in simplest form." if followed by "Write your answer in simplest terms."
            q_text = q_text.replace('Express your answer in simplest form. Write your answer in simplest terms.', 'Write your answer in simplest terms.')
            q_text = q_text.replace('Express your answer in simplest form.', 'Write your answer in simplest terms.')

            # Ensure proper ending format
            if '$\\\\\\\\[1em]$' not in q_text:
                q_text = q_text.replace('Write your answer in simplest terms.', 'Write your answer in simplest terms. $\\\\\\\\[1em]$')

            if not q_text.endswith('_/_ '):
                if '\\n\\n_/_ ' not in q_text:
                    q_text = q_text.rstrip() + '\\n\\n_/_ '

            # For E1 (non-word problems), format as: "Operation.\n\n$equation$ = ?. Write..."
            if not is_word_problem and 'Calculate:' in q_text:
                # Extract the equation part
                equation_match = re.search(r'Calculate: (.+?) = \?', q_text)
                if equation_match:
                    equation = equation_match.group(1).strip()
                    q_text = f"{operation}.\n\n{equation} = ?. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

            question['question_text'] = q_text

            # Update skill based on operation and whether it's a word problem
            if is_word_problem:
                if operator == '+':
                    question['skills'] = 'add-fractions-with-unlike-denominators-word-problems'
                    add_count += 1
                else:
                    question['skills'] = 'subtract-fractions-with-unlike-denominators-word-problems'
                    subtract_count += 1
            else:
                if operator == '+':
                    question['skills'] = 'add-fractions-with-unlike-denominators'
                    add_count += 1
                else:
                    question['skills'] = 'subtract-fractions-with-unlike-denominators'
                    subtract_count += 1

            # Fix correct_answers format - if single answer with fraction, split it
            correct_ans = question['correct_answers']
            if len(correct_ans) == 1 and '/' in correct_ans[0]:
                # Split "a/b" into ["a", "b"]
                parts = correct_ans[0].split('/')
                question['correct_answers'] = [parts[0], parts[1]]
                question['question_type'] = 'Multiple fill in the blank'
            elif len(correct_ans) == 1:
                # Whole number - keep as Multiple fill in the blank with denominator 1
                question['correct_answers'] = [correct_ans[0], '1']
                question['question_type'] = 'Multiple fill in the blank'

            print(f"  Question {idx}: {operation}")

        print(f"\nFixed {source_file}:")
        print(f"  - Add: {add_count} questions")
        print(f"  - Subtract: {subtract_count} questions")

        # Write both files
        output_files = [
            source_file,
            os.path.join('edited_by_tag', tag, f'{tag}_edited.json')
        ]

        for output_file in output_files:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Fixed {output_file}")

if __name__ == "__main__":
    fix_formatting_only()
