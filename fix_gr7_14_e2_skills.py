import json
import os

def fix_skills():
    """Fix the skills field to match the actual operation in each question"""

    # Read the source file
    source_file = 'Gr7_14_E2_variations.json'

    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        return

    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Fixing skills for {len(data['quizzes'])} questions...")

    add_count = 0
    subtract_count = 0
    multiply_count = 0

    for question in data['quizzes']:
        q_text = question['question_text']

        # Determine operation type and set the correct skill
        if q_text.startswith('Add'):
            question['skills'] = 'add-fractions-with-unlike-denominators'
            add_count += 1
        elif q_text.startswith('Subtract'):
            question['skills'] = 'subtract-fractions-with-unlike-denominators'
            subtract_count += 1
        elif q_text.startswith('Multiply'):
            question['skills'] = 'multiply-fractions'
            multiply_count += 1

    # Write both files
    output_files = [
        source_file,
        os.path.join('edited_by_tag', 'Gr7_14_E2', 'Gr7_14_E2_edited.json')
    ]

    for output_file in output_files:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Fixed {output_file}")

    print(f"\nSuccessfully fixed all {len(data['quizzes'])} questions!")
    print(f"  - Add: {add_count} questions")
    print(f"  - Subtract: {subtract_count} questions")
    print(f"  - Multiply: {multiply_count} questions")

if __name__ == "__main__":
    fix_skills()
