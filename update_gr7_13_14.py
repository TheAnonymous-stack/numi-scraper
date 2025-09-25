import json
import os
from typing import Dict, List, Any

def determine_answer_format(question: Dict[str, Any]) -> str:
    """Determine the answer format based on the question type and content."""
    question_text = question.get('question_text', '')

    # Get answer from correct_answers or answer field
    answer = ''
    if 'correct_answers' in question and question['correct_answers']:
        answer = str(question['correct_answers'][0])
    elif 'answer' in question:
        answer = str(question['answer'])

    question_type = question.get('question_type', '')

    # Check for fractions
    if '/' in answer and not answer.startswith('$'):
        # Check if it's already in simplest form
        parts = answer.split('/')
        if len(parts) == 2:
            try:
                num = int(parts[0])
                den = int(parts[1])
                from math import gcd
                if gcd(abs(num), abs(den)) == 1:
                    return "Express your answer in simplest form."
                else:
                    return "Express your answer as a fraction in simplest form."
            except:
                return "Express your answer as a fraction in simplest form."

    # Check for mixed numbers
    if ' ' in answer and '/' in answer:
        return "Express your answer as a mixed number in simplest form."

    # Check for improper fractions that should be mixed
    if '/' in answer:
        parts = answer.split('/')
        if len(parts) == 2:
            try:
                num = int(parts[0])
                den = int(parts[1])
                if abs(num) > abs(den):
                    return "Express your answer as an improper fraction."
            except:
                pass

    # Check for decimals
    if '.' in answer and not answer.startswith('$'):
        return "Express your answer as a decimal."

    # Check for percentages
    if '%' in answer or 'percent' in question_text.lower():
        return "Express your answer as a percentage."

    # Check for money
    if '$' in answer or 'dollar' in question_text.lower() or 'cost' in question_text.lower():
        return "Express your answer in dollars."

    # Check for equations
    if '=' in answer or 'x' in answer.lower() or 'equation' in question_text.lower():
        return "Write your answer as an equation."

    # Check for ratios
    if ':' in answer or 'ratio' in question_text.lower():
        return "Express your answer as a ratio in simplest form."

    # Default for numeric answers
    return "Simplify your answer."

def update_question_text(question: Dict[str, Any]) -> Dict[str, Any]:
    """Update the question text to include answer format instruction."""
    question_text = question.get('question_text', '')

    # Check if already has format instruction
    format_indicators = [
        'express your answer',
        'simplify',
        'write your answer',
        'give your answer',
        'round to',
        'in simplest form',
        'as a fraction',
        'as a decimal',
        'as a mixed number'
    ]

    # Return as-is if already has format instruction
    # We'll still generate HTML for these
    if any(indicator in question_text.lower() for indicator in format_indicators):
        return question

    # Determine the format instruction
    format_instruction = determine_answer_format(question)

    # Add the instruction to the question text
    if not question_text.endswith('.'):
        question_text += '.'
    question['question_text'] = f"{question_text} {format_instruction}"

    return question

def generate_html_for_question(question: Dict[str, Any], week: int, exercise: int,
                               question_num: int, variation_num: int) -> str:
    """Generate HTML content for a single question."""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 7 - Week {week} Exercise {exercise} - Q{question_num} V{variation_num}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .question-container {{
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
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
            margin-bottom: 30px;
        }}
        .answer-section {{
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin-top: 20px;
        }}
        .answer-label {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .answer {{
            font-size: 20px;
            color: #27ae60;
            font-weight: bold;
        }}
        .metadata {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            font-size: 14px;
            color: #7f8c8d;
        }}
        .steps-container {{
            margin-top: 20px;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 5px;
        }}
        .step {{
            margin-bottom: 15px;
            padding: 10px;
            background-color: white;
            border-left: 3px solid #3498db;
        }}
        .step-header {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        .math {{
            font-family: 'Cambria Math', 'Times New Roman', serif;
            font-size: 1.1em;
        }}
    </style>
</head>
<body>
    <div class="question-container">
        <h1 class="question-header">Grade 7 - Week {week}, Exercise {exercise}</h1>
        <div class="question-text">
            <strong>Question {question_num} (Variation {variation_num}):</strong><br>
            {question_text}
        </div>

        {image_tag}

        <div class="answer-section">
            <div class="answer-label">Answer:</div>
            <div class="answer">{answer}</div>
        </div>

        {steps_html}

        <div class="metadata">
            <strong>Question Type:</strong> {question_type}<br>
            <strong>Difficulty:</strong> {difficulty}<br>
            <strong>Topic:</strong> {topic}
        </div>
    </div>
</body>
</html>'''

    # Handle image tag if present
    image_html = ''
    if question.get('image_tag'):
        image_html = f'<div style="margin: 20px 0;"><img src="{question["image_tag"]}" alt="Question diagram" style="max-width: 100%;"></div>'

    # Handle solution steps if present
    steps_html = ''
    if question.get('solution'):
        steps_html = '<div class="steps-container"><h3>Solution Steps:</h3>'
        for i, step in enumerate(question['solution'], 1):
            if isinstance(step, list) and len(step) >= 2:
                # Format: [fraction, explanation]
                steps_html += f'<div class="step"><div class="step-header">Step {i}:</div>{step[1]}</div>'
            elif isinstance(step, str):
                steps_html += f'<div class="step"><div class="step-header">Step {i}:</div>{step}</div>'
        steps_html += '</div>'
    elif question.get('solution_steps'):
        steps_html = '<div class="steps-container"><h3>Solution Steps:</h3>'
        for i, step in enumerate(question['solution_steps'], 1):
            steps_html += f'<div class="step"><div class="step-header">Step {i}:</div>{step}</div>'
        steps_html += '</div>'

    # Get the correct answer
    answer = ''
    if 'correct_answers' in question and question['correct_answers']:
        answer = question['correct_answers'][0]
    elif 'answer' in question:
        answer = question['answer']

    # Get difficulty and topic from backend_description or use defaults
    difficulty = question.get('difficulty', 'Medium')
    topic = question.get('skills', 'Grade 7 Math').replace('-', ' ').title()

    return html_content.format(
        week=week,
        exercise=exercise,
        question_num=question_num,
        variation_num=variation_num,
        question_text=question.get('question_text', ''),
        answer=answer,
        question_type=question.get('question_type', 'Mathematics'),
        difficulty=difficulty,
        topic=topic,
        image_tag=image_html,
        steps_html=steps_html
    )

def process_files():
    """Process Grade 7 files from week 13 E1 to week 14 E2."""
    changes_log = []
    files_processed = []
    html_files_created = []

    # Create HTML directory if it doesn't exist
    os.makedirs('HTML', exist_ok=True)

    # Define the specific files to process
    target_files = [
        ('Gr7_13_E1_variations.json', 13, 1),
        ('Gr7_13_E2_variations.json', 13, 2),
        ('Gr7_14_E1_variations.json', 14, 1),
        ('Gr7_14_E2_variations.json', 14, 2)
    ]

    for filename, week, exercise in target_files:
        if not os.path.exists(filename):
            print(f"File {filename} not found, skipping...")
            continue

        print(f"Processing {filename}...")
        files_processed.append(filename)

        try:
            # Read the JSON file
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Track if we made changes
            file_changed = False
            questions_updated = []
            file_html_count = 0

            # Check if data has 'quizzes' key
            if 'quizzes' in data and isinstance(data['quizzes'], list):
                # Process each quiz/variation
                for idx, quiz in enumerate(data['quizzes'], 1):
                    if isinstance(quiz, dict):
                        original_text = quiz.get('question_text', '')
                        updated_quiz = update_question_text(quiz)
                        new_text = updated_quiz.get('question_text', '')

                        if original_text != new_text:
                            file_changed = True
                            questions_updated.append(f"V{idx}")
                            data['quizzes'][idx - 1] = updated_quiz

                        # Extract question and variation number from question_number field
                        q_num_str = quiz.get('question_number', f'1_{idx}')
                        parts = q_num_str.split('_')
                        q_num = parts[0] if len(parts) > 0 else '1'
                        var_num = parts[1] if len(parts) > 1 else str(idx)

                        # Generate HTML file
                        html_filename = f'HTML/Gr7_{week}_{exercise}_{q_num}_{var_num}.html'
                        html_content = generate_html_for_question(
                            updated_quiz, week, exercise,
                            int(q_num), int(var_num)
                        )

                        with open(html_filename, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        html_files_created.append(html_filename)
                        file_html_count += 1

            # Save updated JSON if changes were made
            if file_changed:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                changes_log.append({
                    'file': filename,
                    'questions_updated': questions_updated,
                    'total_updates': len(questions_updated),
                    'html_files': file_html_count
                })
                print(f"  Updated {len(questions_updated)} questions")
                print(f"  Generated {file_html_count} HTML files")
            else:
                changes_log.append({
                    'file': filename,
                    'questions_updated': [],
                    'total_updates': 0,
                    'html_files': file_html_count
                })
                print(f"  No text updates needed")
                print(f"  Generated {file_html_count} HTML files")

        except Exception as e:
            print(f"  Error processing {filename}: {str(e)}")
            changes_log.append({
                'file': filename,
                'error': str(e)
            })

    return changes_log, files_processed, html_files_created

def generate_report(changes_log: List[Dict], files_processed: List[str],
                   html_files_created: List[str]) -> str:
    """Generate a detailed report of all changes."""
    report = "# Grade 7 Math Questions Update Report (Weeks 13-14)\n\n"
    report += f"## Summary\n"
    report += f"- Files processed: {len(files_processed)}\n"
    report += f"- Files with updates: {len([c for c in changes_log if c.get('total_updates', 0) > 0])}\n"
    report += f"- Total questions updated: {sum(c.get('total_updates', 0) for c in changes_log)}\n"
    report += f"- HTML files created: {len(html_files_created)}\n\n"

    report += "## Files Processed\n"
    for file in files_processed:
        report += f"- {file}\n"
    report += "\n"

    report += "## Detailed Changes\n"
    for change in changes_log:
        if 'error' in change:
            report += f"\n### {change['file']} - ERROR\n"
            report += f"Error: {change['error']}\n"
        else:
            report += f"\n### {change['file']}\n"
            report += f"- Questions updated: {change.get('total_updates', 0)}\n"
            report += f"- HTML files generated: {change.get('html_files', 0)}\n"
            if change.get('total_updates', 0) > 0:
                report += f"- Updated variations: {', '.join(change['questions_updated'][:10])}"
                if len(change['questions_updated']) > 10:
                    report += f" ... and {len(change['questions_updated']) - 10} more"
                report += "\n"

    report += f"\n## HTML Files Generated\n"
    report += f"Total: {len(html_files_created)} files\n\n"

    # Group by week and exercise
    html_by_week = {}
    for html_file in html_files_created:
        # Parse filename to get week and exercise
        parts = os.path.basename(html_file).replace('.html', '').split('_')
        if len(parts) >= 4:
            week = parts[1]
            exercise = parts[2]
            key = f"Week {week}, Exercise {exercise}"
            if key not in html_by_week:
                html_by_week[key] = 0
            html_by_week[key] += 1

    for key in sorted(html_by_week.keys()):
        report += f"- {key}: {html_by_week[key]} files\n"

    report += "\n## Answer Format Instructions Added\n"
    report += "The following types of answer format instructions may have been added:\n"
    report += "- Express your answer in simplest form\n"
    report += "- Express your answer as a fraction in simplest form\n"
    report += "- Express your answer as a mixed number in simplest form\n"
    report += "- Express your answer as an improper fraction\n"
    report += "- Express your answer as a decimal\n"
    report += "- Express your answer as a percentage\n"
    report += "- Express your answer in dollars\n"
    report += "- Write your answer as an equation\n"
    report += "- Express your answer as a ratio in simplest form\n"
    report += "- Simplify your answer\n"

    return report

if __name__ == "__main__":
    print("Starting Grade 7 Math Questions Update (Weeks 13-14)")
    print("=" * 50)

    # Process all files
    changes_log, files_processed, html_files_created = process_files()

    # Generate and save report
    report = generate_report(changes_log, files_processed, html_files_created)

    report_filename = "gr7_13_14_update_report.md"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)

    print("\n" + "=" * 50)
    print(f"Report saved to: {report_filename}")
    print(f"Total files processed: {len(files_processed)}")
    print(f"Total HTML files created: {len(html_files_created)}")