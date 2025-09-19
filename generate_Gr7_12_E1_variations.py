import json
import random
import copy

def load_templates():
    """Load template questions from the original file"""
    with open(r'C:\Users\kapil\numi-scraper\file.json', 'r') as f:
        content = f.read().strip().rstrip(',')
        content = '[' + content + ']'
        data = json.loads(content)

    # Filter for Gr7_12_E1 templates
    templates = [q for q in data if q.get('tag') == 'Gr7_12_E1']
    return templates

def generate_variations(templates, num_variations=50):
    """Generate variations for adding/subtracting integers using counters"""
    variations = []

    # Generate 50 new variations (1_2 is template, so we need 1_3 through 1_52)
    for i in range(3, 53):
        # Random selection of operations
        operations = [
            (-2, 5), (-3, 7), (-4, 6), (-1, 3), (-5, 8),
            (-2, 3), (-4, 5), (-3, 4), (-6, 9), (-1, 5),
            (-3, 6), (-2, 7), (-5, 7), (-4, 8), (-1, 2),
            (-7, 10), (-3, 5), (-2, 4), (-6, 8), (-4, 7),
            (-5, 9), (-1, 6), (-3, 8), (-2, 6), (-8, 11),
            (-4, 9), (-5, 6), (-3, 9), (-6, 7), (-2, 8),
            (-7, 8), (-1, 7), (-4, 10), (-5, 11), (-6, 10),
            (-3, 10), (-7, 9), (-2, 9), (-8, 10), (-5, 10),
            (-6, 11), (-4, 11), (-7, 11), (-1, 8), (-8, 12),
            (-3, 11), (-9, 11), (-2, 10), (-7, 12), (-5, 12)
        ]

        # Get a unique operation for this variation
        neg, pos = operations[i-3]
        result = neg + pos

        # Create variation based on template
        var = copy.deepcopy(templates[0])

        # Update question text
        var['question_text'] = f"Use counters to add {neg} + {pos}.\\n\\nWhich picture shows the sum?\\n"

        # Update image tags
        var['image_tag'] = f"Gr7_12_1_{i}"
        var['backend_description'] = f"Shows a visual representation for adding {neg} + {pos} using counter symbols. Multiple choice options display different combinations of positive and negative counters."

        # Update image choice tags
        var['image_choice_tags'] = [
            f"Gr7_12_1_{i}_A",
            f"Gr7_12_1_{i}_B",
            f"Gr7_12_1_{i}_C",
            f"Gr7_12_1_{i}_D"
        ]

        # Create answer options (one correct, three distractors)
        abs_neg = abs(neg)
        abs_pos = abs(pos)

        # Rotate correct answer position
        correct_positions = ['A', 'B', 'C', 'D']
        correct_pos = correct_positions[i % 4]
        var['correct_answers'] = [correct_pos]

        # Generate choice descriptions
        choices_desc = []
        if result > 0:
            correct_desc = f"Shows {result} yellow circles with plus signs, representing +{result}"
        elif result < 0:
            correct_desc = f"Shows {abs(result)} red circles with minus signs, representing {result}"
        else:
            correct_desc = "Shows no circles remaining, representing 0"

        # Create distractors
        distractors = []
        if result != abs_pos:
            distractors.append(f"Shows {abs_pos} yellow circles with plus signs, representing +{abs_pos}")
        if result != neg:
            distractors.append(f"Shows {abs_neg} red circles with minus signs, representing {neg}")
        if result != (abs_pos - abs_neg) and (abs_pos - abs_neg) != result:
            diff = abs(abs_pos - abs_neg)
            if abs_pos > abs_neg:
                distractors.append(f"Shows {diff} yellow circles with plus signs, representing +{diff}")
            else:
                distractors.append(f"Shows {diff} red circles with minus signs, representing -{diff}")
        if result != (abs_pos + abs_neg):
            distractors.append(f"Shows {abs_pos + abs_neg} yellow circles with plus signs, representing +{abs_pos + abs_neg}")

        # Ensure we have exactly 3 distractors
        while len(distractors) < 3:
            rand_val = random.randint(1, 12)
            if rand_val != abs(result):
                if random.choice([True, False]):
                    distractors.append(f"Shows {rand_val} yellow circles with plus signs, representing +{rand_val}")
                else:
                    distractors.append(f"Shows {rand_val} red circles with minus signs, representing -{rand_val}")

        # Shuffle and limit to 3 distractors
        random.shuffle(distractors)
        distractors = distractors[:3]

        # Place correct answer in the right position
        all_choices = []
        distractor_idx = 0
        for pos in ['A', 'B', 'C', 'D']:
            if pos == correct_pos:
                all_choices.append(correct_desc)
            else:
                all_choices.append(distractors[distractor_idx])
                distractor_idx += 1

        var['image_choice_tags_backend_description'] = all_choices

        # Update solution image tags
        var['solution_image_tag'] = [
            ["2/6", f"Gr7_12_1_{i}_step_2", f"Shows {abs_neg} red circle{'s' if abs_neg > 1 else ''} with {'minus signs' if abs_neg > 1 else 'a minus sign'}, representing the starting value of {neg}."],
            ["3/6", f"Gr7_12_1_{i}_step_3", f"Shows {abs_neg} red circle{'s' if abs_neg > 1 else ''} ({neg}) and {abs_pos} yellow circles (+{pos}) together, representing {neg} + {pos}."],
            ["4/6", f"Gr7_12_1_{i}_step_4", f"Shows {min(abs_neg, abs_pos)} red and {min(abs_neg, abs_pos)} yellow circle{'s' if min(abs_neg, abs_pos) > 1 else ''} grouped together with an arrow, demonstrating how positive and negative counters cancel each other out as zero pair{'s' if min(abs_neg, abs_pos) > 1 else ''}."],
            ["5/6", f"Gr7_12_1_{i}_step_5", f"Shows {abs(result)} {'yellow' if result > 0 else 'red'} circle{'s' if abs(result) > 1 else ''} with {'plus' if result > 0 else 'minus'} sign{'s' if abs(result) > 1 else ''} remaining after removing the zero pair{'s' if min(abs_neg, abs_pos) > 1 else ''}, giving the final answer of {'+' if result > 0 else ''}{result}." if result != 0 else "Shows no circles remaining after removing all zero pairs, giving the final answer of 0."]
        ]

        # Update solution
        var['solution'] = [
            ["1/6", f"We are solving {neg} + {pos} using counters."],
            ["2/6", f"Start with {abs_neg} negative counter{'s' if abs_neg > 1 else ''} to represent {neg}."],
            ["3/6", f"Add {abs_pos} positive counter{'s' if abs_pos > 1 else ''} to represent +{pos}."],
            ["4/6", f"Pair {min(abs_neg, abs_pos)} negative and {min(abs_neg, abs_pos)} positive counter{'s' if min(abs_neg, abs_pos) > 1 else ''} together to make {'zero pairs' if min(abs_neg, abs_pos) > 1 else 'a zero pair'}, then remove them."],
            ["5/6", f"{abs(result)} {'positive' if result > 0 else 'negative'} counter{'s remain' if abs(result) > 1 else ' remains'}." if result != 0 else "No counters remain."],
            ["6/6", f"So {neg} + {pos} = {result}.\\nOption {correct_pos} is correct because it shows {abs(result)} {'positive' if result > 0 else 'negative'} counter{'s' if abs(result) > 1 else ''}." if result != 0 else f"So {neg} + {pos} = 0.\\nOption {correct_pos} is correct because it shows no counters remaining."]
        ]

        # Update question number
        var['question_number'] = f"1_{i}"

        variations.append(var)

    return variations

def save_variations(variations, tag):
    """Save variations to JSON file"""
    filename = f"{tag} variations.json"
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Saved {len(variations)} variations to {filename}")

def main():
    # Load templates
    templates = load_templates()
    print(f"Loaded {len(templates)} template(s) for Gr7_12_E1")

    # Generate variations
    variations = generate_variations(templates)

    # Save to file
    save_variations(variations, "Gr7_12_E1")

if __name__ == "__main__":
    main()