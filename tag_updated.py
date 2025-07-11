import json
import re
import os
from collections import defaultdict

def update_tags_and_numbers(json_data, start_group=1, start_exercise=1):
    """
    Update tags and question numbers according to the new format:
    - if original tags are the same: keep original tag, only update question numbers (1_1, 1_2, etc.)
    - if original tag changes: start new exercise group with GrX_<group>_E<exercise> format
    - question numbers restart from 1 for each exercise
    - image tags: "GrX_<group>_<exercise>_<question>"
    - image choice tags: "GrX_<group>_<exercise>_<question>_<option>"
    """
    
    # save original tags before we start modifying them
    original_tags = [question.get('tag', '') for question in json_data]
    
    current_group = start_group
    updated_data = []
    current_exercise = start_exercise  # E1, E2, E3, E4
    question_counter = 1  # counter within current exercise
    
    for i, question in enumerate(json_data):
        original_tag = original_tags[i]  # Use the saved original tag
        
        # check if this is a new exercise (original tag changed)
        if i > 0:
            prev_original_tag = original_tags[i-1]  # use saved original tag for comparison
            if original_tag != prev_original_tag:
                # new exercise - increment exercise number or group
                if current_exercise < 4:
                    current_exercise += 1
                else:
                    # move to next group and reset exercise to 1
                    current_group += 1
                    current_exercise = 1
                question_counter = 1  # reset question counter for new exercise
            else:
                # same original tag - current exercise stays the same as previous exercise
                # only increment question counter
                question_counter += 1
        # determine the new tag format
        if i == 0 or original_tag != original_tags[i-1]:
            # first question or new exercise - use Gr8 format
            new_tag = f"Gr8_{current_group}_E{current_exercise}"
        else:
            # same exercise - use Gr8 format but keep same exercise number
            new_tag = f"Gr8_{current_group}_E{current_exercise}"
        
        question['tag'] = new_tag
        
        # update question number - use the current exercise and question counter
        question['question_number'] = f"{current_exercise}_{question_counter}"
        
        # remove original image_tag and update with new format
        if 'image_tag' in question:
            old_image_tag = question['image_tag']
            if old_image_tag and old_image_tag != "":
                # create new image tag format
                question['image_tag'] = f"Gr8_{current_group}_{current_exercise}_{question_counter}"
            else:
                # remove empty image tags
                question.pop('image_tag', None)
        
        # update image choice tags if they exist
        if 'image_choice_tags' in question:
            updated_choice_tags = []
            for choice_tag in question['image_choice_tags']:
                # extract option letter (A, B, C, etc.) from the end
                # handle both formats: "Grade8_J.7.1_A" and "Grade8_J.7.1_A.png"
                match = re.search(r'Grade8_(.+)_([A-Z])(?:\.png)?$', choice_tag)
                if match:
                    option_letter = match.group(2)
                    new_choice_tag = f"Gr8_{current_group}_{current_exercise}_{question_counter}_{option_letter}"
                    updated_choice_tags.append(new_choice_tag)
                else:
                    # fallback if pattern doesn't match
                    updated_choice_tags.append(choice_tag)
            question['image_choice_tags'] = updated_choice_tags
        
        # update solution image tags if they exist
        if 'solution_image_tag' in question:
            updated_solution_tags = []
            for solution_tag in question['solution_image_tag']:
                # extract the step number from the original tag
                match = re.search(r'Grade8_(.+)_solution_step_(\d+)', solution_tag)
                if match:
                    step_num = match.group(2)
                    new_solution_tag = f"Gr8_{current_group}_{current_exercise}_{question_counter}_step_{step_num}"
                    updated_solution_tags.append(new_solution_tag)
                else:
                    updated_solution_tags.append(solution_tag)
            question['solution_image_tag'] = updated_solution_tags
        
        updated_data.append(question)
    
    return updated_data

def process_json_file(input_filename, output_filename, start_group=1, start_exercise=1):
    
    print(f"Processing {input_filename}...")
    
    # Read the input JSON file
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {input_filename} not found!")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_filename}: {e}")
        return
    
    print(f"Found {len(data)} questions to process")
    
    # Update tags and numbers
    updated_data = update_tags_and_numbers(data, start_group, start_exercise)
    
    # Write the updated data to output file
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully created {output_filename}")
        print(f"Updated {len(updated_data)} questions")
        
        # Print some examples of the new format
        print("\nExample of new tag format:")
        for i, question in enumerate(updated_data[:8]):  # Show first 8 questions
            print(f"  Question {i+1}: tag='{question['tag']}', number='{question['question_number']}'")
            
    except Exception as e:
        print(f"Error writing to {output_filename}: {e}")

def list_available_files():
    """List all available files"""
    json_files = []
    for filename in os.listdir('.'):
        if filename.endswith('.json') and not filename.endswith('_updated.json'):
            json_files.append(filename)
    return json_files

def main():

    print("tag update")
    print("=" * 50)
    
    while True:
        # List available files
        json_files = list_available_files()
        
        if not json_files:
            print("No JSON files found")
            return
        
        print(f"\nAvailable JSON files:")
        for i, filename in enumerate(json_files):
            print(f"  {i+1}. {filename}")
        
        print(f"  {len(json_files)+1}. Exit")
        
        # Get user choice
        try:
            choice = input(f"\nSelect a file to process (1-{len(json_files)+1}): ").strip()
            
            if choice == str(len(json_files)+1):
                print("Exiting...")
                break
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(json_files):
                selected_file = json_files[choice_idx]
                
                # Get start group and exercise from user
                start_group_input = input(f"Enter start group number for {selected_file} (default=1): ").strip()
                start_group = int(start_group_input) if start_group_input.isdigit() else 1
                
                start_exercise_input = input(f"Enter start exercise number for {selected_file} (default=1): ").strip()
                start_exercise = int(start_exercise_input) if start_exercise_input.isdigit() else 1
                
                # Create output filename
                base_name = selected_file.replace('.json', '')
                output_filename = f"{base_name}_updated.json"
                
                print(f"\nProcessing {selected_file} with start_group={start_group}, start_exercise={start_exercise}")
                process_json_file(selected_file, output_filename, start_group, start_exercise)
                
               
                continue_choice = input("\nProcess another file? (y/n): ").strip().lower()
                if continue_choice != 'y':
                    print("Exiting...")
                    break
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main() 