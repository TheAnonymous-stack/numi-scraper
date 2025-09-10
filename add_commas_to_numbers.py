import json
import re

def add_commas_to_number(text):
    """Add comma separators to numbers with 4+ digits in text"""
    def format_number(match):
        number = match.group()
        # Only add commas to numbers with 4+ digits
        if len(number) >= 4:
            return f"{int(number):,}"
        return number
    
    # Find all sequences of digits (including those in mathematical expressions)
    return re.sub(r'\d+', format_number, text)

def process_string(field_value):
    """Process a field value, handling strings, lists, and nested structures"""
    return add_commas_to_number(field_value)

def add_commas_to_json(input_file):
    """Add comma separators to numbers in question_text, correct_answers, and solution fields"""
    
    # Read the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Process each question
    for question in data:
        # Process question_text - directly modify
        if 'question_text' in question:
            question['question_text'] = process_string(question['question_text'])
        
        # Process correct_answers - append comma-separated versions as new nested lists
        if question['question_type'] == "Fill in the blank":
            
            if isinstance(question['correct_answers'][0], str) and len(question['correct_answers'][0]) > 3:
                answer = question['correct_answers'][0]
                new_ans = [[answer]]
                new_ans.append([process_string(answer)])
                question['correct_answers'] = new_ans
                question['has_alternate_answers'] = True
            elif isinstance(question['correct_answers'][0], list):
                additional_ans = []
                for answer in question['correct_answers']:
                    ans = answer[0]
                    additional_ans.append([process_string(ans)])


            
                # Append the new comma-separated versions
                question['correct_answers'] += additional_ans
        elif question['question_type'] == "Ordering Items":
            for i in range(len(question['choices'])):
                question['choices'][i] = process_string(question['choices'][i])
            for i in range(len(question['correct_answers'])):
                question['correct_answers'][i] = process_string(question['correct_answers'][i])
        
        # Process solution - directly modify the solution steps
        if 'solution' in question:
            for step in question["solution"]:
                if len(step) > 1:
                    step[1] = process_string(step[1])
    
    # Write to output file for preview
    output_file = "output.json"
    with open(input_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully added comma separators to numbers from {input_file}")
    print(f"Output saved to {output_file} for preview")

if __name__ == "__main__":
    input_file = "Gr5_2_E2_variations.json"
    add_commas_to_json(input_file)