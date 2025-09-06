import json
import random
import copy

def load_templates():
    """Load template questions from the templates file."""
    with open('templates.json', 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # Filter for Gr6_46_E3 templates
    templates = [q for q in all_questions if q.get('tag') == 'Gr6_46_E3']
    return templates

def generate_variations():
    """Generate 51 total versions including templates for Gr6_46_E3."""
    templates = load_templates()
    
    # We have 1 template, need 50 more variations
    variations = []
    
    # 3D object view variations
    view_variations = []
    
    # Different 3D objects and their dimensions
    objects_3d = [
        {"shape": "rectangular prism", "dims": (4, 3, 2), "top_view": "4 by 3"},
        {"shape": "rectangular prism", "dims": (5, 2, 3), "top_view": "5 by 2"},
        {"shape": "rectangular prism", "dims": (3, 3, 4), "top_view": "3 by 3"},
        {"shape": "rectangular prism", "dims": (6, 2, 2), "top_view": "6 by 2"},
        {"shape": "rectangular prism", "dims": (4, 4, 3), "top_view": "4 by 4"},
        {"shape": "rectangular prism", "dims": (2, 5, 3), "top_view": "2 by 5"},
        {"shape": "cube arrangement", "dims": (3, 4, 2), "top_view": "3 by 4"},
        {"shape": "cube arrangement", "dims": (5, 3, 2), "top_view": "5 by 3"},
        {"shape": "rectangular prism", "dims": (7, 2, 3), "top_view": "7 by 2"},
        {"shape": "rectangular prism", "dims": (3, 5, 2), "top_view": "3 by 5"},
        {"shape": "cube tower", "dims": (2, 2, 5), "top_view": "2 by 2"},
        {"shape": "rectangular prism", "dims": (8, 2, 2), "top_view": "8 by 2"},
        {"shape": "rectangular prism", "dims": (4, 5, 2), "top_view": "4 by 5"},
        {"shape": "cube arrangement", "dims": (6, 3, 2), "top_view": "6 by 3"},
        {"shape": "rectangular prism", "dims": (3, 6, 2), "top_view": "3 by 6"},
        {"shape": "rectangular prism", "dims": (5, 4, 3), "top_view": "5 by 4"},
        {"shape": "cube tower", "dims": (3, 3, 3), "top_view": "3 by 3"},
        {"shape": "rectangular prism", "dims": (2, 7, 2), "top_view": "2 by 7"},
        {"shape": "rectangular prism", "dims": (6, 4, 2), "top_view": "6 by 4"},
        {"shape": "cube arrangement", "dims": (4, 6, 2), "top_view": "4 by 6"},
        {"shape": "rectangular prism", "dims": (5, 5, 3), "top_view": "5 by 5"},
        {"shape": "rectangular prism", "dims": (7, 3, 2), "top_view": "7 by 3"},
        {"shape": "cube tower", "dims": (4, 4, 4), "top_view": "4 by 4"},
        {"shape": "rectangular prism", "dims": (2, 8, 2), "top_view": "2 by 8"},
        {"shape": "rectangular prism", "dims": (8, 3, 2), "top_view": "8 by 3"}
    ]
    
    # Different viewing angles
    view_types = [
        {"view": "top", "question": "If you look at this object from the top, what will you see?"},
        {"view": "front", "question": "If you look at this object from the front, what will you see?"},
        {"view": "side", "question": "If you look at this object from the side, what will you see?"},
        {"view": "bottom", "question": "If you look at this object from the bottom, what will you see?"},
        {"view": "left side", "question": "If you look at this object from the left side, what will you see?"},
        {"view": "right side", "question": "If you look at this object from the right side, what will you see?"}
    ]
    
    variation_num = 2  # Start from 2 since template is 1
    
    for i in range(50):  # Generate 50 variations
        template = templates[0]  # Only one template
        variation = copy.deepcopy(template)
        
        # Select random object and view
        obj = random.choice(objects_3d)
        view = random.choice(view_types)
        
        variation['question_number'] = f"3_{variation_num}"
        variation['question_text'] = view['question']
        
        # Update image tag
        if 'image_tag' in variation:
            variation['image_tag'] = f"Gr6_46_3_{variation_num}"
        
        # Generate appropriate backend description
        if view['view'] == 'top':
            correct_view = obj['top_view']
            incorrect_view = f"{obj['dims'][0]+1} by {obj['dims'][1]}" if i % 2 == 0 else f"{obj['dims'][0]} by {obj['dims'][1]+1}"
        elif view['view'] == 'front':
            correct_view = f"{obj['dims'][0]} by {obj['dims'][2]}"
            incorrect_view = f"{obj['dims'][0]+1} by {obj['dims'][2]}" if i % 2 == 0 else f"{obj['dims'][0]} by {obj['dims'][2]+1}"
        else:  # side view
            correct_view = f"{obj['dims'][1]} by {obj['dims'][2]}"
            incorrect_view = f"{obj['dims'][1]+1} by {obj['dims'][2]}" if i % 2 == 0 else f"{obj['dims'][1]} by {obj['dims'][2]+1}"
        
        # Update backend description
        colors = ["pink and purple", "blue and green", "red and yellow", "orange and gray", "cyan and magenta"]
        color_scheme = random.choice(colors)
        
        variation['backend_description'] = f"The image shows a 3D {obj['shape']} made up of small {color_scheme} cubes. The prism has a length of {obj['dims'][0]} cubes from front to back, a height of {obj['dims'][2]} cubes from bottom to top, and a width of {obj['dims'][1]} cubes from left to right."
        
        # Update image choice tags
        if 'image_choice_tags' in variation:
            variation['image_choice_tags'] = [
                f"Gr6_46_3_{variation_num}_A",
                f"Gr6_46_3_{variation_num}_B"
            ]
        
        # Update image choice descriptions
        if 'image_choice_backend_description' in variation:
            variation['image_choice_backend_description'] = [
                f"The image shows a flat 2D grid made up of {incorrect_view.replace(' by ', ' rows and ')} columns of colored squares.",
                f"The image shows a flat 2D grid made up of {correct_view.replace(' by ', ' rows and ')} columns of colored squares."
            ]
        
        # Randomly swap correct answer between A and B
        if random.random() < 0.5:
            variation['correct_answers'] = ['A']
            # Swap the descriptions
            variation['image_choice_backend_description'] = variation['image_choice_backend_description'][::-1]
        
        # Update solution image tags
        if 'solution_image_tag' in variation:
            for j, step in enumerate(variation['solution_image_tag']):
                old_tag = step[1]
                new_tag = f"Gr6_46_3_{variation_num}_step_{j+1}"
                variation['solution_image_tag'][j][1] = new_tag
        
        # Update solution text
        if view['view'] == 'top':
            variation['solution'][-1][1] = f"If you look at this object from the {view['view']}, you will see:"
        elif view['view'] == 'front':
            variation['solution'][-1][1] = f"If you look at this object from the {view['view']}, you will see:"
        else:
            variation['solution'][-1][1] = f"If you look at this object from the {view['view']}, you will see:"
        
        variations.append(variation)
        variation_num += 1
    
    return variations

def main():
    """Main function to generate and save variations."""
    variations = generate_variations()
    
    # Save to JSON file
    output_file = 'Gr6_46_E3_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_46_E3")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()