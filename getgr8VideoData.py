import csv
from getVideoInfo import get_info
import json
tags_file = "tag.csv"
links_file = "links.csv"
data = {"videos": []}
with open(tags_file, newline="") as tagsFile, open(links_file, newline = "") as linksFile, open("gr8VideoData.json", "w") as output:
    tags_reader = csv.reader(tagsFile)
    links_reader = csv.reader(linksFile)
    for row1, row2 in zip(tags_reader, links_reader):
        tag = row1[0]
        parts = tag.split("_")
        week_number = parts[1]
        exercise_number = parts[2].split("E")[-1]
        link = row2[0]
        if link == "empty":
            continue
        info = get_info(link)
        data["videos"].append({
            "_id": f"8_{exercise_number}_{week_number}",
            "title": info['title'].split("|")[0].strip(),
            "url": link,
            "duration": info['duration'],
            "tag": tag
        })
    json.dump(data, output, indent=2)

    
