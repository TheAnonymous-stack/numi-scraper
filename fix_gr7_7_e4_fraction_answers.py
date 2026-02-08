import json
import re
import os

def fix_gr7_7_e4():
    """Fix Gr7_7_E4: Convert fraction answers to proper _/_ format"""
    print("\n" + "=" * 60)
    print("Fixing Gr7_7_E4 fraction answer formats...")
    print("=" * 60)

    filename = 'Gr7_7_E4_variations.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for idx, question in enumerate(data['quizzes'], 1):
        # Check if this is a "Fill in the blank" with a fraction answer
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
                q_text = question['question_text']
                if '_/_' not in q_text:
                    # Replace = $ ____ with _/_
                    q_text = q_text.replace('= $ ____', '= _/_')
                    question['question_text'] = q_text

                fixed_count += 1
                print(f"  Question {idx}: Converted {answer} to {question['correct_answers']} format")

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
total_fixed = fix_gr7_7_e4()

print("\n" + "=" * 60)
print(f"All fraction answers converted to proper _/_ format!")
print("=" * 60)
