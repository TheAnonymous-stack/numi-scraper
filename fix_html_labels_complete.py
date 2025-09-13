import json
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def get_all_image_tags_from_json(json_file, question_number):
    """Extract ALL image tags for a specific question from JSON file"""
    tags = []
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data.get('quizzes', [])
        
        # Find the matching question
        for question in questions:
            if question.get('question_number') == question_number:
                # Get main image tag (if exists)
                image_tag = question.get('image_tag')
                if image_tag:
                    tags.append(image_tag)
                
                # Get image choice tags (if exists)
                choice_tags = question.get('image_choice_tags', [])
                if choice_tags:
                    for tag in choice_tags:
                        if tag:
                            tags.append(tag)
                
                # Get solution image tags (if exists)
                solution_tags = question.get('solution_image_tag', [])
                if solution_tags:
                    # solution_image_tag is a list of [step, tag, description] tuples
                    for tag_info in solution_tags:
                        if len(tag_info) >= 2:
                            tag = tag_info[1]  # The tag is the second element
                            if tag and tag not in tags:  # Avoid duplicates
                                tags.append(tag)
                
                break
    
    except Exception as e:
        print(f"Error reading {json_file}: {e}")
    
    return tags

def update_html_file_with_correct_labels(html_file, json_file, question_number):
    """Update HTML file with correct label attributes based on JSON"""
    
    # Get all tags from JSON
    tags = get_all_image_tags_from_json(json_file, question_number)
    
    if not tags:
        # If no tags found, generate default tags based on the pattern
        # This handles cases where image tags might not be explicitly in JSON
        match = re.match(r'Gr6_(\d+)_E(\d+)_(.+)\.html', html_file.name)
        if match:
            week = match.group(1)
            exercise = match.group(2)
            q_num = match.group(3)
            
            # Try common patterns
            default_tag = f"Gr6_{week}_{exercise}_{q_num}"
            tags = [default_tag]
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all divs with class="visual-element" or class containing "item"
        visual_elements = soup.find_all('div', class_=lambda x: x and ('visual-element' in x or 'item' in x))
        
        if not visual_elements:
            # No visual elements to update
            return False
        
        # Assign labels to visual elements
        tag_index = 0
        for element in visual_elements:
            # Check if element already has a label that looks correct
            current_label = element.get('label', '')
            
            # If current label looks like an image tag, keep it
            if current_label and ('Gr6_' in current_label or 'Gr5_' in current_label):
                # Check if it's a step label
                if '_step_' in current_label:
                    # This is likely correct, keep it
                    continue
                # Check if it's in our tags list
                if current_label in tags:
                    continue
            
            # Assign new label from our tags
            if tag_index < len(tags):
                element['label'] = tags[tag_index]
                tag_index += 1
            elif tags:
                # If we run out of tags, use the last one
                element['label'] = tags[-1]
            
            # Ensure class="item" is present
            classes = element.get('class', [])
            if 'item' not in classes:
                classes.append('item')
            element['class'] = classes
        
        # Write back the updated HTML
        updated_html = str(soup.prettify())
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        return True
    
    except Exception as e:
        print(f"Error updating {html_file}: {e}")
        return False

def process_all_html_files():
    """Process all HTML files and fix labels completely"""
    
    base_path = Path(r'C:\Users\kapil\numi-scraper')
    html_path = base_path / 'HTML'
    
    # Get all HTML files
    html_files = list(html_path.glob('Gr6_*.html'))
    
    total_files = len(html_files)
    processed = 0
    updated = 0
    
    print(f"Found {total_files} HTML files to process")
    
    for html_file in html_files:
        # Parse filename to get week, exercise, and question number
        # Format: Gr6_{week}_E{exercise}_{question_number}.html
        match = re.match(r'Gr6_(\d+)_E(\d+)_(.+)\.html', html_file.name)
        
        if not match:
            continue
        
        week = match.group(1)
        exercise = match.group(2)
        question_num = match.group(3)
        
        # Find corresponding JSON file
        json_file = base_path / f'Gr6_{week}_E{exercise}_variations.json'
        
        if not json_file.exists():
            # Try without E prefix (some files might be named differently)
            json_file = base_path / f'Gr6_{week}_{exercise}_variations.json'
            
        if not json_file.exists():
            print(f"JSON file not found for {html_file.name}")
            continue
        
        # Update HTML with correct labels
        if update_html_file_with_correct_labels(html_file, json_file, question_num):
            updated += 1
        
        processed += 1
        
        if processed % 500 == 0:
            print(f"Processed {processed}/{total_files} files, updated {updated} files...")
    
    print(f"\nCompleted! Processed {processed} files, updated {updated} files with correct labels")

if __name__ == "__main__":
    process_all_html_files()