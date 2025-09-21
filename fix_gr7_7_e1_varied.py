import json
import random

def generate_varied_decimal_problems():
    """Generate varied decimal word problems for Gr7_7_E1"""

    with open('Gr7_7_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Different scenarios for word problems
    scenarios = [
        # Shopping scenarios
        {
            "context": "Sarah bought {item1} for ${price1} and {item2} for ${price2}.",
            "question": "How much did she spend in total?",
            "operation": "add",
            "items": [("a book", "12.75"), ("a pen", "3.49"), ("a notebook", "8.25"), ("a calculator", "24.99")]
        },
        {
            "context": "Mike had ${total}. He spent ${spent} on {item}.",
            "question": "How much money does he have left?",
            "operation": "subtract",
            "items": [("groceries", "45.67", "100.00"), ("games", "32.99", "75.50"), ("clothes", "67.25", "150.00")]
        },

        # Distance/measurement scenarios
        {
            "context": "Emma ran {dist1} km on Monday and {dist2} km on Tuesday.",
            "question": "How many kilometers did she run in total?",
            "operation": "add",
            "distances": [("3.5", "4.2"), ("2.75", "5.8"), ("6.25", "3.9")]
        },
        {
            "context": "A rope is {total} meters long. If {cut} meters is cut off,",
            "question": "how many meters of rope remain?",
            "operation": "subtract",
            "lengths": [("15.75", "3.25"), ("24.5", "8.75"), ("18.3", "6.45")]
        },

        # Weight scenarios
        {
            "context": "A recipe needs {amount1} kg of flour and {amount2} kg of sugar.",
            "question": "What is the total weight of these ingredients?",
            "operation": "add",
            "weights": [("2.5", "1.75"), ("3.25", "2.8"), ("1.45", "0.85")]
        },

        # Time scenarios
        {
            "context": "Tom studied for {time1} hours on Saturday and {time2} hours on Sunday.",
            "question": "How many hours did he study in total?",
            "operation": "add",
            "times": [("2.5", "3.75"), ("1.25", "2.5"), ("4.5", "3.25")]
        },

        # Multiplication scenarios
        {
            "context": "Each {item} costs ${price}. If you buy {quantity},",
            "question": "how much will you pay?",
            "operation": "multiply",
            "items": [("apple", "0.75", "6"), ("orange", "1.25", "4"), ("banana", "0.45", "8")]
        },
        {
            "context": "A car travels at {speed} km per hour for {time} hours.",
            "question": "How far does it travel?",
            "operation": "multiply",
            "speeds": [("65.5", "2.5"), ("72.25", "3"), ("58.75", "4")]
        },

        # Division scenarios
        {
            "context": "{total} liters of juice is poured equally into {containers} containers.",
            "question": "How many liters are in each container?",
            "operation": "divide",
            "amounts": [("7.5", "3"), ("12.6", "4"), ("15.75", "5")]
        },
        {
            "context": "A {length} meter board is cut into {pieces} equal pieces.",
            "question": "How long is each piece?",
            "operation": "divide",
            "lengths": [("8.4", "3"), ("15.6", "4"), ("22.5", "5")]
        }
    ]

    questions = []

    for i in range(51):
        # Cycle through different scenario types
        scenario_type = i % 10

        if scenario_type == 0:
            # Addition - Shopping
            items = [("a book", "12.75", "3.49", "a pen"),
                    ("a shirt", "24.99", "8.75", "a belt"),
                    ("a game", "35.50", "12.25", "a controller"),
                    ("a jacket", "45.75", "15.99", "a scarf"),
                    ("a watch", "89.99", "22.50", "a strap")]
            item = items[i % len(items)]
            num1, num2 = item[1], item[2]
            result = round(float(num1) + float(num2), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"Sarah bought {item[0]} for ${num1} and {item[3]} for ${num2}. How much did she spend in total?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the total amount spent, add the two prices: ${num1} + ${num2}"],
                    ["2/2", f"${num1} + ${num2} = ${result}"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif scenario_type == 1:
            # Subtraction - Money left
            amounts = [("100.00", "45.67"), ("75.50", "32.99"), ("150.00", "67.25"),
                      ("200.00", "89.75"), ("50.00", "18.45")]
            amount = amounts[i % len(amounts)]
            total, spent = amount[0], amount[1]
            result = round(float(total) - float(spent), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"Mike had ${total}. He spent ${spent} on groceries. How much money does he have left?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find how much money is left, subtract the amount spent from the total: ${total} - ${spent}"],
                    ["2/2", f"${total} - ${spent} = ${result}"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif scenario_type == 2:
            # Addition - Distance
            distances = [("3.5", "4.2"), ("2.75", "5.8"), ("6.25", "3.9"),
                        ("4.5", "7.25"), ("8.75", "2.5")]
            dist = distances[i % len(distances)]
            d1, d2 = dist[0], dist[1]
            result = round(float(d1) + float(d2), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"Emma ran {d1} km on Monday and {d2} km on Tuesday. How many kilometers did she run in total?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the total distance, add the two distances: {d1} km + {d2} km"],
                    ["2/2", f"{d1} + {d2} = {result} km"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif scenario_type == 3:
            # Subtraction - Rope length
            lengths = [("15.75", "3.25"), ("24.5", "8.75"), ("18.3", "6.45"),
                      ("30.25", "12.5"), ("22.8", "9.35")]
            length = lengths[i % len(lengths)]
            total, cut = length[0], length[1]
            result = round(float(total) - float(cut), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"A rope is {total} meters long. If {cut} meters is cut off, how many meters of rope remain?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the remaining length, subtract the cut length from the total: {total} m - {cut} m"],
                    ["2/2", f"{total} - {cut} = {result} meters"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif scenario_type == 4:
            # Multiplication - Cost
            items = [("0.75", "6"), ("1.25", "4"), ("0.45", "8"), ("2.35", "3"), ("1.85", "5")]
            item = items[i % len(items)]
            price, qty = item[0], item[1]
            result = round(float(price) * float(qty), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"Each apple costs ${price}. If you buy {qty} apples, how much will you pay?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the total cost, multiply the price by the quantity: ${price} × {qty}"],
                    ["2/2", f"${price} × {qty} = ${result}"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif scenario_type == 5:
            # Division - Liquid
            amounts = [("7.5", "3"), ("12.6", "4"), ("15.75", "5"), ("18.9", "6"), ("22.4", "7")]
            amount = amounts[i % len(amounts)]
            total, containers = amount[0], amount[1]
            result = round(float(total) / float(containers), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"{total} liters of juice is poured equally into {containers} containers. How many liters are in each container?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the amount in each container, divide the total by the number of containers: {total} L ÷ {containers}"],
                    ["2/2", f"{total} ÷ {containers} = {result} liters"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif scenario_type == 6:
            # Addition - Weight
            weights = [("2.5", "1.75"), ("3.25", "2.8"), ("1.45", "0.85"), ("4.65", "3.35"), ("5.25", "2.45")]
            weight = weights[i % len(weights)]
            w1, w2 = weight[0], weight[1]
            result = round(float(w1) + float(w2), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"A recipe needs {w1} kg of flour and {w2} kg of sugar. What is the total weight of these ingredients?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the total weight, add the two weights: {w1} kg + {w2} kg"],
                    ["2/2", f"{w1} + {w2} = {result} kg"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif scenario_type == 7:
            # Multiplication - Distance
            speeds = [("65.5", "2.5"), ("72.25", "3"), ("58.75", "4"), ("45.5", "3.5"), ("82.4", "2")]
            speed = speeds[i % len(speeds)]
            spd, time = speed[0], speed[1]
            result = round(float(spd) * float(time), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"A car travels at {spd} km per hour for {time} hours. How far does it travel?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the distance, multiply speed by time: {spd} km/h × {time} h"],
                    ["2/2", f"{spd} × {time} = {result} km"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        elif scenario_type == 8:
            # Division - Board cutting
            lengths = [("8.4", "3"), ("15.6", "4"), ("22.5", "5"), ("31.2", "6"), ("18.2", "7")]
            length = lengths[i % len(lengths)]
            total, pieces = length[0], length[1]
            result = round(float(total) / float(pieces), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"A {total} meter board is cut into {pieces} equal pieces. How long is each piece?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the length of each piece, divide the total length by the number of pieces: {total} m ÷ {pieces}"],
                    ["2/2", f"{total} ÷ {pieces} = {result} meters"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        else:
            # Addition - Time studied
            times = [("2.5", "3.75"), ("1.25", "2.5"), ("4.5", "3.25"), ("3.75", "2.25"), ("5.5", "1.75")]
            time = times[i % len(times)]
            t1, t2 = time[0], time[1]
            result = round(float(t1) + float(t2), 2)

            question = {
                "skills": "add-subtract-multiply-and-divide-decimals-word-problems",
                "question_text": f"Tom studied for {t1} hours on Saturday and {t2} hours on Sunday. How many hours did he study in total?",
                "question_type": "Fill in the blank",
                "correct_answers": [str(result)],
                "solution": [
                    ["1/2", f"To find the total study time, add the two times: {t1} hours + {t2} hours"],
                    ["2/2", f"{t1} + {t2} = {result} hours"]
                ],
                "tag": "Gr7_7_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_7_E1_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 varied decimal word problems for Gr7_7_E1")

# Run the fix
generate_varied_decimal_problems()
print("Fixed Gr7_7_E1 with varied word problems")