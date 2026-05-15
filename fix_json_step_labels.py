import json
import os
import re

# List of exercises to fix
exercises = [
    "Gr6_54_E3", "Gr6_55_E1", "Gr6_1_E4", "Gr6_1_E5", "Gr6_2_E1",
    "Gr6_3_E4", "Gr6_5_E1", "Gr6_3_E2", "Gr6_15_E5", "Gr6_16_E1",
    "Gr6_23_E1", "Gr6_23_E2", "Gr6_23_E3", "Gr6_24_E1", "Gr6_24_E2",
    "Gr6_24_E3", "Gr6_28_E3", "Gr6_33_E1", "Gr6_33_E2", "Gr6_34_E3",
    "Gr6_35_E1", "Gr6_36_E1", "Gr6_42_E4", "Gr6_43_E2", "Gr6_44_E1",
    "Gr6_44_E2", "Gr6_44_E3", "Gr6_45_E2", "Gr6_45_E4", "Gr6_50_E1",
    "Gr6_50_E2", "Gr6_51_E1", "Gr6_51_E2", "Gr6_51_E3", "Gr6_51_E4",
    "Gr6_52_E1", "Gr6_46_E3", "Gr6_47_E1", "Gr6_47_E2", "Gr6_48_E1"
]

files_fixed = []
total_fixes = 0

for exercise in exercises:
    json_file = f"{exercise}_variations.json"

    if not os.path.exists(json_file):
        print(f"File not found: {json_file}")
        continue

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        modified = False

        # Process each quiz variation
        for idx, quiz in enumerate(data.get('quizzes', [])):
            variation_num = idx + 1  # Variations are 1-indexed

            # Fix solution_image_tag if present
            if 'solution_image_tag' in quiz and quiz['solution_image_tag']:
                for step in quiz['solution_image_tag']:
                    if len(step) >= 2:
                        old_label = step[1]
                        # Check if it's a step label that needs fixing
                        # Pattern: Gr6_XX_Y_Z_step_N
                        match = re.match(r"(Gr\d+_\d+_)(\d+)_(\d+)(_step_\d+)", old_label)
                        if match:
                            prefix = match.group(1)
                            tag_num = match.group(2)
                            wrong_var = match.group(3)
                            suffix = match.group(4)

                            # The variation in the label should match the current variation
                            correct_var = str(variation_num)
                            if wrong_var != correct_var:
                                new_label = f"{prefix}{tag_num}_{correct_var}{suffix}"
                                step[1] = new_label
                                modified = True
                                total_fixes += 1
                                print(f"  Fixed: {old_label} -> {new_label} in {json_file}")

        # Save if modified
        if modified:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            files_fixed.append(json_file)

    except Exception as e:
        print(f"Error processing {json_file}: {e}")

print(f"\n\nSummary:")
print(f"Fixed {total_fixes} labels in {len(files_fixed)} JSON files")
if files_fixed:
    print("\nFiles modified:")
    for file in sorted(files_fixed):
        print(f"  {file}")