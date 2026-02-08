import json
import re

def add_dollar_signs_to_question(question_text):
    """Add dollar signs to decimal numbers in money-related questions"""
    # Pattern to match decimal numbers that don't already have a $ sign before them
    # Matches patterns like "0.77" or "12.5" but not "$0.77"
    # We'll be careful to not match numbers that already have $ or are in math mode

    # First, let's handle patterns like "0.77 + 0.23" or "51.69 - 45.89"
    # We want to add $ before each number if it's a decimal

    def add_dollar(match):
        """Add $ before a decimal number if it doesn't already have one"""
        before = match.group(1)
        number = match.group(2)
        # Only add $ if there's not already one
        if before.endswith('$'):
            return before + number
        return before + '$' + number

    # Match decimal numbers (with context before them)
    # Pattern: capture any char before + the decimal number
    # But only if it's not already preceded by $
    result = re.sub(r'([^$\d])(\d+\.\d+)', add_dollar, question_text)

    # Also handle numbers at the start of expressions
    result = re.sub(r'^(\d+\.\d+)', r'$\1', result, flags=re.MULTILINE)

    # Handle numbers after "Add.\n" or "Subtract.\n"
    result = re.sub(r'(Add\.\\n)(\d+\.\d+)', r'\1$\2', result)
    result = re.sub(r'(Subtract\.\\n )(\d+\.\d+)', r'\1$\2', result)

    return result

# Process all three files
files_to_process = [
    "Gr5_20_E1_variations.json",
    "Gr5_20_E2_variations.json",
    "Gr5_20_E3_variations.json"
]

for filename in files_to_process:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            questions = json.load(f)

        modified_count = 0

        for question in questions:
            original_text = question.get('question_text', '')

            # Only process if it's a money-related question (has decimal points)
            if '.' in original_text and 'add-and-subtract-money-amounts' in question.get('skills', ''):
                modified_text = add_dollar_signs_to_question(original_text)

                if modified_text != original_text:
                    question['question_text'] = modified_text
                    modified_count += 1

        # Save the file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)

        print(f"Processed {filename}: {modified_count} questions modified")

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("\nAll files processed!")
