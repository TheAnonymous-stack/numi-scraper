import json
import csv
import os 

# tags = []
# with open("miniMapping.csv", newline="") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         tag, skill = row
#         if skill != "empty":
#             tags.append(tag)
# data = []
# for tag in tags:
#     with open(f"{tag}_variations.json", "r") as f:
#         data += json.load(f)
data = []
files = [
    "FORMAT_UPDATE - gr7ScrapedQuestions(K.7-W.8).json",
    "FORMAT_UPDATE - gr7ScrapedQuestions(W.8-O.10).json"
]
for file in files:
    with open(file, "r") as f:
        data += json.load(f)

for question in data:

    tag = question["tag"]
    week_number = tag.split("_")[1]
    
    # check image_tag
    if "image_tag" in question:
        if not os.path.exists(f"Grade7_Master_Images/{week_number}/{question['image_tag']}.png"):
            print(f"{tag} is missing image for image_tag")
            print(f"variation: {question['question_number']}")
    
    if "image_choice_tags" in question:
        for choice in question["image_choice_tags"]:
            if not os.path.exists(f"Grade7_Master_Images/{week_number}/{choice}.png"):
                print(f"{tag} is missing image choice tag {choice}")
    
    if "shape_image_tags" in question:
        for choice in question['shape_image_tags']:
            img_tag = choice["tag"]
            if not os.path.exists(f"Grade7_Master_Images/{week_number}/{img_tag}.png"):
                print(f"{tag} is missing shape image tag for {img_tag}")
                
    if len(question["solution_image_tag"]) > 0:
        for step in question["solution_image_tag"]:
            img_tag = step[1]
            if not os.path.exists(f"Grade7_Master_Images/{week_number}/{img_tag}.png"):
                print(f"{tag} is missing solution_image_tag for {img_tag}")
    