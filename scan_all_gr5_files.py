import json
import os
import re

# Find all Gr5_*_E*_variations.json files
all_files = []
for filename in os.listdir('.'):
    if re.match(r'Gr5_\d+_E\d+_variations\.json', filename):
        all_files.append(filename)

# Sort them by number
def get_numbers(filename):
    match = re.match(r'Gr5_(\d+)_E(\d+)_variations\.json', filename)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return (0, 0)

all_files.sort(key=get_numbers)

print(f"Found {len(all_files)} Gr5 files to scan\n")
print("="*80)

issues_found = []

for filename in all_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        file_issues = []

        # Check 1: Is it nested under "quizzes"?
        if isinstance(data, dict) and "quizzes" in data:
            questions = data["quizzes"]
            nested = True
        elif isinstance(data, list):
            questions = data
            nested = False
            file_issues.append("NOT nested under 'quizzes' key")
        else:
            file_issues.append("UNEXPECTED data structure")
            questions = []

        # Check 2: Count questions
        question_count = len(questions)

        # Check 3: Check for common issues in questions
        if questions:
            # Sample first question for quick checks
            first_q = questions[0]

            # Check if question_text exists
            if 'question_text' not in first_q:
                file_issues.append("Missing 'question_text' field")

            # Check if it's a money question without $ signs
            if 'add-and-subtract-money-amounts' in first_q.get('skills', ''):
                q_text = first_q.get('question_text', '')
                if '.' in q_text and '$' not in q_text and 'dollars' not in q_text.lower():
                    file_issues.append("Money question possibly missing $ signs")

            # Check for fraction answers
            has_fraction_answers = False
            has_mixed_fractions = False
            for q in questions[:5]:  # Check first 5 questions
                answers = q.get('correct_answers', [])
                if isinstance(answers, list):
                    for ans in answers:
                        if isinstance(ans, str):
                            if '/' in ans:
                                has_fraction_answers = True
                                if ' ' in ans and '/' in ans:
                                    has_mixed_fractions = True

            if has_fraction_answers:
                # Check if fractions are in the right format
                sample_with_fraction = None
                for q in questions[:10]:
                    answers = q.get('correct_answers', [])
                    if isinstance(answers, list) and len(answers) == 2:
                        if isinstance(answers[0], str) and isinstance(answers[1], str):
                            if answers[0].isdigit() and answers[1].isdigit():
                                # This is the new format (numerator, denominator split)
                                break
                    if isinstance(answers, list) and len(answers) > 0:
                        if isinstance(answers[0], str) and '/' in answers[0]:
                            sample_with_fraction = answers[0]
                            break

                if sample_with_fraction and not has_mixed_fractions:
                    file_issues.append(f"Has fraction answers (e.g., '{sample_with_fraction}') - may need transformation")

        # Print summary
        if file_issues:
            print(f"⚠️  {filename}")
            print(f"    Questions: {question_count}")
            for issue in file_issues:
                print(f"    - {issue}")
            print()
            issues_found.append((filename, file_issues))
        else:
            # Only show files without issues if they're significant
            if not nested:
                print(f"⚠️  {filename}")
                print(f"    Questions: {question_count}")
                print(f"    - NOT nested under 'quizzes' key")
                print()
                issues_found.append((filename, ["NOT nested under 'quizzes' key"]))

    except json.JSONDecodeError as e:
        print(f"❌ {filename}")
        print(f"    JSON DECODE ERROR: {e}")
        print()
        issues_found.append((filename, [f"JSON decode error: {e}"]))
    except FileNotFoundError:
        print(f"❌ {filename}")
        print(f"    FILE NOT FOUND")
        print()
        issues_found.append((filename, ["File not found"]))
    except Exception as e:
        print(f"❌ {filename}")
        print(f"    ERROR: {e}")
        print()
        issues_found.append((filename, [f"Error: {e}"]))

print("="*80)
print(f"\nSCAN COMPLETE")
print(f"Total files scanned: {len(all_files)}")
print(f"Files with potential issues: {len(issues_found)}")

if issues_found:
    print("\nSUMMARY OF ISSUES:")
    print("-"*80)

    # Group by issue type
    not_nested = []
    has_fractions = []
    missing_dollars = []
    other_issues = []

    for filename, issues in issues_found:
        for issue in issues:
            if "NOT nested" in issue:
                not_nested.append(filename)
            elif "fraction" in issue.lower():
                has_fractions.append(filename)
            elif "$ signs" in issue:
                missing_dollars.append(filename)
            else:
                other_issues.append((filename, issue))

    if not_nested:
        print(f"\n📦 Files NOT nested under 'quizzes' ({len(not_nested)}):")
        for f in not_nested[:10]:  # Show first 10
            print(f"   - {f}")
        if len(not_nested) > 10:
            print(f"   ... and {len(not_nested) - 10} more")

    if has_fractions:
        print(f"\n🔢 Files with fraction answers that may need transformation ({len(has_fractions)}):")
        for f in has_fractions[:10]:
            print(f"   - {f}")
        if len(has_fractions) > 10:
            print(f"   ... and {len(has_fractions) - 10} more")

    if missing_dollars:
        print(f"\n💵 Files possibly missing $ signs ({len(missing_dollars)}):")
        for f in missing_dollars:
            print(f"   - {f}")

    if other_issues:
        print(f"\n⚠️  Other issues ({len(other_issues)}):")
        for f, issue in other_issues[:5]:
            print(f"   - {f}: {issue}")
else:
    print("\n✅ No major issues found!")
