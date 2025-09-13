import json

def main():
    # Load the original templates
    print("Loading original templates...")
    
    template1 = {
        "skills": "estimate-sums-and-differences-word-problems",
        "question_text": "The Weston Public Library used a grant to purchase 13456 books. Now the library has a total of 72398 books. About how many books did the library have before the grant? Choose the better estimate.",
        "tag": "Gr6_14_E4",
        "question_number": "4_1",
        "question_type": "Multiple Choice Question with Single Answer",
        "choices": ["60000", "160000"],
        "correct_answers": ["A"],
        "solution": [
            ["1/5", "Subtract the number of books purchased from the total number of books.\n72398 - 13456 = ?"],
            ["2/5", "Round each number to the nearest ten thousand."],
            ["3/5", "72398 $\\rightarrow$ 70000\n13456 $\\rightarrow$ 10000"],
            ["4/5", "$72398 - 13456 \\rightarrow 70000 - 10000 =$?"],
            ["5/5", "$70000-10000= 60000$ \n60 000 is the better estimate."]
        ]
    }
    
    template2 = {
        "skills": "estimate-sums-and-differences-word-problems",
        "question_text": "A dust storm sweeps across the prairie. It covers 934 acres of the prairie in dust, but leaves 991 acres untouched. About how many acres does the prairie cover? Choose the better estimate.",
        "tag": "Gr6_14_E4",
        "question_number": "4_2",
        "question_type": "Multiple Choice Question with Single Answer",
        "choices": ["1900", "2400"],
        "correct_answers": ["A"],
        "solution": [
            ["1/6", "Add the acres.\n934 + 991 = ?"],
            ["2/6", "Round each number to the nearest hundred."],
            ["3/6", "934 $\\rightarrow$ 900\n991 $\\rightarrow$ 1000"],
            ["4/6", "$934+991 \\rightarrow 900+1000 = $?"],
            ["5/6", "900+1000=1900"],
            ["6/6", "1900 is the better estimate."]
        ]
    }
    
    # Load variations
    print("Loading variations...")
    with open('Gr6_14_E4_variations.json', 'r', encoding='utf-8') as f:
        variations = json.load(f)
    
    # Combine all questions
    all_questions = [template1, template2] + variations
    
    print(f"Total questions: {len(all_questions)}")
    
    # Save combined file
    output_file = "Gr6_14_E4_complete.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    
    print(f"Saved complete set to {output_file}")
    
    # Create a summary report
    print("\n" + "="*60)
    print("SUMMARY REPORT FOR Gr6_14_E4 VARIATIONS")
    print("="*60)
    print(f"Original templates: 2")
    print(f"Generated variations: {len(variations)}")
    print(f"Total questions: {len(all_questions)}")
    print(f"\nFiles created:")
    print(f"  - Gr6_14_E4_variations.json (49 variations only)")
    print(f"  - Gr6_14_E4_complete.json (all 51 questions)")
    print(f"  - HTML/ folder with 51 HTML files")
    print("\nQuestion types:")
    
    # Count operation types
    addition_count = 0
    subtraction_count = 0
    
    for q in all_questions:
        if "subtract" in q['solution'][0][1].lower() or "before" in q['question_text'].lower() or "left" in q['question_text'].lower():
            subtraction_count += 1
        else:
            addition_count += 1
    
    print(f"  - Addition problems: {addition_count}")
    print(f"  - Subtraction problems: {subtraction_count}")
    
    # Sample some themes used
    print("\nSample themes used in variations:")
    themes_seen = set()
    for q in variations[:20]:  # Check first 20 variations
        text = q['question_text']
        if "video game" in text.lower():
            themes_seen.add("Video games")
        elif "anime" in text.lower():
            themes_seen.add("Anime")
        elif "pokemon" in text.lower():
            themes_seen.add("Pokemon")
        elif "tiktok" in text.lower():
            themes_seen.add("TikTok")
        elif "youtube" in text.lower():
            themes_seen.add("YouTube")
        elif "library" in text.lower():
            themes_seen.add("Library")
        elif "school" in text.lower():
            themes_seen.add("School")
        elif "basketball" in text.lower() or "soccer" in text.lower():
            themes_seen.add("Sports")
        elif "forest" in text.lower() or "garden" in text.lower():
            themes_seen.add("Nature")
        elif "bakery" in text.lower() or "store" in text.lower():
            themes_seen.add("Business")
    
    for theme in list(themes_seen)[:5]:
        print(f"  - {theme}")
    
    print("\n" + "="*60)
    print("GENERATION COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()