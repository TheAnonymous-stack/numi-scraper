import csv
import json

counter = {}
with open("mapping.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tag, skill = row
        if skill != "empty":
            counter[(tag, skill)] = 0
files = [
    "FORMAT_UPDATE4 - gr8MasterQuestions(C.8-CC.9).json",
    "FORMAT_UPDATE4 - gr8MasterQuestions(H.1-D.24).json",
    "FORMAT_UPDATE4 - gr8MasterQuestions(T.3-L.10).json"
]

data = []

for file in files:
    with open(file, "r") as f:
        data += json.load(f)

for question in data:
    skill = question["skills"].replace("-", " ")
    counter[(question["tag"], skill)] = 1

for pair in counter:
    if counter[pair] == 0:
        print(f"Missing {pair[0]}")
