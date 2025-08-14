
import json
import csv

tags = []

with open("miniMapping.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tag, skill = row
        if skill != "empty":
            tags.append(tag)

with open('/Users/hypebeast/numi-scraper/FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_14_E1_1_1-Gr4_26_E4_4_1).json', 'r') as f:
    data = json.load(f)


i = 0

for tag in tags:
    # Load generated variations
    with open(f'/Users/hypebeast/numi-scraper/{tag}_variations.json', 'r') as f:
        variations = json.load(f)

    # Combine them
    while i < len(data):
        question = data[i]
        if question["tag"] == tag:
            if i == len(data) - 1:
                data = data + variations
                print(f"✓ Combined variations of {tag}")
                i += (len(variations) + 1)
                break
            else:
                if data[i + 1]["tag"] != tag:
                    first_half = data[:i+1]
                    second_half = data[i+1:]
                    data = first_half + variations + second_half
                    print(f"✓ Combined variations of {tag}")
                    i += (len(variations) + 1)
                    break
        i += 1

                    
    
# Save the combined file
with open('/Users/hypebeast/numi-scraper/FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_14_E1_1_1-Gr4_26_E4_4_1).json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
        
        

