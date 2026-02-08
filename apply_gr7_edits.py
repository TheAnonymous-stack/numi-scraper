import os
import shutil

# List of files that were edited
edited_files = [
    'Gr7_5_E2_variations.json',
    'Gr7_5_E3_variations.json',
    'Gr7_6_E2_variations.json',
    'Gr7_7_E3_variations.json',
    'Gr7_13_E1_variations.json',
    'Gr7_13_E2_variations.json',
    'Gr7_14_E1_variations.json',
    'Gr7_14_E2_variations.json',
    'Gr7_15_E1_variations.json',
    'Gr7_15_E2_variations.json',
    'Gr7_16_E1_variations.json',
    'Gr7_16_E2_variations.json',
    'Gr7_17_E2_variations.json',
    'Gr7_20_E1_variations.json',
    'Gr7_20_E2_variations.json',
    'Gr7_20_E3_variations.json',
    'Gr7_22_E1_variations.json',
    'Gr7_22_E3_variations.json',
    'Gr7_22_E4_variations.json',
    'Gr7_27_E3_variations.json',
    'Gr7_35_E2_variations.json',
]

print("=" * 80)
print("APPLYING EDITS TO MAIN FILES AND REORGANIZING")
print("=" * 80)

for filename in edited_files:
    # Extract tag from filename
    tag = filename.replace('_variations.json', '').replace('.json', '')

    # Paths
    edited_path = f'edited_by_tag/{tag}/{filename.replace(".json", "_edited.json")}'
    original_path = f'edited_by_tag/{tag}/{filename.replace(".json", "_original.json")}'
    tag_edited_only = f'edited_by_tag/{tag}/{tag}_edited.json'
    main_file_path = filename

    if os.path.exists(edited_path):
        print(f"\nProcessing {filename}...")

        # Step 1: Copy edited version back to main directory (replace original)
        shutil.copy(edited_path, main_file_path)
        print(f"  Copied edited version to main directory: {main_file_path}")

        # Step 2: Rename edited file to just {tag}_edited.json
        if os.path.exists(tag_edited_only):
            os.remove(tag_edited_only)
        os.rename(edited_path, tag_edited_only)
        print(f"  Renamed to: {tag_edited_only}")

        # Step 3: Remove the original file from edited_by_tag
        if os.path.exists(original_path):
            os.remove(original_path)
            print(f"  Removed original backup from edited_by_tag")
    else:
        print(f"\nWARNING: {edited_path} not found, skipping...")

print("\n" + "=" * 80)
print("DONE!")
print("=" * 80)
print("Main files have been updated with edited versions")
print("edited_by_tag/ now contains only *_edited.json files")
