"""
Generate variations for Gr6_50_E1 - Measure angles with a protractor
"""

import json
import random
import copy

def generate_angle_variations():
    """Generate 50 variations of protractor angle measurement questions."""
    
    # Load the template
    with open('parsed_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    # Find the template for this tag
    template = None
    for q in templates:
        if q.get('tag') == 'Gr6_50_E1':
            template = q
            break
    
    if not template:
        print("Template not found!")
        return
    
    variations = []
    
    # Generate diverse angle measurements
    # Using different ranges to ensure variety
    angle_sets = [
        # Acute angles (less than 90°)
        list(range(10, 90, 5)),
        # Obtuse angles (between 90° and 180°)
        list(range(95, 180, 5)),
        # Mix of common angles
        [15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 155, 165, 175],
        # Special angles
        [30, 60, 90, 120, 150, 45, 135, 22.5, 67.5, 112.5, 157.5],
    ]
    
    # Flatten and remove duplicates
    all_angles = []
    for angle_set in angle_sets:
        all_angles.extend(angle_set)
    all_angles = list(set(all_angles))
    
    # Ensure we have enough unique angles
    if len(all_angles) < 50:
        # Add more angles
        for i in range(5, 180, 3):
            if i not in all_angles:
                all_angles.append(i)
    
    # Shuffle for randomness
    random.shuffle(all_angles)
    
    # Take 50 angles (we already have 1 template, so we need 50 more variations)
    selected_angles = all_angles[:50]
    
    for i, angle in enumerate(selected_angles, 1):
        variation = copy.deepcopy(template)
        
        # Update question number
        variation['question_number'] = f"1_{i+1}"
        
        # Keep the same question text format
        variation['question_text'] = "What is the measurement of this angle?\n___°"
        
        # Update the correct answer
        variation['correct_answers'] = [str(angle)]
        
        # Update image tag
        variation['image_tag'] = f"Gr6_50_1_{i+1}"
        
        # Update backend description with the new angle
        if angle < 90:
            angle_type = "acute"
        elif angle == 90:
            angle_type = "right"
        elif angle < 180:
            angle_type = "obtuse"
        else:
            angle_type = "straight"
            
        variation['backend_description'] = (
            f"This image shows a protractor measuring an {angle_type} angle. "
            f"One ray extends horizontally to the left, passing through the 0° and 180° marks, "
            f"while the other ray extends upward and to the right, passing through the {angle}° mark "
            f"on the outer scale. The vertex of the angle is centered at the midpoint of the protractor."
        )
        
        # Update solution with the new angle
        variation['solution'] = [
            [
                "1/2",
                "One ray is lined up with 0°. Follow the other ray to find the angle measurement."
            ],
            [
                "2/2",
                f"This angle measures {angle}°."
            ]
        ]
        
        variations.append(variation)
    
    # Save variations to file
    output_file = 'Gr6_50_E1_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(variations)} variations for Gr6_50_E1")
    print(f"Saved to {output_file}")
    
    # Verify total count
    print(f"Template: 1 + Variations: {len(variations)} = Total: {1 + len(variations)}")

if __name__ == "__main__":
    generate_angle_variations()