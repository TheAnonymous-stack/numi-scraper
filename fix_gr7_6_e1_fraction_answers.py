import json
import re
import os

def fix_gr7_6_e1():
    """Fix Gr7_6_E1: Convert fraction answers to proper _/_ format"""
    print("\n" + "=" * 60)
    print("Fixing Gr7_6_E1 fraction answer formats...")
    print("=" * 60)

    filename = 'Gr7_6_E1_variations.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for idx, question in enumerate(data['quizzes'], 1):
        # Check if this asks to convert TO a fraction (not to a decimal)
        q_text = question['question_text']

        if 'to a fraction' in q_text.lower():
            # Check if the answer is in format "3/4" (single string)
            if (question.get('question_type') == 'Fill in the blank' and
                len(question.get('correct_answers', [])) == 1):

                answer = question['correct_answers'][0]

                # Parse the fraction answer
                match = re.match(r'(\d+)/(\d+)', answer)
                if match:
                    num, den = match.groups()

                    # Update to Multiple fill in the blank format
                    question['question_type'] = 'Multiple fill in the blank'
                    question['correct_answers'] = [num, den]

                    # Add required fields
                    if 'orderMatter' not in question:
                        question['orderMatter'] = True
                    if 'has_alternate_answers' not in question:
                        question['has_alternate_answers'] = True

                    # Update question_text to have _/_ format
                    if '_/_' not in q_text:
                        # Add the format at the end
                        q_text = re.sub(r'\.$', r'. $\\\\[1em]$\n\n_/_ ', q_text)
                        question['question_text'] = q_text

                    fixed_count += 1
                    print(f"  Question {idx}: Converted {answer} to {question['correct_answers']} format")

    # Save files
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    output_dir = "edited_by_tag/Gr7_6_E1"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/Gr7_6_E1_edited.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n  Total questions fixed: {fixed_count}")
    print(f"  Saved to: {output_file}")
    return fixed_count

# Run the fix
total_fixed = fix_gr7_6_e1()

print("\n" + "=" * 60)
print(f"All fraction answers converted to proper _/_ format!")
print("=" * 60)
