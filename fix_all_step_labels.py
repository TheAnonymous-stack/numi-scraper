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
files_changed = {}
total_fixes = 0

for exercise in exercises:
    # Parse exercise name
    parts = exercise.split("_")
    week = parts[0][2:]  # Remove "Gr" prefix
    ex_num = parts[1][1:]  # Remove "E" prefix

    # Find all HTML files for this exercise
    pattern = f"{exercise}_\\d+_\\d+\\.html"
    exercise_files_changed = []

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
                changes = []

                # Fix step labels that have exercise identifier (should NOT have it)
                # Pattern: Gr6_XX_EY_T_V_step_N -> Gr6_XX_T_V_step_N
                wrong_step_pattern = f'label="Gr6_{week}_E{ex_num}_{tag}_\\d+_step_\\d+"'
                for match in re.finditer(wrong_step_pattern, content):
                    old_label = match.group(0)
                    # Extract the parts
                    label_match = re.match(r'label="Gr6_(\d+)_E(\d+)_(\d+)_(\d+)_step_(\d+)"', old_label)
                    if label_match:
                        week_num = label_match.group(1)
                        tag_num = label_match.group(3)
                        var_num = label_match.group(4)
                        step = label_match.group(5)

                        # Correct format: WITHOUT exercise identifier, WITH correct variation
                        correct_label = f'label="Gr6_{week_num}_{tag_num}_{variation}_step_{step}"'
                        if old_label != correct_label:
                            content = content.replace(old_label, correct_label)
                            changes.append(f"{old_label} -> {correct_label}")

                # Also fix step labels that have wrong variation number (but no exercise identifier)
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
                            new_label = old_label.replace(f"_{tag}_{wrong_var}_step_", f"_{tag}_{variation}_step_")
                            if new_label not in content:  # Avoid duplicate replacements
                                content = content.replace(old_label, new_label)
                                changes.append(f"{old_label} -> {new_label}")

                # Save if modified
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    exercise_files_changed.append((filename, changes))
                    total_fixes += len(changes)

    if exercise_files_changed:
        files_changed[exercise] = exercise_files_changed

print(f"\n=== COMPREHENSIVE FIX REPORT ===")
print(f"Total exercises processed: {len(exercises)}")
print(f"Total files changed: {sum(len(files) for files in files_changed.values())}")
print(f"Total label fixes: {total_fixes}")

print(f"\n=== CHANGES BY EXERCISE ===")
for exercise in sorted(files_changed.keys()):
    print(f"\n{exercise}: {len(files_changed[exercise])} files changed")
    for filename, changes in files_changed[exercise][:3]:  # Show first 3 files
        print(f"  {filename}:")
        for change in changes[:2]:  # Show first 2 changes per file
            print(f"    {change}")
        if len(changes) > 2:
            print(f"    ... and {len(changes) - 2} more changes")
    if len(files_changed[exercise]) > 3:
        print(f"  ... and {len(files_changed[exercise]) - 3} more files")

# Save detailed report
with open("COMPLETE_FIX_REPORT.txt", "w") as f:
    f.write(f"=== COMPREHENSIVE HTML LABEL FIX REPORT ===\n")
    f.write(f"Total exercises processed: {len(exercises)}\n")
    f.write(f"Total files changed: {sum(len(files) for files in files_changed.values())}\n")
    f.write(f"Total label fixes: {total_fixes}\n\n")

    for exercise in sorted(files_changed.keys()):
        f.write(f"\n{exercise}: {len(files_changed[exercise])} files changed\n")
        for filename, changes in files_changed[exercise]:
            f.write(f"  {filename}:\n")
            for change in changes:
                f.write(f"    {change}\n")

print(f"\nDetailed report saved to COMPLETE_FIX_REPORT.txt")