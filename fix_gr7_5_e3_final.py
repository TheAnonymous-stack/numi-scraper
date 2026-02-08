import json

# Read Gr7_5_E3
with open('Gr7_5_E3_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data["quizzes"]

print("Fixing Gr7_5_E3 improper to mixed format...\n")

for i, question in enumerate(questions, 1):
    q_text = question.get("question_text", "")

    # Check if it's asking to convert TO mixed number (improper to mixed)
    if "as a mixed number" in q_text or "to a mixed number" in q_text:
        # This should be "Multiple fill in the blank" with _ _/_ format
        question["question_type"] = "Multiple fill in the blank"

        # Ensure it has the _ _/_ format - already there, don't change question_text

        # The 3 answers are already correct: [whole, numerator, denominator]
        # Just need to add the proper flags
        question["has_alternate_answers"] = True
        question["orderMatter"] = True

        print(f"Question {i}: Improper to Mixed - 3 answers (whole, num, denom): {question['correct_answers']}")

    # Mixed to improper - already correct, just verify
    elif "to an improper fraction" in q_text or "as an improper fraction" in q_text:
        print(f"Question {i}: Mixed to Improper - 2 answers (num, denom): {question['correct_answers']}")

# Save the fixed file
output_data = {"quizzes": questions}

with open('Gr7_5_E3_variations.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

with open('edited_by_tag/Gr7_5_E3/Gr7_5_E3_edited.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("\nDone! Gr7_5_E3 has been fixed properly.")
print("- Improper to Mixed: Multiple fill in the blank, 3 answers [whole, num, denom], _ _/_ format")
print("- Mixed to Improper: Multiple fill in the blank, 2 answers [num, denom], _/_ format")
