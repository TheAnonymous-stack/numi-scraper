import json
import glob
import os

# Get all Gr5 variation files
files = sorted(glob.glob("Gr5_*_E*_variations.json"))

# Filter to only include the main files (not file1_complete versions)
files = [f for f in files if "file1_complete" not in f]

print(f"Analyzing 51st question for nested array format in {len(files)} files...\n")

files_with_nested_format = []
files_without_nested_format = []

for filepath in files:
    filename = os.path.basename(filepath)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle both formats: direct array or nested under "quizzes"
        if isinstance(data, dict) and "quizzes" in data:
            questions = data["quizzes"]
        elif isinstance(data, list):
            questions = data
        else:
            continue

        # Check if there are at least 51 questions
        if len(questions) < 51:
            continue

        # Get the 51st question (index 50)
        question_51 = questions[50]

        # Check for the specific nested format
        has_nested_format = False

        if "has_alternate_answers" in question_51 and question_51["has_alternate_answers"] == True:
            if "correct_answers" in question_51:
                answers = question_51["correct_answers"]
                # Check if it's a nested array structure (list of lists)
                if isinstance(answers, list) and len(answers) > 0:
                    if isinstance(answers[0], list):
                        has_nested_format = True
                        files_with_nested_format.append((filename, answers))
                    else:
                        files_without_nested_format.append(filename)

    except Exception as e:
        print(f"ERROR: {filename} - {str(e)}")

print("=" * 80)
print(f"FILES WITH NESTED ALTERNATE ANSWERS FORMAT IN 51ST QUESTION ({len(files_with_nested_format)}):")
print("=" * 80)
for filename, answers in sorted(files_with_nested_format):
    print(f"\n{filename} ({len(answers)} alternate answers):")
    for i, ans in enumerate(answers, 1):
        print(f"  {i}. {ans}")

print(f"\n{'=' * 80}")
print(f"Total files with nested format: {len(files_with_nested_format)}")
