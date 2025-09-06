#!/usr/bin/env python3
"""
Comprehensive HTML Visual Quality Check for Grade 6 Math Questions
This script verifies that HTML visual components match their JSON specifications.
"""

import json
import os
from pathlib import Path
import re
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

class Gr6HTMLChecker:
    def __init__(self):
        self.base_dir = Path(".")
        self.html_dir = self.base_dir / "HTML"
        self.total_files = 0
        self.files_with_images = 0
        self.files_passed = []
        self.files_with_issues = []
        self.detailed_issues = defaultdict(list)
        self.all_html_files = set()
        
    def load_all_html_files(self):
        """Load all HTML filenames into memory for quick lookup."""
        if self.html_dir.exists():
            self.all_html_files = {f.name for f in self.html_dir.glob("*.html")}
        print(f"Found {len(self.all_html_files)} HTML files in {self.html_dir}")
        
    def extract_image_divs(self, html_content: str) -> Dict[str, str]:
        """Extract all divs with class='item' and their labels from HTML content."""
        divs = {}
        # Pattern to match divs with class="item" and label attribute
        pattern = r'<div[^>]*class\s*=\s*["\']item["\'][^>]*label\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</div>'
        matches = re.finditer(pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            label = match.group(1)
            content = match.group(2).strip()
            divs[label] = content
            
        return divs
    
    def find_html_files_for_question(self, week: int, exercise: int, question_num: str) -> List[str]:
        """Find all HTML files that might correspond to this question."""
        # Try different naming patterns
        patterns = [
            f"Gr6_{week}_E{exercise} {question_num}.html",  # Exact match
            f"Gr6_{week}_E{exercise} {question_num}_*.html",  # With variation suffix
        ]
        
        found_files = []
        for pattern in patterns:
            # Convert glob pattern to regex for searching
            regex_pattern = pattern.replace("*", r"\d+")
            regex_pattern = regex_pattern.replace(" ", r" ")
            
            for html_file in self.all_html_files:
                if re.match(regex_pattern, html_file):
                    found_files.append(html_file)
        
        # Also look for pattern like "Gr6_1_E1 1_1_1.html" for question "1_1"
        pattern_with_variation = f"Gr6_{week}_E{exercise} {question_num}_\\d+\\.html"
        for html_file in self.all_html_files:
            if re.match(pattern_with_variation, html_file):
                if html_file not in found_files:
                    found_files.append(html_file)
                    
        return sorted(found_files)
    
    def check_question_images(self, question: dict, week: int, exercise: int, 
                            question_num: str, question_index: int) -> List[str]:
        """Check all image requirements for a single question."""
        issues = []
        required_tags = set()
        tag_descriptions = {}
        
        # Check for image_tag
        if "image_tag" in question and question["image_tag"]:
            tag = question["image_tag"]
            desc = question.get("backend_description", "")
            required_tags.add(tag)
            tag_descriptions[tag] = desc
        
        # Check for image_choice_tags
        if "image_choice_tags" in question and question["image_choice_tags"]:
            descriptions = question.get("image_choice_tags_backend_description", [])
            for i, tag in enumerate(question["image_choice_tags"]):
                if tag:
                    desc = descriptions[i] if i < len(descriptions) else ""
                    required_tags.add(tag)
                    tag_descriptions[tag] = desc
        
        # Check for shape_image_tags
        if "shape_image_tags" in question and question["shape_image_tags"]:
            for shape_obj in question["shape_image_tags"]:
                if isinstance(shape_obj, dict) and "tag" in shape_obj:
                    tag = shape_obj["tag"]
                    desc = shape_obj.get("backend_description", "")
                    required_tags.add(tag)
                    tag_descriptions[tag] = desc
        
        # Check for solution_image_tag
        if "solution_image_tag" in question and question["solution_image_tag"]:
            if isinstance(question["solution_image_tag"], list):
                for item in question["solution_image_tag"]:
                    if isinstance(item, list) and len(item) >= 3:
                        tag = item[1] if len(item) > 1 else None
                        desc = item[2] if len(item) > 2 else ""
                        if tag:
                            required_tags.add(tag)
                            tag_descriptions[tag] = desc
        
        # If no images required, return empty list
        if not required_tags:
            return []
        
        # Find potential HTML files
        html_files = self.find_html_files_for_question(week, exercise, question_num)
        
        if not html_files:
            # Try with question index as variation number
            variation_filename = f"Gr6_{week}_E{exercise} {question_num}_{question_index}.html"
            if variation_filename in self.all_html_files:
                html_files = [variation_filename]
            else:
                issues.append(f"No HTML files found for question {question_num} (expected tags: {', '.join(required_tags)})")
                return issues
        
        # Check each HTML file
        found_tags = set()
        files_checked = []
        
        for html_filename in html_files:
            html_path = self.html_dir / html_filename
            
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    
                # Extract divs from HTML
                html_divs = self.extract_image_divs(html_content)
                
                # Track which tags are found in this file
                for tag in required_tags:
                    if tag in html_divs:
                        found_tags.add(tag)
                        
                files_checked.append(html_filename)
                
            except Exception as e:
                issues.append(f"Error reading HTML file {html_filename}: {str(e)}")
        
        # Report missing tags
        missing_tags = required_tags - found_tags
        if missing_tags:
            issues.append(f"Missing tags in HTML files: {', '.join(missing_tags)}")
            if files_checked:
                issues.append(f"  Checked files: {', '.join(files_checked)}")
        
        return issues
    
    def check_json_file(self, json_path: Path) -> Tuple[int, int, List[str]]:
        """Check all questions in a JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return 0, 0, [f"Error reading JSON: {str(e)}"]
        
        # Extract week and exercise from filename
        match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', json_path.name)
        if not match:
            return 0, 0, [f"Invalid filename format: {json_path.name}"]
        
        week = int(match.group(1))
        exercise = int(match.group(2))
        
        total_questions = 0
        questions_with_images = 0
        file_issues = []
        
        # Handle both array and object formats
        if isinstance(data, list):
            # Process array of questions
            for idx, question in enumerate(data, 1):
                if not isinstance(question, dict):
                    continue
                    
                total_questions += 1
                
                # Extract question number from the question object
                question_num = question.get("question_number", str(idx))
                
                # Check for images
                has_images = any([
                    question.get("image_tag"),
                    question.get("image_choice_tags"),
                    question.get("shape_image_tags"),
                    question.get("solution_image_tag")
                ])
                
                if has_images:
                    questions_with_images += 1
                    issues = self.check_question_images(question, week, exercise, question_num, idx)
                    if issues:
                        for issue in issues:
                            file_issues.append(f"  Question {question_num}: {issue}")
        
        return total_questions, questions_with_images, file_issues
    
    def run_check(self):
        """Run the comprehensive check on all Grade 6 JSON files."""
        print("Starting comprehensive HTML visual quality check for Grade 6...")
        print("=" * 80)
        
        # Load all HTML files first
        self.load_all_html_files()
        
        # Get all Grade 6 JSON files
        json_files = sorted(self.base_dir.glob("Gr6_*_variations.json"))
        
        for json_file in json_files:
            self.total_files += 1
            
            total_q, with_images, issues = self.check_json_file(json_file)
            
            if with_images > 0:
                self.files_with_images += 1
                
            if issues:
                self.files_with_issues.append(json_file.name)
                self.detailed_issues[json_file.name] = issues
            else:
                if with_images > 0:  # Only count as passed if it had images to check
                    self.files_passed.append(json_file.name)
        
        self.generate_report()
    
    def generate_report(self):
        """Generate the comprehensive report."""
        print("\n" + "=" * 80)
        print("HTML VISUAL QUALITY CHECK REPORT - GRADE 6")
        print("=" * 80)
        
        print(f"\nSummary Statistics:")
        print(f"  Total JSON files checked: {self.total_files}")
        print(f"  Files with visual components: {self.files_with_images}")
        print(f"  Files passed validation: {len(self.files_passed)}")
        print(f"  Files with issues: {len(self.files_with_issues)}")
        
        if self.files_passed:
            print(f"\n[PASSED] Files with correct HTML ({len(self.files_passed)}):")
            # Group by week for better organization
            files_by_week = defaultdict(list)
            for filename in sorted(self.files_passed):
                match = re.match(r'Gr6_(\d+)_', filename)
                if match:
                    week = int(match.group(1))
                    files_by_week[week].append(filename)
            
            for week in sorted(files_by_week.keys()):
                print(f"\n  Week {week}:")
                for filename in files_by_week[week]:
                    print(f"    - {filename}")
        
        if self.files_with_issues:
            print(f"\n[FAILED] Files with issues ({len(self.files_with_issues)}):")
            print("=" * 80)
            
            # Group by week for better organization
            issues_by_week = defaultdict(list)
            for filename in sorted(self.files_with_issues):
                match = re.match(r'Gr6_(\d+)_', filename)
                if match:
                    week = int(match.group(1))
                    issues_by_week[week].append(filename)
            
            # Limit output for readability
            total_issues_shown = 0
            max_issues_to_show = 50
            
            for week in sorted(issues_by_week.keys()):
                if total_issues_shown >= max_issues_to_show:
                    remaining = len(self.files_with_issues) - total_issues_shown
                    print(f"\n... and {remaining} more files with issues (truncated for readability)")
                    break
                    
                print(f"\nWeek {week}:")
                for filename in issues_by_week[week]:
                    if total_issues_shown >= max_issues_to_show:
                        break
                        
                    print(f"\n  {filename}:")
                    issue_count = 0
                    for issue in self.detailed_issues[filename]:
                        if issue_count < 5:  # Show max 5 issues per file
                            print(f"    {issue}")
                            issue_count += 1
                        else:
                            print(f"    ... and {len(self.detailed_issues[filename]) - 5} more issues")
                            break
                    total_issues_shown += 1
        
        # Final summary
        print("\n" + "=" * 80)
        print("SUMMARY:")
        print(f"  Total files: {self.total_files}")
        print(f"  Files with visual components: {self.files_with_images}")
        print(f"  Pass rate: {len(self.files_passed)}/{self.files_with_images} " +
              f"({100*len(self.files_passed)/max(1,self.files_with_images):.1f}%)")
        print("=" * 80)
        print("END OF REPORT")

if __name__ == "__main__":
    checker = Gr6HTMLChecker()
    checker.run_check()