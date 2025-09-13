import json

def generate_quiz_data():
    """Generate all 51 quiz questions with proper formatting"""
    
    # Define all the problems
    problems = [
        (5, 54, 2), (5, 48, 2), (18, 93, 30), (5, 104, 10), (34, 30, 17),
        (5, 52, 25), (33, 51, 29), (7864, 27, 2), (14329, 69, 2), (5, 101, 44),
        (53, 5138, 2), (38, 91, 16), (334, 334, 36), (15, 92, 2), (414, 84, 2),
        (12, 96, 2), (5, 261, 2), (5, 86, 35), (3, 21, 2), (5, 75, 3024),
        (35, 90, 18), (438, 63, 23), (5, 19, 14), (5, 318, 2), (5, 100, 45),
        (5, 64, 2), (5, 15, 14), (5, 83, 48), (5, 55, 145), (38, 73, 48),
        (5, 93, 41), (41, 941, 7), (5, 718, 2), (5, 17, 18), (51, 40, 34),
        (5, 9, 2), (6, 49, 10), (15, 48, 3), (6, 60, 12), (6, 37, 14),
        (34, 38, 2), (7, 64, 38), (5, 91, 438), (348, 85, 6), (18, 59, 18),
        (5, 9, 35), (5, 18, 11), (5, 37, 14), (5, 100, 2), (7, 71, 5), (7, 43, 9)
    ]
    
    quizzes = []
    
    for idx, (num1, num2, num3) in enumerate(problems, 1):
        # Determine which number to rearrange (usually the smaller one goes first)
        if num1 <= num3:
            first_blank = num1
            middle_num = num2
            last_num = num3
            product_inside = num1 * num3
        else:
            first_blank = num3
            middle_num = num2
            last_num = num1
            product_inside = num1 * num3
            
        final_answer = num1 * num2 * num3
        
        # For problems 50 and 51, fix the specific values
        if idx == 50:  # 7 × 71 × 5
            first_blank = 7
            middle_num = 71
            last_num = 5
            product_inside = 35
            final_answer = 2485
        elif idx == 51:  # 7 × 43 × 9
            first_blank = 7
            middle_num = 43
            last_num = 9
            product_inside = 63
            final_answer = 2709
        
        quiz = {
            "skills": "multiply-using-properties",
            "question_text": f"""Use properties to find the product.
${num1} \\cdot {num2} \\cdot {num3}$
$= {middle_num} \\cdot$ _____ $\\cdot {last_num}$
$= {middle_num} \\cdot ($ _____ $\\cdot {last_num})$
$= {middle_num} \\cdot$ _____
$=$ _____""",
            "tag": "Gr6_12_E2",
            "question_number": f"2_{idx}",
            "question_type": "Multiple fill in the blank",
            "orderMatter": "TRUE",
            "correct_answers": [
                str(first_blank),
                str(first_blank),
                str(product_inside),
                str(final_answer)
            ],
            "solution": [
                ["1/4", f"Use properties to find ${num1} \\cdot {num2} \\cdot {num3}$"],
                ["2/4", f"Rearrange using commutative property: ${middle_num} \\cdot {first_blank} \\cdot {last_num}$"],
                ["3/4", f"Group using associative property: ${middle_num} \\cdot ({first_blank} \\cdot {last_num}) = {middle_num} \\cdot {product_inside}$"],
                ["4/4", f"Final calculation: ${middle_num} \\cdot {product_inside} = {final_answer}$"]
            ],
            "has_alternate_answers": True
        }
        
        quizzes.append(quiz)
    
    return {"quizzes": quizzes}

def main():
    """Generate and save the JSON file"""
    
    print("Regenerating Gr6_12_E2_variations.json...")
    
    data = generate_quiz_data()
    
    # Save to file
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E2_variations.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully regenerated {len(data['quizzes'])} questions")

if __name__ == "__main__":
    main()