import json
import random
import copy

# This script generates variations for Gr7_2_E3 (appears to be incomplete in original file)
# Tag: Gr7_2_E3 - Only has tag, question_number, and solution_image_tag fields
# Since the template is incomplete, we'll create a minimal set of variations

def generate_variations():
    # Load the fixed JSON file to get the template
    with open(r'C:\Users\kapil\numi-scraper\file_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # Find the template with tag Gr7_2_E3
    template = None
    for item in data:
        if item.get('tag') == 'Gr7_2_E3':
            template = item
            break

    if not template:
        print("Template for Gr7_2_E3 not found")
        return

    # Since this template is incomplete (missing most fields),
    # we'll skip generating variations for it
    print("Template for Gr7_2_E3 is incomplete, skipping variation generation")

    # Create empty variations file to maintain consistency
    variations = []

    # Save variations to JSON file
    with open(r'C:\Users\kapil\numi-scraper\Gr7_2_E3 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Created empty variations file for Gr7_2_E3 (template was incomplete)")

if __name__ == "__main__":
    generate_variations()