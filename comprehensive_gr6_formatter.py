#!/usr/bin/env python3
"""
Comprehensive Grade 6 JSON Formatter
Fixes critical formatting issues in all Grade 6 variation files.
"""

import json
import os
import re
from pathlib import Path

def count_underscores(text):
    """Count underscores in question text"""
    if not isinstance(text, str):
        return 0
    return text.count('_')

def fix_order_matter_boolean(data):
    """Convert orderMatter string values to boolean"""
    if 'orderMatter' in data:
        if isinstance(data['orderMatter'], str):
            if data['orderMatter'].upper() == 'TRUE':
                data['orderMatter'] = True
            elif data['orderMatter'].upper() == 'FALSE':
                data['orderMatter'] = False
    return data

def fix_tag_consistency(variations):
    """Fix tag consistency - all variations should share the same base tag"""
    if not variations:
        return variations
    
    # Extract base tag from filename or first variation
    first_tag = variations[0].get('tag', '')
    if '_V' in first_tag:
        base_tag = first_tag.split('_V')[0]
    else:
        base_tag = first_tag
    
    # Apply base tag to all variations
    for variation in variations:
        variation['tag'] = base_tag
    
    return variations

def fix_multiple_choice_format(data):
    """Ensure multiple choice answers store option letters, not literal text"""
    if data.get('type') == 'Multiple Choice Question with Single Answer':
        choices = data.get('choices', [])
        correct_answers = data.get('correct_answers', [])
        
        if choices and correct_answers:
            # Check if correct_answers contains literal text instead of letters
            for i, answer in enumerate(correct_answers):
                if answer in choices:
                    # Find the index and convert to letter
                    choice_index = choices.index(answer)
                    correct_answers[i] = chr(65 + choice_index)  # A, B, C, etc.
    
    return data

def fix_fill_blank_consistency(data):
    """Fix fill-in-the-blank questions to have consistent underscores and answers"""
    if data.get('type') == 'Multiple fill in the blank':
        question_text = data.get('question_text', '')
        correct_answers = data.get('correct_answers', [])
        
        underscore_count = count_underscores(question_text)
        answer_count = len(correct_answers)
        
        if underscore_count != answer_count and answer_count > 0:
            # Adjust underscores to match answer count
            if underscore_count < answer_count:
                # Add more underscores
                missing_underscores = answer_count - underscore_count
                question_text += ' ' + '_ ' * missing_underscores
                data['question_text'] = question_text.strip()
            elif underscore_count > answer_count:
                # This is trickier - we'd need to remove underscores carefully
                # For now, just log this issue
                print(f"Warning: More underscores ({underscore_count}) than answers ({answer_count}) in question")
        
        # Ensure orderMatter is boolean
        data = fix_order_matter_boolean(data)
    
    return data

def process_variation_file(file_path):
    """Process a single variation file"""
    try:
        print(f"Processing: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"Error: {file_path} doesn't contain a list of variations")
            return False
        
        # Fix tag consistency first
        data = fix_tag_consistency(data)
        
        # Process each variation
        for variation in data:
            # Fix multiple choice format
            variation = fix_multiple_choice_format(variation)
            
            # Fix fill-in-the-blank consistency
            variation = fix_fill_blank_consistency(variation)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Fixed: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def main():
    """Main function to process all Grade 6 variation files"""
    current_dir = Path('.')
    gr6_files = list(current_dir.glob('Gr6_*_E*_variations.json'))
    
    print(f"Found {len(gr6_files)} Grade 6 variation files")
    
    success_count = 0
    failure_count = 0
    
    for file_path in sorted(gr6_files):
        if process_variation_file(file_path):
            success_count += 1
        else:
            failure_count += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {failure_count} files")
    print(f"Total files: {len(gr6_files)} files")
    
    if failure_count == 0:
        print("\nAll Grade 6 variation files have been successfully formatted!")
    else:
        print(f"\n{failure_count} files need manual review")

if __name__ == "__main__":
    main()