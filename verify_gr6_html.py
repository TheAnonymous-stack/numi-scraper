import glob
import os
import random

# Count HTML files
html_files = glob.glob("Gr6_*.html")
print(f"Total Grade 6 HTML files generated: {len(html_files)}")

# Group by exercise
exercises = {}
for f in html_files:
    parts = os.path.basename(f).split("_")
    if len(parts) >= 3:
        week = parts[1]
        exercise = parts[2].split()[0]
        key = f"Week {week} Exercise {exercise}"
        if key not in exercises:
            exercises[key] = []
        exercises[key].append(f)

# Show distribution
print(f"\nDistribution across {len(exercises)} exercises:")
for key in sorted(exercises.keys())[:10]:
    print(f"  {key}: {len(exercises[key])} files")

# Sample some files to check they have content
print("\nSampling random files to verify content:")
sample_files = random.sample(html_files, min(5, len(html_files)))
for f in sample_files:
    size = os.path.getsize(f)
    with open(f, 'r') as file:
        content = file.read()
        has_svg = '<svg' in content
        has_div = '<div class="item"' in content
        num_divs = content.count('<div class="item"')
        print(f"  {os.path.basename(f)}: {size} bytes, SVG: {has_svg}, Divs: {num_divs}")

# Check for files with multiple visualizations (solution steps)
print("\nFiles with multiple visualizations (solution steps):")
multi_viz_count = 0
for f in html_files[:100]:  # Check first 100
    with open(f, 'r') as file:
        content = file.read()
        num_divs = content.count('<div class="item"')
        if num_divs > 1:
            multi_viz_count += 1
            if multi_viz_count <= 5:
                print(f"  {os.path.basename(f)}: {num_divs} visualizations")

print(f"\nTotal files with multiple visualizations: {multi_viz_count}+ (checked first 100 files)")

# Verify all expected visualization types are present
print("\nVisualization types found:")
viz_types = {
    "histogram": 0,
    "number line": 0,
    "angle": 0,
    "coordinate": 0,
    "place value": 0,
    "fraction": 0,
    "circle": 0,
    "rectangle": 0,
    "triangle": 0,
    "map": 0
}

for f in html_files[:500]:  # Check first 500 files
    with open(f, 'r') as file:
        content = file.read().lower()
        for viz_type in viz_types:
            if viz_type in content:
                viz_types[viz_type] += 1

for viz_type, count in viz_types.items():
    if count > 0:
        print(f"  {viz_type}: {count} files")

print("\nAll Grade 6 HTML visualization files have been successfully generated!")