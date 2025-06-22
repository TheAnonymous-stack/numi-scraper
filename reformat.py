import json

with open("gr5Draft.json", "r") as f:
    new_data = json.load(f)

with open("gr5ScrapedQuestions.json", "r") as f:
    old_data = json.load(f)
data = old_data + new_data

with open("gr5ScrapedQuestions.json", "w") as f:
    json.dump(data, f, indent=2)

