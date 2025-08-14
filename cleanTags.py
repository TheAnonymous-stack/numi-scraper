import json
import csv

tags = []
with open("miniMapping.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tag, skill = row
        if skill != "empty":
            tags.append(tag)
for tag in tags:

    with open(f"{tag}_variations.json") as f:
        data = json.load(f)
    for question in data:
        parts = question["tag"].split("_")
        variation_number = question["question_number"].split("_")[-1]
        week_number = parts[1]
        exercise_number = parts[2].split("E")[-1]
        if "image_tag" in question:
            question["image_tag"] = f"Gr4_{week_number}_{exercise_number}_{variation_number}"
        if "image_choice_tags" in question:
            old_tags = question["image_choice_tags"]
            new_tags = []
            for tag in old_tags:
                option = tag.split("_")[-1]
                new_tags.append(f"Gr4_{week_number}_{exercise_number}_{variation_number}_{option}")
            question["image_choice_tags"] = new_tags
        if "shape_image_tags" in question:
            old_lst = question["shape_image_tags"]
            new_lst = []
            for obj in old_lst:
                option = obj["id"]
                new_lst.append({
                    "tag": f"Gr4_{week_number}_{exercise_number}_{variation_number}_{option}",
                    "backend_description": obj[1],
                    "id": option
                })
            question["shape_image_tags"] = new_lst
        if len(question["solution_image_tag"]) > 0:
            old_lst = question["solution_image_tag"]
            new_lst = []
            for step in old_lst:
                parts = step[0].split("/")
                step_number = parts[0]
                total_steps = parts[1]
                new_lst.append([
                    f"{step_number}/{total_steps}",
                    f"Gr4_{week_number}_{exercise_number}_{variation_number}_step_{step_number}",
                    step[2]
                ])
            question["solution_image_tag"] = new_lst

    with open(f"{tag}_variations.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

