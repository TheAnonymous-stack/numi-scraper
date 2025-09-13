import json
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def get_image_tags_from_json(json_file, question_number):
    """Extract image tags for a specific question from JSON file"""
    tags = []
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data.get('quizzes', [])
        
        # Find the matching question
        for question in questions:
            if question.get('question_number') == question_number:
                # Get main image tag
                image_tag = question.get('image_tag')
                if image_tag:
                    tags.append(image_tag)
                
                # Get solution image tags
                solution_tags = question.get('solution_image_tag', [])
                if solution_tags:
                    # solution_image_tag is a list of [step, tag, description] tuples
                    for tag_info in solution_tags:
                        if len(tag_info) >= 2:
                            tag = tag_info[1]  # The tag is the second element
                            if tag:
                                tags.append(tag)
                
                # Get image choice tags if present
                choice_tags = question.get('image_choice_tags', [])
                if choice_tags:
                    for tag in choice_tags:
                        if tag:
                            tags.append(tag)
                
                break
    
    except Exception as e:
        print(f"Error reading {json_file}: {e}")
    
    return tags

def update_html_with_labels(html_file, labels):
    """Update HTML file with proper label attributes"""
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all divs with class="visual-element"
        visual_elements = soup.find_all('div', class_='visual-element')
        
        # Update labels for each visual element
        for i, element in enumerate(visual_elements):
            if i < len(labels):
                # Remove any existing label attribute
                if element.has_attr('label'):
                    del element['label']
                
                # Add the correct label
                element['label'] = labels[i]
                # Also add class="item" for consistency
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
    """Process all HTML files and add proper labels"""
    
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
            print(f"JSON file not found for {html_file.name}")
            continue
        
        # Get image tags from JSON
        labels = get_image_tags_from_json(json_file, question_num)
        
        if labels:
            # Update HTML with labels
            if update_html_with_labels(html_file, labels):
                updated += 1
        
        processed += 1
        
        if processed % 500 == 0:
            print(f"Processed {processed}/{total_files} files, updated {updated} files...")
    
    print(f"\nCompleted! Processed {processed} files, updated {updated} files with proper labels")

if __name__ == "__main__":
    process_all_html_files()