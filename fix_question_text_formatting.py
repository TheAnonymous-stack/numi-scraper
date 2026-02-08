import json
import os
import re

def fix_gr7_5_e3():
    """Fix Gr7_5_E3 question text formatting"""
    filepath = os.path.join('edited_by_tag', 'Gr7_5_E3', 'Gr7_5_E3_edited.json')

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for question in data['quizzes']:
        q_text = question['question_text']

        # Check if this is improper to mixed (has "Write $\frac{...}$ as a mixed number")
        if 'as a mixed number' in q_text:
            # Extract the fraction pattern like \frac{27}{8}
            frac_match = re.search(r'\$\\frac\{(\d+)\}\{(\d+)\}\$', q_text)
            if frac_match:
                frac = f"$\\frac{{{frac_match.group(1)}}}{{{frac_match.group(2)}}}$"
                # Format should be: "Write $\frac{27}{8}$ as a mixed number. Write your answer in simplest terms.\n$\frac{27}{8}$ = _ _/_"
                question['question_text'] = f"Write {frac} as a mixed number. Write your answer in simplest terms.\n{frac} = _ _/_"

        # Check if this is mixed to improper (has "Convert $...")
        elif 'Convert' in q_text:
            # Extract the mixed number pattern like 3\frac{1}{2}
            mixed_match = re.search(r'\$(\d+)\\frac\{(\d+)\}\{(\d+)\}\$', q_text)
            if mixed_match:
                mixed = f"${mixed_match.group(1)}\\frac{{{mixed_match.group(2)}}}{{{mixed_match.group(3)}}}$"
                # Format should be: "Convert $3\frac{1}{2}$ to an improper fraction. Write your answer in simplest terms. $\\\\[1em]$\n\n_/_ "
                question['question_text'] = f"Convert {mixed} to an improper fraction. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Fixed Gr7_5_E3_edited.json")

def fix_other_gr7_files():
    """Fix other Grade 7 files with similar formatting issues"""
    all_gr7_files = [
        'Gr7_5_E2', 'Gr7_6_E2', 'Gr7_7_E3', 'Gr7_13_E1', 'Gr7_13_E2',
        'Gr7_14_E1', 'Gr7_14_E2', 'Gr7_15_E1', 'Gr7_15_E2', 'Gr7_16_E1',
        'Gr7_16_E2', 'Gr7_17_E2', 'Gr7_20_E1', 'Gr7_20_E2', 'Gr7_20_E3',
        'Gr7_22_E1', 'Gr7_22_E3', 'Gr7_22_E4', 'Gr7_27_E3'
    ]

    for tag in all_gr7_files:
        filepath = os.path.join('edited_by_tag', tag, f'{tag}_edited.json')

        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False
        for question in data['quizzes']:
            q_text = question['question_text']

            # Check if instruction text is in the wrong place
            if 'Write your answer in simplest terms.' in q_text and '$\\\\\\\\[1em]$\\n\\n_/_ ' in q_text:
                # Remove the misplaced instruction and add it properly
                # The pattern should end with: "Write your answer in simplest terms. $\\\\[1em]$\n\n_/_ "

                # Remove any duplicate text patterns
                # Fix pattern: remove "...= Write your answer... = _/_" and make it "...Write your answer... = _/_"
                if '= Write your answer in simplest terms.' in q_text:
                    # Extract the base question before the first "="
                    parts = q_text.split('=', 1)
                    base = parts[0].strip()

                    # Check if instruction is already in base
                    if 'Write your answer in simplest terms.' not in base:
                        # Add instruction to base, then add "= $\\\\[1em]$\n\n_/_ "
                        question['question_text'] = f"{base} Write your answer in simplest terms.\n{base.split()[-1]} = $\\\\\\\\[1em]$\\n\\n_/_ "
                        modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Fixed {tag}_edited.json")

if __name__ == "__main__":
    print("Fixing Gr7_5_E3 question text formatting...")
    fix_gr7_5_e3()

    print("\nFixing other Grade 7 files...")
    fix_other_gr7_files()

    print("\nDone!")
