import json
import random
import copy

def load_templates():
    """Load template questions from the templates file."""
    with open('templates.json', 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # Filter for Gr6_47_E1 templates
    templates = [q for q in all_questions if q.get('tag') == 'Gr6_47_E1']
    return templates

def generate_variations():
    """Generate 51 total versions including templates for Gr6_47_E1."""
    templates = load_templates()
    
    # We have 2 templates, need 49 more variations
    variations = []
    
    # Generate coordinate variations (positive numbers only)
    coordinate_variations = []
    
    # Generate diverse coordinates for points
    for i in range(49):
        # Generate random points with diverse coordinates
        points = []
        point_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        # Select 2 random point names
        selected_names = random.sample(point_names, 2)
        
        # Generate coordinates (positive only, 0-20 range)
        coord1 = (random.randint(1, 20), random.randint(1, 20))
        coord2 = (random.randint(1, 20), random.randint(1, 20))
        
        # Ensure coordinates are different
        while coord2 == coord1:
            coord2 = (random.randint(1, 20), random.randint(1, 20))
        
        # Randomly choose which coordinate to ask about
        if i % 2 == 0:  # Ask for x-coordinate
            question_text = f"What is the x-coordinate of point {selected_names[0]}? \nx-coordinate: ___"
            correct_answer = str(coord1[0])
            target_point = selected_names[0]
            target_coord = coord1
            other_point = selected_names[1]
            other_coord = coord2
            axis_type = "x"
            solution_direction = "down"
            axis_position = f"{coord1[0]} units to the right of"
        else:  # Ask for y-coordinate
            question_text = f"What is the y-coordinate of point {selected_names[1]}?\ny-coordinate: ___"
            correct_answer = str(coord2[1])
            target_point = selected_names[1]
            target_coord = coord2
            other_point = selected_names[0]
            other_coord = coord1
            axis_type = "y"
            solution_direction = "left"
            axis_position = f"{coord2[1]} units above"
        
        coordinate_variations.append({
            "question_text": question_text,
            "target_point": target_point,
            "target_coord": target_coord,
            "other_point": other_point,
            "other_coord": other_coord,
            "correct_answer": correct_answer,
            "axis_type": axis_type,
            "solution_direction": solution_direction,
            "axis_position": axis_position
        })
    
    # Generate variations
    variation_num = 3  # Start from 3 since we have templates 1 and 2
    
    for var_data in coordinate_variations:
        # Randomly select a template
        template = random.choice(templates)
        template_num = template['question_number'].split('_')[0]
        
        variation = copy.deepcopy(template)
        variation['question_number'] = f"{template_num}_{variation_num}"
        variation['question_text'] = var_data['question_text']
        variation['correct_answers'] = [var_data['correct_answer']]
        
        # Update image tag
        if 'image_tag' in variation:
            variation['image_tag'] = f"Gr6_47_{template_num}_{variation_num}"
        
        # Update backend description
        colors = ["pink", "yellow", "green", "blue", "purple", "orange", "red", "cyan"]
        color1, color2 = random.sample(colors, 2)
        
        variation['backend_description'] = (
            f"This image shows a coordinate plane with x-axis is labeled 'x' and the y-axis is labeled 'y'. "
            f"Point {var_data['target_point']} is labeled '{var_data['target_point']}' with a {color1} dot and is located at the point {var_data['target_coord']}. "
            f"Point {var_data['other_point']} is labeled '{var_data['other_point']}' with a {color2} dot and is located at the point {var_data['other_coord']}."
        )
        
        # Update solution
        if var_data['axis_type'] == 'x':
            variation['solution'] = [
                ["1/3", f"Start at point {var_data['target_point']} and move {var_data['solution_direction']} until you reach the {var_data['axis_type']}-axis."],
                ["2/3", f"This position on the {var_data['axis_type']}-axis is {var_data['axis_position']} the origin."],
                ["3/3", f"So, the {var_data['axis_type']}-coordinate of point {var_data['target_point']} is {var_data['correct_answer']}."]
            ]
        else:
            variation['solution'] = [
                ["1/3", f"Start at point {var_data['target_point']} and move {var_data['solution_direction']} until you reach the {var_data['axis_type']}-axis."],
                ["2/3", f"This position on the {var_data['axis_type']}-axis is {var_data['axis_position']} the origin."],
                ["3/3", f"So, the {var_data['axis_type']}-coordinate of point {var_data['target_point']} is {var_data['correct_answer']}."]
            ]
        
        # Update solution image tag
        if 'solution_image_tag' in variation:
            step_tag = variation['solution_image_tag'][0][1]
            new_tag = f"Gr6_47_{template_num}_{variation_num}_step_1"
            
            line_type = "horizontal" if var_data['axis_type'] == 'y' else "vertical"
            end_point = f"(0, {var_data['target_coord'][1]})" if var_data['axis_type'] == 'y' else f"({var_data['target_coord'][0]}, 0)"
            
            variation['solution_image_tag'][0][1] = new_tag
            variation['solution_image_tag'][0][2] = (
                f"This image shows a coordinate plane with x-axis is labeled 'x' and the y-axis is labeled 'y'. "
                f"Point {var_data['other_point']} is faded out, labeled '{var_data['other_point']}' and located at the point {var_data['other_coord']}. "
                f"Point {var_data['target_point']} is labeled '{var_data['target_point']}' with a {color1} dot and is located at the point {var_data['target_coord']}. "
                f"There is a dashed red {line_type} line connecting point {var_data['target_point']} to the {var_data['axis_type']}-axis, ending at the point {end_point}."
            )
        
        variations.append(variation)
        variation_num += 1
    
    return variations

def main():
    """Main function to generate and save variations."""
    variations = generate_variations()
    
    # Save to JSON file
    output_file = 'Gr6_47_E1_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_47_E1")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()