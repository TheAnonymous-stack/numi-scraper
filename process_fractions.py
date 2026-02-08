import json
import re
import copy

# List of files to process
files_to_process = [
    "Gr5_21_E2_variations.json",
    "Gr5_21_E3_variations.json",
    "Gr5_22_E1_variations.json",
    "Gr5_22_E2_variations.json",
    "Gr5_22_E3_variations.json",
    "Gr5_23_E1_variations.json",
    "Gr5_23_E3_variations.json",
    "Gr5_23_E4_variations.json",
    "Gr5_24_E1_variations.json",
    "Gr5_24_E2_variations.json",
    "Gr5_27_E1_variations.json",
    "Gr5_27_E4_variations.json",
    "Gr5_3_E3_variations.json",
    "Gr5_3_E4_variations.json",
    "Gr5_42_E1_variations.json",
    "Gr5_42_E3_variations.json",
    "Gr5_5_E1_variations.json",
    "Gr5_5_E2_variations.json",
    "Gr5_5_E3_variations.json",
    "Gr5_5_E4_variations.json",
    "Gr5_8_E2_variations.json",
    "Gr5_9_E1_variations.json",
    "Gr5_9_E3_variations.json"
]

# Regex patterns
regular_fraction_pattern = re.compile(r'^(\d+)/(\d+)$')  # Only regular fractions like "2/5"
mixed_fraction_pattern = re.compile(r'\d+\s+\d+/\d+')  # Mixed fractions like "1 1/2"

def is_mixed_fraction(answer):
    """Check if answer contains a mixed fraction"""
    return bool(mixed_fraction_pattern.search(answer))

def is_regular_fraction(answer):
    """Check if answer is a regular fraction (not mixed)"""
    return bool(regular_fraction_pattern.match(answer.strip()))

def transform_question(question):
    """Transform a question with regular fraction answer to grade6 format"""
    q = copy.deepcopy(question)

    # Check if this question has fraction answers
    correct_answers = q.get('correct_answers', [])
    if not correct_answers:
        return q

    # Check if it already has nested arrays (has_alternate_answers structure)
    has_nested = False
    if correct_answers and isinstance(correct_answers[0], list):
        has_nested = True
        # Flatten to check all answers
        all_answers = []
        for ans_group in correct_answers:
            if isinstance(ans_group, list):
                all_answers.extend(ans_group)
            else:
                all_answers.append(ans_group)
    else:
        all_answers = correct_answers

    # Check if any answer is a mixed fraction - if so, don't transform
    for ans in all_answers:
        if isinstance(ans, str) and is_mixed_fraction(ans):
            return q  # Return unchanged

    # Find the first regular fraction answer
    fraction_to_split = None
    if has_nested:
        # Look in the nested arrays for a fraction
        for ans_group in correct_answers:
            if isinstance(ans_group, list):
                for ans in ans_group:
                    if isinstance(ans, str):
                        match = regular_fraction_pattern.match(ans.strip())
                        if match:
                            fraction_to_split = match
                            break
            if fraction_to_split:
                break
    else:
        # Simple list, check first answer
        first_answer = correct_answers[0] if correct_answers else ""
        if isinstance(first_answer, str):
            match = regular_fraction_pattern.match(first_answer.strip())
            if match:
                fraction_to_split = match

    # If no regular fraction found, return unchanged
    if not fraction_to_split:
        return q

    numerator = fraction_to_split.group(1)
    denominator = fraction_to_split.group(2)

    # Transform the question
    q['question_type'] = "Multiple fill in the blank"

    # Update question_text to end with the fraction format
    question_text = q.get('question_text', '')
    # Add the fraction blank format at the end
    if not question_text.endswith('_/_ '):
        # Remove any trailing punctuation/whitespace and add the new format
        question_text = question_text.rstrip()
        q['question_text'] = f"{question_text} $\\\\[1em]$\n\n_/_ "

    # Split the fraction into numerator and denominator
    q['correct_answers'] = [numerator, denominator]

    # Add the required fields
    q['has_alternate_answers'] = True
    q['orderMatter'] = True

    return q

# Process all files
all_original_questions = []
all_edited_questions = []

for filename in files_to_process:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            # Store original questions
            all_original_questions.extend(copy.deepcopy(data))

            # Transform questions
            edited_data = []
            for question in data:
                transformed = transform_question(question)
                edited_data.append(transformed)

            all_edited_questions.extend(edited_data)

            print(f"Processed {filename}: {len(data)} questions")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

# Save combined files
print(f"\nTotal questions: {len(all_original_questions)}")

with open('combined_original.json', 'w', encoding='utf-8') as f:
    json.dump(all_original_questions, f, indent=2, ensure_ascii=False)
print(f"Saved combined_original.json")

with open('combined_edited.json', 'w', encoding='utf-8') as f:
    json.dump(all_edited_questions, f, indent=2, ensure_ascii=False)
print(f"Saved combined_edited.json")

# Count how many questions were transformed
transformed_count = 0
for orig, edited in zip(all_original_questions, all_edited_questions):
    if orig != edited:
        transformed_count += 1

print(f"\nTransformed {transformed_count} questions with regular fractions")
print(f"Left {len(all_original_questions) - transformed_count} questions unchanged")
