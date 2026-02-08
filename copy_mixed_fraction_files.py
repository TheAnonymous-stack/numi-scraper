import json
import os
import shutil

# List of files to copy
files_to_copy = [
    "Gr7_3_E2_variations.json",
    "Gr7_3_E5_variations.json",
    "Gr7_6_E1_variations.json",
    "Gr7_7_E4_variations.json",
    "Gr7_17_E1_variations.json",
    "Gr7_21_E1_variations.json",
    "Gr7_21_E2_variations.json",
    "Gr7_22_E2_variations.json"
]

for filename in files_to_copy:
    print(f"\nProcessing {filename}...")

    # Read the source file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract the tag from the first question
    tag = data['quizzes'][0]['tag']

    # Create the edited_by_tag directory structure
    output_dir = f"edited_by_tag/{tag}"
    os.makedirs(output_dir, exist_ok=True)

    # Create the output filename
    output_filename = f"{tag}_edited.json"
    output_path = os.path.join(output_dir, output_filename)

    # Write the file to edited_by_tag
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  Copied to: {output_path}")

print("\n" + "=" * 60)
print("All files copied to edited_by_tag!")
print("=" * 60)
