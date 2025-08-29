import csv
from getYoutubeURLS import extract_youtube_from_khan
import re
input_file = "rawURLS.csv"
output_file = "links.csv"
videos = {}
pattern = r"/embed/([^/?]+)"
with open(input_file, newline="") as csv_in, open("tag.csv", "r") as tag_file, open(output_file, "w", newline="") as csv_out:
    reader = csv.reader(csv_in)
    writer = csv.writer(csv_out)
    tag_reader = csv.reader(tag_file)
    for row, tag_row in zip(reader, tag_reader):
        if not row or all(cell.strip() == "" for cell in row):
            # replace empty row/newline with ["empty"]
            writer.writerow(["empty"])
        else:
            tag = tag_row[0]
            print(f"processing tag {tag}")
            link = row[0]
            week_number = tag.split("_")[1]
            if week_number not in videos:
                videos[week_number] = []
            if link not in videos[week_number]:
                videos[week_number].append(link)
                if "khanacademy" in link:
                    print(f"{tag} has khanacademy link")
                    processed_link = extract_youtube_from_khan(link)
                    match = re.search(pattern, processed_link)
                    if match:
                        video_id = match.group(1)
                        new_link = f"https://youtu.be/{video_id}"
                        writer.writerow([new_link])
                    else:
                        print("Error when processing khanacademy link")
                        writer.writerow(["empty"])
                    

                elif "youtube.com" in link:
                    print(f"{tag} has youtube.com link")
                    video_id = link.split("=")[-1]
                    new_link = f"https://youtu.be/{video_id}"
                    writer.writerow([new_link])
                else:
                    writer.writerow(row)

            else: # if link is already used in the same week
                writer.writerow(["empty"])
