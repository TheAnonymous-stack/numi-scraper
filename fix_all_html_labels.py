import json
import os
import re
from pathlib import Path
from collections import defaultdict

def get_json_visual_tags():
    """Extract all visual tags from JSON files"""
    json_tags = defaultdict(dict)
    
    # Get all Grade 6 JSON variation files
    json_files = list(Path('.').glob('Gr6_*_variations.json'))
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for question in data:
                question_num = question.get('question_number', '')
                
                # Get all visual tags
                visual_tags = []
                
                # Solution image tags
                if 'solution_image_tag' in question:
                    for tag_info in question['solution_image_tag']:
                        if len(tag_info) >= 2:
                            visual_tags.append(tag_info[1])
                
                # Main image tag
                if 'image_tag' in question and question['image_tag']:
                    visual_tags.append(question['image_tag'])
                
                # Shape image tags
                if 'shape_image_tags' in question:
                    for tag in question['shape_image_tags']:
                        if tag:
                            visual_tags.append(tag)
                
                # Image choice tags
                if 'image_choice_tags' in question:
                    for tag in question['image_choice_tags']:
                        if tag:
                            visual_tags.append(tag)
                
                if visual_tags:
                    # Store the tags for this question
                    file_key = str(json_file.stem)  # e.g., "Gr6_1_E1_variations"
                    json_tags[file_key][question_num] = visual_tags
                    
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    
    return json_tags

def get_html_files_for_json(json_filename):
    """Get all HTML files that correspond to a JSON file"""
    # Extract week and exercise from JSON filename
    match = re.match(r'Gr6_(\d+)_E(\d+)_variations', json_filename)
    if not match:
        return []
    
    week, exercise = match.groups()
    pattern = f"Gr6_{week}_E{exercise} *.html"
    
    html_dir = Path('HTML')
    if not html_dir.exists():
        return []
    
    return list(html_dir.glob(pattern))

def extract_question_num_from_html(html_filename):
    """Extract the question number from HTML filename"""
    # Pattern: Gr6_W_EX Q_V.html where Q is question number, V is variation
    filename = html_filename.stem
    parts = filename.split(' ')
    if len(parts) >= 2:
        # The second part should be the question_variation (e.g., "1_1_1")
        q_v = parts[1]
        # We need to match this to the question_number format in JSON
        # HTML: "1_1_1" might correspond to JSON question_number: "1_1"
        q_parts = q_v.split('_')
        if len(q_parts) >= 2:
            return f"{q_parts[0]}_{q_parts[1]}"
    return None

def fix_html_file(html_file, tags):
    """Fix the label attributes in an HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find all div elements with label="visual_main"
        pattern = r'(<div[^>]*\slabel=")[^"]*(")'
        
        # Count how many visual_main labels we have
        visual_main_count = len(re.findall(r'label="visual_main"', content))
        
        if visual_main_count > 0 and tags:
            # If we have multiple tags for multiple visuals, distribute them
            if visual_main_count == 1 and len(tags) >= 1:
                # Single visual, use the first tag
                content = re.sub(r'label="visual_main"', f'label="{tags[0]}"', content, count=1)
            elif visual_main_count > 1 and len(tags) >= visual_main_count:
                # Multiple visuals, replace each with corresponding tag
                for i in range(min(visual_main_count, len(tags))):
                    content = re.sub(r'label="visual_main"', f'label="{tags[i]}"', content, count=1)
            else:
                # Use the first tag for all if we don't have enough tags
                content = re.sub(r'label="visual_main"', f'label="{tags[0]}"', content)
        
        # Only write if we made changes
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error fixing {html_file}: {e}")
        return False

def main():
    print("Starting HTML label fix process...")
    print("=" * 60)
    
    # Get all visual tags from JSON files
    print("\n1. Extracting visual tags from JSON files...")
    json_tags = get_json_visual_tags()
    print(f"   Found visual tags in {len(json_tags)} JSON files")
    
    # Statistics
    total_files = 0
    fixed_files = 0
    error_files = 0
    
    print("\n2. Fixing HTML files...")
    print("-" * 40)
    
    for json_filename, questions in json_tags.items():
        html_files = get_html_files_for_json(json_filename)
        
        if not html_files:
            print(f"   No HTML files found for {json_filename}")
            continue
        
        print(f"\n   Processing {json_filename}:")
        print(f"   Found {len(html_files)} HTML files")
        
        for html_file in html_files:
            total_files += 1
            
            # Extract question number from HTML filename
            question_num = extract_question_num_from_html(html_file)
            
            if question_num and question_num in questions:
                tags = questions[question_num]
                if fix_html_file(html_file, tags):
                    fixed_files += 1
                    print(f"   [FIXED] {html_file.name} with tags: {tags[:2]}...")
                else:
                    print(f"   - No changes needed: {html_file.name}")
            else:
                # Try alternative matching (for variations)
                # HTML file might be "1_1_1" for JSON question "1_1"
                found_match = False
                for q_num, tags in questions.items():
                    if html_file.stem.endswith(f" {q_num}_"):
                        if fix_html_file(html_file, tags):
                            fixed_files += 1
                            print(f"   [FIXED] {html_file.name} with tags: {tags[:2]}...")
                            found_match = True
                            break
                
                if not found_match:
                    # As a fallback, if the HTML file contains any question from this exercise
                    # Try to match by the first part of the filename
                    html_name = html_file.stem
                    for q_num, tags in questions.items():
                        # Check if this HTML file might be for this question
                        if q_num.replace('_', '_') in html_name:
                            if fix_html_file(html_file, tags):
                                fixed_files += 1
                                print(f"   [FIXED] {html_file.name} with tags: {tags[:2]}...")
                                found_match = True
                                break
                    
                    if not found_match:
                        print(f"   ? Could not match: {html_file.name} to any question")
    
    print("\n" + "=" * 60)
    print("FIX COMPLETE!")
    print(f"Total HTML files processed: {total_files}")
    print(f"Files fixed: {fixed_files}")
    print(f"Files with errors: {error_files}")
    print(f"Success rate: {fixed_files/total_files*100:.1f}%" if total_files > 0 else "N/A")

if __name__ == "__main__":
    main()