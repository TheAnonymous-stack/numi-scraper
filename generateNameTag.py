import json
import csv

tags = []
data = {
    "tags": []
}
with open("tag.csv", newline="") as tag_file, open("skill.csv", newline="") as skill_file, open("gr6Name-Tag.json", "w") as output_file:
    tag_reader = csv.reader(tag_file)
    skill_reader = csv.reader(skill_file)
    writer = csv.writer(output_file)
    for tag_row, skill_row in zip(tag_reader, skill_reader):
        if len(skill_row) > 0 and skill_row[0] != "":
            tag, skill = tag_row[0], skill_row
            skill = " ".join(",".join(skill).split(" ")[:-1])
            data["tags"].append({
                "name": skill,
                "tag": tag
            })
    json.dump(data, output_file, indent=2)