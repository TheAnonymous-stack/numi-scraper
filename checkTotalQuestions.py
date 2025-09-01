import csv
import json

counter = {}
with open("miniMapping.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tag, skill = row
        if skill != "empty":
            counter[tag] = 0
# files = ["FORMAT_UPDATE4 - gr8MasterQuestions(T.3-L.10).json"]
# data = []
# for file in files:
#     with open(file, "r") as f:
#         data += json.load(f)
# for question in data:
#     week_number = int(question["tag"].split("_")[1])
#     if week_number <= 41 or week_number >= 47:
#         counter[question["tag"]] += 1

for tag in counter:
    with open(f"{tag}_variations.json", "r") as f:
        variations = json.load(f)
    counter[tag] += len(variations)

for tag in counter:
    if counter[tag] != 51:
        print(f"{tag} has {counter[tag]} variations")