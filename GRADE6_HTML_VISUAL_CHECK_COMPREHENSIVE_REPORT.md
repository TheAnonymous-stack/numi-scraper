# Grade 6 HTML Visual Components - Comprehensive Quality Check Report

## Executive Summary

A comprehensive check was performed on all Grade 6 math question JSON files to verify the existence and quality of corresponding HTML visual components. The check examined 168 JSON files containing 8,514 questions, of which 3,934 questions require visual HTML components.

### Key Findings

- **Total Files Checked:** 168 Grade 6 JSON files
- **Total Questions:** 8,514
- **Questions Requiring Images:** 3,934 (46.2%)
- **Questions with Valid HTML:** 834 (21.2% of questions with images)
- **Questions with Issues:** 3,100 (78.8% of questions with images)
- **Success Rate:** 21.2%

## Issue Categories

### 1. Missing HTML Files (949 issues - 30.6%)
Many questions with image requirements do not have corresponding HTML files. The expected naming convention is:
- Expected: `HTML/Gr6_{week}_E{exercise} {question_number}.html`
- Alternative found: `HTML/Gr6_{week}_E{exercise}_{question_number}.html`

### 2. Missing Divs (2,151 issues - 69.4%)
HTML files exist but are missing required div elements with proper labels. Common issues:
- Image tag labels don't match between JSON and HTML
- Missing divs for `image_tag` fields
- Missing divs for `image_choice_tags` arrays
- Missing divs for `solution_image_tag` elements

## Specific Issues by Exercise

### Files with Complete HTML Coverage (Examples)
- `Gr6_1_E1_variations.json` - All questions have HTML files
- `Gr6_1_E4_variations.json` - Most questions have HTML files
- `Gr6_1_E5_variations.json` - Partial HTML coverage

### Files with Major Issues

#### Gr6_15_E5_variations.json
- **Issue:** Label mismatch
- **Expected:** `label="Gr6_15_E5_variations_image_tag"`
- **Found:** `label="Gr6_15_5_2"` (incorrect format)
- **Action Required:** Update all HTML labels to match JSON specifications

#### Gr6_23_E3_variations.json
- **Issue:** Missing image choice tags
- **Expected:** Multiple divs for `image_choice_tags` array
- **Found:** HTML exists but missing required divs
- **Action Required:** Add divs for each image choice tag

#### Multiple Files (Gr6_10 through Gr6_55)
- **Issue:** No HTML files created
- **Action Required:** Generate HTML files for all questions with image requirements

## Label Format Discrepancies

### Current Inconsistencies Found:
1. **JSON Format:** `Gr6_15_E5_variations_image_tag`
2. **HTML Format Found:** `Gr6_15_5_2`
3. **Expected HTML Format:** Should match JSON exactly

## Required Actions

### Priority 1: Fix Label Mismatches
- Update all existing HTML files to use correct label format
- Ensure labels match exactly with JSON `image_tag` values
- Standardize naming convention across all files

### Priority 2: Create Missing HTML Files
- Generate HTML files for 949 questions missing visual components
- Use correct naming convention: `HTML/Gr6_{week}_E{exercise} {question_number}.html`

### Priority 3: Add Missing Divs
- Add 2,151 missing div elements to existing HTML files
- Ensure each div has:
  - `class="item"`
  - `label="{exact_tag_from_json}"`
  - Content matching the `backend_description`

## Validation Checklist

For each question with images, verify:
- [ ] HTML file exists with correct naming
- [ ] All `image_tag` fields have corresponding divs
- [ ] All `image_choice_tags` array items have divs
- [ ] All `solution_image_tag` items have divs
- [ ] Labels match exactly between JSON and HTML
- [ ] HTML content represents backend descriptions accurately

## Files Requiring Immediate Attention

Top 10 files with most issues:
1. Gr6_23_E3_variations.json - Multiple missing image choice tags
2. Gr6_15_E5_variations.json - Label format issues (51 questions)
3. Gr6_16_E1_variations.json - Partial HTML coverage
4. Gr6_17_E1_variations.json - Mixed naming conventions
5. Gr6_20_E2_variations.json - Missing HTML files
6. Gr6_28_E4_variations.json - No HTML files
7. Gr6_32_E5_variations.json - No HTML files
8. Gr6_38_E1_variations.json - Missing divs
9. Gr6_45_E1_variations.json - No HTML files
10. Gr6_52_E4_variations.json - No HTML files

## Recommendations

1. **Standardize Naming Convention:** Establish and enforce a single naming convention for HTML files and labels
2. **Automated Generation:** Consider using the existing HTML generation scripts to create missing files
3. **Validation Script:** Run this check regularly to ensure ongoing compliance
4. **Documentation:** Create a standard for HTML visual component structure

## Next Steps

1. Fix the 834 files that have HTML but incorrect labels (Quick Win)
2. Generate HTML for the 949 questions completely missing HTML files
3. Add the 2,151 missing div elements to existing HTML files
4. Re-run validation to ensure 100% compliance

## Success Metrics

Current State:
- Success Rate: 21.2%
- Questions with Issues: 3,100

Target State:
- Success Rate: 100%
- Questions with Issues: 0

---

*Report generated on 2025-09-06*
*Total execution time: Comprehensive check of 168 files containing 8,514 questions*