import json
import re

# Mapping of shape names to their descriptions
SHAPE_DESCRIPTIONS = {
    "cube": {
        "net": "This image shows a net made of six connected squares. This is a 2D layout that can be folded along the dashed lines to form a 3D cube shape.",
        "step": "This image shows a net made up of six connected squares arranged in a cross shape. This is a 2D layout that can be folded along the dashed lines to form a 3D cube shape."
    },
    "triangular pyramid": {
        "net": "This image shows a net with one triangular base and three triangular faces. This is a 2D layout that can be folded along the dashed lines to form a 3D triangular pyramid shape.",
        "step": "This image shows a net made up of triangular shapes. This is a 2D layout that can be folded along the dashed lines to form a 3D triangular pyramid shape."
    },
    "square pyramid": {
        "net": "This image shows a net with one square base and four triangular faces. This is a 2D layout that can be folded along the dashed lines to form a 3D square pyramid shape.",
        "step": "This image shows a net made up of a square base with four triangular faces. This is a 2D layout that can be folded along the dashed lines to form a 3D square pyramid shape."
    },
    "rectangular prism": {
        "net": "This image shows a net made of six connected rectangles. This is a 2D layout that can be folded along the dashed lines to form a 3D rectangular prism shape.",
        "step": "This image shows a net made up of six connected rectangles arranged in a cross shape. This is a 2D layout that can be folded along the dashed lines to form a 3D rectangular prism shape."
    },
    "triangular prism": {
        "net": "This image shows a net with two triangular faces and three rectangular faces. This is a 2D layout that can be folded along the dashed lines to form a 3D triangular prism shape.",
        "step": "This image shows a net made up of two triangles and three rectangles. This is a 2D layout that can be folded along the dashed lines to form a 3D triangular prism shape."
    },
    "cylinder": {
        "net": "This image shows a net with two circular faces and one rectangular face. This is a 2D layout that can be folded along the dashed lines to form a 3D cylinder shape.",
        "step": "This image shows a net made up of two circles and one rectangle. This is a 2D layout that can be folded along the dashed lines to form a 3D cylinder shape."
    }
}

def extract_shape_from_text(text):
    """Extract the shape name from solution text"""
    text_lower = text.lower()

    # Check for each shape in order of specificity
    if "triangular pyramid" in text_lower:
        return "triangular pyramid"
    elif "square pyramid" in text_lower:
        return "square pyramid"
    elif "triangular prism" in text_lower:
        return "triangular prism"
    elif "rectangular prism" in text_lower:
        return "rectangular prism"
    elif "cylinder" in text_lower:
        return "cylinder"
    elif "cube" in text_lower:
        return "cube"

    return None

def is_correct_answer(text):
    """Check if this step describes the correct answer"""
    text_lower = text.lower()
    return "correct" in text_lower and "not" not in text_lower

def update_descriptions(input_file, output_file):
    """Update backend_description and solution_image_tag descriptions"""

    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    # Process each quiz
    for quiz in data['quizzes']:
        solution = quiz.get('solution', [])
        solution_image_tags = quiz.get('solution_image_tag', [])

        # Find the correct shape from solution text
        correct_shape = None
        for step in solution:
            if len(step) >= 2:
                step_text = step[1]
                if is_correct_answer(step_text):
                    shape = extract_shape_from_text(step_text)
                    if shape:
                        correct_shape = shape
                        break

        # Update backend_description with the correct shape
        if correct_shape and correct_shape in SHAPE_DESCRIPTIONS:
            quiz['backend_description'] = SHAPE_DESCRIPTIONS[correct_shape]['net']
            print(f"Updated backend_description for {quiz['question_number']}: {correct_shape}")

        # Update solution_image_tag descriptions based on corresponding solution text
        for i, img_tag in enumerate(solution_image_tags):
            if i < len(solution) and len(img_tag) >= 3 and len(solution[i]) >= 2:
                step_text = solution[i][1]

                # For step 1, use a generic description about folding the net
                if i == 0:
                    img_tag[2] = "This image shows the net with dotted lines indicating where to fold to create the 3D shape."
                    print(f"  Updated solution_image_tag {i+1} for {quiz['question_number']}: folding instruction")
                else:
                    # For other steps, extract the shape name
                    shape = extract_shape_from_text(step_text)
                    if shape and shape in SHAPE_DESCRIPTIONS:
                        # Use the step description for solution images
                        img_tag[2] = SHAPE_DESCRIPTIONS[shape]['step']
                        print(f"  Updated solution_image_tag {i+1} for {quiz['question_number']}: {shape}")
                    else:
                        # If no shape found, check previous step for the shape
                        # (this handles steps like "This is not the correct net")
                        if i > 0 and i-1 < len(solution_image_tags):
                            prev_step_text = solution[i-1][1] if i-1 < len(solution) else ""
                            prev_shape = extract_shape_from_text(prev_step_text)
                            if prev_shape and prev_shape in SHAPE_DESCRIPTIONS:
                                img_tag[2] = SHAPE_DESCRIPTIONS[prev_shape]['step']
                                print(f"  Updated solution_image_tag {i+1} for {quiz['question_number']}: {prev_shape} (from previous step)")

        updated_count += 1

    # Write the updated JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Updated {updated_count} quizzes")
    print(f"✓ Updated file saved to {output_file}")

if __name__ == "__main__":
    update_descriptions("output.json", "output.json")
