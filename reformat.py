import json
import csv
import os
import shutil

map = {}
with open("mapping.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        tag, skill = row
        map[skill] = tag


files = [
    "FORMAT_UPDATE3-gr4ScrapedQuestions(Gr4_1_E1_1_1-Gr4_13_E4_4_1).json",
    "FORMAT_UPDATE3-gr4ScrapedQuestions(Gr4_14_E1_1_1-Gr4_26_E4_4_1).json",
    "FORMAT_UPDATE3-gr4ScrapedQuestions(Gr4_27_E1_1_1-Gr4_39_E4_4_1).json",
    "FORMAT_UPDATE3-gr4ScrapedQuestions(Gr4_40_E1_1_1-Gr4_52_E4_4_1).json"
]

new_files = [
    "FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_1_E1_1_1-Gr4_13_E4_4_1).json",
    "FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_14_E1_1_1-Gr4_26_E4_4_1).json",
    "FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_27_E1_1_1-Gr4_39_E4_4_1).json",
    "FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_40_E1_1_1-Gr4_52_E4_4_1).json"
]
for i, file in enumerate(files):
    with open(file, "r") as f:
        data = json.load(f)
    for question in data:
        skill = question["skills"].replace("-", " ")
        old_tag = question["tag"]
        if skill not in map:
            continue
        new_tag = map[skill]
        parts = new_tag.split("_")
        variation_number = question["question_number"].split("_")[-1]
        new_week_number = parts[1]
        new_exercise_number = parts[2].split("E")[-1]
        old_week_number = old_tag.split("_")[1]
        
        # update the name of the image files
        if "image_tag" in question:
            old_image_tag = question["image_tag"]
            new_image_tag = f"Gr4_{new_week_number}_{new_exercise_number}_{variation_number}"
            os.makedirs(f"New_Grade4_Master_Images/{new_week_number}", exist_ok=True)
            shutil.copy2(f"Grade4_Master_Images/{old_week_number}/{old_image_tag}.png", f"New_Grade4_Master_Images/{new_week_number}/{new_image_tag}.png")
            question["image_tag"] = new_image_tag
        
        if "image_choice_tags" in question:
            old_image_choice_tags = question["image_choice_tags"]
            new_image_choice_tags = []
            for old_image_tag in old_image_choice_tags:
                choice = old_image_tag[-1]
                new_image_tag = f"Gr4_{new_week_number}_{new_exercise_number}_{variation_number}_{choice}"
                os.makedirs(f"New_Grade4_Master_Images/{new_week_number}", exist_ok=True)
                shutil.copy2(f"Grade4_Master_Images/{old_week_number}/{old_image_tag}.png", f"New_Grade4_Master_Images/{new_week_number}/{new_image_tag}.png")
                new_image_choice_tags.append(new_image_tag)
            question["image_choice_tags"] = new_image_choice_tags
        
        if "shape_image_tags" in question:
            old_shape_image_tags = question["shape_image_tags"]
            new_shape_image_tags = []
            for obj in old_shape_image_tags:
                old_image_tag = obj["tag"]
                choice = old_image_tag[-1]
                new_image_tag = f"Gr4_{new_week_number}_{new_exercise_number}_{variation_number}_{choice}"
                os.makedirs(f"New_Grade4_Master_Images/{new_week_number}", exist_ok=True)
                shutil.copy2(f"Grade4_Master_Images/{old_week_number}/{old_image_tag}.png", f"New_Grade4_Master_Images/{new_week_number}/{new_image_tag}.png")
                new_shape_image_tags.append({
                    "tag": new_image_tag,
                    "backend_description": obj["backend_description"],
                    "id": obj["id"]
                })
            question["shape_image_tags"] = new_shape_image_tags
        
        if len(question["solution_image_tag"]) > 0:
            old_solution_image_tag = question["solution_image_tag"]
            new_solution_image_tag = []
            for obj in old_solution_image_tag:
                old_image_tag = obj[1]
                step_number = old_image_tag.split("_")[-1]
                new_image_tag = f"Gr4_{new_week_number}_{new_exercise_number}_{variation_number}_step_{step_number}"
                os.makedirs(f"New_Grade4_Master_Images/{new_week_number}", exist_ok=True)
                shutil.copy2(f"Grade4_Master_Images/{old_week_number}/{old_image_tag}.png", f"New_Grade4_Master_Images/{new_week_number}/{new_image_tag}.png")
                new_solution_image_tag.append([
                    obj[0],
                    new_image_tag,
                    obj[2]
                ])
            question["solution_image_tag"] = new_solution_image_tag
        
        # update tag, question_number
        question["tag"] = new_tag
        question["question_number"] = f"{new_exercise_number}_{variation_number}"

    with open(new_files[i], "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



