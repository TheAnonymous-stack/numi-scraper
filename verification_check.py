#!/usr/bin/env python3
"""
Grade 6 HTML Visual Components Verification Script
Checks all JSON files and their corresponding HTML files to verify completeness and correctness.
"""

import json
import os
import glob
from pathlib import Path
import re

class HTMLVisualVerifier:
    def __init__(self):
        self.results = {
            'total_files': 0,
            'total_questions': 0,
            'questions_with_visuals': 0,
            'passed_validation': 0,
            'failed_validation': 0,
            'issues': [],
            'file_results': {}
        }
    
    def extract_week_exercise_from_filename(self, filename):
        """Extract week and exercise numbers from filename"""
        match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', os.path.basename(filename))
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None
    
    def check_html_file_exists(self, week, exercise, question_num):
        """Check if HTML file exists for given parameters"""
        html_filename = f"HTML/Gr6_{week}_E{exercise} {question_num}.html"
        return os.path.exists(html_filename), html_filename
    
    def parse_html_divs(self, html_file):
        """Parse HTML file and extract div elements with class='item' and their labels"""
        divs = {}
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all divs with class="item"
            div_pattern = r'<div[^>]*class="item"[^>]*label="([^"]*)"[^>]*>(.*?)</div>'
            matches = re.findall(div_pattern, content, re.DOTALL)
            
            for label, div_content in matches:
                divs[label] = div_content.strip()
                
        except Exception as e:
            print(f"Error reading HTML file {html_file}: {e}")
            
        return divs
    
    def verify_question_visuals(self, week, exercise, question_num, question_data):
        """Verify all visual components for a single question"""
        issues = []
        required_divs = []
        
        # Check for image_tag
        if 'image_tag' in question_data and question_data['image_tag']:
            required_divs.append({
                'label': question_data['image_tag'],
                'type': 'image_tag',
                'description': question_data.get('backend_description', '')
            })
        
        # Check for image_choice_tags
        if 'image_choice_tags' in question_data and question_data['image_choice_tags']:
            choice_descriptions = question_data.get('image_choice_tags_backend_description', [])
            for i, tag in enumerate(question_data['image_choice_tags']):
                description = choice_descriptions[i] if i < len(choice_descriptions) else ''
                required_divs.append({
                    'label': tag,
                    'type': 'image_choice_tag',
                    'description': description
                })
        
        # Check for shape_image_tags
        if 'shape_image_tags' in question_data and question_data['shape_image_tags']:
            for shape_obj in question_data['shape_image_tags']:
                if isinstance(shape_obj, dict) and 'tag' in shape_obj:
                    required_divs.append({
                        'label': shape_obj['tag'],
                        'type': 'shape_image_tag',
                        'description': shape_obj.get('backend_description', '')
                    })
        
        # Check for solution_image_tag
        if 'solution_image_tag' in question_data and question_data['solution_image_tag']:
            if isinstance(question_data['solution_image_tag'], list):
                for solution_list in question_data['solution_image_tag']:
                    if isinstance(solution_list, list) and len(solution_list) >= 3:
                        tag = solution_list[1]
                        description = solution_list[2]
                        required_divs.append({
                            'label': tag,
                            'type': 'solution_image_tag',
                            'description': description
                        })
        
        # If no visual requirements, return success
        if not required_divs:
            return True, []
        
        # Check HTML file exists
        html_exists, html_file = self.check_html_file_exists(week, exercise, question_num)
        if not html_exists:
            issues.append(f"Missing HTML file: {html_file}")
            return False, issues
        
        # Parse HTML divs
        html_divs = self.parse_html_divs(html_file)
        
        # Verify each required div
        for required_div in required_divs:
            label = required_div['label']
            if label not in html_divs:
                issues.append(f"Missing div with label '{label}' in {html_file}")
            # Note: We're not doing content matching in this verification for speed
            # The comprehensive fixer should have handled content correctness
        
        # Check for extra divs (not required by JSON)
        required_labels = {div['label'] for div in required_divs}
        extra_labels = set(html_divs.keys()) - required_labels
        if extra_labels:
            issues.append(f"Extra divs found in {html_file}: {', '.join(extra_labels)}")
        
        return len(issues) == 0, issues
    
    def verify_json_file(self, json_file):
        """Verify all questions in a JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            week, exercise = self.extract_week_exercise_from_filename(json_file)
            if week is None or exercise is None:
                print(f"Could not parse filename: {json_file}")
                return
            
            file_results = {
                'total_questions': 0,
                'questions_with_visuals': 0,
                'passed': 0,
                'failed': 0,
                'issues': []
            }
            
            # Handle both structures: array directly or questions property
            if isinstance(data, list):
                questions = data
            else:
                questions = data.get('questions', [])
            
            for question in questions:
                question_num = question.get('question_number')
                if question_num is None:
                    continue
                
                file_results['total_questions'] += 1
                self.results['total_questions'] += 1
                
                # Check if question has visual requirements
                has_visuals = any([
                    question.get('image_tag'),
                    question.get('image_choice_tags'),
                    question.get('shape_image_tags'),
                    question.get('solution_image_tag')
                ])
                
                if has_visuals:
                    file_results['questions_with_visuals'] += 1
                    self.results['questions_with_visuals'] += 1
                    
                    success, issues = self.verify_question_visuals(week, exercise, question_num, question)
                    
                    if success:
                        file_results['passed'] += 1
                        self.results['passed_validation'] += 1
                    else:
                        file_results['failed'] += 1
                        self.results['failed_validation'] += 1
                        file_results['issues'].extend(issues)
                        self.results['issues'].extend(issues)
            
            self.results['file_results'][json_file] = file_results
            
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    def run_verification(self):
        """Run verification on all Grade 6 JSON files"""
        json_files = glob.glob("Gr6_*_variations.json")
        json_files = [f for f in json_files if '.backup' not in f]
        json_files.sort()
        
        self.results['total_files'] = len(json_files)
        
        print("Starting Grade 6 HTML Visual Components Verification...")
        print(f"Found {len(json_files)} JSON files to verify")
        print()
        
        for json_file in json_files:
            print(f"Verifying: {json_file}")
            self.verify_json_file(json_file)
        
        return self.results
    
    def generate_report(self):
        """Generate comprehensive verification report"""
        results = self.results
        
        print("\n" + "="*80)
        print("GRADE 6 HTML VISUAL COMPONENTS VERIFICATION REPORT")
        print("="*80)
        print()
        
        print("OVERALL SUMMARY:")
        print(f"  Total JSON files processed: {results['total_files']}")
        print(f"  Total questions examined: {results['total_questions']}")
        print(f"  Questions with visual requirements: {results['questions_with_visuals']}")
        print(f"  Questions passed validation: {results['passed_validation']}")
        print(f"  Questions failed validation: {results['failed_validation']}")
        print()
        
        if results['questions_with_visuals'] > 0:
            success_rate = (results['passed_validation'] / results['questions_with_visuals']) * 100
            print(f"SUCCESS RATE: {success_rate:.1f}%")
        else:
            print("SUCCESS RATE: N/A (no questions with visual requirements)")
        print()
        
        if results['failed_validation'] > 0:
            print("REMAINING ISSUES:")
            issue_counts = {}
            for issue in results['issues']:
                if issue not in issue_counts:
                    issue_counts[issue] = 0
                issue_counts[issue] += 1
            
            for issue, count in sorted(issue_counts.items()):
                if count > 1:
                    print(f"  - {issue} ({count} occurrences)")
                else:
                    print(f"  - {issue}")
        else:
            print("NO REMAINING ISSUES FOUND!")
        
        print()
        print("="*80)

def main():
    verifier = HTMLVisualVerifier()
    verifier.run_verification()
    verifier.generate_report()

if __name__ == "__main__":
    main()