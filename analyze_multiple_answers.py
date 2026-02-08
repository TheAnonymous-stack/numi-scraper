import json
import glob
import os

# Get all Gr5 variation files
files = sorted(glob.glob("Gr5_*_E*_variations.json"))

# Filter to only include the main files (not file1_complete versions)
files = [f for f in files if "file1_complete" not in f]

print(f"Analyzing {len(files)} files...\n")

files_with_multiple_answers = []
files_with_single_answers = []

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
            print(f"SKIP: {filename} - Unknown format")
            continue

        if not questions:
            print(f"SKIP: {filename} - No questions found")
            continue

        # Check if any question has multiple correct answers
        has_multiple = False
        max_answers = 0

        for q in questions:
            if "correct_answers" in q:
                num_answers = len(q["correct_answers"])
                max_answers = max(max_answers, num_answers)
                if num_answers > 1:
                    has_multiple = True
                    break

        if has_multiple:
            files_with_multiple_answers.append((filename, max_answers))
        else:
            files_with_single_answers.append(filename)

    except Exception as e:
        print(f"ERROR: {filename} - {str(e)}")

print("=" * 80)
print(f"FILES WITH MULTIPLE CORRECT ANSWERS ({len(files_with_multiple_answers)}):")
print("=" * 80)
for filename, max_ans in sorted(files_with_multiple_answers):
    print(f"  {filename} (max {max_ans} answers)")

print("\n" + "=" * 80)
print(f"FILES WITH SINGLE CORRECT ANSWERS ONLY ({len(files_with_single_answers)}):")
print("=" * 80)
for filename in sorted(files_with_single_answers):
    print(f"  {filename}")

print(f"\nTotal files analyzed: {len(files_with_multiple_answers) + len(files_with_single_answers)}")
