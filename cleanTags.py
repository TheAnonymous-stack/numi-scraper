import json
import csv

grade = "7"
files = []
with open("miniMapping.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tag, skill = row
        files.append(f"{tag}_variations.json")
# for global_tag in tags:

#     with open(f"{global_tag}_variations.json") as f:
#         data = json.load(f)
# files = [
#     "FORMAT_UPDATE - gr7ScrapedQuestions(K.7-W.8).json",
#     "FORMAT_UPDATE - gr7ScrapedQuestions(W.8-O.10).json"
# ]

for file in files:
    with open(file, "r") as f:
        data = json.load(f)
    for question in data:
        parts = question["tag"].split("_")
        variation_number = question["question_number"].split("_")[-1]
        week_number = parts[1]
        exercise_number = parts[2].split("E")[-1]
        question["question_number"] = f"{exercise_number}_{variation_number}"
        if "image_tag" in question:
            question["image_tag"] = f"Gr{grade}_{week_number}_{exercise_number}_{variation_number}"
        if "image_choice_tags" in question:
            old_tags = question["image_choice_tags"]
            new_tags = []
            for tag in old_tags:
                option = tag.split("_")[-1]
                new_tags.append(f"Gr{grade}_{week_number}_{exercise_number}_{variation_number}_{option}")
            question["image_choice_tags"] = new_tags
        if "shape_image_tags" in question:
            old_lst = question["shape_image_tags"]
            new_lst = []
            for obj in old_lst:
                option = obj["id"]
                new_lst.append({
                    "tag": f"Gr{grade}_{week_number}_{exercise_number}_{variation_number}_{option}",
                    "backend_description": obj["backend_description"],
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
                    f"Gr{grade}_{week_number}_{exercise_number}_{variation_number}_step_{step_number}",
                    step[2]
                ])
            question["solution_image_tag"] = new_lst

    # with open(f"{global_tag}_variations.json", "w") as f:
    #     json.dump(data, f, indent=2, ensure_ascii=False)
    with open(file, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
