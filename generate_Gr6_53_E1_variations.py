import json
import random

def generate_gr6_53_e1_variations():
    """Generate 51 variations for Gr6_53_E1 - Volume of rectangular prisms"""
    variations = []
    
    # Generate 51 variations
    for i in range(1, 52):
        # Generate dimensions for rectangular prism
        if i <= 20:
            # Small whole numbers
            length = random.randint(2, 10)
            width = random.randint(2, 10)
            height = random.randint(2, 10)
        elif i <= 35:
            # Larger numbers
            length = random.randint(5, 20)
            width = random.randint(5, 15)
            height = random.randint(3, 12)
        else:
            # Mixed with some having same dimensions (cubes)
            if i % 3 == 0:
                # Cube
                side = random.randint(3, 15)
                length = width = height = side
            else:
                length = random.randint(4, 25)
                width = random.randint(4, 20)
                height = random.randint(3, 15)
        
        volume = length * width * height
        
        # Determine units
        units = ["centimetres", "metres", "inches", "feet"]
        unit = random.choice(units) if i > 10 else "centimetres"
        
        question_text = f"What is the volume of a rectangular prism with length {length} {unit}, width {width} {unit}, and height {height} {unit}?\\n___ cubic {unit}"
        
        # Add image tag for visual representation
        image_tag = f"Gr6_53_1_{i}"
        backend_description = f"This image shows a rectangular prism with length {length} {unit}, width {width} {unit}, and height {height} {unit}."
        
        question = {
            "skills": "volume-of-rectangular-prisms",
            "question_text": question_text,
            "image_tag": image_tag,
            "backend_description": backend_description,
            "tag": "Gr6_53_E1",
            "question_number": f"1_{i}",
            "question_type": "Fill in the blank",
            "correct_answers": [
                str(volume)
            ],
            "solution": [
                [
                    "1/6",
                    f"To find the volume of a rectangular prism, multiply length × width × height."
                ],
                [
                    "2/6",
                    f"Length = {length} {unit}"
                ],
                [
                    "3/6",
                    f"Width = {width} {unit}"
                ],
                [
                    "4/6",
                    f"Height = {height} {unit}"
                ],
                [
                    "5/6",
                    f"Volume = {length} × {width} × {height} = {volume}"
                ],
                [
                    "6/6",
                    f"The volume is {volume} cubic {unit}."
                ]
            ],
            "has_alternate_answers": False
        }
        
        variations.append(question)
    
    # Save to JSON file
    output = {"quizzes": variations}
    
    with open('Gr6_53_E1_variations.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Generated {len(output['quizzes'])} variations for Gr6_53_E1")

if __name__ == "__main__":
    generate_gr6_53_e1_variations()