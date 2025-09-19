import json
import glob
import os

# Get all variation files that were just generated for the test.json data
variation_files = [
    "Gr7_17_E1 variations.json",
    "Gr7_17_E2 variations.json",
    "Gr7_18_E1 variations.json",
    "Gr7_18_E2 variations.json",
    "Gr7_18_E3 variations.json",
    "Gr7_19_E1 variations.json",
    "Gr7_19_E2 variations.json",
    "Gr7_19_E3 variations.json",
    "Gr7_20_E2 variations.json",
    "Gr7_20_E3 variations.json",
    "Gr7_21_E1 variations.json",
    "Gr7_21_E2 variations.json"
]

print("=" * 60)
print("VARIATION GENERATION SUMMARY")
print("=" * 60)

# Load original templates
with open('test_fixed.json', 'r') as f:
    templates = json.load(f)

# Count templates by tag
template_counts = {}
for item in templates:
    tag = item.get('tag')
    if tag:
        template_counts[tag] = template_counts.get(tag, 0) + 1

total_variations = 0
total_questions = 0

print("\nTag-wise Summary:")
print("-" * 60)

for file in variation_files:
    if os.path.exists(file):
        with open(file, 'r') as f:
            variations = json.load(f)

        # Extract tag from filename
        tag = file.replace(" variations.json", "")
        template_count = template_counts.get(tag, 0)
        variation_count = len(variations)
        total_count = template_count + variation_count

        print(f"\n{tag}:")
        print(f"  Templates: {template_count}")
        print(f"  Variations: {variation_count}")
        print(f"  Total: {total_count}")

        total_variations += variation_count
        total_questions += total_count

        # Check if we reached 51 total
        if total_count == 51:
            print(f"  [SUCCESS] Target of 51 reached")
        else:
            print(f"  [WARNING] Expected 51, got {total_count}")

print("\n" + "=" * 60)
print("OVERALL SUMMARY:")
print("-" * 60)
print(f"Total template questions: {len(templates)}")
print(f"Total variations generated: {total_variations}")
print(f"Total questions (templates + variations): {total_questions}")
print("=" * 60)

# Sample a variation to show structure
print("\nSample variation from Gr7_17_E1:")
print("-" * 60)
if os.path.exists("Gr7_17_E1 variations.json"):
    with open("Gr7_17_E1 variations.json", 'r') as f:
        sample_variations = json.load(f)
        if sample_variations:
            sample = sample_variations[0]
            print(f"Question number: {sample.get('question_number')}")
            print(f"Skills: {sample.get('skills')}")
            print(f"Tag: {sample.get('tag')}")
            print(f"Has image tag: {'image_tag' in sample}")
            print(f"Has solution: {'solution' in sample}")
            print(f"Has correct answers: {'correct_answers' in sample}")