import json
import csv
map = {}
variationCounter = {}
isCorrupt = {}
tags = []
with open("miniMapping.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tag, skill = row
        if skill != "empty":
            map[tag] = skill
            variationCounter[tag] = 0
            isCorrupt[tag] = False
            tags.append(tag)




with open("FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_40_E1_1_1-Gr4_52_E4_4_1).json", "r") as f:
    data = json.load(f)
    for question in data: 
        variationCounter[question["tag"]] += 1
        if map[question["tag"]] != question["skills"].replace("-", " "):
            isCorrupt[question["tag"]] = True
    for tag in tags:
        if variationCounter[tag] < 51:
            print(f"{tag} has less than 51 variations")
        elif variationCounter[tag] > 51:
            print(f"{tag} has more than 51 variations")
        if isCorrupt[tag]:
            print(f"{tag} is corrupt")
