import json
import os
from pathlib import Path

# Analyze the structure of Grade 6 JSON files
json_files = sorted(Path('.').glob('Gr6_*_variations.json'))

print(f"Found {len(json_files)} Grade 6 JSON files\n")

# Sample a few files to understand the structure
for i, json_file in enumerate(json_files[:5]):
    print(f"File: {json_file.name}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check what keys are present
        keys = list(data.keys())
        print(f"  Keys: {keys}")
        
        # Check if it has questions or quizzes
        if 'questions' in data:
            print(f"  Has 'questions' field with {len(data['questions'])} items")
        if 'quizzes' in data:
            print(f"  Has 'quizzes' field with {len(data['quizzes'])} items")
            
        # Check for image fields in first item
        items = data.get('questions', data.get('quizzes', []))
        if items:
            first_item = items[0]
            image_fields = []
            if 'image_tag' in first_item:
                image_fields.append('image_tag')
            if 'image_choice_tags' in first_item:
                image_fields.append('image_choice_tags')
            if 'shape_image_tags' in first_item:
                image_fields.append('shape_image_tags')
            if 'solution_image_tag' in first_item:
                image_fields.append('solution_image_tag')
            
            if image_fields:
                print(f"  Image fields in first item: {image_fields}")
            else:
                print(f"  No image fields in first item")
                
    except Exception as e:
        print(f"  Error: {e}")
    print()

# Now count how many files have image fields
files_with_images = 0
for json_file in json_files:
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = data.get('questions', data.get('quizzes', []))
        has_images = False
        for item in items:
            if ('image_tag' in item or 'image_choice_tags' in item or 
                'shape_image_tags' in item or 'solution_image_tag' in item):
                has_images = True
                break
        
        if has_images:
            files_with_images += 1
            
    except:
        pass

print(f"\nSummary:")
print(f"Total Grade 6 JSON files: {len(json_files)}")
print(f"Files with image fields: {files_with_images}")