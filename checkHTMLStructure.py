import os
import re
import json

directory = "./HTML"
for file in os.listdir(directory):
    # Check naming convention first
    matchUnderscore = re.match(r"Gr6_(\d+)_E(\d+)_(\d+)_(\d+)\.html", file)
    matchSpace = re.match(r"Gr6_(\d+)_E(\d+)\s(\d+)_(\d+)\.html", file)
    if matchUnderscore is None and matchSpace is None:
        print(f"{file} does not follow naming convention")
        continue
    match = matchUnderscore if matchUnderscore else matchSpace

    if match.group(2) != match.group(3):
        print(f"{file} does not follow naming convention")
        continue

    week = match.group(1)
    exercise = match.group(2)
    variation = int(match.group(4))
    
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
        if len(question["solution_image_tag"]) > 0:
            for step in question['solution_image_tag']:
                img = step[1]
                imagesToCreate[img] = 0
        if "shape_image_tags" in question:
            for shape in question['shape_image_tags']:
                img = shape['tag']
                imagesToCreate[img] = 0
        # Read the HTML file and search for divs with class="item" and expected labels
        html_file_path = os.path.join(directory, file)
        with open(html_file_path, "r") as html_file:
            html_content = html_file.read()
            
        # Check for each expected image label
        missing_labels = []
        found_labels = []
        
        for label in imagesToCreate:
            # Search for div with class="item" and the specific label
            pattern = rf'<div[^>]*class="item"[^>]*label="{re.escape(label)}"'
            if re.search(pattern, html_content):
                imagesToCreate[label] = 1
        
        # Report results
        for label in imagesToCreate:
            if imagesToCreate[label] == 0:
                print(f"{file} is missing {label}")
        
