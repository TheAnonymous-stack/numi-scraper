import json
import glob
import os

# Get all Gr5 variation files
files = sorted(glob.glob("Gr5_*_E*_variations.json"))

# Filter to only include the main files (not file1_complete versions)
files = [f for f in files if "file1_complete" not in f]

print(f"Analyzing 51st question in {len(files)} files...\n")

files_with_multiple_in_51st = []
files_with_single_in_51st = []
files_without_51st = []

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

        # Check if there are at least 51 questions
        if len(questions) < 51:
            files_without_51st.append((filename, len(questions)))
            continue

        # Get the 51st question (index 50)
        question_51 = questions[50]

        if "correct_answers" in question_51:
            num_answers = len(question_51["correct_answers"])
            if num_answers > 1:
                files_with_multiple_in_51st.append((filename, num_answers, question_51["correct_answers"]))
            else:
                files_with_single_in_51st.append((filename, question_51["correct_answers"]))
        else:
            print(f"SKIP: {filename} - No correct_answers field in 51st question")

    except Exception as e:
        print(f"ERROR: {filename} - {str(e)}")

print("=" * 80)
print(f"FILES WITH MULTIPLE ANSWERS IN 51ST QUESTION ({len(files_with_multiple_in_51st)}):")
print("=" * 80)
for filename, num_ans, answers in sorted(files_with_multiple_in_51st):
    print(f"\n{filename} ({num_ans} answers):")
    for i, ans in enumerate(answers, 1):
        print(f"  {i}. {ans}")

print("\n" + "=" * 80)
print(f"FILES WITH SINGLE ANSWER IN 51ST QUESTION ({len(files_with_single_in_51st)}):")
print("=" * 80)
for filename, answers in sorted(files_with_single_in_51st):
    print(f"  {filename}: {answers[0]}")

if files_without_51st:
    print("\n" + "=" * 80)
    print(f"FILES WITH FEWER THAN 51 QUESTIONS ({len(files_without_51st)}):")
    print("=" * 80)
    for filename, count in sorted(files_without_51st):
        print(f"  {filename} (has {count} questions)")

print(f"\nTotal files analyzed: {len(files_with_multiple_in_51st) + len(files_with_single_in_51st) + len(files_without_51st)}")
