import json
import re
import os
import shutil

# All files with regular fractions that need to be formatted like Gr5_3
regular_fraction_files = [
    'Gr7_5_E2_variations.json',
    'Gr7_5_E3_variations.json',
    'Gr7_6_E2_variations.json',
    'Gr7_7_E3_variations.json',
    'Gr7_13_E1_variations.json',
    'Gr7_13_E2_variations.json',
    'Gr7_14_E1_variations.json',
    'Gr7_14_E2_variations.json',
    'Gr7_15_E1_variations.json',
    'Gr7_15_E2_variations.json',
    'Gr7_16_E1_variations.json',
    'Gr7_16_E2_variations.json',
    'Gr7_17_E2_variations.json',
    'Gr7_20_E1_variations.json',
    'Gr7_20_E2_variations.json',
    'Gr7_20_E3_variations.json',
    'Gr7_22_E1_variations.json',
    'Gr7_22_E3_variations.json',
    'Gr7_22_E4_variations.json',
    'Gr7_27_E3_variations.json',
    'Gr7_35_E2_variations.json',
]

def extract_fraction_from_answer(answer):
    """Extract numerator and denominator from a fraction answer"""
    # Handle various formats: "3/4", "\\frac{3}{4}", "\\dfrac{3}{4}"

    # First check for \frac or \dfrac format
    match = re.search(r'\\[d]?frac\{(\d+)\}\{(\d+)\}', str(answer))
    if match:
        return match.group(1), match.group(2)

    # Check for simple fraction format
    match = re.search(r'^(\d+)/(\d+)$', str(answer).strip())
    if match:
        return match.group(1), match.group(2)

    return None, None

def process_question(question):
    """Process a single question to match Gr5_3 format"""

    if "correct_answers" not in question:
        return False

    original_answers = question["correct_answers"]

    # Check if this answer contains a fraction
    has_fraction = False
    numerator = None
    denominator = None

    # Handle different answer formats
    if isinstance(original_answers, list):
        if len(original_answers) > 0:
            # Check if it's nested format [[...], [...]]
            if isinstance(original_answers[0], list):
                # Extract from first nested answer
                for ans_variant in original_answers:
                    if len(ans_variant) > 0:
                        num, denom = extract_fraction_from_answer(ans_variant[0])
                        if num and denom:
                            numerator, denominator = num, denom
                            has_fraction = True
                            break
            else:
                # Check if first answer is a fraction
                num, denom = extract_fraction_from_answer(original_answers[0])
                if num and denom:
                    numerator, denominator = num, denom
                    has_fraction = True

    if not has_fraction:
        return False

    # Transform the question to match Gr5_3 format:

    # 1. Change question_type to "Multiple fill in the blank"
    question["question_type"] = "Multiple fill in the blank"

    # 2. Add $\\\\[1em]$\n\n_/_ to the end of question_text if not already there
    if "$\\\\\\\\[1em]$\\n\\n_/_ " not in question["question_text"]:
        # Remove any existing formatting at the end first
        q_text = question["question_text"].rstrip()
        question["question_text"] = q_text + " $\\\\\\\\[1em]$\\n\\n_/_ "

    # 3. Set correct_answers to just numerator and denominator
    question["correct_answers"] = [numerator, denominator]

    # 4. Add has_alternate_answers and orderMatter
    question["has_alternate_answers"] = True
    question["orderMatter"] = True

    return True

# Main processing
print("=" * 80)
print("FORMATTING ALL GRADE 7 FILES EXACTLY LIKE GRADE 5")
print("=" * 80)

total_files = 0
total_questions = 0

for filename in regular_fraction_files:
    if not os.path.exists(filename):
        print(f"\nWARNING: {filename} not found, skipping...")
        continue

    tag = filename.replace('_variations.json', '')

    print(f"\nProcessing {filename}...")

    # Read file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both formats
    if isinstance(data, dict) and "quizzes" in data:
        questions = data["quizzes"]
    elif isinstance(data, list):
        questions = data
    else:
        print(f"  ERROR: Unknown format")
        continue

    changes = 0

    # Process each question
    for question in questions:
        if process_question(question):
            changes += 1

    if changes > 0:
        total_files += 1
        total_questions += changes

        # Save to main directory
        output_data = {"quizzes": questions} if isinstance(data, dict) and "quizzes" in data else questions

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        # Update edited version in edited_by_tag
        tag_dir = os.path.join('edited_by_tag', tag)
        os.makedirs(tag_dir, exist_ok=True)
        edited_path = os.path.join(tag_dir, f'{tag}_edited.json')

        with open(edited_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"  Formatted {changes} questions with fractions")
    else:
        print(f"  No fractions found to format")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Files processed: {total_files}")
print(f"Total questions formatted: {total_questions}")
print(f"All files now match Gr5_3 format!")
