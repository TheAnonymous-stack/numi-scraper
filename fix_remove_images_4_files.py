import json

def remove_images_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        # Remove image-related fields
        if 'image_tag' in quiz:
            del quiz['image_tag']
        if 'backend_description' in quiz:
            del quiz['backend_description']
        if 'solution_image_tag' in quiz:
            del quiz['solution_image_tag']
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Removed images from {filename}")

# Process all 4 files
files = [
    'Gr6_47_E3_variations.json',
    'Gr6_48_E2_variations.json',
    'Gr6_48_E3_variations.json',
    'Gr6_48_E4_variations.json'
]

for file in files:
    remove_images_from_file(file)

print("\nAll 4 files have been processed!")