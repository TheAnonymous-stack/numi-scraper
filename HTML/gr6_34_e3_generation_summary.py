# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime

def verify_html_generation():
    """Verify that all HTML files were generated correctly"""
    
    # Load JSON to count expected files
    with open('Gr6_34_E3_variations.json', 'r') as f:
        data = json.load(f)
    
    html_dir = "HTML"
    total_questions = len(data)
    
    # Count files that should exist
    expected_main_files = total_questions  # One main file per question
    expected_component_files = total_questions  # One component file per question
    expected_solution_files = total_questions * 4  # 4 solution steps per question
    expected_total = expected_main_files + expected_component_files + expected_solution_files
    
    print("="*60)
    print("GR6_34_E3 HTML GENERATION VERIFICATION REPORT")
    print("="*60)
    print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check main question files
    main_files_found = 0
    component_files_found = 0
    solution_files_found = 0
    files_with_actual_content = 0
    files_with_svg_graphs = 0
    files_with_data_tables = 0
    
    for question in data:
        question_number = question['question_number']
        
        # Check main HTML files
        main_file = f"Gr6_34_E3 3_{question_number}.html"
        main_path = os.path.join(html_dir, main_file)
        if os.path.exists(main_path):
            main_files_found += 1
            
            # Check content
            with open(main_path, 'r') as f:
                content = f.read()
                if '<svg' in content:
                    files_with_svg_graphs += 1
                if '<table' in content:
                    files_with_data_tables += 1
                if 'Mathematical Visual Element' not in content:  # Not a placeholder
                    files_with_actual_content += 1
        
        # Check component files
        component_file = f"Gr6_34_E3_3_{question_number}.html"
        component_path = os.path.join(html_dir, component_file)
        if os.path.exists(component_path):
            component_files_found += 1
        
        # Check solution step files
        if 'solution_image_tag' in question:
            for step in question['solution_image_tag']:
                step_tag = step[1]
                step_file = f"{step_tag}.html"
                step_path = os.path.join(html_dir, step_file)
                if os.path.exists(step_path):
                    solution_files_found += 1
    
    print("FILE COUNTS:")
    print(f"  Questions in JSON: {total_questions}")
    print(f"  Expected total HTML files: {expected_total}")
    print()
    print(f"  Main question files found: {main_files_found}/{expected_main_files}")
    print(f"  Component files found: {component_files_found}/{expected_component_files}")
    print(f"  Solution step files found: {solution_files_found}/{expected_solution_files}")
    print(f"  Total files found: {main_files_found + component_files_found + solution_files_found}")
    print()
    
    print("CONTENT QUALITY:")
    print(f"  Files with actual visual content: {files_with_actual_content}/{main_files_found}")
    print(f"  Files with SVG coordinate graphs: {files_with_svg_graphs}/{main_files_found}")
    print(f"  Files with HTML data tables: {files_with_data_tables}/{main_files_found}")
    print()
    
    # Success rates
    main_success = (main_files_found / expected_main_files * 100) if expected_main_files > 0 else 0
    component_success = (component_files_found / expected_component_files * 100) if expected_component_files > 0 else 0
    solution_success = (solution_files_found / expected_solution_files * 100) if expected_solution_files > 0 else 0
    content_quality = (files_with_actual_content / main_files_found * 100) if main_files_found > 0 else 0
    
    print("SUCCESS RATES:")
    print(f"  Main files: {main_success:.1f}%")
    print(f"  Component files: {component_success:.1f}%")
    print(f"  Solution files: {solution_success:.1f}%")
    print(f"  Content quality: {content_quality:.1f}%")
    print()
    
    # Sample file paths for verification
    print("SAMPLE GENERATED FILES:")
    sample_files = [
        "Gr6_34_E3 3_2.html",
        "Gr6_34_E3_3_2.html", 
        "Gr6_34_3_2_step_1.html",
        "Gr6_34_3_2_step_2.html",
        "Gr6_34_3_2_step_3.html",
        "Gr6_34_3_2_step_4.html"
    ]
    
    for file in sample_files:
        path = os.path.join(html_dir, file)
        exists = "FOUND" if os.path.exists(path) else "MISSING"
        print(f"  {exists}: {file}")
    
    print()
    print("="*60)
    if main_success >= 95 and solution_success >= 95 and content_quality >= 90:
        print("STATUS: GENERATION SUCCESSFUL!")
        print("All HTML files generated with proper visual components.")
    else:
        print("STATUS: GENERATION INCOMPLETE")
        print("Some files may be missing or contain placeholder content.")
    print("="*60)

if __name__ == "__main__":
    verify_html_generation()