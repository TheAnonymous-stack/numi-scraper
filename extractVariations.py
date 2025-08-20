import csv
import json

tags = ["Gr4_36_E2"]
with open("FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_27_E1_1_1-Gr4_39_E4_4_1).json", "r") as f:
    data = json.load(f)
# with open("miniMapping.csv", newline="") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         tag, skill = row 
#         if skill != "empty":
#             tags.append(tag)
    for tag in tags:
        variations = []
        counter = 0
        i = 0
        while counter < 51:
            question = data[i]
            if question["tag"] == tag:
                variations.append(question)
                counter += 1
            i += 1
        with open(f"{tag} variations.json", "w") as f:
            json.dump(variations, f, indent=2, ensure_ascii=False)