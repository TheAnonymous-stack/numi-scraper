
import json

def append_variations():
    """Append generated variations to existing variations.json file."""
    with open('/Users/hypebeast/numi-scraper/FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_1_E1_1_1-Gr4_13_E4_4_1).json', 'r') as f:
        data = json.load(f)
    tags = ["Gr4_8_E3"]

    i = 0
    
    for tag in tags:
        # Load generated variations
        with open(f'/Users/hypebeast/numi-scraper/{tag} variations.json', 'r') as f:
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
    with open('/Users/hypebeast/numi-scraper/FORMAT_UPDATE4-gr4ScrapedQuestions(Gr4_1_E1_1_1-Gr4_13_E4_4_1).json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
        

if __name__ == "__main__":
    append_variations()