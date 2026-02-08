import json
import re

# Read Gr7_5_E3
with open('Gr7_5_E3_variations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data["quizzes"]

print("Fixing Gr7_5_E3_variations.json...\n")

for i, question in enumerate(questions, 1):
    q_text = question.get("question_text", "")

    # Check if it's asking to convert TO improper fraction (mixed → improper)
    if "to an improper fraction" in q_text or "as an improper fraction" in q_text:
        # Should have ONLY 2 answers: numerator, denominator
        # Change to Multiple fill in the blank
        question["question_type"] = "Multiple fill in the blank"

        # Add _/_ format if not there
        if "$\\\\\\\\[1em]$\\n\\n_/_ " not in q_text:
            q_text = q_text.replace("= ?", "=").strip()
            if not q_text.endswith("_/_"):
                question["question_text"] = q_text.rstrip() + " $\\\\\\\\[1em]$\\n\\n_/_ "

        # Ensure only 2 answers (numerator, denominator)
        if len(question["correct_answers"]) != 2:
            question["correct_answers"] = question["correct_answers"][:2]

        question["has_alternate_answers"] = True
        question["orderMatter"] = True

        print(f"Question {i}: Mixed to Improper - Fixed to 2 answers: {question['correct_answers']}")

    # Check if it's asking to convert TO mixed number (improper to mixed)
    elif "as a mixed number" in q_text or "to a mixed number" in q_text:
        # Leave as is - these are already correct with 3 answers
        print(f"Question {i}: Improper to Mixed - Keeping 3 answers: {question['correct_answers']}")

# Save the fixed file
output_data = {"quizzes": questions}

with open('Gr7_5_E3_variations.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

with open('edited_by_tag/Gr7_5_E3/Gr7_5_E3_edited.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("\nDone! Gr7_5_E3 has been fixed.")
