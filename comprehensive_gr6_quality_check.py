#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path

def count_underscores(text):
    """Count underscore placeholders in text"""
    return len(re.findall(r'_+', text))

def analyze_variation_file(file_path):
    """Analyze a single variation file for quality issues"""
    issues = []
    file_name = os.path.basename(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {
            'file': file_name,
            'status': 'ERROR',
            'variation_count': 0,
            'issues': [f"Failed to parse JSON: {str(e)}"],
            'critical_issues': 1,
            'major_issues': 0,
            'minor_issues': 0
        }
    
    # Check if data is a list of variations
    if not isinstance(data, list):
        issues.append("File structure invalid - should contain a list of variations")
        return {
            'file': file_name,
            'status': 'FAIL',
            'variation_count': 0,
            'issues': issues,
            'critical_issues': 1,
            'major_issues': 0,
            'minor_issues': 0
        }
    
    variation_count = len(data)
    critical_issues = 0
    major_issues = 0
    minor_issues = 0
    
    # Check variation count
    if variation_count != 51:
        issues.append(f"Expected 51 variations, found {variation_count}")
        if variation_count < 45:
            critical_issues += 1
        else:
            major_issues += 1
    
    # Analyze each variation
    correct_answer_positions = []
    tags_found = set()
    
    for i, variation in enumerate(data):
        variation_num = i + 1
        
        # Check required fields
        required_fields = ['question_text', 'correct_answers', 'tag']
        for field in required_fields:
            if field not in variation:
                issues.append(f"Variation {variation_num}: Missing required field '{field}'")
                critical_issues += 1
                continue
        
        # Collect tags for consistency check
        if 'tag' in variation:
            tags_found.add(variation['tag'])
        
        # Check multiple fill-in-the-blank questions
        question_text = variation.get('question_text', '')
        underscore_count = count_underscores(question_text)
        correct_answers = variation.get('correct_answers', [])
        
        if underscore_count > 1:
            # Multiple fill-in-the-blank
            if len(correct_answers) != underscore_count:
                issues.append(f"Variation {variation_num}: {underscore_count} blanks but {len(correct_answers)} answers")
                major_issues += 1
            
            if 'orderMatter' not in variation:
                issues.append(f"Variation {variation_num}: Multiple blanks missing 'orderMatter' field")
                major_issues += 1
            elif not isinstance(variation['orderMatter'], bool):
                issues.append(f"Variation {variation_num}: 'orderMatter' should be boolean")
                minor_issues += 1
        
        # Check multiple acceptable answers
        if 'has_alternate_answers' in variation:
            if variation['has_alternate_answers'] is True:
                if not all(isinstance(ans, list) for ans in correct_answers):
                    issues.append(f"Variation {variation_num}: has_alternate_answers=True but answers not in nested arrays")
                    major_issues += 1
        
        # Check multiple choice questions
        if 'options' in variation:
            options = variation['options']
            if len(options) < 2:
                issues.append(f"Variation {variation_num}: Multiple choice needs at least 2 options")
                major_issues += 1
            
            # Check if correct_answers contain option letters
            if correct_answers:
                first_answer = correct_answers[0]
                if isinstance(first_answer, list) and first_answer:
                    first_answer = first_answer[0]
                
                if first_answer not in ['A', 'B', 'C', 'D', 'E', 'F']:
                    # Check if it's the literal text instead of letter
                    if first_answer in options:
                        issues.append(f"Variation {variation_num}: correct_answers should contain option letters (A,B,C) not literal text")
                        major_issues += 1
                
                # Track correct answer position for variety check
                try:
                    if first_answer in ['A', 'B', 'C', 'D', 'E', 'F']:
                        correct_answer_positions.append(ord(first_answer) - ord('A'))
                except:
                    pass
    
    # Check tag consistency
    if len(tags_found) > 1:
        issues.append(f"Inconsistent tags found: {', '.join(tags_found)}")
        critical_issues += 1
    
    # Check correct answer position variety for multiple choice
    if correct_answer_positions:
        unique_positions = len(set(correct_answer_positions))
        total_mc_questions = len(correct_answer_positions)
        
        if unique_positions < 2:
            issues.append(f"All {total_mc_questions} multiple choice questions have correct answer in same position")
            major_issues += 1
        elif unique_positions < max(2, total_mc_questions // 10):
            issues.append(f"Limited variety in correct answer positions: {unique_positions} unique positions in {total_mc_questions} questions")
            minor_issues += 1
    
    # Determine status
    if critical_issues > 0:
        status = 'FAIL'
    elif major_issues > 5:
        status = 'NEEDS REVISION'
    elif major_issues > 0 or minor_issues > 10:
        status = 'NEEDS REVISION'
    else:
        status = 'PASS'
    
    return {
        'file': file_name,
        'status': status,
        'variation_count': variation_count,
        'issues': issues,
        'critical_issues': critical_issues,
        'major_issues': major_issues,
        'minor_issues': minor_issues,
        'tags': list(tags_found)
    }

def main():
    """Main function to analyze all Grade 6 variation files"""
    
    # Find all Grade 6 variation files
    gr6_files = list(Path('.').glob('Gr6_*_E*_variations.json'))
    gr6_files.sort()
    
    print("=" * 80)
    print("COMPREHENSIVE GRADE 6 MATH VARIATIONS QUALITY CHECK REPORT")
    print("=" * 80)
    print(f"Total files found: {len(gr6_files)}")
    print()
    
    results = []
    overall_stats = {
        'total_files': len(gr6_files),
        'pass_count': 0,
        'needs_revision_count': 0,
        'fail_count': 0,
        'total_variations': 0,
        'files_with_correct_count': 0,
        'total_critical_issues': 0,
        'total_major_issues': 0,
        'total_minor_issues': 0
    }
    
    # Analyze each file
    for file_path in gr6_files:
        result = analyze_variation_file(file_path)
        results.append(result)
        
        # Update overall stats
        overall_stats['total_variations'] += result['variation_count']
        overall_stats['total_critical_issues'] += result['critical_issues']
        overall_stats['total_major_issues'] += result['major_issues']
        overall_stats['total_minor_issues'] += result['minor_issues']
        
        if result['variation_count'] == 51:
            overall_stats['files_with_correct_count'] += 1
        
        if result['status'] == 'PASS':
            overall_stats['pass_count'] += 1
        elif result['status'] == 'NEEDS REVISION':
            overall_stats['needs_revision_count'] += 1
        else:
            overall_stats['fail_count'] += 1
    
    # Print detailed results
    print("DETAILED ANALYSIS BY STATUS")
    print("-" * 40)
    
    # Group by status
    for status in ['FAIL', 'NEEDS REVISION', 'PASS']:
        status_files = [r for r in results if r['status'] == status]
        if status_files:
            print(f"\n{status} ({len(status_files)} files):")
            print("-" * 30)
            for result in status_files:
                print(f"\n{result['file']} ({result['variation_count']} variations)")
                if result['issues']:
                    for issue in result['issues'][:10]:  # Limit to first 10 issues per file
                        print(f"  - {issue}")
                    if len(result['issues']) > 10:
                        print(f"  - ... and {len(result['issues']) - 10} more issues")
                if result['tags']:
                    print(f"  Tags: {', '.join(result['tags'])}")
    
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total files analyzed: {overall_stats['total_files']}")
    print(f"Total variations: {overall_stats['total_variations']}")
    print(f"Files with correct variation count (51): {overall_stats['files_with_correct_count']}")
    print()
    print("STATUS DISTRIBUTION:")
    print(f"  PASS: {overall_stats['pass_count']} ({overall_stats['pass_count']/overall_stats['total_files']*100:.1f}%)")
    print(f"  NEEDS REVISION: {overall_stats['needs_revision_count']} ({overall_stats['needs_revision_count']/overall_stats['total_files']*100:.1f}%)")
    print(f"  FAIL: {overall_stats['fail_count']} ({overall_stats['fail_count']/overall_stats['total_files']*100:.1f}%)")
    print()
    print("ISSUE DISTRIBUTION:")
    print(f"  Critical issues: {overall_stats['total_critical_issues']}")
    print(f"  Major issues: {overall_stats['total_major_issues']}")
    print(f"  Minor issues: {overall_stats['total_minor_issues']}")
    print(f"  Total issues: {overall_stats['total_critical_issues'] + overall_stats['total_major_issues'] + overall_stats['total_minor_issues']}")
    
    # Files needing immediate attention
    critical_files = [r for r in results if r['critical_issues'] > 0]
    if critical_files:
        print(f"\nFILES REQUIRING IMMEDIATE ATTENTION ({len(critical_files)} files):")
        print("-" * 50)
        for result in critical_files:
            print(f"  {result['file']} - {result['critical_issues']} critical, {result['major_issues']} major issues")
    
    # Variation count issues
    wrong_count_files = [r for r in results if r['variation_count'] != 51]
    if wrong_count_files:
        print(f"\nFILES WITH INCORRECT VARIATION COUNT ({len(wrong_count_files)} files):")
        print("-" * 55)
        for result in wrong_count_files:
            print(f"  {result['file']}: {result['variation_count']} variations (expected 51)")
    
    print("\n" + "=" * 80)
    
    # Return results for further processing if needed
    return results, overall_stats

if __name__ == "__main__":
    main()