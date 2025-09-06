import json
import os
from pathlib import Path
import re

def get_json_files_with_visuals():
    """Get all JSON files that have visual components"""
    json_visual_files = {}
    
    json_files = list(Path('.').glob('Gr6_*_variations.json'))
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            questions_with_visuals = []
            for question in data:
                has_visual = False
                
                # Check for any visual components
                if 'solution_image_tag' in question and question['solution_image_tag']:
                    has_visual = True
                if 'image_tag' in question and question['image_tag']:
                    has_visual = True
                if 'shape_image_tags' in question and question['shape_image_tags']:
                    has_visual = True
                if 'image_choice_tags' in question and question['image_choice_tags']:
                    has_visual = True
                
                if has_visual:
                    questions_with_visuals.append(question)
            
            if questions_with_visuals:
                json_visual_files[str(json_file)] = questions_with_visuals
                
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    
    return json_visual_files

def check_html_exists(json_filename, question):
    """Check if HTML file exists for a question"""
    # Extract week and exercise from JSON filename
    match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', json_filename)
    if not match:
        return False
    
    week, exercise = match.groups()
    question_num = question.get('question_number', '')
    
    # Check various possible HTML filename patterns
    html_dir = Path('HTML')
    if not html_dir.exists():
        return False
    
    # Patterns to check
    patterns = [
        f"Gr6_{week}_E{exercise} {question_num}.html",
        f"Gr6_{week}_E{exercise} {question_num}_*.html",
        f"Gr6_{week}_E{exercise} {question_num.replace('_', '_')}_*.html"
    ]
    
    for pattern in patterns:
        if list(html_dir.glob(pattern)):
            return True
    
    return False

def main():
    print("Identifying missing HTML files for Grade 6 visual components...")
    print("=" * 60)
    
    json_visual_files = get_json_files_with_visuals()
    
    missing_html = {}
    has_html = {}
    
    for json_file, questions in json_visual_files.items():
        json_name = Path(json_file).name
        missing_count = 0
        has_count = 0
        
        for question in questions:
            if not check_html_exists(json_name, question):
                missing_count += 1
                if json_file not in missing_html:
                    missing_html[json_file] = []
                missing_html[json_file].append(question)
            else:
                has_count += 1
        
        if missing_count > 0:
            print(f"\n{json_name}:")
            print(f"  - Questions with visuals: {len(questions)}")
            print(f"  - Missing HTML files: {missing_count}")
            print(f"  - Has HTML files: {has_count}")
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Total JSON files with visuals: {len(json_visual_files)}")
    print(f"JSON files missing some/all HTML: {len(missing_html)}")
    
    print("\n" + "=" * 60)
    print("FILES NEEDING HTML GENERATION:")
    for json_file in sorted(missing_html.keys()):
        json_name = Path(json_file).name
        questions = missing_html[json_file]
        print(f"\n{json_name}: {len(questions)} questions need HTML")
        # Show first few question numbers
        q_nums = [q.get('question_number', 'unknown') for q in questions[:5]]
        print(f"  Question numbers: {', '.join(q_nums)}{'...' if len(questions) > 5 else ''}")
    
    # Save detailed list for generation script
    with open('missing_html_details.json', 'w') as f:
        json.dump(missing_html, f, indent=2)
    print(f"\nDetailed list saved to missing_html_details.json")

if __name__ == "__main__":
    main()