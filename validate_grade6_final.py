import json
import os
import re
from pathlib import Path
from collections import defaultdict

def extract_all_image_tags_from_json(json_data):
    """Extract all image tags that should have HTML files from a question."""
    tags = []
    
    # Check image_tag
    if 'image_tag' in json_data and json_data['image_tag']:
        tags.append(json_data['image_tag'])
    
    # Check image_choice_tags
    if 'image_choice_tags' in json_data and json_data['image_choice_tags']:
        tags.extend(json_data['image_choice_tags'])
    
    # Check shape_image_tags
    if 'shape_image_tags' in json_data and json_data['shape_image_tags']:
        for shape_obj in json_data['shape_image_tags']:
            if isinstance(shape_obj, dict) and 'tag' in shape_obj:
                tags.append(shape_obj['tag'])
    
    # Check solution_image_tag
    if 'solution_image_tag' in json_data and json_data['solution_image_tag']:
        for step in json_data['solution_image_tag']:
            if isinstance(step, list) and len(step) >= 2:
                tags.append(step[1])  # The tag is the second element
    
    return tags

def check_html_content(html_path):
    """Check HTML file content for quality issues."""
    issues = []
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for placeholder rectangles
        if 'width="100" height="100"' in content and 'fill="lightgray"' in content:
            issues.append("Contains placeholder rectangle")
        
        # Check for empty SVG
        if '<svg' in content and not ('<rect' in content or '<circle' in content or 
                                      '<line' in content or '<path' in content or 
                                      '<text' in content or '<polygon' in content):
            issues.append("SVG appears to be empty")
        
        # Check for duplicate divs
        div_pattern = r'<div[^>]*class="item"[^>]*label="([^"]+)"'
        labels = re.findall(div_pattern, content)
        if len(labels) != len(set(labels)):
            duplicates = [l for l in set(labels) if labels.count(l) > 1]
            issues.append(f"Contains duplicate divs: {', '.join(duplicates)}")
        
        # Check if it's just a wrapper HTML with no actual content
        if len(labels) == 0:
            issues.append("No divs with class='item' found")
        
        # Check for basic visual elements
        has_visual = False
        if any(elem in content for elem in ['<rect', '<circle', '<line', '<path', 
                                             '<polygon', '<text', '<image', 'histogram',
                                             'bar', 'fraction', 'coordinate']):
            has_visual = True
        
        if not has_visual and '<svg' in content:
            issues.append("SVG present but no visual elements found")
            
    except Exception as e:
        issues.append(f"Error reading file: {str(e)}")
    
    return issues

def main():
    """Main validation function."""
    print("=" * 80)
    print("GRADE 6 HTML VISUAL FILES - FINAL COMPREHENSIVE CHECK")
    print("=" * 80)
    print()
    
    # Get all Grade 6 HTML files
    html_files = list(Path('HTML').glob('Gr6_*.html'))
    html_tags = set()
    html_file_map = {}
    
    for html_file in html_files:
        # Extract tag from filename (everything before .html)
        tag = html_file.stem
        html_tags.add(tag)
        html_file_map[tag] = html_file
    
    print(f"Total HTML files found: {len(html_files)}")
    
    # Get all Grade 6 JSON files and extract expected tags
    json_files = sorted(Path('.').glob('Gr6_*_variations.json'))
    expected_tags = set()
    tag_to_question = defaultdict(list)
    
    total_questions = 0
    questions_with_visuals = 0
    
    for json_file in json_files:
        parts = json_file.stem.split('_')
        week = parts[1]
        exercise = parts[2][1:]
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle Grade 6 structure
        if 'quizzes' in data:
            for quiz in data['quizzes']:
                total_questions += 1
                question_num = quiz.get('question_number', '')
                tags = extract_all_image_tags_from_json(quiz)
                
                if tags:
                    questions_with_visuals += 1
                    for tag in tags:
                        expected_tags.add(tag)
                        tag_to_question[tag].append(f"W{week}_E{exercise}_Q{question_num}")
    
    print(f"Total questions examined: {total_questions}")
    print(f"Questions with visuals: {questions_with_visuals}")
    print(f"Total unique image tags expected: {len(expected_tags)}")
    print()
    
    # Compare expected vs actual
    missing_html = expected_tags - html_tags
    extra_html = html_tags - expected_tags
    matched_html = expected_tags & html_tags
    
    print("FILE PRESENCE CHECK")
    print("-" * 40)
    print(f"HTML files matching expected tags: {len(matched_html)}")
    print(f"Missing HTML files: {len(missing_html)}")
    print(f"Extra HTML files (not referenced): {len(extra_html)}")
    print()
    
    # Quality check on existing HTML files
    print("QUALITY CHECK ON EXISTING FILES")
    print("-" * 40)
    
    files_with_issues = 0
    files_clean = 0
    issue_summary = defaultdict(int)
    
    for tag in matched_html:
        html_path = html_file_map[tag]
        issues = check_html_content(html_path)
        
        if issues:
            files_with_issues += 1
            for issue in issues:
                issue_summary[issue] += 1
        else:
            files_clean += 1
    
    print(f"Files passing quality check: {files_clean}")
    print(f"Files with issues: {files_with_issues}")
    
    if issue_summary:
        print("\nIssue breakdown:")
        for issue, count in sorted(issue_summary.items(), key=lambda x: -x[1]):
            print(f"  - {issue}: {count} files")
    print()
    
    # Sample of missing files
    if missing_html:
        print("SAMPLE OF MISSING HTML FILES (first 10)")
        print("-" * 40)
        for tag in list(missing_html)[:10]:
            questions = tag_to_question.get(tag, ['Unknown'])
            print(f"  {tag} (used in: {', '.join(questions[:3])})")
        if len(missing_html) > 10:
            print(f"  ... and {len(missing_html) - 10} more")
        print()
    
    # Sample of extra files
    if extra_html:
        print("SAMPLE OF EXTRA HTML FILES (first 10)")
        print("-" * 40)
        for tag in list(extra_html)[:10]:
            print(f"  {tag}")
        if len(extra_html) > 10:
            print(f"  ... and {len(extra_html) - 10} more")
        print()
    
    # Check specific visualization types
    print("VISUALIZATION TYPE CHECK")
    print("-" * 40)
    
    viz_types = {
        'histograms': 0,
        'number_lines': 0,
        'coordinate_planes': 0,
        'fractions': 0,
        'shapes': 0,
        'other': 0
    }
    
    sample_count = min(100, len(matched_html))
    for tag in list(matched_html)[:sample_count]:
        html_path = html_file_map[tag]
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            if 'histogram' in content or ('rect' in content and 'bar' in content):
                viz_types['histograms'] += 1
            elif 'number' in content and 'line' in content:
                viz_types['number_lines'] += 1
            elif 'coordinate' in content or 'grid' in content:
                viz_types['coordinate_planes'] += 1
            elif 'fraction' in content or 'numerator' in content:
                viz_types['fractions'] += 1
            elif 'shape' in content or 'polygon' in content or 'circle' in content:
                viz_types['shapes'] += 1
            else:
                viz_types['other'] += 1
        except:
            pass
    
    print(f"Sample of {sample_count} files shows:")
    for viz_type, count in viz_types.items():
        if count > 0:
            print(f"  - {viz_type}: {count}")
    print()
    
    # Final assessment
    print("=" * 80)
    print("FINAL ASSESSMENT")
    print("-" * 40)
    
    total_expected = len(expected_tags)
    total_present = len(matched_html)
    total_clean = files_clean
    
    if total_expected > 0:
        coverage = (total_present / total_expected) * 100
        quality = (total_clean / total_present * 100) if total_present > 0 else 0
        
        print(f"File Coverage: {coverage:.1f}% ({total_present}/{total_expected} files present)")
        print(f"Quality Rate: {quality:.1f}% ({total_clean}/{total_present} files clean)")
        print()
        
        if coverage >= 99 and quality >= 95:
            print("EXCELLENT: Files are ready for upload to NUMI")
            print("  - Nearly all expected files are present")
            print("  - High quality visualizations confirmed")
        elif coverage >= 95 and quality >= 90:
            print("GOOD: Files are mostly ready with minor fixes needed")
            print("  - Most files are present and of good quality")
            print(f"  - Address {len(missing_html)} missing files")
            print(f"  - Fix {files_with_issues} files with quality issues")
        elif coverage >= 90:
            print("ACCEPTABLE: Files need attention before upload")
            print(f"  - {len(missing_html)} files still missing")
            print(f"  - {files_with_issues} files have quality issues")
        else:
            print("NEEDS WORK: Significant gaps remain")
            print(f"  - Missing {len(missing_html)} files ({100-coverage:.1f}%)")
            print(f"  - Quality issues in {files_with_issues} files")
    
    print()
    print("SUMMARY STATISTICS")
    print("-" * 40)
    print(f"1. Total HTML files: {len(html_files)} (4,301 expected)")
    print(f"2. Questions with visuals: {questions_with_visuals} (4,020 expected)")
    print(f"3. Unique tags expected: {len(expected_tags)}")
    print(f"4. Files present and matching: {len(matched_html)}")
    print(f"5. Files passing quality check: {files_clean}")
    
    # Save detailed report
    report_path = Path('grade6_final_validation_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("GRADE 6 HTML FILES - FINAL VALIDATION REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Date: 2025-01-09\n")
        f.write(f"Total HTML files: {len(html_files)}\n")
        f.write(f"Expected unique tags: {len(expected_tags)}\n")
        f.write(f"Matched files: {len(matched_html)}\n")
        f.write(f"Missing files: {len(missing_html)}\n")
        f.write(f"Extra files: {len(extra_html)}\n")
        f.write(f"Files passing quality: {files_clean}\n")
        f.write(f"Files with issues: {files_with_issues}\n\n")
        
        if missing_html:
            f.write("MISSING HTML FILES:\n")
            f.write("-" * 40 + "\n")
            for tag in sorted(missing_html):
                f.write(f"{tag}\n")
            f.write("\n")
        
        if files_with_issues > 0 and matched_html:
            f.write("FILES WITH QUALITY ISSUES:\n")
            f.write("-" * 40 + "\n")
            count = 0
            for tag in matched_html:
                if count >= 50:  # Limit to first 50
                    break
                html_path = html_file_map[tag]
                issues = check_html_content(html_path)
                if issues:
                    f.write(f"{tag}: {', '.join(issues)}\n")
                    count += 1
    
    print(f"\nDetailed report saved to: {report_path.absolute()}")
    
    return {
        'total_html_files': len(html_files),
        'expected_tags': len(expected_tags),
        'matched': len(matched_html),
        'missing': len(missing_html),
        'extra': len(extra_html),
        'clean': files_clean,
        'with_issues': files_with_issues
    }

if __name__ == "__main__":
    results = main()