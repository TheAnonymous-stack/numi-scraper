import json
import glob
import os
import re

# Get all Gr7 variation files
files = sorted(glob.glob("Gr7_*_E*_variations.json"))

# Filter to only include the main files (not file1_complete versions)
files = [f for f in files if "file1_complete" not in f]

print(f"Analyzing {len(files)} Grade 7 files for fractions...\n")

files_with_fractions = []
files_without_fractions = []

# Regex pattern to detect fractions (e.g., 1/2, 3/4, 10/100, etc.)
fraction_pattern = r'\d+/\d+'

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

        # Check if any question has fractions in correct_answers
        has_fractions = False
        fraction_examples = []

        for q in questions:
            if "correct_answers" in q:
                # Convert correct_answers to string to search for fractions
                answers_str = str(q["correct_answers"])
                if re.search(fraction_pattern, answers_str):
                    has_fractions = True
                    # Get a few examples
                    matches = re.findall(fraction_pattern, answers_str)
                    if matches and len(fraction_examples) < 3:
                        fraction_examples.extend(matches[:3])
                    if len(fraction_examples) >= 3:
                        break

        if has_fractions:
            files_with_fractions.append((filename, fraction_examples[:3]))
        else:
            files_without_fractions.append(filename)

    except Exception as e:
        print(f"ERROR: {filename} - {str(e)}")

print("=" * 80)
print(f"FILES WITH FRACTIONS IN CORRECT ANSWERS ({len(files_with_fractions)}):")
print("=" * 80)
for filename, examples in sorted(files_with_fractions):
    example_str = ", ".join(examples) if examples else "N/A"
    print(f"  {filename}")
    print(f"    Examples: {example_str}")

print("\n" + "=" * 80)
print(f"FILES WITHOUT FRACTIONS ({len(files_without_fractions)}):")
print("=" * 80)
for filename in sorted(files_without_fractions):
    print(f"  {filename}")

print(f"\nTotal files analyzed: {len(files_with_fractions) + len(files_without_fractions)}")
print(f"Files with fractions: {len(files_with_fractions)}")
print(f"Files without fractions: {len(files_without_fractions)}")
