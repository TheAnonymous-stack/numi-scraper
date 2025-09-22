import json
import random

def generate_decimal_rounding_variations():
    """Generate 51 varied decimal rounding questions for Grade 7"""

    variations = []

    # Define different rounding scenarios
    rounding_scenarios = [
        # Small decimals (0.x to 9.x)
        {"number": 0.4, "round_to": "whole", "answer": "0", "round_type": "down"},
        {"number": 0.7, "round_to": "whole", "answer": "1", "round_type": "up"},
        {"number": 2.3, "round_to": "whole", "answer": "2", "round_type": "down"},
        {"number": 3.8, "round_to": "whole", "answer": "4", "round_type": "up"},
        {"number": 5.5, "round_to": "whole", "answer": "6", "round_type": "up"},
        {"number": 7.1, "round_to": "whole", "answer": "7", "round_type": "down"},
        {"number": 8.9, "round_to": "whole", "answer": "9", "round_type": "up"},

        # Two-digit numbers with decimals
        {"number": 12.4, "round_to": "whole", "answer": "12", "round_type": "down"},
        {"number": 15.6, "round_to": "whole", "answer": "16", "round_type": "up"},
        {"number": 23.5, "round_to": "whole", "answer": "24", "round_type": "up"},
        {"number": 37.2, "round_to": "whole", "answer": "37", "round_type": "down"},
        {"number": 48.7, "round_to": "whole", "answer": "49", "round_type": "up"},
        {"number": 56.3, "round_to": "whole", "answer": "56", "round_type": "down"},
        {"number": 69.8, "round_to": "whole", "answer": "70", "round_type": "up"},
        {"number": 74.1, "round_to": "whole", "answer": "74", "round_type": "down"},
        {"number": 89.5, "round_to": "whole", "answer": "90", "round_type": "up"},
        {"number": 91.4, "round_to": "whole", "answer": "91", "round_type": "down"},

        # Three-digit numbers
        {"number": 123.7, "round_to": "whole", "answer": "124", "round_type": "up"},
        {"number": 156.2, "round_to": "whole", "answer": "156", "round_type": "down"},
        {"number": 234.5, "round_to": "whole", "answer": "235", "round_type": "up"},
        {"number": 345.3, "round_to": "whole", "answer": "345", "round_type": "down"},
        {"number": 467.9, "round_to": "whole", "answer": "468", "round_type": "up"},
        {"number": 512.4, "round_to": "whole", "answer": "512", "round_type": "down"},
        {"number": 678.6, "round_to": "whole", "answer": "679", "round_type": "up"},
        {"number": 789.1, "round_to": "whole", "answer": "789", "round_type": "down"},
        {"number": 899.8, "round_to": "whole", "answer": "900", "round_type": "up"},

        # Rounding to nearest tenth
        {"number": 3.24, "round_to": "tenth", "answer": "3.2", "round_type": "down"},
        {"number": 5.67, "round_to": "tenth", "answer": "5.7", "round_type": "up"},
        {"number": 8.35, "round_to": "tenth", "answer": "8.4", "round_type": "up"},
        {"number": 12.43, "round_to": "tenth", "answer": "12.4", "round_type": "down"},
        {"number": 25.76, "round_to": "tenth", "answer": "25.8", "round_type": "up"},
        {"number": 34.52, "round_to": "tenth", "answer": "34.5", "round_type": "down"},
        {"number": 47.88, "round_to": "tenth", "answer": "47.9", "round_type": "up"},
        {"number": 56.21, "round_to": "tenth", "answer": "56.2", "round_type": "down"},
        {"number": 67.95, "round_to": "tenth", "answer": "68.0", "round_type": "up"},
        {"number": 78.14, "round_to": "tenth", "answer": "78.1", "round_type": "down"},
        {"number": 89.65, "round_to": "tenth", "answer": "89.7", "round_type": "up"},
        {"number": 123.44, "round_to": "tenth", "answer": "123.4", "round_type": "down"},
        {"number": 234.87, "round_to": "tenth", "answer": "234.9", "round_type": "up"},

        # Rounding to nearest hundredth
        {"number": 2.345, "round_to": "hundredth", "answer": "2.35", "round_type": "up"},
        {"number": 4.672, "round_to": "hundredth", "answer": "4.67", "round_type": "down"},
        {"number": 7.895, "round_to": "hundredth", "answer": "7.90", "round_type": "up"},
        {"number": 9.234, "round_to": "hundredth", "answer": "9.23", "round_type": "down"},
        {"number": 12.567, "round_to": "hundredth", "answer": "12.57", "round_type": "up"},
        {"number": 23.451, "round_to": "hundredth", "answer": "23.45", "round_type": "down"},
        {"number": 34.785, "round_to": "hundredth", "answer": "34.79", "round_type": "up"},
        {"number": 45.123, "round_to": "hundredth", "answer": "45.12", "round_type": "down"},
        {"number": 56.456, "round_to": "hundredth", "answer": "56.46", "round_type": "up"},
        {"number": 67.892, "round_to": "hundredth", "answer": "67.89", "round_type": "down"},
        {"number": 78.345, "round_to": "hundredth", "answer": "78.35", "round_type": "up"},
        {"number": 89.674, "round_to": "hundredth", "answer": "89.67", "round_type": "down"}
    ]

    # Generate 51 questions
    for i in range(1, 52):
        scenario = rounding_scenarios[i-1] if i <= len(rounding_scenarios) else random.choice(rounding_scenarios)

        # Create question text
        if scenario["round_to"] == "whole":
            question_text = f"What is {scenario['number']} rounded to the nearest whole number?\n\n"
            place_name = "ones"
            next_place = "tenths"
            digit_desc = f"the digit in the ones place"
        elif scenario["round_to"] == "tenth":
            question_text = f"What is {scenario['number']} rounded to the nearest tenth?\n\n"
            place_name = "tenths"
            next_place = "hundredths"
            digit_desc = f"the digit in the tenths place"
        else:  # hundredth
            question_text = f"What is {scenario['number']} rounded to the nearest hundredth?\n\n"
            place_name = "hundredths"
            next_place = "thousandths"
            digit_desc = f"the digit in the hundredths place"

        # Extract digits for solution explanation
        num_str = str(scenario["number"])
        parts = num_str.split('.')
        whole_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else "0"

        # Create solution based on rounding type
        if scenario["round_to"] == "whole":
            target_digit = whole_part[-1]
            decision_digit = decimal_part[0] if decimal_part else "0"
            if scenario["round_type"] == "up":
                round_explanation = f"Since {decision_digit} is 5 or greater, we must round up"
                if int(whole_part) + 1 == int(scenario["answer"]):
                    final_text = f"The final answer is {scenario['answer']}."
                else:
                    final_text = f"The final answer is {scenario['answer']}."
            else:
                round_explanation = f"Since {decision_digit} is less than 5, we must round down"
                final_text = f"The final answer is {scenario['answer']}."

            solution = [
                ["1/4", f"First, find {digit_desc}. This is the digit you want to round.\n\nIn this case it is the {target_digit} in {scenario['number']}."],
                ["2/4", f"When rounding, we will either round down to {whole_part} or round up to {int(whole_part)+1}. This decision will depend on the number in the {next_place} place ({decision_digit})."],
                ["3/4", f"{round_explanation}. Remove all digits right of the {place_name} place."],
                ["4/4", final_text]
            ]
        elif scenario["round_to"] == "tenth":
            target_digit = decimal_part[0] if decimal_part else "0"
            decision_digit = decimal_part[1] if len(decimal_part) > 1 else "0"
            base_tenth = f"{whole_part}.{target_digit}"
            if scenario["round_type"] == "up":
                next_tenth = f"{whole_part}.{int(target_digit)+1}" if int(target_digit) < 9 else f"{int(whole_part)+1}.0"
                round_explanation = f"Since {decision_digit} is 5 or greater, we must round up"
            else:
                next_tenth = f"{whole_part}.{int(target_digit)+1}" if int(target_digit) < 9 else f"{int(whole_part)+1}.0"
                round_explanation = f"Since {decision_digit} is less than 5, we must round down"

            solution = [
                ["1/4", f"First, find {digit_desc}. This is the digit you want to round.\n\nIn this case it is the {target_digit} in {scenario['number']}."],
                ["2/4", f"When rounding to the nearest tenth, we look at the {next_place} place ({decision_digit}) to make our decision."],
                ["3/4", f"{round_explanation}. Keep one decimal place."],
                ["4/4", f"The final answer is {scenario['answer']}."]
            ]
        else:  # hundredth
            target_digit = decimal_part[1] if len(decimal_part) > 1 else "0"
            decision_digit = decimal_part[2] if len(decimal_part) > 2 else "0"
            if scenario["round_type"] == "up":
                round_explanation = f"Since {decision_digit} is 5 or greater, we must round up"
            else:
                round_explanation = f"Since {decision_digit} is less than 5, we must round down"

            solution = [
                ["1/4", f"First, find {digit_desc}. This is the digit you want to round.\n\nIn this case it is the {target_digit} in {scenario['number']}."],
                ["2/4", f"When rounding to the nearest hundredth, we look at the {next_place} place ({decision_digit}) to make our decision."],
                ["3/4", f"{round_explanation}. Keep two decimal places."],
                ["4/4", f"The final answer is {scenario['answer']}."]
            ]

        # Create correct answers list
        correct_answers = [[scenario["answer"]]]
        # Add alternative formats for whole numbers
        if scenario["round_to"] == "whole":
            correct_answers.append([f"{scenario['answer']}.0"])
            correct_answers.append([f"{scenario['answer']}.00"])
        # Add alternative format for tenths (e.g., 3.0 can also be 3.00)
        elif scenario["round_to"] == "tenth" and scenario["answer"].endswith(".0"):
            correct_answers.append([f"{scenario['answer']}0"])

        question = {
            "skills": "round-decimals",
            "question_text": question_text,
            "question_type": "Fill in the blank",
            "has_alternative_answers": True,
            "correct_answers": correct_answers,
            "solution": solution,
            "tag": "Gr7_2_E3",
            "question_number": f"3_{i}",
            "image_tag": f"Gr7_2_3_{i}",
            "solution_image_tag": []
        }

        variations.append(question)

    return variations

def main():
    """Generate and save the variations"""
    print("Generating Grade 7 decimal rounding variations...")

    variations = generate_decimal_rounding_variations()

    # Create the JSON structure
    output = {
        "quizzes": variations
    }

    # Save to file
    output_path = "C:\\Users\\kapil\\numi-scraper\\Gr7_2_E3_variations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {len(variations)} variations")
    print(f"Saved to: {output_path}")

    # Print a sample for verification
    print("\nSample questions generated:")
    for i in [0, 10, 20, 30, 40, 50]:
        if i < len(variations):
            q = variations[i]
            print(f"  Question {q['question_number']}: {q['question_text'].strip()}")
            print(f"    Answer: {q['correct_answers'][0][0]}")

if __name__ == "__main__":
    main()