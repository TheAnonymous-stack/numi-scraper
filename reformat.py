import json

with open("FORMAT_UPDATE2-gr4ScrapedQuestions(Gr4_40_E1_1_1-Gr4_52_E4_4_1).json", "r") as f:
    data = json.load(f)

for question in data:
    if "image_tag" in question:
        tag = question["image_tag"]["tag"]
        backend_description = question["image_tag"]["backend_description"]
        question["image_tag"] = tag
        question["backend_description"] = backend_description

    if "image_choice_tags" in question:
        filenames = []
        descriptions = []
        for file in question["image_choice_tags"]:
            filenames.append(file["tag"])
            descriptions.append(file["backend_description"])
        question["image_choice_tags"] = filenames
        question["image_choice_tags_backend_description"] = descriptions

    if "shape_image_tags" in question:
        for file in question["shape_image_tags"]:
            id = file["tag"].split("_")[-1]
            file["id"] = id
    
    if question["question_type"] == "Fill in the blank":
        if question["question_text"].count("_") > 1 and len(question["correct_answers"]) > 1:
            question["question_type"] = "Multiple fill in the blank"

    
    

with open("FORMAT_UPDATE3-gr4ScrapedQuestions(Gr4_40_E1_1_1-Gr4_52_E4_4_1).json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)


