import json
import glob
import os
import re

# Get all Gr7 variation files
files = sorted(glob.glob("Gr7_*_E*_variations.json"))

# Filter to only include the main files (not file1_complete versions)
files = [f for f in files if "file1_complete" not in f]

print(f"Analyzing {len(files)} Grade 7 files for mixed vs regular fractions...\n")

files_with_mixed_fractions = []
files_with_regular_fractions_only = []
files_without_fractions = []

# Regex patterns
# Mixed fraction: number space number/number (e.g., "1 1/2", "3 2/5")
mixed_fraction_pattern = r'\d+\s+\d+/\d+'
# Regular fraction: just number/number (e.g., "1/2", "3/4")
regular_fraction_pattern = r'\d+/\d+'

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

        if not questions:
            continue

        # Check all questions for fractions
        has_mixed = False
        has_regular = False
        mixed_examples = []
        regular_examples = []

        for q in questions:
            if "correct_answers" in q:
                # Convert correct_answers to string to search for fractions
                answers_str = str(q["correct_answers"])

                # Check for mixed fractions first
                mixed_matches = re.findall(mixed_fraction_pattern, answers_str)
                if mixed_matches:
                    has_mixed = True
                    if len(mixed_examples) < 3:
                        mixed_examples.extend(mixed_matches[:3])

                # Check for regular fractions
                regular_matches = re.findall(regular_fraction_pattern, answers_str)
                if regular_matches:
                    has_regular = True
                    if len(regular_examples) < 3:
                        regular_examples.extend(regular_matches[:3])

        if has_mixed:
            files_with_mixed_fractions.append((filename, mixed_examples[:3], regular_examples[:3]))
        elif has_regular:
            files_with_regular_fractions_only.append((filename, regular_examples[:3]))
        else:
            files_without_fractions.append(filename)

    except Exception as e:
        print(f"ERROR: {filename} - {str(e)}")

print("=" * 80)
print(f"FILES WITH MIXED FRACTIONS ({len(files_with_mixed_fractions)}):")
print("=" * 80)
for filename, mixed_ex, regular_ex in sorted(files_with_mixed_fractions):
    print(f"\n{filename}")
    if mixed_ex:
        print(f"  Mixed examples: {', '.join(mixed_ex)}")
    if regular_ex:
        print(f"  Regular examples: {', '.join(regular_ex)}")

print("\n" + "=" * 80)
print(f"FILES WITH REGULAR FRACTIONS ONLY ({len(files_with_regular_fractions_only)}):")
print("=" * 80)
for filename, examples in sorted(files_with_regular_fractions_only):
    example_str = ", ".join(examples) if examples else "N/A"
    print(f"  {filename}")
    print(f"    Examples: {example_str}")

print("\n" + "=" * 80)
print(f"FILES WITHOUT ANY FRACTIONS ({len(files_without_fractions)}):")
print("=" * 80)
for filename in sorted(files_without_fractions):
    print(f"  {filename}")

print(f"\n{'=' * 80}")
print(f"SUMMARY:")
print(f"  Total files analyzed: {len(files_with_mixed_fractions) + len(files_with_regular_fractions_only) + len(files_without_fractions)}")
print(f"  Files with mixed fractions: {len(files_with_mixed_fractions)}")
print(f"  Files with regular fractions only: {len(files_with_regular_fractions_only)}")
print(f"  Files without fractions: {len(files_without_fractions)}")
