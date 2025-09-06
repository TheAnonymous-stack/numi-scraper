#!/usr/bin/env python3
"""
Comprehensive Grade 6 Files Verification Script
Checks all JSON and HTML files for compliance with specifications
"""

import json
import os
import glob
import re
from collections import defaultdict

class Grade6Verifier:
    def __init__(self):
        self.json_issues = []
        self.html_issues = []
        self.json_files_checked = 0
        self.html_files_checked = 0
        self.compliance_summary = {
            'json_files_total': 0,
            'json_files_compliant': 0,
            'html_files_total': 0,
            'html_files_compliant': 0,
            'missing_html_files': 0
        }

    def verify_json_file(self, filepath):
        """Verify a single JSON file for all requirements"""
        filename = os.path.basename(filepath)
        issues = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if it's a variations file
            if not isinstance(data, list):
                issues.append(f"File should contain a list of variations")
                return issues
            
            # Check for exactly 51 variations
            if len(data) != 51:
                issues.append(f"Expected 51 variations, found {len(data)}")
            
            # Check tag consistency
            base_tags = set()
            for i, variation in enumerate(data, 1):
                if 'tag' in variation:
                    base_tags.add(variation['tag'])
            
            if len(base_tags) > 1:
                issues.append(f"Inconsistent base tags found: {base_tags}")
            
            # Check each variation
            for i, variation in enumerate(data, 1):
                var_issues = self.verify_variation(variation, i, filename)
                issues.extend(var_issues)
            
        except json.JSONDecodeError as e:
            issues.append(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            issues.append(f"Error processing file: {str(e)}")
        
        return issues

    def verify_variation(self, variation, var_num, filename):
        """Verify a single variation for all requirements"""
        issues = []
        
        # Check for required fields
        required_fields = ['question', 'correct_answers', 'question_type']
        for field in required_fields:
            if field not in variation:
                issues.append(f"Variation {var_num}: Missing required field '{field}'")
        
        # Check question_type specific requirements
        if 'question_type' in variation:
            q_type = variation['question_type']
            
            if q_type == 'fill in the blank':
                issues.extend(self.verify_fill_in_blank(variation, var_num))
            elif q_type == 'multiple choice':
                issues.extend(self.verify_multiple_choice(variation, var_num))
        
        # Check orderMatter field if present
        if 'orderMatter' in variation:
            if not isinstance(variation['orderMatter'], bool):
                issues.append(f"Variation {var_num}: 'orderMatter' should be boolean, found {type(variation['orderMatter'])}")
        
        # Check has_alternate_answers if present
        if 'has_alternate_answers' in variation:
            if variation['has_alternate_answers'] is True:
                if 'correct_answers' not in variation:
                    issues.append(f"Variation {var_num}: has_alternate_answers=True but no correct_answers")
                else:
                    # Check nested array structure
                    if not isinstance(variation['correct_answers'], list):
                        issues.append(f"Variation {var_num}: correct_answers should be list when has_alternate_answers=True")
                    else:
                        for j, answer_group in enumerate(variation['correct_answers']):
                            if not isinstance(answer_group, list):
                                issues.append(f"Variation {var_num}: correct_answers[{j}] should be nested array")
        
        return issues

    def verify_fill_in_blank(self, variation, var_num):
        """Verify fill in the blank specific requirements"""
        issues = []
        
        if 'question' in variation and 'correct_answers' in variation:
            question = variation['question']
            correct_answers = variation['correct_answers']
            
            # Count underscores
            underscore_count = question.count('_')
            
            # Check if correct_answers is properly structured
            if isinstance(correct_answers, list) and len(correct_answers) > 0:
                if isinstance(correct_answers[0], list):
                    # Has alternate answers structure
                    answer_count = len(correct_answers)
                else:
                    # Simple list structure
                    answer_count = len(correct_answers)
                
                if underscore_count != answer_count:
                    issues.append(f"Variation {var_num}: Underscore count ({underscore_count}) != answer count ({answer_count})")
        
        return issues

    def verify_multiple_choice(self, variation, var_num):
        """Verify multiple choice specific requirements"""
        issues = []
        
        if 'correct_answers' in variation:
            correct_answers = variation['correct_answers']
            
            # Check that correct_answers contains option letters (A, B, C, D)
            valid_options = {'A', 'B', 'C', 'D'}
            if isinstance(correct_answers, list):
                for answer in correct_answers:
                    if isinstance(answer, str) and answer not in valid_options:
                        # Check if it's not a letter but actual text
                        if len(answer) > 1:
                            issues.append(f"Variation {var_num}: Multiple choice answer should be option letter (A,B,C,D), found '{answer}'")
        
        return issues

    def verify_html_files(self):
        """Verify HTML files exist and have proper structure"""
        html_pattern = "HTML/Gr6_*_E*_*_*.html"
        html_files = glob.glob(html_pattern)
        
        self.compliance_summary['html_files_total'] = len(html_files)
        compliant_count = 0
        
        for filepath in html_files:
            filename = os.path.basename(filepath)
            issues = self.verify_html_file(filepath)
            
            if issues:
                self.html_issues.append({
                    'file': filename,
                    'issues': issues
                })
            else:
                compliant_count += 1
            
            self.html_files_checked += 1
        
        self.compliance_summary['html_files_compliant'] = compliant_count

    def verify_html_file(self, filepath):
        """Verify a single HTML file"""
        filename = os.path.basename(filepath)
        issues = []
        
        # Check filename format: Gr6_X_EX_Y_Z.html
        pattern = r'^Gr6_(\d+)_E(\d+)_(\d+)_(\d+)\.html$'
        if not re.match(pattern, filename):
            issues.append(f"Filename doesn't match pattern Gr6_X_EX_Y_Z.html")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for proper div structure
            div_pattern = r'<div\s+class="item"\s+label="[^"]+"\s+style="display:inline-block"[^>]*>'
            if not re.search(div_pattern, content):
                issues.append(f"Missing proper div structure with class='item' and style='display:inline-block'")
            
        except Exception as e:
            issues.append(f"Error reading file: {str(e)}")
        
        return issues

    def check_json_html_correspondence(self):
        """Check that all questions with images have corresponding HTML files"""
        json_files = glob.glob("Gr6_*_E*_variations.json")
        missing_html = []
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract week and exercise from filename
                match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', json_file)
                if not match:
                    continue
                
                week, exercise = match.groups()
                
                for q_num, variation in enumerate(data, 1):
                    # Check if variation has image fields
                    has_images = any(field in variation for field in 
                                   ['image_tag', 'image_choice_tags', 'shape_image_tags', 'solution_image_tag'])
                    
                    if has_images:
                        # Check for corresponding HTML files
                        for var_num in range(1, 52):  # 51 variations
                            html_file = f"HTML/Gr6_{week}_E{exercise}_{q_num}_{var_num}.html"
                            if not os.path.exists(html_file):
                                missing_html.append(html_file)
                                
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
        
        self.compliance_summary['missing_html_files'] = len(missing_html)
        return missing_html

    def run_comprehensive_verification(self):
        """Run all verification checks"""
        print("=== COMPREHENSIVE GRADE 6 FILES VERIFICATION ===\n")
        
        # Check JSON files
        print("1. Verifying JSON files...")
        json_files = glob.glob("Gr6_*_E*_variations.json")
        self.compliance_summary['json_files_total'] = len(json_files)
        compliant_json = 0
        
        for json_file in json_files:
            issues = self.verify_json_file(json_file)
            if issues:
                self.json_issues.append({
                    'file': os.path.basename(json_file),
                    'issues': issues
                })
            else:
                compliant_json += 1
            self.json_files_checked += 1
        
        self.compliance_summary['json_files_compliant'] = compliant_json
        
        # Check HTML files
        print("2. Verifying HTML files...")
        self.verify_html_files()
        
        # Check JSON-HTML correspondence
        print("3. Checking JSON-HTML correspondence...")
        missing_html = self.check_json_html_correspondence()
        
        # Generate report
        self.generate_final_report(missing_html)

    def generate_final_report(self, missing_html):
        """Generate comprehensive final report"""
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE GRADE 6 FILES VERIFICATION REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary Statistics
        report.append("SUMMARY STATISTICS:")
        report.append("-" * 40)
        report.append(f"Total JSON files found: {self.compliance_summary['json_files_total']}")
        report.append(f"JSON files compliant: {self.compliance_summary['json_files_compliant']}")
        report.append(f"JSON files with issues: {len(self.json_issues)}")
        report.append(f"Total HTML files found: {self.compliance_summary['html_files_total']}")
        report.append(f"HTML files compliant: {self.compliance_summary['html_files_compliant']}")
        report.append(f"HTML files with issues: {len(self.html_issues)}")
        report.append(f"Missing HTML files: {self.compliance_summary['missing_html_files']}")
        report.append("")
        
        # Overall Compliance
        json_compliance = (self.compliance_summary['json_files_compliant'] / 
                          max(1, self.compliance_summary['json_files_total'])) * 100
        html_compliance = (self.compliance_summary['html_files_compliant'] / 
                          max(1, self.compliance_summary['html_files_total'])) * 100
        
        report.append("OVERALL COMPLIANCE:")
        report.append("-" * 40)
        report.append(f"JSON Files Compliance: {json_compliance:.1f}%")
        report.append(f"HTML Files Compliance: {html_compliance:.1f}%")
        report.append("")
        
        # JSON Issues
        if self.json_issues:
            report.append("JSON FILES WITH ISSUES:")
            report.append("-" * 40)
            for item in self.json_issues[:10]:  # Show first 10
                report.append(f"\nFile: {item['file']}")
                for issue in item['issues'][:5]:  # Show first 5 issues per file
                    report.append(f"  - {issue}")
                if len(item['issues']) > 5:
                    report.append(f"  ... and {len(item['issues']) - 5} more issues")
            
            if len(self.json_issues) > 10:
                report.append(f"\n... and {len(self.json_issues) - 10} more files with issues")
            report.append("")
        
        # HTML Issues
        if self.html_issues:
            report.append("HTML FILES WITH ISSUES:")
            report.append("-" * 40)
            for item in self.html_issues[:10]:  # Show first 10
                report.append(f"\nFile: {item['file']}")
                for issue in item['issues']:
                    report.append(f"  - {issue}")
            
            if len(self.html_issues) > 10:
                report.append(f"\n... and {len(self.html_issues) - 10} more files with issues")
            report.append("")
        
        # Missing HTML Files
        if missing_html:
            report.append("MISSING HTML FILES:")
            report.append("-" * 40)
            for html_file in missing_html[:20]:  # Show first 20
                report.append(f"  - {html_file}")
            
            if len(missing_html) > 20:
                report.append(f"  ... and {len(missing_html) - 20} more missing files")
            report.append("")
        
        # Final Assessment
        report.append("FINAL ASSESSMENT:")
        report.append("-" * 40)
        
        if (len(self.json_issues) == 0 and len(self.html_issues) == 0 and 
            len(missing_html) == 0 and self.compliance_summary['json_files_total'] >= 168):
            report.append("✅ ALL GRADE 6 FILES MEET SPECIFICATIONS")
            report.append("✅ All 168 JSON files are compliant")
            report.append("✅ All HTML files have proper structure")
            report.append("✅ All visual components have corresponding HTML files")
        else:
            report.append("❌ ISSUES FOUND - COMPLIANCE NOT MET")
            if len(self.json_issues) > 0:
                report.append(f"❌ {len(self.json_issues)} JSON files have formatting issues")
            if len(self.html_issues) > 0:
                report.append(f"❌ {len(self.html_issues)} HTML files have structure issues")
            if len(missing_html) > 0:
                report.append(f"❌ {len(missing_html)} HTML files are missing")
            if self.compliance_summary['json_files_total'] < 168:
                report.append(f"❌ Expected 168 JSON files, found {self.compliance_summary['json_files_total']}")
        
        report.append("")
        report.append("=" * 80)
        
        # Write report to file
        with open('COMPREHENSIVE_GRADE6_FINAL_VERIFICATION_REPORT.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        # Print summary
        for line in report:
            print(line)

if __name__ == "__main__":
    verifier = Grade6Verifier()
    verifier.run_comprehensive_verification()