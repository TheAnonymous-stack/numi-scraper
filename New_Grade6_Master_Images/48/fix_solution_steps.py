import json
import re

def split_solution_text(text, num_steps):
    """Split solution text into num_steps parts intelligently"""

    # Split by sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    if len(sentences) < num_steps:
        # If we have fewer sentences than steps, distribute what we have
        result = []
        for i in range(num_steps):
            if i < len(sentences):
                result.append(sentences[i])
            else:
                result.append("")  # Empty for extra steps
        return result

    # Calculate how many sentences per step
    sentences_per_step = len(sentences) / num_steps

    steps = []
    current_step = []
    target_count = sentences_per_step

    for i, sentence in enumerate(sentences):
        current_step.append(sentence)

        # Check if we should start a new step
        if len(current_step) >= target_count and len(steps) < num_steps - 1:
            steps.append(' '.join(current_step))
            current_step = []
            target_count = sentences_per_step

    # Add remaining sentences to the last step
    if current_step:
        steps.append(' '.join(current_step))

    # Ensure we have exactly num_steps
    while len(steps) < num_steps:
        steps.append("")

    return steps[:num_steps]

def fix_output_json(input_file, output_file):
    """Fix the solution text in output.json"""

    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    # Process each quiz
    for quiz in data['quizzes']:
        solution = quiz.get('solution', [])

        # Check if this needs fixing (steps 2+ have placeholder text)
        if len(solution) > 1:
            needs_fixing = False
            for i in range(1, len(solution)):
                if 'Step' in solution[i][1] and 'of the solution' in solution[i][1]:
                    needs_fixing = True
                    break

            if needs_fixing and solution[0][1]:
                # Get the full text from step 1
                full_text = solution[0][1]
                num_steps = len(solution)

                # Split the text intelligently
                step_texts = split_solution_text(full_text, num_steps)

                # Update the solution
                for i in range(num_steps):
                    step_num = solution[i][0]  # Keep the original numbering like "1/4"
                    solution[i][1] = step_texts[i]

                fixed_count += 1
                print(f"Fixed solution for question {quiz['question_number']}")
                for i, step in enumerate(solution):
                    print(f"  {step[0]}: {step[1][:80]}...")

    # Write the updated JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Fixed {fixed_count} solutions")
    print(f"✓ Updated file saved to {output_file}")

if __name__ == "__main__":
    fix_output_json("output.json", "output.json")
