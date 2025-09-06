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

class HTMLVisualChecker:
    def __init__(self):
        self.base_dir = Path(".")
        self.html_dir = self.base_dir / "HTML"
        self.total_files = 0
        self.files_with_images = 0
        self.files_passed = []
        self.files_with_issues = []
        self.detailed_issues = defaultdict(list)
        
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
    
    def normalize_html(self, html: str) -> str:
        """Normalize HTML for comparison by removing extra whitespace."""
        # Remove extra whitespace between tags
        html = re.sub(r'>\s+<', '><', html)
        # Normalize whitespace within text
        html = re.sub(r'\s+', ' ', html)
        return html.strip()
    
    def compare_html_to_description(self, html: str, description: str) -> bool:
        """Compare HTML content to backend description."""
        # This is a basic comparison - in reality, we'd need more sophisticated
        # comparison logic based on the actual HTML structure and descriptions
        # For now, we'll do a normalized comparison
        html_norm = self.normalize_html(html).lower()
        desc_norm = description.lower()
        
        # Check for key elements from description in HTML
        # This would need to be expanded based on actual description format
        key_elements = re.findall(r'\w+', desc_norm)
        matches = sum(1 for elem in key_elements if elem in html_norm)
        
        # Consider it a match if most key elements are present
        return matches >= len(key_elements) * 0.7
    
    def check_question_images(self, question: dict, week: int, exercise: int, question_num: str) -> List[str]:
        """Check all image requirements for a single question."""
        issues = []
        required_images = {}
        
        # Check for image_tag
        if "image_tag" in question and question["image_tag"]:
            tag = question["image_tag"]
            desc = question.get("backend_description", "")
            required_images[tag] = ("image_tag", desc)
        
        # Check for image_choice_tags
        if "image_choice_tags" in question and question["image_choice_tags"]:
            descriptions = question.get("image_choice_tags_backend_description", [])
            for i, tag in enumerate(question["image_choice_tags"]):
                if tag:
                    desc = descriptions[i] if i < len(descriptions) else ""
                    required_images[tag] = (f"image_choice_tag[{i}]", desc)
        
        # Check for shape_image_tags
        if "shape_image_tags" in question and question["shape_image_tags"]:
            for shape_obj in question["shape_image_tags"]:
                if isinstance(shape_obj, dict) and "tag" in shape_obj:
                    tag = shape_obj["tag"]
                    desc = shape_obj.get("backend_description", "")
                    required_images[tag] = ("shape_image_tag", desc)
        
        # Check for solution_image_tag
        if "solution_image_tag" in question and question["solution_image_tag"]:
            # solution_image_tag is typically a list of lists
            if isinstance(question["solution_image_tag"], list):
                for item in question["solution_image_tag"]:
                    if isinstance(item, list) and len(item) >= 3:
                        tag = item[1] if len(item) > 1 else None
                        desc = item[2] if len(item) > 2 else ""
                        if tag:
                            required_images[tag] = ("solution_image_tag", desc)
        
        # If no images required, return empty list
        if not required_images:
            return []
        
        # Check for HTML file
        html_filename = f"Gr6_{week}_E{exercise} {question_num}.html"
        html_path = self.html_dir / html_filename
        
        if not html_path.exists():
            issues.append(f"Missing HTML file: {html_filename}")
            return issues
        
        # Read and parse HTML file
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except Exception as e:
            issues.append(f"Error reading HTML file {html_filename}: {str(e)}")
            return issues
        
        # Extract divs from HTML
        html_divs = self.extract_image_divs(html_content)
        
        # Check each required image
        for tag, (source, description) in required_images.items():
            if tag not in html_divs:
                issues.append(f"Missing div with label='{tag}' (from {source})")
            elif description and not self.compare_html_to_description(html_divs[tag], description):
                issues.append(f"Content mismatch for label='{tag}' (from {source})")
        
        # Check for extra divs
        extra_divs = set(html_divs.keys()) - set(required_images.keys())
        for extra in extra_divs:
            issues.append(f"Extra div found with label='{extra}' not in JSON")
        
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
            for question in data:
                if not isinstance(question, dict):
                    continue
                    
                total_questions += 1
                
                # Extract question number from the question object
                question_num = question.get("question_number", str(total_questions))
                
                # Check for images
                has_images = any([
                    question.get("image_tag"),
                    question.get("image_choice_tags"),
                    question.get("shape_image_tags"),
                    question.get("solution_image_tag")
                ])
                
                if has_images:
                    questions_with_images += 1
                    issues = self.check_question_images(question, week, exercise, question_num)
                    if issues:
                        for issue in issues:
                            file_issues.append(f"  Question {question_num}: {issue}")
        
        elif isinstance(data, dict):
            # Process dictionary format (if any files use this)
            for var_key, var_data in data.items():
                if not isinstance(var_data, dict):
                    continue
                    
                variations = var_data.get("variations", {})
                
                for q_key, question in variations.items():
                    if not isinstance(question, dict):
                        continue
                        
                    total_questions += 1
                    
                    # Extract question number
                    question_num = q_key.replace("q_", "")
                    
                    # Check for images
                    has_images = any([
                        question.get("image_tag"),
                        question.get("image_choice_tags"),
                        question.get("shape_image_tags"),
                        question.get("solution_image_tag")
                    ])
                    
                    if has_images:
                        questions_with_images += 1
                        issues = self.check_question_images(question, week, exercise, question_num)
                        if issues:
                            for issue in issues:
                                file_issues.append(f"  Question {question_num}: {issue}")
        
        return total_questions, questions_with_images, file_issues
    
    def run_check(self):
        """Run the comprehensive check on all Grade 6 JSON files."""
        print("Starting comprehensive HTML visual quality check for Grade 6...")
        print("=" * 80)
        
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
            
            for week in sorted(issues_by_week.keys()):
                print(f"\nWeek {week}:")
                for filename in issues_by_week[week]:
                    print(f"\n  {filename}:")
                    for issue in self.detailed_issues[filename]:
                        print(f"    {issue}")
        
        print("\n" + "=" * 80)
        print("END OF REPORT")
        print("=" * 80)

if __name__ == "__main__":
    checker = HTMLVisualChecker()
    checker.run_check()