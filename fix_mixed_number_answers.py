import json
import re
import os

def parse_mixed_number(answer_str):
    """
    Parse a mixed number string like "4 4/21" into [whole, numerator, denominator]
    or return single value for whole numbers
    """
    answer_str = answer_str.strip()

    # Check if it's a mixed number (e.g., "4 4/21")
    mixed_pattern = r'(\d+)\s+(\d+)/(\d+)'
    match = re.match(mixed_pattern, answer_str)
    if match:
        whole, num, den = match.groups()
        return [whole, num, den], True

    # Check if it's just a fraction (e.g., "4/21") - shouldn't be mixed number format
    frac_pattern = r'(\d+)/(\d+)'
    match = re.match(frac_pattern, answer_str)
    if match:
        num, den = match.groups()
        return [num, den], False

    # It's a whole number
    return [answer_str], False

def fix_file(filename, tag):
    print(f"\nFixing {filename}...")

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for idx, question in enumerate(data['quizzes'], 1):
        # Check if it has correct_answers that need fixing
        if 'correct_answers' in question and len(question['correct_answers']) == 1:
            answer = question['correct_answers'][0]
            parsed, is_mixed = parse_mixed_number(answer)

            if is_mixed:
                # It's a mixed number - update to proper format
                question['correct_answers'] = parsed
                question['question_type'] = "Multiple fill in the blank"

                # Add these fields if not present
                if 'orderMatter' not in question:
                    question['orderMatter'] = True
                if 'has_alternate_answers' not in question:
                    question['has_alternate_answers'] = True

                # Update question_text to have proper blank format
                q_text = question['question_text']

                # Replace various answer formats with _ _/_
                q_text = re.sub(r'=\s*\?\.?\s*Express', '= _ _/_. Express', q_text)
                q_text = re.sub(r'=\s*\?\s*$', '= _ _/_', q_text)

                question['question_text'] = q_text

                fixed_count += 1
                print(f"  Question {idx}: Fixed mixed number answer {answer} -> {parsed}")

    # Save main file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save to edited_by_tag
    output_dir = f"edited_by_tag/{tag}"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/{tag}_edited.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  Fixed {fixed_count} questions")
    print(f"  Saved to: {output_file}")

    return fixed_count

# Process all files
files_to_fix = [
    ("Gr7_3_E2_variations.json", "Gr7_3_E2"),
    ("Gr7_3_E5_variations.json", "Gr7_3_E5"),
    ("Gr7_6_E1_variations.json", "Gr7_6_E1"),
    ("Gr7_7_E4_variations.json", "Gr7_7_E4"),
    ("Gr7_17_E1_variations.json", "Gr7_17_E1"),
    ("Gr7_21_E1_variations.json", "Gr7_21_E1"),
    ("Gr7_21_E2_variations.json", "Gr7_21_E2"),
    ("Gr7_22_E2_variations.json", "Gr7_22_E2")
]

print("=" * 60)
print("Fixing mixed number answer formats")
print("=" * 60)

total_fixed = 0
for filename, tag in files_to_fix:
    count = fix_file(filename, tag)
    total_fixed += count

print("\n" + "=" * 60)
print(f"Total questions fixed: {total_fixed}")
print("All files processed!")
print("=" * 60)
