import base64
from playwright.sync_api import TimeoutError
def extract_question_text(page, json):
    # Wait for question section
    section = page.query_selector("div.question-component section.ixl-practice-crate")

    # Extract text
    text = section.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')  # gets all rendered (visible) text
    
    json["question_text"] = text

def extract_answer_fill_in_the_blank(page, json):
    
    
    # Fill wrong answer into input inside .math.section
    print("Locating the input field...")
    fill_in = page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn")
    for blank in fill_in:
        blank.fill("m")
        print("Wrong answer 'm' entered.")

    try:
        # Click the Submit button
        print("Clicking the Submit button...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return False

    try:
        print("Waiting for the correct answer section to appear...")
        page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
        print("Correct answer section appeared.")
    except TimeoutError:
        print("Correct answer section did not appear.")
        return False

    try:
        print("Extracting correct answer...")
        section = page.query_selector("div.correct-answer.ixl-practice-crate")
        value = section.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
        input_boxes = page.query_selector_all("div.correct-answer.ixl-practice-crate input.fillIn")
        if input_boxes:
            for box in input_boxes:
                value += box.evaluate("e => e.value").replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
        json['correct_answers'] = [value]
        section = page.query_selector("div.explanation-box section.tab-box.web.optional-tab-box.solve-box")
        explanation = section.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
        json['solution'] = explanation
        return True
    except Exception as e:
        print(f"Failed to extract correct answer: {e}")
        return False

def multiple_choices_loop(page, json):
    """
    Return True if selected the wrong option because wrong option will lead to answer with full explanation
    Return False if selected the right option
    """
    extract_question_text(page, json)
    try:
        print("Collecting all options...")
        options = page.query_selector_all("section.ixl-practice-crate div.responsive-info-higher-order-component div.LaidOutTiles div.SelectableTile.MULTIPLE_CHOICE")

    except TimeoutError:
        print("Error occurred while collecting options")
        return
    
    try:
        print("Extracting all options...")
        json["choices"] = []
        for i, option in enumerate(options):
            class_attr = option.get_attribute("class")
            if "nonInteractive" not in class_attr.split():
                json["choices"].append(option.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape'))
                # image_bytes = option.screenshot()
                # option.screenshot(path=f"option{i}.png")
                # image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                # json["choices"].append(image_b64)
    except Exception as e:
        print("Error while extracting options:", e)
        return
    
    try:
        print("Clicking first option")
        selected_option = options[0]
        selected_option.click()
    except Exception as e:
        print("Error occurred while clicking first option:", e)
        return
    
    try:
        # Click the Submit button
        print("Clicking the Submit button...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return
    try:
        print("Checking if selected option is false...")
        res = page.wait_for_selector("div.answer-box h2.feedback-header.correct", timeout=8000)
        text = res.inner_text()
        if "Sorry" in text:
            print("Selected option is confirmed to be false")
            try:
                options = page.query_selector_all("div.answer-box div.LaidOutTiles div.SelectableTile.MULTIPLE_CHOICE")
                answerFound = False
                i = 1
                while not answerFound:
                    class_attr = options[i].get_attribute("class")
                    if "selected" in class_attr.split():
                        json["correct_answers"] = [chr(i+65)]
                        print("Saved the index of the answer in options")
                        answerFound = True
                    i += 1
                section = page.query_selector("div.explanation-box section.tab-box.web.optional-tab-box.solve-box")
                explanation = section.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
                json['solution'] = explanation
                return True # Selected wrong option and extracted answer with full explanation
            
            except Exception as e:
                print("Error while searching for answer:", e)
                return

    except TimeoutError:
        incomplete_answer = page.query_selector("div.incomplete-answer-popover-content")
        if incomplete_answer:
            return
        print("Selected the right option. Reloading for a different question...")
        return False

def extract_answer_multiple_choices(page, json):
    gotWrongOption = multiple_choices_loop(page, json)
    while not gotWrongOption:
        page.reload()
        gotWrongOption = multiple_choices_loop(page, json)
        if gotWrongOption is None: # this means an error occured => move on to the next question
            break

def fill_in_the_blank_and_multiple_choices_loop(page, json):
    extract_question_text(page, json)
    try:
        print("Collecting all options...")
        options = page.query_selector_all("section.ixl-practice-crate div.responsive-info-higher-order-component div.LaidOutTiles div.SelectableTile.MULTIPLE_CHOICE")

    except TimeoutError:
        print("Error occurred while collecting options")
        return
    
    try:
        print("Taking screenshots of all options...")
        json["choices"] = []
        for i, option in enumerate(options):
            class_attr = option.get_attribute("class")
            if "nonInteractive" not in class_attr.split():
                json["choices"].append(option.inner_text())
                # image_bytes = option.screenshot()
                # option.screenshot(path=f"option{i}.png")
                # image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                # json["choices"].append(image_b64)
    except Exception as e:
        print("Error while taking screenshots of options:", e)
        return
    
    try:
        print("Clicking first option")
        selected_option = options[0]
        selected_option.click()
    except Exception as e:
        print("Error occurred while clicking first option:", e)
        return
    
    
    input_boxes = page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn")
    for box in input_boxes:
        box.fill("m")
        print("Wrong answer 'm' entered")
    
    try:
        # Click the Submit button
        print("Clicking the Submit button...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return
    try:
        print("Checking if selected option is false...")
        res = page.wait_for_selector("div.answer-box h2.feedback-header.correct", timeout=8000)
        text = res.inner_text()
        if "Sorry" in text:
            print("Selected option is confirmed to be false")
            try:
                options = page.query_selector_all("div.answer-box div.correct-answer.ixl-practice-crate")
                answerFound = False
                i = 1
                json["correct_answers"] = []
                while not answerFound:
                    class_attr = options[i].get_attribute("class")
                    if "selected" in class_attr.split():
                        json["correct_answers"].append(chr(65 + i))

                        print("Saved the index of the answer in options")
                        answerFound = True
                    i += 1
                section = page.query_selector("div.correct-answer.ixl-practice-crate")
                value = section.inner_text()
                input_boxes = page.query_selector_all("div.correct-answer.ixl-practice-crate input.fillIn")
                if input_boxes:
                    for box in input_boxes:
                        value += box.evaluate("e => e.value")
                json['correct_answers'].append(value)

                section = page.query_selector("div.explanation-box section.tab-box.web.optional-tab-box.solve-box")
                explanation = section.inner_text().replace("\xa0", "")
                json['solution'] = explanation

                return True # Selected wrong option and extracted answer with full explanation
            
            except Exception as e:
                print("Error while searching for answer:", e)
                return

    except TimeoutError:
        print("Selected the right option. Reloading for a different question...")
        return False
    
    

def extract_answer_fill_in_the_blank_and_multiple_choices(page, json):
    gotWrongOption = fill_in_the_blank_and_multiple_choices_loop(page, json)
    while not gotWrongOption:
        page.reload()
        gotWrongOption = fill_in_the_blank_and_multiple_choices_loop(page, json)
    
def extract_answer_drag_and_drop(page, json):
    try:
        print("Collecting all drag and drop items...")
        options = page.query_selector_all(
            "section.ixl-practice-crate div.ddItemBankDropSlot.dropArea")

    except TimeoutError:
        print("Error occurred while collecting drag and drop items")
        return

    try:
        print("Collecting all drag and drop categories...")
        categories = page.query_selector_all(
            "section.ixl-practice-crate div.binsContainer div.bin.dropArea")
    except TimeoutError:
        print("Error occurred while collecting drag and drop categories")
        return

    try:
        print("Taking screenshots of all drag and drop items...")
        json["drag_and_drop_items"] = []
        for i, option in enumerate(options):
            image_bytes = option.screenshot()
            option.screenshot(path=f"drag_and_drop_item{i}.png")
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            json["drag_and_drop_items"].append(image_b64)
    except Exception as e:
        print("Error while taking screenshots of drag and drop items:", e)
        return

    try:
        print("Taking screenshots of all drag and drop categories...")
        json["categories"] = []
        for i, option in enumerate(categories):
            image_bytes = option.screenshot()
            option.screenshot(path=f"drag_and_drop_categories{i}.png")
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            json["categories"].append(image_b64)
    except Exception as e:
        print("Error while taking screenshots of drag and drop items:", e)
        return

    try:
        print("Clicking submit button right away...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return

    # There exists a pop up so need to confirm submission
    try:
        res = page.wait_for_selector("div.ixl-modal-inside div.ixl-modal-content h3.hd", timeout=8000)
        text = res.inner_text()
        if "Incomplete" in text:
            print("Confirming submission of ordering items...")
            confirm_button = page.get_by_label("Incomplete Answer").get_by_role("button", name="Submit")
            confirm_button.click()
            print("Submission confirmed.")
    except TimeoutError:
        print("No pop up confirmation found, something went wrong")
        return

    try:
        print("Waiting for the correct answer section to appear...")
        page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
        print("Correct answer section appeared.")
        extract_answer_explanation_with_images(page, json)
        print("Extracting correct sorting...")
        answer = page.query_selector("div.correct-answer.ixl-practice-crate div.dragAndDropContainer")
        if answer:
            print("Taking a screenshot of the correct sorting...")
            image_bytes = answer.screenshot()
            answer.screenshot(path="correct_sorting.png")
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            json["answer"] = image_b64
            print("Correct order extracted and saved.")
            return
    except TimeoutError:
        print("Correct answer section did not appear.")
        return
    
def extract_answer_ordering_items(page, json):
    try:
        print("Collecting all items...")
        options = page.query_selector_all(
            "section.ixl-practice-crate div.order-items-item.order-items-numbers")

    except TimeoutError:
        print("Error occurred while collecting ordering items")
        return

    try:
        print("Taking screenshots of all ordering items...")
        json["order_items"] = []
        for i, option in enumerate(options):
            image_bytes = option.screenshot()
            option.screenshot(path=f"order_item{i}.png")
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            json["order_items"].append(image_b64)
    except Exception as e:
        print("Error while taking screenshots of ordering items:", e)
        return

    try:
        print("Clicking submit button right away...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return

    # There exists a pop up so need to confirm submission
    try:
        res = page.wait_for_selector("div.ixl-modal-inside div.ixl-modal-content h3.hd", timeout=8000)
        text = res.inner_text()
        if "Incomplete" in text:
            print("Confirming submission of ordering items...")
            confirm_button = page.get_by_label("Incomplete Answer").get_by_role("button", name="Submit")
            confirm_button.click()
            print("Submission confirmed.")
    except TimeoutError:
        print("No pop up confirmation found, something went wrong")
        return

    try:
        print("Waiting for the correct answer section to appear...")
        page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
        print("Correct answer section appeared.")
        extract_answer_explanation(page, json)
        print("Extracting correct number order...")
        answer = page.query_selector("section.solve-box section.ixl-practice-crate div.order-items-container.interactive")
        if answer:
            print("Taking a screenshot of the correct order...")
            image_bytes = answer.screenshot()
            answer.screenshot(path="correct_order.png")
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            json["answer"] = image_b64
            print("Correct order extracted and saved.")
            return
    except TimeoutError:
        print("Correct answer section did not appear.")
        return

def extract_answer_explanation(page, json):
    try:
        print("Extracting answer explanation...")
        res = page.wait_for_selector("section.solve-box section.ixl-practice-crate", timeout=5000)
        explanation = res.inner_text().replace("\xa0", "")
        json["explanation"] = explanation
        print("Explanation extracted.")
        return
    except Exception as e:
        print("An error occurred while extracting the explanation:", e)
        return

def extract_answer_explanation_with_images(page, json):
    try:
        print("Extracting answer explanation with graphics as image...")
        print("Extracting graphics first...")
        res = page.query_selector_all("section.solve-box section.ixl-practice-crate div.fractionBarContainer")
        for i, option in enumerate(res):
            image_bytes = option.screenshot()
            option.screenshot(path=f"option{i}.png")
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            json["explanation_image_tag"].append(image_b64)
        image_bytes = res.screenshot(path=f"answer_explanation_image_tag.png")
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        json["explanation_image_tag"] = image_b64
        print("explanation images extracted.")
    except Exception as e:
        print("An error occurred while extracting the graphics from the explanation:", e)
        return

    try:
        print("Extracting answer explanation text...")
        res = page.wait_for_selector("section.solve-box section.ixl-practice-crate", timeout=5000)
        explanation = res.inner_text().replace("\xa0", "")
        json["explanation"] = explanation
        print("Explanation text extracted.")
        return
    except Exception as e:
        print("An error occurred while extracting the explanation text:", e)
        return