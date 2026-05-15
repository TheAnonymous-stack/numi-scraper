import os
import re
import json

# List of exercises to check
target_exercises = [
    "Gr6_54_E3", "Gr6_55_E1", "Gr6_1_E4", "Gr6_1_E5", "Gr6_2_E1",
    "Gr6_3_E4", "Gr6_5_E1", "Gr6_3_E2", "Gr6_15_E5", "Gr6_16_E1",
    "Gr6_23_E1", "Gr6_23_E2", "Gr6_23_E3", "Gr6_24_E1", "Gr6_24_E2",
    "Gr6_24_E3", "Gr6_28_E3", "Gr6_33_E1", "Gr6_33_E2", "Gr6_34_E3",
    "Gr6_35_E1", "Gr6_36_E1", "Gr6_42_E4", "Gr6_43_E2", "Gr6_44_E1"
]

issues_found = {}
directory = "./html"

for file in os.listdir(directory):
    # Check naming convention first
    matchUnderscore = re.match(r"Gr6_(\d+)_E(\d+)_(\d+)_(\d+)\.html", file)
    matchSpace = re.match(r"Gr6_(\d+)_E(\d+)\s(\d+)_(\d+)\.html", file)
    if matchUnderscore is None and matchSpace is None:
        continue
    match = matchUnderscore if matchUnderscore else matchSpace

    if match.group(2) != match.group(3):
        continue

    week = match.group(1)
    exercise = match.group(2)
    variation = int(match.group(4))

    # Check if this is one of our target exercises
    exercise_tag = f"Gr6_{week}_E{exercise}"
    if exercise_tag not in target_exercises:
        continue
    
    # Opening JSON variation file to check for compatibility
    with open(f"Gr6_{week}_E{exercise}_variations.json", "r") as f:
        data = json.load(f)['quizzes']
        question = data[variation - 1]
        imagesToCreate = {}
        if "image_tag" in question:
            imagesToCreate[question["image_tag"]] = 0
        if "image_choice_tags" in question:
            for choice in question['image_choice_tags']:
                imagesToCreate[choice] = 0
        if "solution_image_tag" in question and len(question["solution_image_tag"]) > 0:
            for step in question["solution_image_tag"]:
                img = step[1]
                imagesToCreate[img] = 0

        if "shape_image_tags" in question:
            for shape in question['shape_image_tags']:
                img = shape['tag']
                imagesToCreate[img] = 0
        # Read the HTML file and search for divs with class="item" and expected labels
        html_file_path = os.path.join(directory, file)
        with open(html_file_path, "r", encoding="utf-8", errors="replace") as html_file:
            html_content = html_file.read()

            
        # Check for each expected image label
        missing_labels = []
        found_labels = []
        
        for label in imagesToCreate:
            # Search for div with class containing "item" and the specific label
            pattern = rf'<div[^>]*class="[^"]*item[^"]*"[^>]*label="{re.escape(label)}"'
            if re.search(pattern, html_content):
                imagesToCreate[label] = 1
        
        # Report results and store issues
        for label in imagesToCreate:
            if imagesToCreate[label] == 0:
                if exercise_tag not in issues_found:
                    issues_found[exercise_tag] = []
                issues_found[exercise_tag].append({
                    'file': file,
                    'missing_label': label
                })
                print(f"{file} is missing {label}")

# Print summary
print("\n" + "="*80)
print("SUMMARY OF ISSUES IN TARGET EXERCISES")
print("="*80)

for exercise in target_exercises:
    if exercise in issues_found:
        print(f"\n{exercise}: {len(issues_found[exercise])} issues found")
        # Count unique missing labels
        missing_labels = set()
        for issue in issues_found[exercise]:
            missing_labels.add(issue['missing_label'])
        print(f"  - Unique missing labels: {len(missing_labels)}")
        print(f"  - Total missing instances: {len(issues_found[exercise])}")
    else:
        print(f"\n{exercise}: ✓ No issues found")

print("\n" + "="*80)
print(f"Total exercises checked: {len(target_exercises)}")
print(f"Exercises with issues: {len(issues_found)}")
print(f"Exercises without issues: {len(target_exercises) - len(issues_found)}")
print("="*80)