import json
import os
import glob
import re
from pathlib import Path

def check_html_visuals():
    # Find all Grade 6 JSON files
    json_files = sorted(glob.glob("Gr6_*_variations.json"))
    
    report = {
        "total_files": 0,
        "total_questions": 0,
        "questions_with_images": 0,
        "passed_validation": [],
        "failed_validation": [],
        "issues": []
    }
    
    for json_file in json_files:
        print(f"Checking {json_file}...")
        report["total_files"] += 1
        
        # Extract week and exercise from filename
        match = re.match(r"Gr6_(\d+)_E(\d+)_variations\.json", json_file)
        if not match:
            continue
            
        week_num = match.group(1)
        exercise_num = match.group(2)
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            report["issues"].append({
                "file": json_file,
                "error": f"Failed to read JSON: {str(e)}"
            })
            continue
        
        # Check each question (data is a list)
        if not isinstance(data, list):
            report["issues"].append({
                "file": json_file,
                "error": f"Unexpected JSON structure: not a list"
            })
            continue
            
        for question in data:
            if not isinstance(question, dict):
                continue
                
            report["total_questions"] += 1
            q_num = question.get("question_number", "")
            
            # Check for image fields
            has_images = False
            image_requirements = []
            
            # Check image_tag
            if "image_tag" in question and question["image_tag"]:
                has_images = True
                image_requirements.append({
                    "type": "image_tag",
                    "tag": question["image_tag"],
                    "description": question.get("backend_description", "")
                })
            
            # Check image_choice_tags
            if "image_choice_tags" in question and question["image_choice_tags"]:
                has_images = True
                descriptions = question.get("image_choice_tags_backend_description", [])
                for i, tag in enumerate(question["image_choice_tags"]):
                    desc = descriptions[i] if i < len(descriptions) else ""
                    image_requirements.append({
                        "type": "image_choice_tag",
                        "tag": tag,
                        "description": desc
                    })
            
            # Check shape_image_tags
            if "shape_image_tags" in question and question["shape_image_tags"]:
                has_images = True
                for shape_obj in question["shape_image_tags"]:
                    if isinstance(shape_obj, dict) and "tag" in shape_obj:
                        image_requirements.append({
                            "type": "shape_image_tag",
                            "tag": shape_obj["tag"],
                            "description": shape_obj.get("backend_description", "")
                        })
            
            # Check solution_image_tag
            if "solution_image_tag" in question and question["solution_image_tag"]:
                has_images = True
                for solution_item in question["solution_image_tag"]:
                    if isinstance(solution_item, list) and len(solution_item) >= 3:
                        image_requirements.append({
                            "type": "solution_image_tag",
                            "tag": solution_item[1],
                            "description": solution_item[2]
                        })
            
            if not has_images:
                continue
                
            report["questions_with_images"] += 1
            
            # Check for corresponding HTML file - try multiple naming patterns
            # Pattern 1: Space separator (e.g., "Gr6_15_E5 1_1.html")
            html_filename = f"HTML/Gr6_{week_num}_E{exercise_num} {q_num}.html"
            html_path = Path(html_filename)
            
            # Pattern 2: Underscore separator (e.g., "Gr6_15_E5_1_1.html")
            if not html_path.exists():
                # Replace first underscore in q_num with nothing if needed
                q_num_parts = q_num.split("_")
                if len(q_num_parts) == 2:
                    html_filename = f"HTML/Gr6_{week_num}_E{exercise_num}_{q_num_parts[0]}_{q_num_parts[1]}.html"
                else:
                    html_filename = f"HTML/Gr6_{week_num}_E{exercise_num}_{q_num}.html"
                html_path = Path(html_filename)
            
            if not html_path.exists():
                report["failed_validation"].append(f"{json_file} - Question {q_num}")
                report["issues"].append({
                    "file": json_file,
                    "question": q_num,
                    "issue_type": "Missing File",
                    "details": f"HTML file not found: {html_filename}",
                    "expected": html_filename,
                    "found": "No file",
                    "action": f"Create HTML file with required image divs"
                })
                continue
            
            # Read and check HTML content
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            except Exception as e:
                report["issues"].append({
                    "file": json_file,
                    "question": q_num,
                    "issue_type": "Read Error",
                    "details": f"Failed to read HTML file: {str(e)}",
                    "expected": "Readable HTML file",
                    "found": "Unreadable file",
                    "action": "Fix file encoding or permissions"
                })
                continue
            
            # Check for required divs
            validation_passed = True
            for req in image_requirements:
                # Look for div with matching label
                pattern = f'<div[^>]*class="item"[^>]*label="{req["tag"]}"[^>]*>'
                if not re.search(pattern, html_content):
                    # Try alternate pattern
                    pattern2 = f'<div[^>]*label="{req["tag"]}"[^>]*class="item"[^>]*>'
                    if not re.search(pattern2, html_content):
                        validation_passed = False
                        report["issues"].append({
                            "file": json_file,
                            "question": q_num,
                            "issue_type": "Missing Div",
                            "details": f"Missing div for {req['type']}: {req['tag']}",
                            "expected": f'<div class="item" label="{req["tag"]}">',
                            "found": "Not found in HTML",
                            "action": f"Add div with label='{req['tag']}' and implement visual as: {req['description'][:100]}..."
                        })
            
            if validation_passed:
                report["passed_validation"].append(f"{json_file} - Question {q_num}")
            else:
                report["failed_validation"].append(f"{json_file} - Question {q_num}")
    
    return report

def generate_report(report):
    print("\n" + "="*60)
    print("=== HTML Visual Quality Check Report ===")
    print("="*60)
    print(f"\nFiles Processed: {report['total_files']}")
    print(f"Total Questions: {report['total_questions']}")
    print(f"Questions with Images: {report['questions_with_images']}")
    print(f"Passed Validation: {len(report['passed_validation'])}")
    print(f"Failed Validation: {len(report['failed_validation'])}")
    
    if report['passed_validation']:
        print(f"\n[PASS] Questions with correct HTML: {len(report['passed_validation'])} total")
        # Show first 10 as examples
        for item in report['passed_validation'][:10]:
            print(f"  - {item}")
        if len(report['passed_validation']) > 10:
            print(f"  ... and {len(report['passed_validation']) - 10} more")
    
    if report['failed_validation']:
        print(f"\n[FAIL] Questions with issues: {len(report['failed_validation'])} total")
        
        # Group issues by type
        issue_types = {}
        for issue in report['issues']:
            issue_type = issue.get('issue_type', 'Unknown')
            if issue_type not in issue_types:
                issue_types[issue_type] = []
            issue_types[issue_type].append(issue)
        
        for issue_type, issues in issue_types.items():
            print(f"\n{issue_type} ({len(issues)} issues):")
            for issue in issues[:5]:  # Show first 5 of each type
                print(f"\n  Question: {issue['file']} - {issue.get('question', 'N/A')}")
                print(f"  Details: {issue['details']}")
                print(f"  Expected: {issue.get('expected', 'N/A')}")
                print(f"  Found: {issue.get('found', 'N/A')}")
                print(f"  Action Required: {issue.get('action', 'N/A')}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more {issue_type} issues")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total files checked: {report['total_files']}")
    print(f"Questions with images: {report['questions_with_images']}")
    print(f"Passed validation: {len(report['passed_validation'])}")
    print(f"Failed validation: {len(report['failed_validation'])}")
    
    if report['questions_with_images'] > 0:
        success_rate = (len(report['passed_validation']) / report['questions_with_images']) * 100
        print(f"Success Rate: {success_rate:.1f}%")
    
    # Save detailed report to file
    with open("COMPREHENSIVE_HTML_CHECK_REPORT.txt", "w", encoding="utf-8") as f:
        f.write("=== COMPREHENSIVE HTML VISUAL CHECK REPORT ===\n")
        f.write("="*60 + "\n\n")
        f.write(f"Files Processed: {report['total_files']}\n")
        f.write(f"Total Questions: {report['total_questions']}\n")
        f.write(f"Questions with Images: {report['questions_with_images']}\n")
        f.write(f"Passed Validation: {len(report['passed_validation'])}\n")
        f.write(f"Failed Validation: {len(report['failed_validation'])}\n\n")
        
        f.write("DETAILED ISSUES:\n")
        f.write("-"*60 + "\n")
        for issue in report['issues']:
            f.write(f"\nFile: {issue['file']}\n")
            f.write(f"Question: {issue.get('question', 'N/A')}\n")
            f.write(f"Issue Type: {issue.get('issue_type', 'Unknown')}\n")
            f.write(f"Details: {issue['details']}\n")
            f.write(f"Expected: {issue.get('expected', 'N/A')}\n")
            f.write(f"Found: {issue.get('found', 'N/A')}\n")
            f.write(f"Action Required: {issue.get('action', 'N/A')}\n")
            f.write("-"*40 + "\n")
    
    print("\nDetailed report saved to: COMPREHENSIVE_HTML_CHECK_REPORT.txt")

if __name__ == "__main__":
    report = check_html_visuals()
    generate_report(report)