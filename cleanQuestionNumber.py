import json
import csv

tags = []
with open("miniMapping.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tag, skill = row
        tags.append(tag)

for tag in tags:
    with open(f"{tag}_variations.json", "r") as f:
        data = json.load(f)
    variation_number = 51
    exercise_number = tag.split("E")[-1]
    for i in range(51, 51 - len(data), -1):
        question = data[i-52]
        question["question_number"] = f"{exercise_number}_{variation_number}"
        variation_number -= 1
    with open(f"{tag}_variations.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)