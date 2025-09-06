import json
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

def extract_week_exercise_from_filename(filename):
    """Extract week and exercise numbers from filename like Gr6_10_E1_variations.json"""
    match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', filename)
    if match:
        return match.group(1), match.group(2)
    return None, None

def check_html_file(json_data, week_num, exercise_num, question_num):
    """Check if HTML file exists and contains correct image divs"""
    html_filename = f"HTML/Gr6_{week_num}_E{exercise_num} {question_num}.html"
    
    if not os.path.exists(html_filename):
        return False, f"Missing HTML file: {html_filename}"
    
    try:
        with open(html_filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        issues = []
        required_tags = set()
        
        # Check image_tag
        if 'image_tag' in json_data and json_data['image_tag']:
            required_tags.add(json_data['image_tag'])
        
        # Check image_choice_tags
        if 'image_choice_tags' in json_data and json_data['image_choice_tags']:
            for tag in json_data['image_choice_tags']:
                if tag:  # Only add non-empty tags
                    required_tags.add(tag)
        
        # Check shape_image_tags
        if 'shape_image_tags' in json_data and json_data['shape_image_tags']:
            for shape_obj in json_data['shape_image_tags']:
                if isinstance(shape_obj, dict) and 'tag' in shape_obj:
                    required_tags.add(shape_obj['tag'])
        
        # Check solution_image_tag
        if 'solution_image_tag' in json_data and json_data['solution_image_tag']:
            for sol_item in json_data['solution_image_tag']:
                if isinstance(sol_item, list) and len(sol_item) >= 2:
                    tag = sol_item[1] if len(sol_item) > 1 else None
                    if tag:
                        required_tags.add(tag)
        
        # Find all divs with class="item" in HTML
        html_divs = soup.find_all('div', class_='item')
        html_tags = set()
        for div in html_divs:
            label = div.get('label', '')
            if label:
                html_tags.add(label)
        
        # Check for missing tags
        missing_tags = required_tags - html_tags
        extra_tags = html_tags - required_tags
        
        if missing_tags:
            issues.append(f"Missing divs with labels: {missing_tags}")
        if extra_tags:
            issues.append(f"Extra divs with labels: {extra_tags}")
        
        if issues:
            return False, "; ".join(issues)
        return True, "All tags match correctly"
        
    except Exception as e:
        return False, f"Error reading HTML: {str(e)}"

def verify_json_file(filename):
    """Verify a single JSON file and its associated HTML files"""
    week_num, exercise_num = extract_week_exercise_from_filename(filename)
    if not week_num or not exercise_num:
        return None, f"Could not parse filename: {filename}"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return None, f"Error reading JSON: {str(e)}"
    
    results = {
        'filename': filename,
        'total_questions': 0,
        'questions_with_images': 0,
        'passed': [],
        'failed': [],
        'no_images': []
    }
    
    # Handle both list and dictionary formats
    questions = {}
    if isinstance(data, list):
        # Convert list to dictionary format
        for i, item in enumerate(data, 1):
            questions[f'question_{i}'] = item
    elif isinstance(data, dict):
        questions = data
    else:
        return None, f"Unexpected data format in {filename}"
    
    # Check each question
    for key, value in questions.items():
        if not key.startswith('question_'):
            continue
        
        question_num = key.replace('question_', '')
        results['total_questions'] += 1
        
        # Check if question has any images
        has_images = False
        if 'image_tag' in value and value['image_tag']:
            has_images = True
        if 'image_choice_tags' in value and value['image_choice_tags']:
            has_images = True
        if 'shape_image_tags' in value and value['shape_image_tags']:
            has_images = True
        if 'solution_image_tag' in value and value['solution_image_tag']:
            has_images = True
        
        if not has_images:
            results['no_images'].append(question_num)
            continue
        
        results['questions_with_images'] += 1
        
        # Check HTML file
        success, message = check_html_file(value, week_num, exercise_num, question_num)
        
        if success:
            results['passed'].append(question_num)
        else:
            results['failed'].append({
                'question': question_num,
                'issue': message
            })
    
    return results, None

def main():
    """Main verification function"""
    # Get all Grade 6 JSON files
    json_files = sorted([f for f in os.listdir('.') if f.startswith('Gr6_') and f.endswith('_variations.json')])
    
    print("=== Grade 6 HTML Visual Components Re-Verification Report ===")
    print(f"Date: 2025-09-06")
    print(f"Total JSON files to check: {len(json_files)}\n")
    
    total_files = 0
    files_passed = []
    files_with_issues = []
    total_questions_checked = 0
    total_questions_with_images = 0
    total_passed = 0
    total_failed = 0
    
    for json_file in json_files:
        results, error = verify_json_file(json_file)
        
        if error:
            print(f"ERROR processing {json_file}: {error}")
            continue
        
        total_files += 1
        total_questions_checked += results['total_questions']
        total_questions_with_images += results['questions_with_images']
        total_passed += len(results['passed'])
        total_failed += len(results['failed'])
        
        if results['failed']:
            files_with_issues.append({
                'file': json_file,
                'issues': results['failed']
            })
            print(f"FAILED: {json_file}")
            for issue in results['failed']:
                print(f"  - Question {issue['question']}: {issue['issue']}")
        else:
            files_passed.append(json_file)
            if results['questions_with_images'] > 0:
                print(f"PASSED: {json_file} - All {results['questions_with_images']} questions with images validated")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total files checked: {total_files}")
    print(f"Files that pass validation: {len(files_passed)}")
    print(f"Files with issues: {len(files_with_issues)}")
    print(f"\nTotal questions checked: {total_questions_checked}")
    print(f"Questions with images: {total_questions_with_images}")
    print(f"Questions passed: {total_passed}")
    print(f"Questions failed: {total_failed}")
    
    if total_questions_with_images > 0:
        success_rate = (total_passed / total_questions_with_images) * 100
        print(f"\nSuccess rate: {success_rate:.1f}%")
    
    if files_with_issues:
        print("\n" + "="*60)
        print("FILES STILL REQUIRING ATTENTION:")
        print("="*60)
        for file_info in files_with_issues:
            print(f"\n{file_info['file']}:")
            for issue in file_info['issues']:
                print(f"  - Question {issue['question']}: {issue['issue']}")
    else:
        print("\n" + "="*60)
        print("ALL FILES PASS VALIDATION!")
        print("="*60)
    
    return len(files_passed), len(files_with_issues)

if __name__ == "__main__":
    passed, failed = main()