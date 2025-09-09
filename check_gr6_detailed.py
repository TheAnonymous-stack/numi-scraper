import json
import os
import re
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

class HTMLDivExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.divs = []
        self.current_div = None
        self.current_content = []
        self.in_item_div = False
        self.depth = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'div' and attrs_dict.get('class') == 'item':
            self.in_item_div = True
            self.depth = 1
            self.current_div = {
                'label': attrs_dict.get('label', ''),
                'content': []
            }
            self.current_content = []
        elif self.in_item_div:
            self.depth += 1 if tag == 'div' else 0
            attr_str = ' '.join([f'{k}="{v}"' for k, v in attrs])
            if attr_str:
                self.current_content.append(f'<{tag} {attr_str}>')
            else:
                self.current_content.append(f'<{tag}>')
    
    def handle_endtag(self, tag):
        if self.in_item_div:
            if tag == 'div':
                self.depth -= 1
                if self.depth == 0:
                    self.current_div['content'] = ''.join(self.current_content)
                    self.divs.append(self.current_div)
                    self.in_item_div = False
                    self.current_div = None
                    self.current_content = []
                else:
                    self.current_content.append(f'</{tag}>')
            else:
                self.current_content.append(f'</{tag}>')
    
    def handle_data(self, data):
        if self.in_item_div:
            self.current_content.append(data)

def analyze_visual_content(html_content, backend_desc):
    """Analyze if HTML visual matches backend description"""
    issues = []
    
    # Extract key elements from backend description
    backend_lower = backend_desc.lower() if backend_desc else ""
    
    # Check for common visual elements
    if 'histogram' in backend_lower and 'rect' not in html_content:
        issues.append("Backend describes histogram but HTML lacks rectangles")
    
    if 'table' in backend_lower and '<table' not in html_content:
        issues.append("Backend describes table but HTML lacks table element")
    
    if 'circle' in backend_lower and '<circle' not in html_content:
        issues.append("Backend describes circles but HTML lacks circle elements")
    
    if 'line' in backend_lower and '<line' not in html_content and '<path' not in html_content:
        issues.append("Backend describes lines but HTML lacks line/path elements")
    
    # Check for numerical values
    import re
    backend_numbers = set(re.findall(r'\b\d+\.?\d*\b', backend_desc))
    html_numbers = set(re.findall(r'\b\d+\.?\d*\b', html_content))
    
    # Some numbers from backend should appear in HTML (excluding style numbers)
    style_numbers = {'1', '2', '10', '20', '100', '200', '300', '400', '500'}
    meaningful_backend_numbers = backend_numbers - style_numbers
    meaningful_html_numbers = html_numbers - style_numbers
    
    if meaningful_backend_numbers and not meaningful_backend_numbers & meaningful_html_numbers:
        missing_numbers = list(meaningful_backend_numbers)[:5]
        issues.append(f"Backend numbers not in HTML: {', '.join(missing_numbers)}")
    
    return issues

# Analyze specific exercises
sample_exercises = ['Gr6_15_E5', 'Gr6_1_E1', 'Gr6_23_E1']

for exercise_key in sample_exercises:
    print(f"\n{'='*60}")
    print(f"DETAILED ANALYSIS: {exercise_key}")
    print('='*60)
    
    # Parse exercise info
    match = re.match(r'Gr6_(\d+)_E(\d+)', exercise_key)
    if not match:
        continue
    week, exercise = match.groups()
    
    # Load JSON
    json_file = Path(f'{exercise_key}_variations.json')
    if not json_file.exists():
        print(f"JSON file not found: {json_file}")
        continue
        
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data.get('quizzes', data.get('questions', []))
    
    # Check first few questions with images
    for q_idx, question in enumerate(questions[:3], 1):
        q_num = question.get('question_number', str(q_idx))
        if '_' in str(q_num):
            q_num = q_num.split('_')[-1]
        
        image_tag = question.get('image_tag')
        if not image_tag:
            continue
            
        print(f"\nQuestion {q_num}:")
        print(f"  Expected image_tag: {image_tag}")
        print(f"  Backend description: {question.get('backend_description', '')[:100]}...")
        
        # Check multiple possible HTML file patterns
        possible_files = [
            Path('HTML') / f"Gr6_{week}_E{exercise} {q_num}.html",
            Path('HTML') / f"Gr6_{week}_E{exercise}_{q_num}.html",
            Path('HTML') / f"Gr6_{week}_E{exercise}_1_{q_num}.html",  # New pattern found
        ]
        
        html_file = None
        for pf in possible_files:
            if pf.exists():
                html_file = pf
                break
        
        if html_file:
            print(f"  HTML file found: {html_file}")
            
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            parser = HTMLDivExtractor()
            parser.feed(html_content)
            
            print(f"  Divs found: {[div['label'] for div in parser.divs]}")
            
            # Check if expected tag exists
            html_divs = {div['label']: div['content'] for div in parser.divs}
            
            if image_tag in html_divs:
                print(f"  [OK] Tag '{image_tag}' found")
                # Analyze content match
                issues = analyze_visual_content(html_divs[image_tag], question.get('backend_description', ''))
                if issues:
                    print(f"  Content issues:")
                    for issue in issues:
                        print(f"    - {issue}")
            else:
                print(f"  [FAIL] Tag '{image_tag}' NOT found")
                print(f"  Available tags: {list(html_divs.keys())}")
        else:
            print(f"  [FAIL] HTML file not found in any of these locations:")
            for pf in possible_files:
                print(f"    - {pf}")

print("\n" + "="*60)
print("SUMMARY OF FINDINGS")
print("="*60)
print("\nKey Issues Identified:")
print("1. HTML files use pattern: Gr6_XX_EX_1_Y.html (with extra '_1')")
print("2. Div labels in HTML don't match image_tag values in JSON")
print("   - HTML has: Gr6_XX_EX_Y")
print("   - JSON expects: Gr6_XX_EX_variations_image_tag")
print("3. HTML visual content may not match backend descriptions")
print("\nRecommendations:")
print("1. Update HTML div labels to match JSON image_tag values")
print("2. Review HTML visual content against backend descriptions")
print("3. Standardize file naming convention")