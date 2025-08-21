import csv
import json

counter = {}
mapping = {}
with open("mapping.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tag, skill = row
        if skill != "empty":
            skill = " ".join(skill.split(" ")[:-1]).lower().replace(":", "").replace("-", " ").replace(",", "").replace("?", "").replace(".", " ")
            counter[(tag, skill)] = 0
            mapping[skill] = tag
files = [
    "FORMAT_UPDATE4-gr5MasterQuestions(A.1-M.3).json",
    "FORMAT_UPDATE4-gr5MasterQuestions(FF.4-LL.5).json",
    "FORMAT_UPDATE4-gr5MasterQuestions(II.1-X.8).json",
    "FORMAT_UPDATE4-gr5MasterQuestions(Q.1-X.9).json",
    "FORMAT_UPDATE4-gr5MasterQuestions(Z.3-GG.11).json"
]

data = []

for file in files:
    with open(file, "r") as f:
        data += json.load(f)

for question in data:
    skill = question["skills"].replace("-", " ")
    if (question["tag"], skill) not in counter:
        print(f"{(question['tag'], skill)} not in counter")
    else:
        counter[(question["tag"], skill)] = 1
    if mapping[skill] != question["tag"]:
        print(f"{skill} should have tag {mapping[skill]} but current have {question['tag']}")

for pair in counter:
    if counter[pair] == 0:
        print(f"Missing {pair[0]}")

