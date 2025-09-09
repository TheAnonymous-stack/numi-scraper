import json
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

def check_grade6_html_files():
    """
    Check Grade 6 HTML visual files for:
    1. Correct label format
    2. Existence of HTML files
    3. Content validation against backend descriptions
    """
    
    results = {
        'total_exercises': 0,
        'exercises_with_images': 0,
        'passed_validation': [],
        'failed_validation': [],
        'missing_html_files': [],
        'label_format_issues': [],
        'content_mismatches': []
    }
    
    # Find all Grade 6 JSON files
    json_files = sorted(Path('.').glob('Gr6_*_variations.json'))
    
    for json_file in json_files:
        print(f"\nChecking {json_file.name}...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        exercises = data.get('quizzes', [])
        results['total_exercises'] += len(exercises)
        
        for exercise in exercises:
            question_number = exercise.get('question_number', '')
            
            # Check if exercise has images
            has_images = False
            image_tags = []
            
            if 'image_tag' in exercise and exercise['image_tag']:
                has_images = True
                image_tags.append(exercise['image_tag'])
            
            if 'image_choice_tags' in exercise and exercise['image_choice_tags']:
                has_images = True
                image_tags.extend(exercise['image_choice_tags'])
            
            if 'shape_image_tags' in exercise and exercise['shape_image_tags']:
                has_images = True
                for shape in exercise['shape_image_tags']:
                    if isinstance(shape, dict) and 'tag' in shape:
                        image_tags.append(shape['tag'])
            
            if 'solution_image_tag' in exercise and exercise['solution_image_tag']:
                has_images = True
                for sol_item in exercise['solution_image_tag']:
                    if isinstance(sol_item, list) and len(sol_item) >= 3:
                        image_tags.append(sol_item[1])
            
            if not has_images:
                continue
            
            results['exercises_with_images'] += 1
            
            # Extract week and exercise number from filename
            match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', json_file.name)
            if not match:
                continue
            
            week_num = match.group(1)
            exercise_num = match.group(2)
            
            # Construct HTML filename
            html_filename = f"HTML/Gr6_{week_num}_E{exercise_num}_{question_number}.html"
            html_path = Path(html_filename)
            
            # Check if HTML file exists
            if not html_path.exists():
                results['missing_html_files'].append({
                    'exercise': f"Gr6_{week_num}_E{exercise_num}",
                    'question': question_number,
                    'expected_file': html_filename,
                    'required_tags': image_tags
                })
                results['failed_validation'].append(f"{json_file.name} Q{question_number}")
                continue
            
            # Parse HTML file
            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Check for divs with class="item"
            item_divs = soup.find_all('div', class_='item')
            found_labels = [div.get('label', '') for div in item_divs]
            
            # Validate labels
            validation_passed = True
            issues = []
            
            # Check label format (should be Gr6_XX_EX_variations_image_tag format)
            for label in found_labels:
                if label and not label.startswith('Gr6_'):
                    issues.append(f"Incorrect label format: {label}")
                    validation_passed = False
            
            # Check if all required tags are present
            for tag in image_tags:
                if tag not in found_labels:
                    issues.append(f"Missing div for tag: {tag}")
                    validation_passed = False
            
            # Check for extra divs
            extra_labels = [label for label in found_labels if label and label not in image_tags]
            if extra_labels:
                issues.append(f"Extra divs found: {extra_labels}")
                validation_passed = False
            
            # Content validation - check if HTML represents the backend description
            if 'backend_description' in exercise and exercise['backend_description']:
                # Simple check: if description mentions "map" or "locations" but HTML only has basic shapes
                desc = exercise['backend_description'].lower()
                if ('map' in desc or 'location' in desc or 'path' in desc) and item_divs:
                    # Check if SVG contains appropriate elements
                    svg_elements = soup.find_all('svg')
                    has_complex_visualization = False
                    
                    for svg in svg_elements:
                        # Check for multiple elements that would represent a map
                        lines = svg.find_all(['line', 'path'])
                        circles = svg.find_all(['circle', 'ellipse'])
                        texts = svg.find_all('text')
                        
                        if (len(lines) >= 2 or len(circles) >= 3 or len(texts) >= 2):
                            has_complex_visualization = True
                            break
                    
                    if not has_complex_visualization:
                        issues.append(f"Content mismatch: Backend describes a map/path visualization but HTML contains only basic shapes")
                        validation_passed = False
                        results['content_mismatches'].append({
                            'file': html_filename,
                            'description': exercise['backend_description'][:100] + '...',
                            'issue': 'Simple shape instead of complex map visualization'
                        })
            
            if validation_passed:
                results['passed_validation'].append(f"{json_file.name} Q{question_number}")
            else:
                results['failed_validation'].append(f"{json_file.name} Q{question_number}")
                if issues:
                    results['label_format_issues'].append({
                        'file': html_filename,
                        'issues': issues
                    })
    
    return results

def print_report(results):
    """Print a detailed report of the validation results"""
    
    print("\n" + "="*60)
    print("GRADE 6 HTML VISUAL QUALITY CHECK REPORT")
    print("="*60)
    
    print(f"\nSummary Statistics:")
    print(f"  Total questions checked: {results['total_exercises']}")
    print(f"  Questions with images: {results['exercises_with_images']}")
    print(f"  Passed validation: {len(results['passed_validation'])}")
    print(f"  Failed validation: {len(results['failed_validation'])}")
    
    # Calculate pass rate
    if results['exercises_with_images'] > 0:
        pass_rate = (len(results['passed_validation']) / results['exercises_with_images']) * 100
        print(f"  Pass rate: {pass_rate:.1f}%")
    
    print(f"\n[PASS] Questions with correct HTML: {len(results['passed_validation'])} files")
    
    if results['missing_html_files']:
        print(f"\n[FAIL] Missing HTML Files: {len(results['missing_html_files'])} files")
        for item in results['missing_html_files'][:5]:  # Show first 5
            print(f"    - {item['expected_file']}")
            print(f"      Required tags: {item['required_tags']}")
        if len(results['missing_html_files']) > 5:
            print(f"    ... and {len(results['missing_html_files']) - 5} more")
    
    if results['label_format_issues']:
        print(f"\n[FAIL] Label Format Issues: {len(results['label_format_issues'])} files")
        for item in results['label_format_issues'][:5]:  # Show first 5
            print(f"    - {item['file']}")
            for issue in item['issues']:
                print(f"      * {issue}")
        if len(results['label_format_issues']) > 5:
            print(f"    ... and {len(results['label_format_issues']) - 5} more")
    
    if results['content_mismatches']:
        print(f"\n[FAIL] Content Mismatches: {len(results['content_mismatches'])} files")
        print("  CRITICAL: HTML visualizations do not match backend descriptions!")
        for item in results['content_mismatches'][:5]:  # Show first 5
            print(f"    - {item['file']}")
            print(f"      Issue: {item['issue']}")
            print(f"      Description: {item['description']}")
        if len(results['content_mismatches']) > 5:
            print(f"    ... and {len(results['content_mismatches']) - 5} more")
    
    print("\n" + "="*60)
    print("KEY FINDINGS:")
    print("="*60)
    
    if results['content_mismatches']:
        print("\n[WARNING] CRITICAL ISSUE DETECTED:")
        print("   The HTML files have correct label formats but the visual content")
        print("   does NOT match the backend descriptions. Most files show simple")
        print("   rectangles instead of the complex map visualizations described.")
        print(f"   Affected files: {len(results['content_mismatches'])} out of {results['exercises_with_images']}")
    
    if not results['missing_html_files'] and not results['label_format_issues']:
        print("\n[PASS] All HTML files exist with correct label formats!")
    
    print("\nRECOMMENDED ACTIONS:")
    if results['content_mismatches']:
        print("1. HIGH PRIORITY: Regenerate HTML visualizations to match backend descriptions")
        print("   - Current HTML shows basic shapes instead of map/path visualizations")
        print("   - Backend descriptions specify complex maps with locations and paths")
    if results['missing_html_files']:
        print("2. Create missing HTML files for questions that require visualizations")
    if results['label_format_issues']:
        print("3. Fix label format issues in existing HTML files")

if __name__ == "__main__":
    results = check_grade6_html_files()
    print_report(results)