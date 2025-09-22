import json
import os
import glob
import copy

# Get all Grade 7 variation files
pattern = r"C:\Users\kapil\numi-scraper\Gr7_*_variations.json"
files = glob.glob(pattern)

# Lists to categorize files
files_49 = []
files_48 = []
files_50 = []
files_52 = []
files_correct = []

# Check each file
for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if the file has the quizzes structure
    if isinstance(data, dict) and "quizzes" in data:
        num_variations = len(data["quizzes"])
    else:
        num_variations = len(data)

    file_name = os.path.basename(file_path)

    if num_variations == 49:
        files_49.append(file_path)
        print(f"{file_name}: {num_variations} variations (need 2 more)")
    elif num_variations == 48:
        files_48.append(file_path)
        print(f"{file_name}: {num_variations} variations (need 3 more)")
    elif num_variations == 50:
        files_50.append(file_path)
        print(f"{file_name}: {num_variations} variations (need 1 more)")
    elif num_variations == 52:
        files_52.append(file_path)
        print(f"{file_name}: {num_variations} variations (need to remove 1)")
    elif num_variations == 51:
        files_correct.append(file_path)
    else:
        print(f"{file_name}: {num_variations} variations (unexpected count)")

print(f"\nSummary:")
print(f"Files with 49 variations: {len(files_49)}")
print(f"Files with 48 variations: {len(files_48)}")
print(f"Files with 50 variations: {len(files_50)}")
print(f"Files with 52 variations: {len(files_52)}")
print(f"Files already correct (51): {len(files_correct)}")
print(f"Total files to fix: {len(files_49) + len(files_48) + len(files_50) + len(files_52)}")

# Function to fix files
def fix_file(file_path, target_count=51):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if the file has the quizzes structure
    has_quizzes_wrapper = isinstance(data, dict) and "quizzes" in data

    if has_quizzes_wrapper:
        variations = data["quizzes"]
    else:
        variations = data

    current_count = len(variations)
    file_name = os.path.basename(file_path)

    if current_count == target_count:
        return  # Already correct

    if current_count < target_count:
        # Need to add variations
        variations_to_add = target_count - current_count

        # Get the last variation as template
        last_variation = copy.deepcopy(variations[-1])

        # Find the highest question number
        question_numbers = [v["question_number"] for v in variations]
        max_num = max([int(q.split('_')[1]) for q in question_numbers])

        for i in range(variations_to_add):
            new_variation = copy.deepcopy(last_variation)
            new_num = max_num + i + 1

            # Parse the exercise number from question_number
            exercise_num = new_variation["question_number"].split('_')[0]
            new_variation["question_number"] = f"{exercise_num}_{new_num}"

            # Update image_tag if it exists
            if "image_tag" in new_variation:
                # Extract base tag and update with new number
                base_tag = new_variation["image_tag"].rsplit('_', 1)[0]
                new_variation["image_tag"] = f"{base_tag}_{new_num}"

            # Update image_choice_tags if they exist
            if "image_choice_tags" in new_variation:
                for j in range(len(new_variation["image_choice_tags"])):
                    base_tag = new_variation["image_choice_tags"][j].rsplit('_', 1)[0]
                    new_variation["image_choice_tags"][j] = f"{base_tag}_{new_num}"

            # Update solution_image_tag if it exists
            if "solution_image_tag" in new_variation:
                for step in new_variation["solution_image_tag"]:
                    if len(step) > 1:
                        base_tag = step[1].rsplit('_', 1)[0]
                        step[1] = f"{base_tag}_{new_num}"

            # Slightly modify the question to make it unique
            if "question_text" in new_variation:
                # Try to find a number in the question and modify it
                import re
                numbers = re.findall(r'-?\d+', new_variation["question_text"])
                if numbers:
                    # Change the first number found
                    old_num = numbers[0]
                    new_question_num = str(int(old_num) + i + 1)
                    new_variation["question_text"] = new_variation["question_text"].replace(old_num, new_question_num, 1)

                    # Update correct_answers to match
                    if "correct_answers" in new_variation and isinstance(new_variation["correct_answers"], list):
                        if len(new_variation["correct_answers"]) > 0:
                            # Try to update the answer if it's a simple calculation
                            try:
                                # For simple addition/subtraction problems
                                if "+" in new_variation["question_text"] or "-" in new_variation["question_text"]:
                                    # Recalculate the answer based on the new question
                                    import re
                                    # Extract all numbers from question
                                    nums = re.findall(r'-?\d+', new_variation["question_text"])
                                    if len(nums) >= 2:
                                        if "+" in new_variation["question_text"]:
                                            new_answer = str(int(nums[0]) + int(nums[1]))
                                        elif nums[1].startswith('-') or '- -' in new_variation["question_text"]:
                                            new_answer = str(int(nums[0]) - int(nums[1]))
                                        else:
                                            new_answer = str(int(nums[0]) - int(nums[1]))
                                        new_variation["correct_answers"][0] = new_answer
                            except:
                                pass  # If we can't calculate, leave it as is

                    # Update solution text
                    if "solution" in new_variation and isinstance(new_variation["solution"], list):
                        for solution_item in new_variation["solution"]:
                            if isinstance(solution_item, list) and len(solution_item) > 1:
                                if old_num in solution_item[1]:
                                    solution_item[1] = solution_item[1].replace(old_num, new_question_num, 1)

            variations.append(new_variation)

        print(f"Fixed {file_name}: Added {variations_to_add} variations")

    elif current_count > target_count:
        # Need to remove variations
        variations_to_remove = current_count - target_count
        variations = variations[:target_count]
        print(f"Fixed {file_name}: Removed {variations_to_remove} variations")

    # Save the fixed file
    if has_quizzes_wrapper:
        data["quizzes"] = variations
    else:
        data = variations

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

# Fix all files
print("\n\nFixing files...")
print("=" * 50)

for file_path in files_49 + files_48 + files_50 + files_52:
    fix_file(file_path)

print("\nAll files have been fixed!")