import json
import os

def rebuild_gr7_14_e2():
    """Completely rebuild Gr7_14_E2 from scratch with correct formatting"""

    # Read the source file
    source_file = 'Gr7_14_E2_variations.json'

    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        return

    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Rebuilding {len(data['quizzes'])} questions...")

    for question in data['quizzes']:
        q_text = question['question_text']

        # Extract the operation type and equation from the original text
        # Format: "Operation.\n\n$equation$. ..."

        # Determine operation type
        if q_text.startswith('Add'):
            operation = 'Add'
        elif q_text.startswith('Subtract'):
            operation = 'Subtract'
        elif q_text.startswith('Multiply'):
            operation = 'Multiply'
        else:
            # Keep as is if we can't determine
            continue

        # Extract the LaTeX equation (between first $ and second $)
        import re
        equation_match = re.search(r'\$(.*?)\$', q_text)
        if not equation_match:
            continue

        equation = equation_match.group(1)

        # Build the correct format following Gr7_13_E1 style:
        # "Operation.\n\n$equation$ = ?. Write your answer in simplest terms. $\\\\[1em]$\n\n_/_ "
        question['question_text'] = f"{operation}.\n\n${equation}$ = ?. Write your answer in simplest terms. $\\\\\\\\[1em]$\\n\\n_/_ "

    # Write both files
    output_files = [
        source_file,
        os.path.join('edited_by_tag', 'Gr7_14_E2', 'Gr7_14_E2_edited.json')
    ]

    for output_file in output_files:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Rebuilt {output_file}")

    print(f"\nSuccessfully rebuilt all {len(data['quizzes'])} questions!")
    print("Format: 'Operation.\\n\\n$equation$ = ?. Write your answer in simplest terms. $\\\\[1em]$\\n\\n_/_ '")

if __name__ == "__main__":
    rebuild_gr7_14_e2()
