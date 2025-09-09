import json
import os
import re
from pathlib import Path

def extract_divs_from_html(html_content):
    """Extract all divs with class='item' and their labels from HTML content."""
    pattern = r'<div[^>]*class="item"[^>]*label="([^"]+)"[^>]*>(.*?)</div>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    return {label: content.strip() for label, content in matches}

def validate_visual_content(html_content, expected_description, tag_name):
    """Check if HTML content matches the expected backend description."""
    # Basic validation - check for key visual elements
    issues = []
    
    # Check for histograms
    if 'histogram' in expected_description.lower() or 'bar' in expected_description.lower():
        if '<rect' not in html_content and 'bar' not in html_content.lower():
            issues.append(f"Expected histogram/bars for {tag_name}, but no rectangles found")
    
    # Check for number lines
    if 'number line' in expected_description.lower():
        if '<line' not in html_content and '<text' not in html_content:
            issues.append(f"Expected number line for {tag_name}, but no lines or text found")
    
    # Check for coordinate planes
    if 'coordinate' in expected_description.lower() or 'grid' in expected_description.lower():
        if '<line' not in html_content:
            issues.append(f"Expected coordinate plane/grid for {tag_name}, but no lines found")
    
    # Check for fractions
    if 'fraction' in expected_description.lower():
        if 'fraction' not in html_content.lower() and '/' not in html_content:
            issues.append(f"Expected fraction visualization for {tag_name}, but none found")
    
    # Check for placeholder rectangles (these should not exist)
    if 'width="100" height="100"' in html_content and 'fill="lightgray"' in html_content:
        issues.append(f"Found placeholder rectangle for {tag_name}")
    
    return issues

def check_html_file(json_data, week, exercise, question_num):
    """Check if HTML file exists and validates its content."""
    # First check if this question has any visuals
    has_visuals = False
    if ('image_tag' in json_data and json_data['image_tag']) or \
       ('image_choice_tags' in json_data and json_data['image_choice_tags']) or \
       ('shape_image_tags' in json_data and json_data['shape_image_tags']) or \
       ('solution_image_tag' in json_data and json_data['solution_image_tag']):
        has_visuals = True
    
    if not has_visuals:
        return {
            'status': 'no_visuals',
            'issues': [],
            'has_visuals': False,
            'required_tags': 0,
            'found_tags': 0
        }
    
    html_path = Path(f"HTML/Gr6_{week}_E{exercise} {question_num}.html")
    
    if not html_path.exists():
        return {
            'status': 'missing',
            'issues': [f"Missing HTML file: {html_path}"],
            'has_visuals': True,
            'required_tags': 0,
            'found_tags': 0
        }
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract all divs from HTML
    html_divs = extract_divs_from_html(html_content)
    required_tags = set()
    issues = []
    
    # Check image_tag
    if 'image_tag' in json_data and json_data['image_tag']:
        tag = json_data['image_tag']
        required_tags.add(tag)
        if tag not in html_divs:
            issues.append(f"Missing div for image_tag: {tag}")
        elif 'backend_description' in json_data:
            content_issues = validate_visual_content(
                html_divs[tag], 
                json_data['backend_description'],
                tag
            )
            issues.extend(content_issues)
    
    # Check image_choice_tags
    if 'image_choice_tags' in json_data and json_data['image_choice_tags']:
        descriptions = json_data.get('image_choice_tags_backend_description', [])
        for i, tag in enumerate(json_data['image_choice_tags']):
            required_tags.add(tag)
            if tag not in html_divs:
                issues.append(f"Missing div for image_choice_tag: {tag}")
            elif i < len(descriptions):
                content_issues = validate_visual_content(
                    html_divs[tag],
                    descriptions[i],
                    tag
                )
                issues.extend(content_issues)
    
    # Check shape_image_tags
    if 'shape_image_tags' in json_data and json_data['shape_image_tags']:
        for shape_obj in json_data['shape_image_tags']:
            if isinstance(shape_obj, dict) and 'tag' in shape_obj:
                tag = shape_obj['tag']
                required_tags.add(tag)
                if tag not in html_divs:
                    issues.append(f"Missing div for shape_image_tag: {tag}")
                elif 'backend_description' in shape_obj:
                    content_issues = validate_visual_content(
                        html_divs[tag],
                        shape_obj['backend_description'],
                        tag
                    )
                    issues.extend(content_issues)
    
    # Check solution_image_tag
    if 'solution_image_tag' in json_data and json_data['solution_image_tag']:
        for step in json_data['solution_image_tag']:
            if isinstance(step, list) and len(step) >= 3:
                tag = step[1]
                description = step[2] if len(step) > 2 else ""
                required_tags.add(tag)
                if tag not in html_divs:
                    issues.append(f"Missing div for solution_image_tag: {tag}")
                elif description:
                    content_issues = validate_visual_content(
                        html_divs[tag],
                        description,
                        tag
                    )
                    issues.extend(content_issues)
    
    # Check for extra divs
    extra_divs = set(html_divs.keys()) - required_tags
    if extra_divs:
        issues.append(f"Extra divs found: {', '.join(extra_divs)}")
    
    # Check for duplicate divs
    div_pattern = r'<div[^>]*class="item"[^>]*label="([^"]+)"'
    all_labels = re.findall(div_pattern, html_content)
    duplicates = [label for label in set(all_labels) if all_labels.count(label) > 1]
    if duplicates:
        issues.append(f"Duplicate divs found: {', '.join(duplicates)}")
    
    return {
        'status': 'fail' if issues else 'pass',
        'issues': issues,
        'required_tags': len(required_tags),
        'found_tags': len(html_divs),
        'has_visuals': len(required_tags) > 0
    }

def main():
    """Main validation function."""
    print("=" * 80)
    print("GRADE 6 HTML VISUAL QUALITY CHECK - COMPREHENSIVE REPORT")
    print("=" * 80)
    print()
    
    # Get all Grade 6 JSON files
    json_files = sorted(Path('.').glob('Gr6_*_variations.json'))
    
    total_questions = 0
    questions_with_visuals = 0
    questions_passed = 0
    questions_failed = 0
    missing_files = 0
    
    all_issues = {}
    summary_by_week = {}
    
    for json_file in json_files:
        # Parse filename
        parts = json_file.stem.split('_')
        week = parts[1]
        exercise = parts[2][1:]  # Remove 'E' prefix
        
        week_key = f"Week {week}"
        if week_key not in summary_by_week:
            summary_by_week[week_key] = {
                'total': 0,
                'with_visuals': 0,
                'passed': 0,
                'failed': 0,
                'missing': 0
            }
        
        # Load JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        questions = []
        if 'quizzes' in data:
            # Grade 6 structure
            for quiz in data['quizzes']:
                question_num = quiz.get('question_number', '')
                questions.append((question_num, quiz))
        else:
            # Other grade structure
            for question_num, question_data in data.items():
                if question_num == "exercise_description":
                    continue
                questions.append((question_num, question_data))
        
        # Check each question
        for question_num, question_data in questions:
            
            total_questions += 1
            summary_by_week[week_key]['total'] += 1
            
            result = check_html_file(question_data, week, exercise, question_num)
            
            if result['has_visuals']:
                questions_with_visuals += 1
                summary_by_week[week_key]['with_visuals'] += 1
                
                if result['status'] == 'missing':
                    missing_files += 1
                    summary_by_week[week_key]['missing'] += 1
                    all_issues[f"Gr6_{week}_E{exercise} Q{question_num}"] = result['issues']
                elif result['status'] == 'fail':
                    questions_failed += 1
                    summary_by_week[week_key]['failed'] += 1
                    all_issues[f"Gr6_{week}_E{exercise} Q{question_num}"] = result['issues']
                else:
                    questions_passed += 1
                    summary_by_week[week_key]['passed'] += 1
    
    # Print results
    print("OVERALL SUMMARY")
    print("-" * 40)
    print(f"Total questions examined: {total_questions}")
    print(f"Questions with visuals: {questions_with_visuals}")
    print(f"Questions without visuals: {total_questions - questions_with_visuals}")
    print()
    
    if questions_with_visuals > 0:
        print("VALIDATION RESULTS FOR VISUAL QUESTIONS")
        print("-" * 40)
        print(f"Passed validation: {questions_passed} ({questions_passed/questions_with_visuals*100:.1f}%)")
        print(f"Failed validation: {questions_failed} ({questions_failed/questions_with_visuals*100:.1f}%)")
        print(f"Missing HTML files: {missing_files} ({missing_files/questions_with_visuals*100:.1f}%)")
        print()
        
        # Count HTML files actually present
        html_files = list(Path('HTML').glob('Gr6_*.html'))
        print(f"Total HTML files found: {len(html_files)}")
        print(f"Expected HTML files (with visuals): {questions_with_visuals}")
        print()
    
    # Week by week summary
    print("WEEK BY WEEK BREAKDOWN")
    print("-" * 40)
    for week in sorted(summary_by_week.keys(), key=lambda x: int(x.split()[1])):
        stats = summary_by_week[week]
        if stats['with_visuals'] > 0:
            print(f"\n{week}:")
            print(f"  Total questions: {stats['total']}")
            print(f"  With visuals: {stats['with_visuals']}")
            print(f"  Passed: {stats['passed']} ({stats['passed']/stats['with_visuals']*100:.1f}%)")
            print(f"  Failed: {stats['failed']} ({stats['failed']/stats['with_visuals']*100:.1f}%)")
            print(f"  Missing: {stats['missing']} ({stats['missing']/stats['with_visuals']*100:.1f}%)")
    
    # Issue details
    if all_issues:
        print("\n" + "=" * 80)
        print("DETAILED ISSUES (First 20)")
        print("-" * 40)
        count = 0
        for question, issues in list(all_issues.items())[:20]:
            count += 1
            print(f"\n{question}:")
            for issue in issues[:3]:  # Show first 3 issues per question
                print(f"  - {issue}")
        
        if len(all_issues) > 20:
            print(f"\n... and {len(all_issues) - 20} more questions with issues")
    
    # Final verdict
    print("\n" + "=" * 80)
    print("FINAL ASSESSMENT")
    print("-" * 40)
    
    if questions_with_visuals > 0:
        pass_rate = questions_passed / questions_with_visuals * 100
        if pass_rate >= 99:
            print("✓ EXCELLENT: Files are ready for upload to NUMI")
            print(f"  {pass_rate:.1f}% of visual questions passed validation")
        elif pass_rate >= 95:
            print("✓ GOOD: Files are mostly ready, minor fixes needed")
            print(f"  {pass_rate:.1f}% of visual questions passed validation")
        elif pass_rate >= 90:
            print("⚠ ACCEPTABLE: Files need some attention before upload")
            print(f"  {pass_rate:.1f}% of visual questions passed validation")
        else:
            print("✗ NEEDS WORK: Significant issues found")
            print(f"  Only {pass_rate:.1f}% of visual questions passed validation")
    
    # Save detailed report
    report_file = Path('grade6_validation_report.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("GRADE 6 HTML VALIDATION DETAILED REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total questions: {total_questions}\n")
        f.write(f"Questions with visuals: {questions_with_visuals}\n")
        f.write(f"Passed: {questions_passed}\n")
        f.write(f"Failed: {questions_failed}\n")
        f.write(f"Missing: {missing_files}\n\n")
        
        if all_issues:
            f.write("DETAILED ISSUES:\n")
            f.write("-" * 40 + "\n")
            for question, issues in all_issues.items():
                f.write(f"\n{question}:\n")
                for issue in issues:
                    f.write(f"  - {issue}\n")
    
    print(f"\nDetailed report saved to: {report_file.absolute()}")
    
    return {
        'total_questions': total_questions,
        'questions_with_visuals': questions_with_visuals,
        'passed': questions_passed,
        'failed': questions_failed,
        'missing': missing_files,
        'pass_rate': questions_passed / questions_with_visuals * 100 if questions_with_visuals > 0 else 0
    }

if __name__ == "__main__":
    results = main()