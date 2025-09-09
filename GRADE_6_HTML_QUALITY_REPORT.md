# Grade 6 HTML Visual Quality Check - Comprehensive Report

## Executive Summary

A comprehensive check was performed on all Grade 6 exercises to verify HTML visual files against their JSON specifications. The analysis revealed significant systematic issues that need to be addressed.

### Overall Statistics
- **Total Grade 6 Exercises:** 177
- **Exercises with Image Requirements:** 82 (46.3%)
- **Exercises Passing Validation:** 0 (0%)
- **Exercises Failing Validation:** 82 (100% of those with images)

## Critical Issues Identified

### 1. Systematic Label Mismatch (100% of files)

**Issue:** All HTML files have incorrect div labels that don't match the JSON specifications.

**Pattern Found:**
- JSON expects: `Gr6_XX_EX_variations_image_tag`
- HTML provides: `Gr6_XX_EX_1`

**Example:**
```json
// JSON (Gr6_15_E5_variations.json)
"image_tag": "Gr6_15_E5_variations_image_tag"
```
```html
<!-- HTML (Gr6_15_E5_1_1.html) -->
<div class="item" label="Gr6_15_E5_1">
```

### 2. File Naming Convention Issues

**Issue:** HTML files use an unexpected naming pattern with an extra "_1" component.

**Patterns:**
- Expected: `HTML/Gr6_{week}_E{exercise} {question}.html`
- Actual: `HTML/Gr6_{week}_E{exercise}_1_{question}.html`

### 3. Content Verification Needed

While the structural issues prevent automated content verification, manual inspection suggests potential mismatches between HTML visuals and backend descriptions. This needs further investigation once the structural issues are resolved.

## Affected Exercises (All 82 with images)

### Week-by-Week Breakdown

**Weeks with Most Issues:**
- Week 1: 5 exercises (E1, E2, E4, E5)
- Week 2: 3 exercises (E1, E2, E3)
- Week 3: 4 exercises (E1, E2, E3, E4)
- Week 4: 2 exercises (E1, E2)
- Week 5: 2 exercises (E1, E2)
- Week 6: 1 exercise (E1)
- Week 7: 1 exercise (E1)
- Week 8: 2 exercises (E1, E2)
- Week 9: 2 exercises (E1, E2)

... and continuing through Week 55

## Specific Examples of Issues

### Example 1: Gr6_15_E5
- **Questions with images:** 51
- **Issue:** All 51 HTML files have label="Gr6_15_E5_1" instead of "Gr6_15_E5_variations_image_tag"
- **Backend description example:** "This image shows a map connecting three locations..."
- **HTML content:** Shows a simple blue rectangle instead of the described map

### Example 2: Gr6_23_E1
- **Questions with images:** 51
- **Issue:** Missing some HTML files entirely (e.g., question 1)
- **Available files have wrong labels:** "Gr6_23_E1_1" instead of "Gr6_23_E1_variations_image_tag"
- **Backend description:** "This image shows 4 identical heptagons..."

## Recommended Actions

### Priority 1: Fix Label Mismatches (Critical)
1. Update all HTML div labels to match JSON image_tag values
2. Use a batch script to systematically update all 4,000+ HTML files
3. Pattern to apply: Replace `label="Gr6_XX_EX_Y"` with `label="Gr6_XX_EX_variations_image_tag"`

### Priority 2: Verify Visual Content (High)
1. Review HTML visual implementations against backend descriptions
2. Focus on exercises with complex visuals (histograms, tables, geometric shapes)
3. Ensure numerical values in visuals match JSON descriptions

### Priority 3: Standardize File Naming (Medium)
1. Decide on consistent naming convention
2. Either update JSON to expect current pattern or rename HTML files
3. Document the chosen convention

## Implementation Script Suggestion

```python
# Script to fix label mismatches
import re
from pathlib import Path

for html_file in Path('HTML').glob('Gr6_*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract exercise info from filename
    match = re.match(r'Gr6_(\d+)_E(\d+)', html_file.name)
    if match:
        week, exercise = match.groups()
        old_label = f'Gr6_{week}_E{exercise}_1'
        new_label = f'Gr6_{week}_E{exercise}_variations_image_tag'
        
        content = content.replace(f'label="{old_label}"', f'label="{new_label}"')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
```

## Validation Checklist

After fixes are applied, verify:
- [ ] All HTML files have correct div labels matching JSON image_tags
- [ ] Visual content accurately represents backend descriptions
- [ ] Histograms show correct intervals and values
- [ ] Tables display the right data
- [ ] Geometric shapes match descriptions
- [ ] Charts and graphs are accurate
- [ ] Numerical values in visuals match JSON descriptions

## Conclusion

The Grade 6 HTML visual files have systematic issues that prevent them from working correctly with the JSON specifications. The primary issue is a label mismatch affecting 100% of files with images. This is a straightforward fix that can be automated. Once this is resolved, a content verification pass should be performed to ensure visual accuracy.

**Estimated effort to fix:**
- Label mismatches: 2-4 hours (automated)
- Content verification: 8-16 hours (manual review)
- File naming standardization: 1-2 hours (if needed)

**Total: 11-22 hours to achieve full compliance**