import json
import glob
import os

def consolidate_variations():
    """Consolidate all variations and templates into a single file"""

    # Load original templates
    with open('test.json', 'r', encoding='utf-8') as f:
        content = f.read()
        content = content.strip()
        if content.endswith(','):
            content = content[:-1]
        content = '[' + content + ']'
        templates = json.loads(content)

    print(f"Loaded {len(templates)} template questions")

    # Dictionary to store all questions by tag
    all_questions = {}

    # Add templates
    for template in templates:
        tag = template.get('tag', '')
        if tag:
            if tag not in all_questions:
                all_questions[tag] = []
            all_questions[tag].append(template)

    # Find all variation files for the tags in test.json
    tags_in_test = set(t.get('tag', '') for t in templates if t.get('tag'))

    for tag in tags_in_test:
        variation_file = f"{tag} variations.json"
        if os.path.exists(variation_file):
            with open(variation_file, 'r', encoding='utf-8') as f:
                variations = json.load(f)
                if tag not in all_questions:
                    all_questions[tag] = []
                all_questions[tag].extend(variations)
                print(f"  Added {len(variations)} variations for {tag}")

    # Create final consolidated list
    consolidated = []
    for tag in sorted(all_questions.keys()):
        questions = all_questions[tag]
        print(f"{tag}: {len(questions)} total questions (including templates)")
        consolidated.extend(questions)

    # Save consolidated file
    with open('all_variations_consolidated.json', 'w', encoding='utf-8') as f:
        json.dump(consolidated, f, indent=2, ensure_ascii=False)

    print(f"\nTotal questions generated: {len(consolidated)}")
    print("Consolidated file saved as: all_variations_consolidated.json")

    # Create summary report
    with open('generation_summary.txt', 'w', encoding='utf-8') as f:
        f.write("VARIATION GENERATION SUMMARY\n")
        f.write("=" * 50 + "\n\n")

        for tag in sorted(all_questions.keys()):
            questions = all_questions[tag]
            # Identify templates (original questions from test.json)
            templates = []
            variations = []
            for q in questions:
                qnum = q['question_number']
                # Original templates have specific numbers like 1_3, 2_1, 3_1, 4_1, 1_1
                if qnum in ['1_3', '2_1', '3_1', '4_1', '1_1']:
                    templates.append(q)
                else:
                    variations.append(q)

            f.write(f"{tag}:\n")
            f.write(f"  Templates: {len(templates)}\n")
            f.write(f"  Variations: {len(variations)}\n")
            f.write(f"  Total: {len(questions)}\n\n")

        f.write(f"GRAND TOTAL: {len(consolidated)} questions\n")

    print("\nSummary report saved as: generation_summary.txt")

if __name__ == "__main__":
    consolidate_variations()