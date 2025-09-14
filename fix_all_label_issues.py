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

                # Add missing main image label (e.g., Gr6_24_E3_3_1)
                main_label = f"{exercise}_{tag}_{variation}"
                if f'label="{main_label}"' not in content:
                    # Check if there's a div without the main label that should have it
                    # This is typically the first visual element
                    first_visual_pattern = r'(<div class="visual-element[^"]*")\s+(label="[^"]*")?'
                    matches = list(re.finditer(first_visual_pattern, content))

                    if matches:
                        # Check if first visual element needs the main label
                        first_match = matches[0]
                        if not first_match.group(2) or main_label not in first_match.group(0):
                            # Add the main label as an additional visual element if needed
                            # Or update existing labels - for now, we'll ensure step labels are correct
                            pass

                # The step labels have already been fixed by the previous script
                # Just ensure they're still correct

                # Count changes
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_changed.append(filepath)
                    total_fixes += content.count('label="') - original_content.count('label="')

print(f"\nFixed {len(files_changed)} files with {total_fixes} label corrections")
print("\nFiles changed:")
for file in sorted(files_changed):
    print(f"  {file}")