import json
import re

def clean_question_text(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Patterns to remove
    patterns_to_remove = [
        r"During a Demon Slayer training session, ",
        r"While creating Attack on Titan wall designs, ",
        r"In a Genshin Impact puzzle room, ",
        r"While playing Fortnite building mode, ",
        r"In a Minecraft building challenge, ",
        r"During a Naruto ninja training, ",
        r"While designing Pokemon gym badges, ",
        r"In a Dragon Ball power level chart, ",
        r"During My Hero Academia hero training, ",
        r"While navigating One Piece treasure maps, ",
        r"In a Roblox building game, ",
        r"While playing Among Us map design, ",
        r"During a League of Legends match, ",
        r"In a Super Mario level design, ",
        r"While creating Zelda dungeon puzzles, ",
        r"During a [^,]+, ",  # Catch any other similar patterns
        r"While [^,]+, choose",  # Catch patterns before "choose"
        r"In a [^,]+, which",  # Catch patterns before "which"
        r"While [^,]+, which",  # Catch patterns before "which"
    ]
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            original = quiz['question_text']
            cleaned = original
            
            # Apply all removal patterns
            for pattern in patterns_to_remove:
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
            
            # Capitalize first letter if needed
            if cleaned and cleaned[0].islower():
                cleaned = cleaned[0].upper() + cleaned[1:]
            
            # Special case: if it starts with "choose" or "which", capitalize
            if cleaned.startswith("choose "):
                cleaned = "C" + cleaned[1:]
            
            quiz['question_text'] = cleaned
            
            # Debug output for changes
            if original != cleaned:
                print(f"Changed: {original[:50]}... -> {cleaned[:50]}...")
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Cleaned pop culture references from {filename}")

# Process the file
clean_question_text('Gr6_46_E1_variations.json')