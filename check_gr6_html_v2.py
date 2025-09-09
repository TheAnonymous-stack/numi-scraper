import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
from html.parser import HTMLParser

class HTMLDivExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.divs = []
        self.current_div = None
        self.current_content = []
        self.in_item_div = False
        self.depth = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'div' and attrs_dict.get('class') == 'item':
            self.in_item_div = True
            self.depth = 1
            self.current_div = {
                'label': attrs_dict.get('label', ''),
                'content': []
            }
            self.current_content = []
        elif self.in_item_div:
            self.depth += 1 if tag == 'div' else 0
            # Store the full tag with attributes
            attr_str = ' '.join([f'{k}="{v}"' for k, v in attrs])
            if attr_str:
                self.current_content.append(f'<{tag} {attr_str}>')
            else:
                self.current_content.append(f'<{tag}>')
    
    def handle_endtag(self, tag):
        if self.in_item_div:
            if tag == 'div':
                self.depth -= 1
                if self.depth == 0:
                    self.current_div['content'] = ''.join(self.current_content)
                    self.divs.append(self.current_div)
                    self.in_item_div = False
                    self.current_div = None
                    self.current_content = []
                else:
                    self.current_content.append(f'</{tag}>')
            else:
                self.current_content.append(f'</{tag}>')
    
    def handle_data(self, data):
        if self.in_item_div:
            self.current_content.append(data)

def validate_html_content(html_content, backend_desc):
    """Basic validation of HTML content against backend description"""
    # This is a simplified check - you can make it more sophisticated
    # For now, just check that HTML is not empty when there's a backend description
    if backend_desc and len(backend_desc) > 10:
        if not html_content.strip():
            return False, "Empty HTML content"
    return True, ""

def check_grade6_exercises():
    results = {
        'passed': [],
        'failed': [],
        'total_checked': 0,
        'with_images': 0,
        'details': {}
    }
    
    # Get all Grade 6 JSON files
    json_files = sorted(Path('.').glob('Gr6_*_variations.json'))
    
    for json_file in json_files:
        file_name = json_file.name
        # Extract week and exercise from filename
        match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', file_name)
        if not match:
            continue
            
        week, exercise = match.groups()
        exercise_key = f"Gr6_{week}_E{exercise}"
        
        print(f"Checking {exercise_key}...")
        results['total_checked'] += 1
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            results['failed'].append(exercise_key)
            results['details'][exercise_key] = [f"Failed to read JSON: {e}"]
            continue
        
        # Use 'quizzes' for Grade 6 files
        questions = data.get('quizzes', data.get('questions', []))
        exercise_issues = []
        has_images = False
        questions_with_images = []
        
        for q_idx, question in enumerate(questions, 1):
            question_issues = []
            question_has_images = False
            
            # Extract question number if available
            q_num = question.get('question_number', str(q_idx))
            # Remove the exercise prefix if present (e.g., "5_1" -> "1")
            if '_' in str(q_num):
                q_num = q_num.split('_')[-1]
            
            # Check for image fields
            image_tag = question.get('image_tag')
            image_choice_tags = question.get('image_choice_tags', [])
            shape_image_tags = question.get('shape_image_tags', [])
            solution_image_tag = question.get('solution_image_tag', [])
            
            # Determine if this question has images
            if image_tag or image_choice_tags or shape_image_tags or solution_image_tag:
                question_has_images = True
                has_images = True
                questions_with_images.append(q_num)
                
                # Construct expected HTML filename - note the space before question number
                html_file = Path('HTML') / f"Gr6_{week}_E{exercise} {q_num}.html"
                
                if not html_file.exists():
                    # Try with underscore instead of space
                    html_file_alt = Path('HTML') / f"Gr6_{week}_E{exercise}_{q_num}.html"
                    if html_file_alt.exists():
                        html_file = html_file_alt
                    else:
                        question_issues.append(f"Question {q_num}: Missing HTML file - expected {html_file} or {html_file_alt}")
                        exercise_issues.extend(question_issues)
                        continue
                
                # Parse HTML file
                try:
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    parser = HTMLDivExtractor()
                    parser.feed(html_content)
                    
                    # Create a dict of label -> content for easy lookup
                    html_divs = {div['label']: div['content'] for div in parser.divs}
                    
                    # Check image_tag
                    if image_tag:
                        if image_tag not in html_divs:
                            question_issues.append(f"Question {q_num}: Missing div with label='{image_tag}'")
                        else:
                            backend_desc = question.get('backend_description', '')
                            valid, error = validate_html_content(html_divs[image_tag], backend_desc)
                            if not valid:
                                question_issues.append(f"Question {q_num}: {error} for image_tag '{image_tag}'")
                    
                    # Check image_choice_tags
                    if image_choice_tags:
                        descriptions = question.get('image_choice_tags_backend_description', [])
                        for idx, tag in enumerate(image_choice_tags):
                            if tag not in html_divs:
                                question_issues.append(f"Question {q_num}: Missing div with label='{tag}' for image_choice_tags[{idx}]")
                            else:
                                desc = descriptions[idx] if idx < len(descriptions) else ''
                                valid, error = validate_html_content(html_divs[tag], desc)
                                if not valid:
                                    question_issues.append(f"Question {q_num}: {error} for image_choice_tag '{tag}'")
                    
                    # Check shape_image_tags
                    if shape_image_tags:
                        for shape_idx, shape_obj in enumerate(shape_image_tags):
                            if isinstance(shape_obj, dict):
                                tag = shape_obj.get('tag')
                                desc = shape_obj.get('backend_description', '')
                                if tag and tag not in html_divs:
                                    question_issues.append(f"Question {q_num}: Missing div with label='{tag}' for shape_image_tags[{shape_idx}]")
                                elif tag:
                                    valid, error = validate_html_content(html_divs[tag], desc)
                                    if not valid:
                                        question_issues.append(f"Question {q_num}: {error} for shape_image_tag '{tag}'")
                    
                    # Check solution_image_tag
                    if solution_image_tag:
                        for sol_idx, solution_item in enumerate(solution_image_tag):
                            if isinstance(solution_item, list) and len(solution_item) >= 3:
                                tag = solution_item[1]  # Second element is the tag
                                desc = solution_item[2] if len(solution_item) > 2 else ''  # Third element is description
                                if tag not in html_divs:
                                    question_issues.append(f"Question {q_num}: Missing div with label='{tag}' for solution_image_tag[{sol_idx}]")
                                else:
                                    valid, error = validate_html_content(html_divs[tag], desc)
                                    if not valid:
                                        question_issues.append(f"Question {q_num}: {error} for solution_image_tag '{tag}'")
                    
                    # Check for extra divs
                    expected_tags = set()
                    if image_tag:
                        expected_tags.add(image_tag)
                    if image_choice_tags:
                        expected_tags.update(image_choice_tags)
                    if shape_image_tags:
                        for shape_obj in shape_image_tags:
                            if isinstance(shape_obj, dict):
                                tag = shape_obj.get('tag')
                                if tag:
                                    expected_tags.add(tag)
                    if solution_image_tag:
                        for solution_item in solution_image_tag:
                            if isinstance(solution_item, list) and len(solution_item) >= 2:
                                expected_tags.add(solution_item[1])
                    
                    extra_tags = set(html_divs.keys()) - expected_tags
                    if extra_tags:
                        question_issues.append(f"Question {q_num}: Extra divs found with labels: {extra_tags}")
                        
                except Exception as e:
                    question_issues.append(f"Question {q_num}: Failed to parse HTML file - {e}")
            
            if question_issues:
                exercise_issues.extend(question_issues)
        
        if has_images:
            results['with_images'] += 1
            if questions_with_images:
                print(f"  - Found images in questions: {questions_with_images}")
            
        if exercise_issues:
            results['failed'].append(exercise_key)
            results['details'][exercise_key] = exercise_issues
        else:
            results['passed'].append(exercise_key)
    
    return results

def print_report(results):
    print("\n" + "="*60)
    print("=== Grade 6 HTML Visual Quality Check Report ===")
    print("="*60)
    
    print(f"\n[PASSED] Exercises with correct HTML ({len(results['passed'])}):")
    if len(results['passed']) <= 20:
        for exercise in sorted(results['passed']):
            print(f"  - {exercise}")
    else:
        # Show first 10 and last 10 if too many
        passed_sorted = sorted(results['passed'])
        for exercise in passed_sorted[:10]:
            print(f"  - {exercise}")
        print(f"  ... ({len(passed_sorted) - 20} more exercises)")
        for exercise in passed_sorted[-10:]:
            print(f"  - {exercise}")
    
    print(f"\n[FAILED] Exercises with issues ({len(results['failed'])}):")
    for exercise in sorted(results['failed']):
        print(f"\n  {exercise}:")
        for issue in results['details'][exercise]:
            print(f"    - {issue}")
    
    print("\n" + "-"*60)
    print("Summary:")
    print(f"- Total exercises checked: {results['total_checked']}")
    print(f"- Exercises with images: {results['with_images']}")
    print(f"- Passed validation: {len(results['passed'])}")
    print(f"- Failed validation: {len(results['failed'])}")
    if results['total_checked'] > 0:
        print(f"- Pass rate: {len(results['passed'])/results['total_checked']*100:.1f}%")
    
    # List exercises with images that failed
    if results['failed']:
        print(f"\nExercises needing attention:")
        for exercise in sorted(results['failed']):
            print(f"  - {exercise}")

if __name__ == "__main__":
    results = check_grade6_exercises()
    print_report(results)