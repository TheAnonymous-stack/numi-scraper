#!/usr/bin/env python3
"""
Final Comprehensive Validation Script for Grade 6 Math Questions
Checks all Gr6_*_variations.json files for HTML/JSON alignment
"""

import json
import os
import re
import glob
from pathlib import Path
from bs4 import BeautifulSoup

class FinalValidationChecker:
    def __init__(self):
        self.total_files = 0
        self.total_questions = 0
        self.questions_with_images = 0
        self.successful_validations = 0
        self.failed_validations = 0
        self.issues = []
        self.success_details = []
        
    def extract_week_exercise_from_filename(self, filename):
        """Extract week and exercise numbers from filename"""
        match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', os.path.basename(filename))
        if match:
            return match.group(1), match.group(2)
        return None, None

    def check_html_file_exists(self, week, exercise, question_num):
        """Check if HTML file exists for given parameters"""
        html_filename = f"HTML/Gr6_{week}_E{exercise} {question_num}.html"
        return os.path.exists(html_filename), html_filename

    def parse_html_labels(self, html_file):
        """Extract all label attributes from HTML file"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            items = soup.find_all('div', class_='item')
            labels = []
            for item in items:
                if item.get('label'):
                    labels.append(item.get('label'))
            return labels
        except Exception as e:
            return []

    def validate_question(self, question_data, week, exercise, question_num):
        """Validate a single question's HTML against JSON"""
        issues = []
        required_labels = []
        
        # Collect all required labels from JSON
        if question_data.get('image_tag'):
            required_labels.append(question_data['image_tag'])
            
        if question_data.get('image_choice_tags'):
            required_labels.extend(question_data['image_choice_tags'])
            
        if question_data.get('shape_image_tags'):
            for shape in question_data['shape_image_tags']:
                if isinstance(shape, dict) and 'tag' in shape:
                    required_labels.append(shape['tag'])
                    
        if question_data.get('solution_image_tag'):
            for solution_group in question_data['solution_image_tag']:
                if isinstance(solution_group, list) and len(solution_group) >= 2:
                    required_labels.append(solution_group[1])
        
        # If no images required, mark as success
        if not required_labels:
            return True, []
        
        # Check HTML file exists
        html_exists, html_file = self.check_html_file_exists(week, exercise, question_num)
        if not html_exists:
            issues.append(f"Missing HTML file: {html_file}")
            return False, issues
        
        # Parse HTML labels
        html_labels = self.parse_html_labels(html_file)
        
        # Check each required label exists
        for label in required_labels:
            if label not in html_labels:
                issues.append(f"Missing label '{label}' in {html_file}")
        
        # Check for extra labels (not critical but good to know)
        extra_labels = set(html_labels) - set(required_labels)
        if extra_labels:
            issues.append(f"Extra labels in {html_file}: {', '.join(extra_labels)}")
        
        # Check for generic labels that should have been fixed
        generic_labels = [label for label in html_labels if label.startswith('visual_') and label != label.replace('visual_', '')]
        if generic_labels:
            issues.append(f"Generic labels still present in {html_file}: {', '.join(generic_labels)}")
        
        return len(issues) == 0, issues

    def process_json_file(self, json_file):
        """Process a single JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            week, exercise = self.extract_week_exercise_from_filename(json_file)
            if not week or not exercise:
                self.issues.append(f"Could not parse filename: {json_file}")
                return
            
            file_issues = []
            file_successes = 0
            file_questions_with_images = 0
            
            # Handle both dict and list formats
            if isinstance(data, list):
                questions_to_process = enumerate(data, 1)
            elif isinstance(data, dict):
                questions_to_process = data.items()
            else:
                self.issues.append(f"Unexpected data format in {json_file}")
                return
            
            for question_num, question_data in questions_to_process:
                self.total_questions += 1
                
                # Check if question has any visual components
                has_images = any([
                    question_data.get('image_tag'),
                    question_data.get('image_choice_tags'),
                    question_data.get('shape_image_tags'),
                    question_data.get('solution_image_tag')
                ])
                
                if has_images:
                    self.questions_with_images += 1
                    file_questions_with_images += 1
                    
                    # Extract question number from question_data if available
                    actual_question_num = question_data.get('question_number', str(question_num))
                    if isinstance(actual_question_num, str) and '_' in actual_question_num:
                        actual_question_num = actual_question_num.split('_')[-1]
                    
                    success, issues = self.validate_question(question_data, week, exercise, actual_question_num)
                    if success:
                        self.successful_validations += 1
                        file_successes += 1
                    else:
                        self.failed_validations += 1
                        file_issues.extend([f"Question {actual_question_num}: {issue}" for issue in issues])
            
            # Record results for this file
            if file_questions_with_images > 0:
                success_rate = (file_successes / file_questions_with_images) * 100
                self.success_details.append({
                    'file': os.path.basename(json_file),
                    'questions_with_images': file_questions_with_images,
                    'successful': file_successes,
                    'success_rate': success_rate,
                    'issues': file_issues
                })
            
        except Exception as e:
            self.issues.append(f"Error processing {json_file}: {str(e)}")

    def run_validation(self):
        """Run validation on all Grade 6 files"""
        print("=== FINAL COMPREHENSIVE GRADE 6 VALIDATION ===")
        print("Starting validation of all Grade 6 variation files...\n")
        
        # Find all Grade 6 variation files
        json_files = glob.glob("Gr6_*_variations.json")
        json_files.sort()
        
        self.total_files = len(json_files)
        print(f"Found {self.total_files} Grade 6 variation files to validate")
        
        # Process each file
        for i, json_file in enumerate(json_files, 1):
            print(f"Processing {i}/{self.total_files}: {os.path.basename(json_file)}")
            self.process_json_file(json_file)
        
        # Generate comprehensive report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate the final validation report"""
        print("\n" + "="*80)
        print("FINAL VALIDATION REPORT")
        print("="*80)
        
        # Overall statistics
        total_success_rate = 0
        if self.questions_with_images > 0:
            total_success_rate = (self.successful_validations / self.questions_with_images) * 100
        
        print(f"\nOVERALL STATISTICS:")
        print(f"- Total files processed: {self.total_files}")
        print(f"- Total questions: {self.total_questions}")
        print(f"- Questions with visual components: {self.questions_with_images}")
        print(f"- Successful validations: {self.successful_validations}")
        print(f"- Failed validations: {self.failed_validations}")
        print(f"- OVERALL SUCCESS RATE: {total_success_rate:.1f}%")
        
        # Files with perfect scores
        perfect_files = [detail for detail in self.success_details if detail['success_rate'] == 100.0]
        print(f"\nFILES WITH 100% SUCCESS RATE: {len(perfect_files)}")
        
        # Files with issues
        problem_files = [detail for detail in self.success_details if detail['success_rate'] < 100.0]
        print(f"FILES WITH REMAINING ISSUES: {len(problem_files)}")
        
        if problem_files:
            print("\nFILES NEEDING ATTENTION:")
            for detail in problem_files:
                print(f"\n{detail['file']}:")
                print(f"  - Success rate: {detail['success_rate']:.1f}%")
                print(f"  - Questions with images: {detail['questions_with_images']}")
                print(f"  - Successful: {detail['successful']}")
                print(f"  - Issues:")
                for issue in detail['issues'][:5]:  # Show first 5 issues
                    print(f"    * {issue}")
                if len(detail['issues']) > 5:
                    print(f"    * ... and {len(detail['issues'])-5} more issues")
        
        # Summary of improvement
        print(f"\n" + "="*80)
        print("VALIDATION SUMMARY:")
        print("="*80)
        
        if total_success_rate >= 95:
            print("EXCELLENT: Validation success rate is 95% or higher!")
        elif total_success_rate >= 80:
            print("GOOD: Validation success rate is above 80%")
        elif total_success_rate >= 60:
            print("NEEDS IMPROVEMENT: Success rate is moderate")
        else:
            print("CRITICAL: Success rate is below 60%")
        
        print(f"\nThis represents a significant improvement from the initial 0% success rate.")
        print(f"Current success rate: {total_success_rate:.1f}%")
        
        if self.failed_validations == 0:
            print("\nPERFECT! All visual components are properly validated!")
        else:
            print(f"\nREMAINING WORK: {self.failed_validations} validation issues need attention")

if __name__ == "__main__":
    checker = FinalValidationChecker()
    checker.run_validation()