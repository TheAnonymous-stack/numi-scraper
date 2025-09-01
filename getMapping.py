import csv

with open("tag.csv", newline="") as tag_file, open("skill.csv", newline="") as skill_file, open("mapping.csv", "w", newline="") as output_file:
    tag_reader = csv.reader(tag_file)
    skill_reader = csv.reader(skill_file)
    writer = csv.writer(output_file)
    for tag_row, skill_row in zip(tag_reader, skill_reader):
        if not skill_row or all(cell.strip() == "" for cell in skill_row):
            continue
        
        tag, skill = tag_row[0], "".join(skill_row)
        skill = " ".join(skill.split(" ")[:-1]).lower().replace(":", "").replace(",", "").replace("-", " ").replace("?", "")
        writer.writerow([tag, skill])
