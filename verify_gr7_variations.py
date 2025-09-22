import json
import os
import glob

# Get all Grade 7 variation files
pattern = r"C:\Users\kapil\numi-scraper\Gr7_*_variations.json"
files = glob.glob(pattern)

print(f"Checking {len(files)} Grade 7 variation files...")
print("=" * 60)

# Counter for different variation counts
variation_counts = {}
incorrect_files = []

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if the file has the quizzes structure
    if isinstance(data, dict) and "quizzes" in data:
        num_variations = len(data["quizzes"])
    else:
        num_variations = len(data)

    file_name = os.path.basename(file_path)

    # Count occurrences
    if num_variations not in variation_counts:
        variation_counts[num_variations] = []
    variation_counts[num_variations].append(file_name)

    # Track incorrect files
    if num_variations != 51:
        incorrect_files.append((file_name, num_variations))
        print(f"INCORRECT: {file_name}: {num_variations} variations")

# Print summary
print("\n" + "=" * 60)
print("SUMMARY:")
print("=" * 60)

for count in sorted(variation_counts.keys()):
    num_files = len(variation_counts[count])
    status = "CORRECT" if count == 51 else "INCORRECT"
    print(f"{status}: Files with {count} variations: {num_files}")

if incorrect_files:
    print(f"\nWARNING: {len(incorrect_files)} files still need fixing!")
    print("Files that don't have 51 variations:")
    for fname, count in incorrect_files:
        print(f"  - {fname}: {count} variations")
else:
    print("\nSUCCESS! All files have exactly 51 variations!")

print(f"\nTotal files checked: {len(files)}")