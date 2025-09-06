import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import glob

class ComprehensiveHTMLFixer:
    def __init__(self):
        self.html_dir = Path("HTML")
        self.html_dir.mkdir(exist_ok=True)
        self.issues_fixed = {
            'labels_fixed': 0,
            'files_created': 0,
            'divs_added': 0,
            'total_questions_fixed': 0
        }
        self.detailed_log = []
        
    def log(self, message: str):
        """Log a message for the report"""
        # Handle Unicode characters for Windows console
        try:
            print(message)
        except UnicodeEncodeError:
            # Replace Unicode checkmarks and crosses with ASCII alternatives
            message_safe = message.replace('✓', '[OK]').replace('✗', '[FAIL]').replace('⚠️', '[WARN]')
            print(message_safe)
        self.detailed_log.append(message)
        
    def get_all_json_files(self) -> List[Path]:
        """Get all Grade 6 variation JSON files"""
        json_files = glob.glob("Gr6_*_variations.json")
        return sorted([Path(f) for f in json_files])
        
    def load_json_file(self, file_path: Path) -> Optional[List[Dict]]:
        """Load and parse a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'questions' in data:
                    return data['questions']
                elif isinstance(data, list):
                    return data
                return None
        except Exception as e:
            self.log(f"Error loading {file_path}: {e}")
            return None
            
    def extract_visual_info(self, question: Dict) -> Dict[str, Any]:
        """Extract all visual information from a question"""
        visual_info = {
            'has_visuals': False,
            'image_tag': None,
            'image_choice_tags': [],
            'solution_image_tag': None,
            'shape_image_tags': [],
            'backend_description': None,
            'backend_descriptions': {},
            'solution_backend_description': None
        }
        
        # Check for main image tag
        if 'image_tag' in question and question['image_tag'] and question['image_tag'].strip():
            visual_info['has_visuals'] = True
            visual_info['image_tag'] = question['image_tag']
            visual_info['backend_description'] = question.get('backend_description', '')
            
        # Check for image choice tags
        if 'image_choice_tags' in question and question['image_choice_tags']:
            visual_info['has_visuals'] = True
            visual_info['image_choice_tags'] = question['image_choice_tags']
            # Get backend descriptions for each choice
            if 'backend_descriptions' in question:
                visual_info['backend_descriptions'] = question['backend_descriptions']
                
        # Check for solution image tag
        if 'solution_image_tag' in question and question['solution_image_tag']:
            visual_info['has_visuals'] = True
            visual_info['solution_image_tag'] = question['solution_image_tag']
            visual_info['solution_backend_description'] = question.get('solution_backend_description', '')
            
        # Check for shape image tags
        if 'shape_image_tags' in question and question['shape_image_tags']:
            visual_info['has_visuals'] = True
            visual_info['shape_image_tags'] = question['shape_image_tags']
            
        return visual_info
        
    def get_html_filename(self, json_filename: str, question_id: str) -> Path:
        """Generate the correct HTML filename"""
        # Extract week and exercise from filename
        match = re.match(r'Gr6_(\d+)_E(\d+)_variations\.json', json_filename)
        if match:
            week = match.group(1)
            exercise = match.group(2)
            # Use space separator as per the expected format
            return self.html_dir / f"Gr6_{week}_E{exercise} {question_id}.html"
        return None
        
    def create_visual_html(self, visual_info: Dict, json_filename: str, question_id: str) -> str:
        """Create HTML content for visual components"""
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="en">')
        html_parts.append('<head>')
        html_parts.append('    <meta charset="UTF-8">')
        html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'    <title>{json_filename.replace(".json", "")} - Question {question_id}</title>')
        html_parts.append('    <style>')
        html_parts.append('        body { font-family: Arial, sans-serif; padding: 20px; }')
        html_parts.append('        .item { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }')
        html_parts.append('        .label { font-weight: bold; color: #333; margin-bottom: 10px; }')
        html_parts.append('        .description { color: #666; line-height: 1.6; }')
        html_parts.append('        .visual-container { background: #f9f9f9; padding: 20px; border-radius: 8px; }')
        html_parts.append('        .choice-container { display: flex; flex-wrap: wrap; gap: 20px; }')
        html_parts.append('        .choice-item { flex: 1; min-width: 200px; }')
        html_parts.append('    </style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('    <div class="visual-container">')
        html_parts.append(f'        <h2>Visual Components for Question {question_id}</h2>')
        
        # Add main image tag if present
        if visual_info['image_tag']:
            html_parts.append(f'        <div class="item" label="{visual_info["image_tag"]}">')
            html_parts.append(f'            <div class="label">Image: {visual_info["image_tag"]}</div>')
            if visual_info['backend_description']:
                html_parts.append(f'            <div class="description">{visual_info["backend_description"]}</div>')
            else:
                html_parts.append('            <div class="description">[Visual component to be implemented]</div>')
            html_parts.append('        </div>')
            
        # Add image choice tags if present
        if visual_info['image_choice_tags']:
            html_parts.append('        <div class="choice-container">')
            for i, tag in enumerate(visual_info['image_choice_tags']):
                html_parts.append(f'            <div class="item choice-item" label="{tag}">')
                html_parts.append(f'                <div class="label">Choice {chr(65+i)}: {tag}</div>')
                # Check if we have backend description for this choice
                if visual_info['backend_descriptions'] and str(i) in visual_info['backend_descriptions']:
                    desc = visual_info['backend_descriptions'][str(i)]
                    html_parts.append(f'                <div class="description">{desc}</div>')
                else:
                    html_parts.append(f'                <div class="description">[Choice {chr(65+i)} visual]</div>')
                html_parts.append('            </div>')
            html_parts.append('        </div>')
            
        # Add solution image tag if present
        if visual_info['solution_image_tag']:
            html_parts.append(f'        <div class="item" label="{visual_info["solution_image_tag"]}">')
            html_parts.append(f'            <div class="label">Solution: {visual_info["solution_image_tag"]}</div>')
            if visual_info['solution_backend_description']:
                html_parts.append(f'            <div class="description">{visual_info["solution_backend_description"]}</div>')
            else:
                html_parts.append('            <div class="description">[Solution visual component]</div>')
            html_parts.append('        </div>')
            
        # Add shape image tags if present
        if visual_info['shape_image_tags']:
            for tag in visual_info['shape_image_tags']:
                html_parts.append(f'        <div class="item" label="{tag}">')
                html_parts.append(f'            <div class="label">Shape: {tag}</div>')
                html_parts.append('            <div class="description">[Shape visual component]</div>')
                html_parts.append('        </div>')
                
        html_parts.append('    </div>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)
        
    def fix_existing_html(self, html_path: Path, visual_info: Dict) -> bool:
        """Fix labels and add missing divs in existing HTML"""
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            fixes_made = False
            
            # Fix label mismatches
            if visual_info['image_tag']:
                # Look for incorrect label patterns and fix them
                wrong_patterns = [
                    r'label="Gr6_\d+_\d+_\d+"',  # Format like Gr6_15_5_2
                    r'label="Gr6_\d+_E\d+_\d+"',  # Format like Gr6_15_E5_2
                ]
                
                for pattern in wrong_patterns:
                    if re.search(pattern, content):
                        # Replace with correct label
                        content = re.sub(pattern, f'label="{visual_info["image_tag"]}"', content, count=1)
                        fixes_made = True
                        self.issues_fixed['labels_fixed'] += 1
                        
                # Check if the div exists at all
                if f'label="{visual_info["image_tag"]}"' not in content:
                    # Need to add the div
                    # Find the visual-container or body tag to insert into
                    if '<div class="visual-container">' in content:
                        insert_pos = content.find('</div>\n</body>')
                        if insert_pos == -1:
                            insert_pos = content.find('</body>')
                            
                        new_div = f'''        <div class="item" label="{visual_info['image_tag']}">
            <div class="label">Image: {visual_info['image_tag']}</div>
            <div class="description">{visual_info.get('backend_description', '[Visual component]')}</div>
        </div>
'''
                        content = content[:insert_pos] + new_div + content[insert_pos:]
                        fixes_made = True
                        self.issues_fixed['divs_added'] += 1
                        
            # Add missing image choice tags
            if visual_info['image_choice_tags']:
                for i, tag in enumerate(visual_info['image_choice_tags']):
                    if f'label="{tag}"' not in content:
                        # Add missing choice div
                        insert_pos = content.find('</div>\n</body>')
                        if insert_pos == -1:
                            insert_pos = content.find('</body>')
                            
                        desc = ''
                        if visual_info['backend_descriptions'] and str(i) in visual_info['backend_descriptions']:
                            desc = visual_info['backend_descriptions'][str(i)]
                        else:
                            desc = f'[Choice {chr(65+i)} visual]'
                            
                        new_div = f'''        <div class="item choice-item" label="{tag}">
            <div class="label">Choice {chr(65+i)}: {tag}</div>
            <div class="description">{desc}</div>
        </div>
'''
                        content = content[:insert_pos] + new_div + content[insert_pos:]
                        fixes_made = True
                        self.issues_fixed['divs_added'] += 1
                        
            # Add missing solution image tag
            if visual_info['solution_image_tag']:
                if f'label="{visual_info["solution_image_tag"]}"' not in content:
                    insert_pos = content.find('</div>\n</body>')
                    if insert_pos == -1:
                        insert_pos = content.find('</body>')
                        
                    new_div = f'''        <div class="item" label="{visual_info['solution_image_tag']}">
            <div class="label">Solution: {visual_info['solution_image_tag']}</div>
            <div class="description">{visual_info.get('solution_backend_description', '[Solution visual]')}</div>
        </div>
'''
                    content = content[:insert_pos] + new_div + content[insert_pos:]
                    fixes_made = True
                    self.issues_fixed['divs_added'] += 1
                    
            # Save if changes were made
            if fixes_made and content != original_content:
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
                
            return False
            
        except Exception as e:
            self.log(f"Error fixing HTML {html_path}: {e}")
            return False
            
    def process_all_files(self):
        """Process all JSON files and fix/create HTML files"""
        json_files = self.get_all_json_files()
        self.log(f"\n{'='*60}")
        self.log("COMPREHENSIVE HTML FIXER - STARTING")
        self.log(f"{'='*60}\n")
        self.log(f"Found {len(json_files)} JSON files to process\n")
        
        for json_file in json_files:
            self.log(f"\nProcessing: {json_file.name}")
            self.log("-" * 40)
            
            questions = self.load_json_file(json_file)
            if not questions:
                self.log(f"  ⚠️  Could not load questions from {json_file.name}")
                continue
                
            questions_with_visuals = 0
            questions_fixed = 0
            
            for question in questions:
                # Extract question ID from various possible fields
                question_id = question.get('tag', question.get('name_tag', question.get('question_id', 'unknown')))
                # Clean the question ID to get just the number part (e.g., "1_1" from "Gr6_15_E5_1_1")
                if '_' in question_id and question_id.startswith('Gr6'):
                    # Extract just the question number part (e.g., "1_1" from "Gr6_15_E5_1_1")
                    parts = question_id.split('_')
                    if len(parts) >= 4:
                        question_id = '_'.join(parts[3:])  # Get everything after E5 part
                        
                visual_info = self.extract_visual_info(question)
                
                if not visual_info['has_visuals']:
                    continue
                    
                questions_with_visuals += 1
                html_path = self.get_html_filename(json_file.name, question_id)
                
                if not html_path:
                    self.log(f"  ⚠️  Could not generate HTML path for {question_id}")
                    continue
                    
                # Check if HTML file exists
                if html_path.exists():
                    # Fix existing HTML
                    if self.fix_existing_html(html_path, visual_info):
                        self.log(f"  ✓ Fixed HTML for question {question_id}")
                        questions_fixed += 1
                        self.issues_fixed['total_questions_fixed'] += 1
                else:
                    # Create new HTML file
                    html_content = self.create_visual_html(visual_info, json_file.name, question_id)
                    try:
                        with open(html_path, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        self.log(f"  ✓ Created HTML for question {question_id}")
                        self.issues_fixed['files_created'] += 1
                        questions_fixed += 1
                        self.issues_fixed['total_questions_fixed'] += 1
                    except Exception as e:
                        self.log(f"  ✗ Error creating HTML for {question_id}: {e}")
                        
            self.log(f"\n  Summary for {json_file.name}:")
            self.log(f"    - Questions with visuals: {questions_with_visuals}")
            self.log(f"    - Questions fixed/created: {questions_fixed}")
            
    def generate_report(self):
        """Generate a comprehensive report of all fixes"""
        report_path = Path("HTML_FIX_REPORT.md")
        
        report_lines = [
            "# Comprehensive HTML Fix Report",
            "",
            f"## Summary of Fixes Applied",
            "",
            f"- **Labels Fixed:** {self.issues_fixed['labels_fixed']}",
            f"- **HTML Files Created:** {self.issues_fixed['files_created']}",
            f"- **Missing Divs Added:** {self.issues_fixed['divs_added']}",
            f"- **Total Questions Fixed:** {self.issues_fixed['total_questions_fixed']}",
            "",
            "## Detailed Log",
            "",
            "```"
        ]
        
        report_lines.extend(self.detailed_log)
        report_lines.append("```")
        report_lines.append("")
        report_lines.append("## Next Steps")
        report_lines.append("")
        report_lines.append("1. Run the HTML checker again to verify all fixes")
        report_lines.append("2. Review generated HTML files for visual accuracy")
        report_lines.append("3. Implement actual visual components (SVG/Canvas) where needed")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append(f"*Report generated on 2025-09-06*")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
            
        self.log(f"\n{'='*60}")
        self.log("FIX COMPLETE!")
        self.log(f"{'='*60}")
        self.log(f"\nReport saved to: {report_path}")
        
def main():
    fixer = ComprehensiveHTMLFixer()
    fixer.process_all_files()
    fixer.generate_report()
    
if __name__ == "__main__":
    main()