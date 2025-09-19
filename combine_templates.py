import json
from collections import defaultdict

# Load both JSON files
with open('C:/Users/kapil/numi-scraper/FORMAT_UPDATE4-gr7ScrapedQuestions(K7-W8).json', encoding='utf-8') as f:
    data1 = json.load(f)

with open('C:/Users/kapil/numi-scraper/FORMAT_UPDATE4-gr7ScrapedQuestions(W8-O10).json', encoding='utf-8') as f:
    data2 = json.load(f)

# Combine all questions
all_questions = data1 + data2

# Group questions by tag
questions_by_tag = defaultdict(list)
for question in all_questions:
    questions_by_tag[question['tag']].append(question)

# Save combined templates
with open('C:/Users/kapil/numi-scraper/all_templates.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, indent=2, ensure_ascii=False)

# Analyze and report
print(f"Total template questions: {len(all_questions)}")
print(f"Total unique tags: {len(questions_by_tag)}")
print("\nQuestions per tag:")

tag_info = []
for tag in sorted(questions_by_tag.keys()):
    questions = questions_by_tag[tag]
    question_numbers = [q.get('question_number', 'N/A') for q in questions]
    tag_info.append({
        'tag': tag,
        'template_count': len(questions),
        'variations_needed': 51 - len(questions),
        'question_numbers': question_numbers
    })
    print(f"{tag}: {len(questions)} templates, need {51 - len(questions)} variations")

# Save tag analysis
with open('C:/Users/kapil/numi-scraper/tag_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(tag_info, f, indent=2)

print(f"\n✓ Combined templates saved to all_templates.json")
print(f"✓ Tag analysis saved to tag_analysis.json")