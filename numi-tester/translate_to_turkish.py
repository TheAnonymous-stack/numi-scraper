import json

# Load the English questions
with open("./scaled_questions.json", "r", encoding='utf-8') as f:
    data = json.load(f)

# Translation dictionaries
skill_translations = {
    "rectangle-perimeter-to-area": "Kenar uzunlukları doğal sayı olan bir dikdörtgenin çevre uzunluğu verildiğinde alanını yorumlayabilme",
    "rectangle-area-to-perimeter": "Kenar uzunlukları doğal sayı olan bir dikdörtgenin alanının ölçüsü verildiğinde çevre uzunluğunu yorumlayabilme"
}

# Common solution step translations
solution_translations = {
    "Identify what we know:": "Bildiklerimizi belirleyin:",
    "Perimeter (distance around the rectangle)": "Çevre (dikdörtgenin etrafındaki mesafe)",
    "Long side (length)": "Uzun kenar (uzunluk)",
    "Short side (width)": "Kısa kenar (genişlik)",
    "Area": "Alan",
    "Find the short side (width): The perimeter formula means going all the way around the rectangle. A rectangle has 4 sides: 2 long sides and 2 short sides": "Kısa kenarı (genişlik) bulun: Çevre formülü dikdörtgenin etrafında dolaşmak anlamına gelir. Bir dikdörtgenin 4 kenarı vardır: 2 uzun kenar ve 2 kısa kenar",
    "Since we are given perimeter is": "Bize çevre verildiğinden",
    "2 long sides + 2 short sides": "2 uzun kenar + 2 kısa kenar",
    "Each long side is": "Her uzun kenar",
    "so": "yani",
    "Simplify we get": "Sadeleştirirsek",
    "Subtracting": "Çıkarma",
    "on both sides, we get": "her iki taraftan, elde ederiz",
    "Dividing": "Bölme",
    "on both sides we get 1 short side": "her iki taraftan 1 kısa kenar elde ederiz",
    "Find the area: Area means how much space is inside the rectangle. Area = long side x short side": "Alanı bulun: Alan dikdörtgenin içindeki boşluk miktarı anlamına gelir. Alan = uzun kenar x kısa kenar",
    "The two different sides are consecutive natural numbers (like 5 and 6, or 9 and 10)": "İki farklı kenar ardışık doğal sayılardır (5 ve 6, veya 9 ve 10 gibi)",
    "Let's call the shorter side = n. Then the longer side = n + 1 because they're consecutive numbers": "Kısa kenarı n olarak adlandıralım. O zaman uzun kenar = n + 1 çünkü ardışık sayılardır",
    "Now we set up the equation. The perimeter formula means going all the way around the rectangle. A rectangle has 4 sides: 2 long sides and 2 short sides.": "Şimdi denklemi kuralım. Çevre formülü dikdörtgenin etrafında dolaşmak anlamına gelir. Bir dikdörtgenin 4 kenarı vardır: 2 uzun kenar ve 2 kısa kenar.",
    "Since shorter side = n and longer side = n + 1 (from step 2), we can plug it in to get:": "Kısa kenar = n ve uzun kenar = n + 1 olduğundan (adım 2'den), yerine koyabiliriz:",
    "Simplify:": "Sadeleştir:",
    "The short side is n": "Kısa kenar n",
    "and the long side is n + 1": "ve uzun kenar n + 1",
    "Find the area: Area means how much space is inside the rectangle. Area = long side x short side": "Alanı bulun: Alan dikdörtgenin içindeki boşluk miktarı anlamına gelir. Alan = uzun kenar x kısa kenar",
    "Both sides must be natural numbers (whole numbers like 1, 2, 3, 4": "Her iki kenar da doğal sayı olmalıdır (1, 2, 3, 4 gibi tam sayılar",
    "We need to find: The LARGEST possible area": "Bulmamız gereken: MÜMKÜN olan EN BÜYÜK alan",
    "We need to find: The SMALLEST possible area": "Bulmamız gereken: MÜMKÜN olan EN KÜÇÜK alan",
    "Find all possible combinations: If a perimeter": "Tüm olası kombinasyonları bulun: Eğer çevre",
    "then 2 long side + 2 short side": "o zaman 2 uzun kenar + 2 kısa kenar",
    "Dividing 2 on both sides, we get 1 long side + 1 short side": "Her iki tarafı 2'ye böldüğümüzde, 1 uzun kenar + 1 kısa kenar elde ederiz",
    "Let's list all possibilities where long side + short side": "uzun kenar + kısa kenar olduğu tüm olasılıkları listeleyelim",
    "Find the maximum: Looking at our table, the largest area is": "Maksimumu bulun: Tablomuza baktığımızda, en büyük alan",
    "when the rectangle is as close to a square as possible. Key: For a fixed perimeter, a rectangle has the largest area when it's as close to a square as possible!": "dikdörtgen mümkün olduğunca kareye yakın olduğunda. Anahtar: Sabit bir çevre için, dikdörtgen mümkün olduğunca kareye yakın olduğunda en büyük alana sahiptir!",
    "Find the minimum: Looking at our table, the smallest area is": "Minimumu bulun: Tablomuza baktığımızda, en küçük alan",
    "when the rectangle is": "dikdörtgen olduğunda",
    "Key: For a fixed perimeter, a rectangle has the smallest area when the sides are as different as possible (one very long, one very short)!": "Anahtar: Sabit bir çevre için, dikdörtgen kenarları mümkün olduğunca farklı olduğunda en küçük alana sahiptir (biri çok uzun, diğeri çok kısa)!",
    "Both rectangles have area": "Her iki dikdörtgenin de alanı",
    "First rectangle:": "Birinci dikdörtgen:",
    "Second rectangle: sides are natural numbers that are closest to each other": "İkinci dikdörtgen: kenarları birbirine en yakın doğal sayılardır",
    "We need to find: Perimeter of the second rectangle": "Bulmamız gereken: İkinci dikdörtgenin çevresi",
    "Find the perimeter: Looking at our table, the rectangle with sides closest to each other is": "Çevreyi bulun: Tablomuza baktığımızda, kenarları birbirine en yakın olan dikdörtgen",
    "Perimeter = 2 long side + 2 short side": "Çevre = 2 uzun kenar + 2 kısa kenar",
    "Both sides must be natural numbers (whole numbers like 1, 2, 3, 4...)": "Her iki kenar da doğal sayı olmalıdır (1, 2, 3, 4... gibi tam sayılar)",
    "We need to find: How many DIFFERENT rectangles": "Bulmamız gereken: Kaç farklı dikdörtgen",
    "We have": "Sahip olduğumuz",
    "different rectangles with area": "farklı dikdörtgen, alan",
    "Note: We count 25 × 1 and 1 × 25 as the SAME rectangle (just rotated), so we only count it once!": "Not: 25 × 1 ve 1 × 25'i AYNI dikdörtgen olarak sayarız (sadece döndürülmüş), bu yüzden sadece bir kez sayarız!",
    "We need to find: The LARGEST perimeter": "Bulmamız gereken: EN BÜYÜK çevre",
    "We need to find: The SMALLEST perimeter": "Bulmamız gereken: EN KÜÇÜK çevre",
    "Find the max perimeter: Looking at our table, the largest perimeter is": "Maksimum çevreyi bulun: Tablomuza baktığımızda, en büyük çevre",
    "when the sides are": "kenarlar olduğunda",
    "Key: For a fixed area, a rectangle has the largest perimeter when the sides are as different as possible (one very long, one very short)!": "Anahtar: Sabit bir alan için, dikdörtgen kenarları mümkün olduğunca farklı olduğunda en büyük çevreye sahiptir (biri çok uzun, diğeri çok kısa)!",
    "Find the min perimeter: Looking at our table, the smallest perimeter is": "Minimum çevreyi bulun: Tablomuza baktığımızda, en küçük çevre",
    "Key: For a fixed area, a rectangle has the smallest perimeter when the sides are as close as possible!": "Anahtar: Sabit bir alan için, dikdörtgen kenarları mümkün olduğunca yakın olduğunda en küçük çevreye sahiptir!",
    "cm": "cm",
    "cm²": "cm²",
    "rectangles": "dikdörtgen"
}

def translate_question_text(text):
    """Translate question text to Turkish"""
    # Template 1: Perimeter + one side
    if "What is the area" in text and "perimeter of" in text and "long side of" in text:
        import re
        match = re.search(r'perimeter of (\d+) cm and a long side of (\d+) cm', text)
        if match:
            perim, long = match.groups()
            return f"Çevresi {perim} cm ve uzun kenarı {long} cm olan bir dikdörtgenin alanı kaç $\\text{{cm}}^2$'dir?\n____ $\\text{{cm}}^2$"

    # Template 2: Consecutive sides
    if "consecutive natural numbers" in text:
        import re
        match = re.search(r'perimeter of (\d+) cm', text)
        if match:
            perim = match.group(1)
            return f"Çevresi {perim} cm olan bir dikdörtgenin kenar uzunlukları ardışık doğal sayılardır. Bu dikdörtgenin alanını bulunuz.\n____ $\\text{{cm}}^2$"

    # Template 3: Max area
    if "maximum area" in text:
        import re
        match = re.search(r'perimeter of (\d+) cm', text)
        if match:
            perim = match.group(1)
            return f"Çevresi {perim} cm olan bir dikdörtgenin kenar uzunlukları doğal sayılardır. Bu dikdörtgenin sahip olabileceği maksimum alanı bulunuz.\n____ $\\text{{cm}}^2$"

    # Template 4: Min area
    if "minimum area" in text and "square meters" in text:
        import re
        match = re.search(r'perimeter of (\d+) cm', text)
        if match:
            perim = match.group(1)
            return f"Çevresi {perim} cm olan bir dikdörtgenin kenar uzunlukları doğal sayılardır. Bu dikdörtgenin santimetrekare cinsinden minimum alanı nedir?\n____ $\\text{{cm}}^2$"

    if "minimum area" in text and "square centimeters" in text:
        import re
        match = re.search(r'area of (\d+) square centimeters', text)
        if match:
            area = match.group(1)
            return f"Kenar uzunlukları santimetre cinsinden doğal sayılar olan ve alanı {area} santimetre kare olan bir dikdörtgenin minimum çevresi santimetre cinsinden kaçtır?"

    # Template 5: Area + context → perimeter
    if "Two different rectangles have areas" in text and "closest natural numbers" in text:
        import re
        match = re.search(r'areas of (\d+).*?side lengths of (\d+) cm and (\d+) cm', text)
        if match:
            area, side1, side2 = match.groups()
            return f"İki farklı dikdörtgenin alanı {area} $\\text{{cm}}^2$'dir. Bir dikdörtgenin kenar uzunlukları {side1} cm ve {side2} cm'dir.\n\nDiğer dikdörtgenin kenar uzunlukları birbirine en yakın doğal sayılar ise, bu dikdörtgenin çevresi cm cinsinden kaçtır?\n\n____ cm"

    # Template 6: Count rectangles
    if "How many different rectangles" in text:
        import re
        match = re.search(r'area of (\d+)', text)
        if match:
            area = match.group(1)
            return f"Alanı {area} $\\text{{cm}}^2$ olan ve kenar uzunlukları doğal sayılar olan kaç farklı dikdörtgen çizilebilir?\n\n____ dikdörtgen"

    # Template 7: Max perimeter
    if "largest perimeter" in text:
        import re
        match = re.search(r'area of (\d+)', text)
        if match:
            area = match.group(1)
            return f"Alanı {area} $\\text{{cm}}^2$ olan ve kenar uzunlukları doğal sayılar olan dikdörtgenler arasında, en büyük çevreye sahip olanının çevresi cm cinsinden kaçtır?\n\n____ cm"

    return text

def translate_solution_step(step_text):
    """Translate solution step text to Turkish"""
    translated = step_text

    # Apply translations
    for eng, tur in solution_translations.items():
        translated = translated.replace(eng, tur)

    return translated

# Process all questions
turkish_quizzes = []

for q in data["quizzes"]:
    turkish_q = q.copy()

    # Translate skill
    turkish_q["skills"] = skill_translations.get(q["skills"], q["skills"])

    # Translate question text
    turkish_q["question_text"] = translate_question_text(q["question_text"])

    # Translate solution steps
    turkish_solution = []
    for step in q["solution"]:
        step_num = step[0]
        step_text = step[1]
        translated_text = translate_solution_step(step_text)
        turkish_solution.append([step_num, translated_text])

    turkish_q["solution"] = turkish_solution

    # Translate solution_image_tag descriptions
    if q["solution_image_tag"]:
        turkish_image_tags = []
        for img_tag in q["solution_image_tag"]:
            step_num, filename, description = img_tag
            # Keep filename same, translate description
            turkish_desc = translate_solution_step(description)
            turkish_image_tags.append([step_num, filename, turkish_desc])
        turkish_q["solution_image_tag"] = turkish_image_tags

    turkish_quizzes.append(turkish_q)

# Save to new file
output = {"quizzes": turkish_quizzes}
with open("/Users/hypebeast/clone/numi-scraper/numi-tester/scaled_questions_turkish_copy.json", "w", encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Created scaled_questions_turkish.json with {len(turkish_quizzes)} questions")
print("All question texts, solutions, and skills translated to Turkish")
