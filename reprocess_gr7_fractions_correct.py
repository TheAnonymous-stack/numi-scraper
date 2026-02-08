import json
import re
import os
import shutil

# Files to reprocess from the edited_by_tag backups
files_to_reprocess = {
    'Gr7_5_E2_variations.json': 'Fill in the blank',
    'Gr7_5_E3_variations.json': 'Fraction fill in the blank',
    'Gr7_6_E2_variations.json': 'Fill in the blank',
    'Gr7_7_E3_variations.json': 'Fill in the blank',
    'Gr7_13_E1_variations.json': 'Fill in the blank',
    'Gr7_13_E2_variations.json': 'Fill in the blank',
    'Gr7_14_E1_variations.json': 'Fill in the blank',
    'Gr7_14_E2_variations.json': 'Fill in the blank',
    'Gr7_15_E1_variations.json': 'Fill in the blank',
    'Gr7_15_E2_variations.json': 'Fill in the blank',
    'Gr7_16_E1_variations.json': 'Fill in the blank',
    'Gr7_16_E2_variations.json': 'Fill in the blank',
    'Gr7_17_E2_variations.json': 'Fill in the blank',
    'Gr7_20_E1_variations.json': 'Fill in the blank',
    'Gr7_20_E2_variations.json': 'Fill in the blank',
    'Gr7_20_E3_variations.json': 'Fill in the blank',
    'Gr7_22_E1_variations.json': 'Fill in the blank',
    'Gr7_22_E3_variations.json': 'Fill in the blank',
    'Gr7_22_E4_variations.json': 'Fill in the blank',
    'Gr7_27_E3_variations.json': 'Fill in the blank',
    'Gr7_35_E2_variations.json': 'Multiple fill in the blank',
}

def process_multiple_fill_blank(question):
    """Process for 'Multiple fill in the blank' - like Gr5_3"""
    if "correct_answers" not in question:
        return False

    original_answers = question["correct_answers"]

    # Check if already in nested format with has_alternate_answers
    if isinstance(original_answers, list) and len(original_answers) > 0:
        if isinstance(original_answers[0], list):
            # Already nested - extract the fraction and split it
            # Get the first answer variant (should be like ["\\frac{2}{5}"])
            first_answer = original_answers[0][0]
            match = re.search(r'\\[d]?frac\{(\d+)\}\{(\d+)\}', first_answer)
            if match:
                numerator = match.group(1)
                denominator = match.group(2)
                question["correct_answers"] = [numerator, denominator]
                question["has_alternate_answers"] = True
                question["orderMatter"] = True

                # Add the special formatting to question_text if not already there
                if not question["question_text"].endswith("$\\\\\\\\[1em]$\\n\\n_/_ "):
                    question["question_text"] += " $\\\\\\\\[1em]$\\n\\n_/_ "

                return True

    return False

def process_fraction_fill_blank(question):
    """Process for 'Fraction fill in the blank' - like Gr5_3 but check existing format"""
    # Similar to Multiple fill in the blank
    return process_multiple_fill_blank(question)

def process_fill_blank(question):
    """Process for regular 'Fill in the blank' - keep  current \frac format"""
    # These are already correctly formatted, keep as is
    return False

# Main processing
print("=" * 80)
print("REPROCESSING GRADE 7 FILES TO MATCH GRADE 5 FORMAT")
print("=" * 80)

for filename, q_type in files_to_reprocess.items():
    tag = filename.replace('_variations.json', '')

    print(f"\nProcessing {filename} ({q_type})...")

    # Read from current main file (which has the nested format)
    if not os.path.exists(filename):
        print(f"  WARNING: {filename} not found, skipping...")
        continue

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

    # Process based on question type
    for question in questions:
        if q_type == "Multiple fill in the blank":
            if process_multiple_fill_blank(question):
                changes += 1
        elif q_type == "Fraction fill in the blank":
            if process_fraction_fill_blank(question):
                changes += 1
        elif q_type == "Fill in the blank":
            # Keep as is - already has \frac format
            pass

    if changes > 0:
        # Save to main directory
        output_data = {"quizzes": questions} if isinstance(data, dict) and "quizzes" in data else questions

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        # Update edited version in edited_by_tag
        tag_dir = os.path.join('edited_by_tag', tag)
        edited_path = os.path.join(tag_dir, f'{tag}_edited.json')

        with open(edited_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"  Updated {changes} questions")
    else:
        print(f"  No changes needed (already correct format)")

print("\n" + "=" * 80)
print("DONE!")
print("=" * 80)
