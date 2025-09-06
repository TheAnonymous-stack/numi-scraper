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
                
            for i, question in enumerate(data):
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
                    # Store by both question_number and index
                    json_tags[file_key][question_num] = visual_tags
                    json_tags[file_key][str(i+1)] = visual_tags  # Also store by index (1-based)
                    
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
    
    # Multiple patterns to match different naming conventions
    patterns = [
        f"Gr6_{week}_E{exercise} *.html",
        f"Gr6_{week}_E{exercise}_*.html"
    ]
    
    html_dir = Path('HTML')
    if not html_dir.exists():
        return []
    
    html_files = []
    for pattern in patterns:
        html_files.extend(html_dir.glob(pattern))
    
    return html_files

def extract_question_info_from_html(html_filename):
    """Extract question information from HTML filename"""
    filename = html_filename.stem
    
    # Try different patterns
    # Pattern 1: "Gr6_W_EX Q_V" or "Gr6_W_EX Q"
    match = re.match(r'Gr6_\d+_E\d+\s+(.+)', filename)
    if match:
        q_info = match.group(1)
        # Could be "1_1_1" or "1_1" or just "1"
        parts = q_info.split('_')
        
        # Return various possible matches
        results = []
        if len(parts) >= 2:
            results.append(f"{parts[0]}_{parts[1]}")  # e.g., "1_1"
        if len(parts) >= 1:
            results.append(parts[0])  # e.g., "1"
        results.append(q_info)  # Full string
        
        return results
    
    return []

def fix_html_file(html_file, tags):
    """Fix the label attributes in an HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find all label attributes
        # Pattern to match label="anything"
        label_pattern = r'label="[^"]*"'
        
        # Find all labels
        labels_found = re.findall(label_pattern, content)
        
        if labels_found and tags:
            # Replace each label with the corresponding tag
            if len(tags) == 1:
                # Single tag, replace all labels with it
                content = re.sub(label_pattern, f'label="{tags[0]}"', content)
            else:
                # Multiple tags, distribute them
                for i, tag in enumerate(tags):
                    if i < len(labels_found):
                        # Replace one at a time
                        content = re.sub(label_pattern, f'label="{tag}"', content, count=1)
        
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
    print("Starting comprehensive HTML tag fix...")
    print("=" * 60)
    
    # Get all visual tags from JSON files
    print("\n1. Extracting visual tags from JSON files...")
    json_tags = get_json_visual_tags()
    print(f"   Found visual tags in {len(json_tags)} JSON files")
    
    # Statistics
    total_files = 0
    fixed_files = 0
    already_correct = 0
    no_match = 0
    
    print("\n2. Fixing HTML files...")
    print("-" * 40)
    
    for json_filename, questions in json_tags.items():
        html_files = get_html_files_for_json(json_filename)
        
        if not html_files:
            continue
        
        print(f"\n   Processing {json_filename}:")
        print(f"   Found {len(html_files)} HTML files")
        
        for html_file in html_files:
            total_files += 1
            
            # Extract possible question identifiers from HTML filename
            possible_matches = extract_question_info_from_html(html_file)
            
            # Try to find matching tags
            tags_found = None
            for match in possible_matches:
                if match in questions:
                    tags_found = questions[match]
                    break
            
            if tags_found:
                # Check if file needs fixing
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if already has correct tags
                has_correct_tag = any(f'label="{tag}"' in content for tag in tags_found)
                
                if has_correct_tag:
                    already_correct += 1
                    print(f"   [OK] Already correct: {html_file.name}")
                else:
                    if fix_html_file(html_file, tags_found):
                        fixed_files += 1
                        print(f"   [FIXED] {html_file.name} -> {tags_found[0][:50]}...")
                    else:
                        print(f"   - No changes needed: {html_file.name}")
            else:
                no_match += 1
                # print(f"   ? No match found: {html_file.name}")
    
    print("\n" + "=" * 60)
    print("FIX COMPLETE!")
    print(f"Total HTML files processed: {total_files}")
    print(f"Files fixed: {fixed_files}")
    print(f"Files already correct: {already_correct}")
    print(f"Files with no match: {no_match}")
    if total_files > 0:
        success_rate = ((fixed_files + already_correct) / total_files) * 100
        print(f"Success rate: {success_rate:.1f}%")

if __name__ == "__main__":
    main()