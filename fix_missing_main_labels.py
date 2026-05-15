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
labels_added = 0

for exercise in exercises:
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
                modified = False

                # The main label should be Gr6_XX_EX_X_X (matching the filename without .html)
                main_label = filename.replace(".html", "")

                # Check if the main label is missing
                if f'label="{main_label}"' not in content:
                    # Find the first div with class="grid-container" and add a new div after it
                    grid_pattern = r'(<div class="grid-container">)'

                    # Create a new div with the main label
                    new_div = f'''
    <div class="visual-element item" label="{main_label}">
    </div>'''

                    # Insert after the grid-container opening tag
                    replacement = f'\\1{new_div}'
                    new_content = re.sub(grid_pattern, replacement, content, count=1)

                    if new_content != content:
                        content = new_content
                        modified = True
                        labels_added += 1

                # Save if modified
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_changed.append(filepath)

print(f"\nAdded {labels_added} main labels to {len(files_changed)} files")
if files_changed:
    print("\nFiles changed:")
    for file in sorted(files_changed)[:20]:  # Show first 20
        print(f"  {file}")
    if len(files_changed) > 20:
        print(f"  ... and {len(files_changed) - 20} more files")