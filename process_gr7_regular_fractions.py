import json
import re
import os
import shutil

# List of files with regular fractions only (no mixed fractions)
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

# Create directories to organize files
os.makedirs('edited_by_tag', exist_ok=True)

def process_fraction(frac_str):
    """
    Convert a fraction string like '3/4' to formatted versions.
    Returns list of alternate answer formats.
    """
    match = re.match(r'^(\d+)/(\d+)$', frac_str.strip())
    if match:
        numerator = match.group(1)
        denominator = match.group(2)

        # Create two versions: \frac and \dfrac
        return [
            f'\\frac{{{numerator}}}{{{denominator}}}',
            f'\\dfrac{{{numerator}}}{{{denominator}}}'
        ]
    return None

def process_answer(answer):
    """
    Process a single answer string. If it's a fraction, return formatted versions.
    Otherwise return original.
    """
    # Check if the answer is a simple fraction
    if isinstance(answer, str) and re.match(r'^\d+/\d+$', answer.strip()):
        formatted = process_fraction(answer)
        if formatted:
            return formatted
    return [answer]  # Return as list for consistency

def process_file(filename):
    """Process a single file and create edited version."""

    print(f"\nProcessing {filename}...")

    # Read original file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both formats: direct array or nested under "quizzes"
    if isinstance(data, dict) and "quizzes" in data:
        questions = data["quizzes"]
    elif isinstance(data, list):
        questions = data
    else:
        print(f"  ERROR: Unknown format")
        return

    total_changes = 0

    # Process each question
    for question in questions:
        if "correct_answers" not in question:
            continue

        original_answers = question["correct_answers"]

        # Check if it's already in nested format (has_alternate_answers)
        if "has_alternate_answers" in question and question["has_alternate_answers"]:
            # Already has alternate answers format - skip or update carefully
            continue

        # Process answers
        new_answers = []
        has_fractions = False

        for answer in original_answers:
            processed = process_answer(answer)
            if len(processed) > 1:  # It was a fraction that got formatted
                has_fractions = True
                # Add each variant as a separate alternate
                for variant in processed:
                    new_answers.append([variant])
            else:
                new_answers.append([processed[0]])

        # Update the question if we found fractions
        if has_fractions:
            question["has_alternate_answers"] = True
            question["correct_answers"] = new_answers
            total_changes += 1

    # Extract tag from first question to organize files
    tag = questions[0].get("tag", "unknown") if questions else "unknown"

    # Create tag-specific directory
    tag_dir = os.path.join('edited_by_tag', tag)
    os.makedirs(tag_dir, exist_ok=True)

    # Save original version
    original_path = os.path.join(tag_dir, filename.replace('.json', '_original.json'))
    shutil.copy(filename, original_path)

    # Save edited version
    edited_path = os.path.join(tag_dir, filename.replace('.json', '_edited.json'))

    # Preserve the original structure (with or without "quizzes" wrapper)
    if isinstance(data, dict) and "quizzes" in data:
        output_data = {"quizzes": questions}
    else:
        output_data = questions

    with open(edited_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"  Processed {total_changes} questions with fractions")
    print(f"  Original saved to: {original_path}")
    print(f"  Edited saved to: {edited_path}")

    return total_changes

# Process all files
print("=" * 80)
print("PROCESSING GRADE 7 REGULAR FRACTION FILES")
print("=" * 80)

total_files = 0
total_questions_changed = 0

for filename in regular_fraction_files:
    if os.path.exists(filename):
        changes = process_file(filename)
        if changes:
            total_files += 1
            total_questions_changed += changes
    else:
        print(f"\nWARNING: {filename} not found, skipping...")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Files processed: {total_files}")
print(f"Total questions with fractions formatted: {total_questions_changed}")
print(f"Files organized in: edited_by_tag/")
