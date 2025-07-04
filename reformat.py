import json

# with open("gr5Draft.json", "r") as f:
#     new_data = json.load(f)

# with open("gr5ScrapedQuestions.json", "r") as f:
#     old_data = json.load(f)
# data = old_data + new_data

# with open("gr5ScrapedQuestions.json", "w") as f:
#     json.dump(data, f, indent=2)

with open("gr5ScrapedQuestions.json", "r") as f:
    data = json.load(f)
    for question in data:
        res = []
        list = question["solution"].split(".")
        total = len(list)
        for i, sentence in enumerate(list):
            sentence_list = []
            sentence_list.append(f"{i + 1}/{total}")
            sentence_list.append(sentence)
            res.append(sentence_list)
        question["solution"] = res

with open("gr5ScrapedQuestions.json", "w") as f:
    json.dump(data, f, indent=2)


