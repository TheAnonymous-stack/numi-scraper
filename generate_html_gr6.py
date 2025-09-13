import json
import os
from pathlib import Path

def create_html_for_question(question_data, week, exercise):
    """Generate HTML content for a single question"""
    
    question_number = question_data.get('question_number', '')
    question_text = question_data.get('question_text', '').replace('\\n', '<br>')
    question_type = question_data.get('question_type', '')
    
    # Start HTML structure
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 - Week {week} - Exercise {exercise} - Question {question_number}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .question-header {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .question-text {{
            font-size: 18px;
            line-height: 1.6;
            color: #34495e;
            margin: 20px 0;
        }}
        .options {{
            margin: 20px 0;
        }}
        .option {{
            background-color: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .option:hover {{
            background-color: #e9ecef;
            border-color: #3498db;
        }}
        .option-label {{
            font-weight: bold;
            color: #3498db;
            margin-right: 10px;
        }}
        .fill-blank {{
            display: inline-block;
            min-width: 100px;
            border-bottom: 2px solid #3498db;
            margin: 0 5px;
            padding: 2px;
        }}
        .item {{
            margin: 20px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
            min-height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px dashed #dee2e6;
        }}
        .math {{
            font-family: 'Cambria Math', 'Times New Roman', serif;
            font-size: 1.1em;
        }}
    </style>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }}
        }};
    </script>
</head>
<body>
    <div class="container">
        <div class="question-header">
            <h1>Grade 6 - Week {week}, Exercise {exercise}</h1>
            <h2>Question {question_number}</h2>
        </div>
        <div class="question-text">
            {question_text}
        </div>
"""
    
    # Handle different question types
    if question_type == "Multiple choice":
        options = question_data.get('multiple_choice_options', [])
        if options:
            html_content += '        <div class="options">\n'
            for i, option in enumerate(options):
                label = chr(65 + i)  # A, B, C, D...
                html_content += f'            <div class="option">\n'
                html_content += f'                <span class="option-label">{label}.</span>\n'
                html_content += f'                <span>{option}</span>\n'
                html_content += f'            </div>\n'
            html_content += '        </div>\n'
    
    elif question_type == "Fill in the blank":
        # Add a visual representation of the blank
        if '_' in question_text:
            # Already has blank in the text
            pass
        else:
            html_content += '        <div style="margin-top: 20px;">\n'
            html_content += '            <span>Answer: </span><span class="fill-blank"></span>\n'
            html_content += '        </div>\n'
    
    # Handle images if present
    if 'image_tag' in question_data and question_data.get('backend_description'):
        image_tag = question_data['image_tag']
        description = question_data['backend_description']
        html_content += f'        <div class="item" label="{image_tag}">\n'
        html_content += f'            <!-- {description} -->\n'
        html_content += f'        </div>\n'
    
    # Handle solution images if present
    if 'solution_image_tag' in question_data:
        for solution_img in question_data['solution_image_tag']:
            if len(solution_img) >= 3:
                tag = solution_img[1]
                description = solution_img[2]
                html_content += f'        <div class="item" label="{tag}">\n'
                html_content += f'            <!-- {description} -->\n'
                html_content += f'        </div>\n'
    
    # Handle image choice tags if present
    if 'image_choice_tags' in question_data and 'image_choice_tags_backend_description' in question_data:
        tags = question_data['image_choice_tags']
        descriptions = question_data['image_choice_tags_backend_description']
        for i, tag in enumerate(tags):
            if i < len(descriptions):
                html_content += f'        <div class="item" label="{tag}">\n'
                html_content += f'            <!-- {descriptions[i]} -->\n'
                html_content += f'        </div>\n'
    
    # Handle shape image tags if present
    if 'shape_image_tags' in question_data:
        for shape_img in question_data['shape_image_tags']:
            if isinstance(shape_img, dict) and 'tag' in shape_img and 'backend_description' in shape_img:
                tag = shape_img['tag']
                description = shape_img['backend_description']
                html_content += f'        <div class="item" label="{tag}">\n'
                html_content += f'            <!-- {description} -->\n'
                html_content += f'        </div>\n'
    
    # Close HTML
    html_content += """    </div>
</body>
</html>"""
    
    return html_content

def process_json_file(json_path):
    """Process a single JSON file and generate HTML files for all questions"""
    
    # Extract week and exercise from filename
    filename = os.path.basename(json_path)
    parts = filename.replace('.json', '').split('_')
    week = parts[1]
    exercise = parts[2].replace('E', '')
    
    print(f"Processing {filename}...")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        quizzes = data.get('quizzes', [])
        
        for quiz in quizzes:
            question_number = quiz.get('question_number', '')
            
            # Generate HTML filename
            html_filename = f"Gr6_{week}_E{exercise}_{question_number}.html"
            html_path = os.path.join('HTML', html_filename)
            
            # Check if question has images
            has_images = False
            if 'image_tag' in quiz and quiz.get('backend_description'):
                has_images = True
            if 'solution_image_tag' in quiz and len(quiz['solution_image_tag']) > 0:
                has_images = True
            if 'image_choice_tags' in quiz and len(quiz.get('image_choice_tags', [])) > 0:
                has_images = True
            if 'shape_image_tags' in quiz and len(quiz.get('shape_image_tags', [])) > 0:
                has_images = True
            
            # Generate HTML content
            html_content = create_html_for_question(quiz, week, exercise)
            
            # Write HTML file
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  Created: {html_filename}")
        
        print(f"  Processed {len(quizzes)} questions from {filename}")
        return len(quizzes)
    
    except Exception as e:
        print(f"  Error processing {filename}: {str(e)}")
        return 0

def main():
    """Main function to process all JSON files"""
    
    # Define the weeks and exercises to process
    weeks_exercises = {
        '9': ['E1', 'E2', 'E3', 'E4'],
        '10': ['E1', 'E2', 'E3', 'E4'],
        '11': ['E1', 'E2', 'E3', 'E4'],
        '12': ['E1', 'E2', 'E3'],
        '13': ['E1', 'E2', 'E3', 'E4'],
        '14': ['E1', 'E2', 'E3'],  # Skip E4 as it already has HTML
        '15': ['E1', 'E2', 'E3', 'E4', 'E5'],
        '19': ['E1', 'E2'],
        '20': ['E1', 'E2', 'E3', 'E4'],
        '21': ['E1'],
        '22': ['E1', 'E2', 'E3']
    }
    
    total_files = 0
    total_questions = 0
    
    print("Starting HTML generation for Grade 6 math questions...")
    print("=" * 60)
    
    for week, exercises in weeks_exercises.items():
        for exercise in exercises:
            json_filename = f"Gr6_{week}_{exercise}_variations.json"
            json_path = json_filename
            
            if os.path.exists(json_path):
                questions_count = process_json_file(json_path)
                total_files += 1
                total_questions += questions_count
            else:
                print(f"File not found: {json_filename}")
    
    print("=" * 60)
    print(f"Processing complete!")
    print(f"Total JSON files processed: {total_files}")
    print(f"Total HTML files generated: {total_questions}")

if __name__ == "__main__":
    main()