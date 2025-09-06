import json
import os

def verify_variations():
    """Verify that all variation files are created correctly."""
    tags = ['Gr6_46_E2', 'Gr6_46_E3', 'Gr6_47_E1', 'Gr6_47_E2', 'Gr6_47_E3', 'Gr6_48_E1']
    
    # Load templates to count them
    with open('templates.json', 'r') as f:
        templates = json.load(f)
    
    template_counts = {}
    for q in templates:
        tag = q.get('tag')
        if tag not in template_counts:
            template_counts[tag] = 0
        template_counts[tag] += 1
    
    print('Verification Report:')
    print('=' * 50)
    
    total_variations = 0
    total_with_templates = 0
    
    for tag in tags:
        file = f'{tag}_variations.json'
        template_count = template_counts.get(tag, 0)
        
        if os.path.exists(file):
            with open(file) as f:
                data = json.load(f)
            
            variation_count = len(data)
            total_count = variation_count + template_count
            total_variations += variation_count
            total_with_templates += total_count
            
            print(f'{tag}:')
            print(f'  Templates: {template_count}')
            print(f'  Variations: {variation_count}')
            print(f'  Total: {total_count} (Target: 51)')
            
            if total_count == 51:
                print(f'  Status: CORRECT')
            else:
                print(f'  Status: INCORRECT (off by {51 - total_count})')
            print()
        else:
            print(f'{tag}: ERROR - {file} not found')
            print()
    
    print('=' * 50)
    print(f'Total variations generated: {total_variations}')
    print(f'Total with templates: {total_with_templates}')
    print(f'Expected total: 306 (51 per tag x 6 tags)')
    
    if total_with_templates == 306:
        print('\nALL VARIATIONS GENERATED SUCCESSFULLY!')
    else:
        print(f'\nMISSING {306 - total_with_templates} QUESTIONS')
        print('\nNeed to generate more variations for tags that are short.')

if __name__ == "__main__":
    verify_variations()