#!/usr/bin/env python3
"""
Script to check variation counts in all Grade 6 variation files.
"""
import json
import glob
import os
from collections import defaultdict

def count_variations_in_file(file_path):
    """Count the number of variations in a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            return len(data)
        elif isinstance(data, dict) and 'variations' in data:
            return len(data['variations'])
        else:
            return 0
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return -1

def main():
    # Find all Grade 6 variation files
    pattern = "Gr6_*_E*_variations.json"
    files = glob.glob(pattern)
    files.sort()
    
    print("Grade 6 Variation File Analysis")
    print("=" * 50)
    
    files_needing_variations = []
    total_files = 0
    files_with_51 = 0
    
    for file_path in files:
        count = count_variations_in_file(file_path)
        total_files += 1
        
        if count == 51:
            status = "COMPLETE"
            files_with_51 += 1
        elif count > 51:
            status = f"EXCESS ({count-51} extra)"
        elif count > 0:
            status = f"MISSING ({51-count} needed)"
            files_needing_variations.append((file_path, count, 51-count))
        elif count == 0:
            status = "EMPTY FILE"
            files_needing_variations.append((file_path, count, 51))
        else:
            status = "ERROR READING"
            files_needing_variations.append((file_path, count, 51))
        
        print(f"{os.path.basename(file_path):<30} Count: {count:>3} {status}")
    
    print("\n" + "=" * 50)
    print(f"SUMMARY:")
    print(f"Total files: {total_files}")
    print(f"Files with 51 variations: {files_with_51}")
    print(f"Files needing variations: {len(files_needing_variations)}")
    
    if files_needing_variations:
        print(f"\nFiles that need additional variations:")
        for file_path, current, needed in files_needing_variations:
            print(f"  {os.path.basename(file_path)}: {current} → needs {needed} more")
    
    return files_needing_variations

if __name__ == "__main__":
    files_needing_variations = main()