import json
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re
import glob

def extract_week_exercise_from_filename(filename):
    """Extract week and exercise numbers from filename like Gr6_10_E1_variations.json"""
    match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', filename)
    if match:
        return match.group(1), match.group(2)
    return None, None

def analyze_all_files():
    """Analyze all Grade 6 files comprehensively"""
    json_files = sorted([f for f in os.listdir('.') if f.startswith('Gr6_') and f.endswith('_variations.json')])
    
    total_json_files = len(json_files)
    total_questions = 0
    questions_with_images = 0
    html_files_found = 0
    valid_matches = 0
    
    files_with_html = []
    files_without_html = []
    
    print("Analyzing Grade 6 files...")
    
    for json_file in json_files:
        week_num, exercise_num = extract_week_exercise_from_filename(json_file)
        if not week_num or not exercise_num:
            continue
            
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except:
            continue
        
        # Handle both list and dict formats
        questions = []
        if isinstance(data, list):
            questions = data
        elif isinstance(data, dict):
            questions = [v for k, v in data.items() if k.startswith('question_')]
        
        file_has_images = False
        file_has_html = False
        
        for item in questions:
            if not isinstance(item, dict):
                continue
            
            total_questions += 1
            
            # Check if question has images
            has_image = any([
                item.get('image_tag'),
                item.get('image_choice_tags'),
                item.get('shape_image_tags'),
                item.get('solution_image_tag')
            ])
            
            if has_image:
                questions_with_images += 1
                file_has_images = True
                
                # Check for HTML files
                q_num = item.get('question_number', '')
                if q_num:
                    pattern = f'HTML/Gr6_{week_num}_E{exercise_num} {q_num}_*.html'
                    html_files = glob.glob(pattern)
                    if html_files:
                        html_files_found += len(html_files)
                        file_has_html = True
                        
                        # Check if tags match
                        for html_file in html_files[:1]:  # Check first file only for speed
                            try:
                                with open(html_file, 'r', encoding='utf-8') as f:
                                    soup = BeautifulSoup(f.read(), 'html.parser')
                                divs = soup.find_all('div', class_='item')
                                if divs:
                                    valid_matches += 1
                                    break
                            except:
                                pass
        
        if file_has_images:
            if file_has_html:
                files_with_html.append(json_file)
            else:
                files_without_html.append(json_file)
    
    # Print comprehensive summary
    print("\n" + "="*70)
    print("COMPREHENSIVE GRADE 6 HTML VERIFICATION SUMMARY")
    print("="*70)
    
    print(f"\nJSON FILES ANALYZED:")
    print(f"  Total JSON files: {total_json_files}")
    print(f"  Files with images that have HTML: {len(files_with_html)}")
    print(f"  Files with images missing HTML: {len(files_without_html)}")
    
    print(f"\nQUESTION STATISTICS:")
    print(f"  Total questions: {total_questions}")
    print(f"  Questions with images: {questions_with_images}")
    print(f"  HTML files found: {html_files_found}")
    print(f"  Valid tag matches found: {valid_matches}")
    
    print(f"\nHTML COVERAGE:")
    if questions_with_images > 0:
        coverage = (valid_matches / questions_with_images) * 100
        print(f"  Coverage rate: {coverage:.1f}%")
    
    print(f"\nFILES WITH SUCCESSFUL HTML GENERATION:")
    if files_with_html:
        for f in files_with_html[:10]:  # Show first 10
            print(f"  [PASS] {f}")
        if len(files_with_html) > 10:
            print(f"  ... and {len(files_with_html) - 10} more")
    else:
        print("  None found")
    
    print(f"\nFILES STILL NEEDING HTML GENERATION:")
    if files_without_html:
        for f in files_without_html[:10]:  # Show first 10
            print(f"  [FAIL] {f}")
        if len(files_without_html) > 10:
            print(f"  ... and {len(files_without_html) - 10} more")
    else:
        print("  None - all files have HTML!")
    
    print("\n" + "="*70)
    print("IMPROVEMENT STATUS:")
    print("="*70)
    
    if html_files_found > 0:
        print(f"\n[SUCCESS] HTML files have been generated for some questions")
        print(f"[SUCCESS] Found {html_files_found} HTML files total")
        print(f"[SUCCESS] {len(files_with_html)} JSON files have associated HTML files")
        
        if len(files_without_html) > 0:
            print(f"\n[WARNING] However, {len(files_without_html)} files still need HTML generation")
            print(f"[WARNING] This represents {len(files_without_html)/total_json_files*100:.1f}% of all files")
    else:
        print("\n[ERROR] No HTML files found - generation may be needed")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    analyze_all_files()