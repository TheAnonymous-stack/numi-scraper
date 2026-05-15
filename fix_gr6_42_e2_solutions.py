import json

def fix_solutions_and_answers(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        # Extract the data from question text
        question_lines = quiz['question_text'].split('\\n')
        if len(question_lines) >= 2:
            # Parse the data line
            data_line = question_lines[1]
            if ':' in data_line:
                # Parse values
                values = {}
                parts = data_line.split(', ')
                for part in parts:
                    if ':' in part:
                        name, value = part.split(': ')
                        values[name.lower()] = int(value)
                
                # Find the mode(s)
                if values:
                    max_value = max(values.values())
                    modes = [name for name, val in values.items() if val == max_value]
                    
                    # Update correct answers based on actual modes
                    choices_lower = [c.lower() for c in quiz['choices']]
                    correct_indices = []
                    for mode in modes:
                        if mode in choices_lower:
                            idx = choices_lower.index(mode)
                            correct_indices.append(chr(65 + idx))  # A, B, C, etc.
                    
                    # Update answer format
                    if len(correct_indices) == 1:
                        quiz['correct_answers'] = [correct_indices[0]]
                        quiz['question_type'] = "Multiple Choice Question with Single Answer"
                        quiz['has_alternate_answers'] = False
                    else:
                        quiz['correct_answers'] = [[idx] for idx in correct_indices]
                        quiz['question_type'] = "Multiple Choice with Multiple Answers"
                        quiz['has_alternate_answers'] = True
                    
                    # Fix solution text
                    mode_text = " and ".join([mode.capitalize() for mode in modes])
                    
                    if len(modes) == 1:
                        solution_text = f"{mode_text} had {max_value}, which is more than any other option. So {mode_text} is the mode."
                    else:
                        solution_text = f"{mode_text} both had {max_value}, which is more than any other option. So both are modes."
                    
                    quiz['solution'] = [
                        ["1/3", "Remember, the mode is the value that occurs most often in a data set."],
                        ["2/3", f"Look at the data: {data_line}"],
                        ["3/3", solution_text]
                    ]
    
    # Fix question 51 - add missing data
    if len(data['quizzes']) >= 51:
        quiz_51 = data['quizzes'][50]  # index 50 for question 51
        quiz_51['question_text'] = "Student council tracked meeting attendance.\\nMonday: 18, Tuesday: 22, Wednesday: 25, Thursday: 22, Friday: 15\\nPick the mode of this data set. There may be more than one.=_"
        quiz_51['choices'] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        quiz_51['correct_answers'] = [["B"], ["D"]]
        quiz_51['question_type'] = "Multiple Choice with Multiple Answers"
        quiz_51['has_alternate_answers'] = True
        quiz_51['solution'] = [
            ["1/3", "Remember, the mode is the value that occurs most often in a data set."],
            ["2/3", "Look at the data: Monday: 18, Tuesday: 22, Wednesday: 25, Thursday: 22, Friday: 15"],
            ["3/3", "Tuesday and Thursday both had 22 attendees, which is more than any other day. So both are modes."]
        ]
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Fixed solutions and answers in {filename}")

# Process the file
fix_solutions_and_answers('Gr6_42_E2_variations.json')