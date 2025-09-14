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

html_dir = "html"
files_changed = []
total_fixes = 0

for exercise in exercises:
    # Parse exercise name
    parts = exercise.split("_")
    week = parts[0][2:]  # Remove "Gr" prefix
    ex_num = parts[1][1:]  # Remove "E" prefix

    # Find all HTML files for this exercise
    pattern = f"{exercise}_\\d+_\\d+\\.html"

    for filename in os.listdir(html_dir):
        if re.match(pattern, filename):
            filepath = os.path.join(html_dir, filename)

            # Extract tag and variation from filename
            # Format: Gr6_24_E3_3_1.html -> tag=3, variation=1
            name_parts = filename.replace(".html", "").split("_")
            if len(name_parts) >= 5:
                tag = name_parts[3]
                variation = name_parts[4]

                # Read the file
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content
                file_fixes = 0

                # First, revert any incorrect fixes that added exercise identifier to step labels
                # Pattern: Gr6_XX_EY_T_V_step_N -> Gr6_XX_T_V_step_N
                wrong_pattern = f'label="Gr6_{week}_E{ex_num}_{tag}_\\d+_step_\\d+"'
                for match in re.finditer(wrong_pattern, content):
                    old_label = match.group(0)
                    # Extract the parts
                    label_match = re.match(r'label="Gr6_(\d+)_E(\d+)_(\d+)_(\d+)_step_(\d+)"', old_label)
                    if label_match:
                        week_num = label_match.group(1)
                        ex = label_match.group(2)
                        tag_num = label_match.group(3)
                        var_num = label_match.group(4)
                        step = label_match.group(5)

                        # The correct format is WITHOUT the exercise identifier for step labels
                        correct_label = f'label="Gr6_{week_num}_{tag_num}_{variation}_step_{step}"'
                        content = content.replace(old_label, correct_label)
                        file_fixes += 1

                # Now fix any remaining incorrect variation numbers
                # Pattern: Gr6_XX_T_WRONG_step_N -> Gr6_XX_T_CORRECT_step_N
                step_pattern = f'label="Gr6_{week}_{tag}_\\d+_step_\\d+"'
                for match in re.finditer(step_pattern, content):
                    old_label = match.group(0)
                    # Extract the variation number from the label
                    label_match = re.match(r'label="Gr6_\d+_\d+_(\d+)_step_\d+"', old_label)
                    if label_match:
                        wrong_var = label_match.group(1)
                        if wrong_var != variation:
                            # Replace with correct variation
                            new_label = old_label.replace(f"_{wrong_var}_step_", f"_{variation}_step_")
                            content = content.replace(old_label, new_label)
                            file_fixes += 1

                # Save if modified
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_changed.append((filepath, file_fixes))
                    total_fixes += file_fixes

print(f"\nFixed {len(files_changed)} files with {total_fixes} label corrections")
print("\nDetailed changes:")
for file, fixes in sorted(files_changed)[:20]:  # Show first 20
    print(f"  {file}: {fixes} labels fixed")
if len(files_changed) > 20:
    print(f"  ... and {len(files_changed) - 20} more files")