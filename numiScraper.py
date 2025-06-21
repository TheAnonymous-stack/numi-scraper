from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import base64
from playwright.sync_api import TimeoutError
from typeChecker import check_fill_in_the_blank, check_multiple_choices, check_ordering_items, check_drag_and_drop


def screenshot_question_section(url, output_path="question.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        counter = 1
        page = browser.new_page()
        for _ in range(50):
            output_path=f"question{str(counter)}.png"
            counter+=1
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)

                # Attempt to close the ad using the 'explore-btn' button
                try:
                    page.wait_for_selector("button.explore-btn", timeout=3000)
                    page.click("button.explore-btn")
                    print("Ad closed via 'explore-btn'")
                except:
                    print("No ad found or already dismissed.")

                # Screenshot the question section
                section = page.wait_for_selector("section.ixl-practice-crate", timeout=5000)
                section.screenshot(path=output_path)
            except:
                print(f"question{counter-1} failed")
        print(f"Screenshots saved to {output_path}")

        browser.close()

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

def extract_question_text2(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        try:
            page.wait_for_selector("button.explore-btn", timeout=3000)
            page.click("button.explore-btn")
        except:
            pass

        # Wait for question section
        section = page.wait_for_selector("section.ixl-practice-crate", timeout=5000)
        # spans = section.query_selector_all("span")
        # text = " ".join([span.inner_text().replace("\xa0", "") for span in spans])
        text = section.inner_text().replace("\xa0", "")
        
        # Extract text
        dict = {}
        dict["question"] = text
        print(dict)
        print(text)
        browser.close()
        return text

def extract_question_text(page, json):
    # Wait for question section
    section = page.wait_for_selector("section.ixl-practice-crate", timeout=5000)

    # Extract text
    text = section.inner_text().replace("\xa0", "")  # gets all rendered (visible) text
    
    json["question"] = text

def extract_answer_fill_in_the_blank(page, json):
    
    try:
        # Fill wrong answer into input inside .math.section
        print("Locating the input field...")
        fill_in = page.wait_for_selector("section.ixl-practice-crate input.fillIn", timeout=20000)
        fill_in.fill("m")
        print("Wrong answer 'm' entered.")
    except TimeoutError:
        print("Could not find the input field")
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
        print("Waiting for the correct answer section to appear...")
        page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
        print("Correct answer section appeared.")
    except TimeoutError:
        print("Correct answer section did not appear.")
        return

    try:
        print("Extracting correct answer...")
        value = page.eval_on_selector("div.correct-answer.ixl-practice-crate input.fillIn", "el => el.value")
        # print("Correct answer extracted:", value)
        json['answer'] = value
    except Exception as e:
        print(f"Failed to extract correct answer: {e}")

def extract_answer_multiple_choices(page, json):
    # Get all choices first
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
                image_bytes = option.screenshot()
                option.screenshot(path=f"option{i}.png")
                image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                json["choices"].append(image_b64)
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
                        json["answer"] = i
                        print("Saved the index of the answer in options")
                        answerFound = True
                    i += 1
                return
            except Exception as e:
                print("Error while searching for answer:", e)
                return
    except TimeoutError:
        print("Selected the right option")
        json["answer"] = 0 
        print("Saved the index of the answer in options")
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

# AKA sorting items
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

def scrape_question(url, json):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set to True if you don't need to see the browser
        page = browser.new_page()
        page.goto(url)
        try:
            page.wait_for_selector("button.explore-btn", timeout=3000)
            page.click("button.explore-btn")
            print("Ad closed via 'explore-btn'")
        except:
            print("No ad found or already dismissed.")
        extract_question_text(page, json)
        if check_fill_in_the_blank(page):
            json["type"] = "fill in the blank"
            extract_answer_fill_in_the_blank(page, json)
        elif check_multiple_choices(page):
            json["type"] = "multiple choices"
            extract_answer_multiple_choices(page, json)
        elif check_ordering_items(page):
            json["type"] = "ordering items"
            extract_answer_ordering_items(page, json)
        elif check_drag_and_drop(page):
            json["type"] = "drag and drop"
            extract_answer_drag_and_drop(page, json)
        browser.close()

def getTopicUrls(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to fetch page. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "lxml")

        # Find the main section with class="skill-tree-body"
        skill_tree_body = soup.find("section", class_="skill-tree-body")
        if not skill_tree_body:
            print("❌ 'skill-tree-body' section not found.")
            return []

        # Get all divs with class="skill-tree-category" inside that section
        skills = skill_tree_body.find_all("a", class_="skill-tree-skill-link")

        # Optional: Return the text of each category, cleaned
        base_url = "https://ca.ixl.com"
        results = [base_url+skill.get("href") for skill in skills]
        return results

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return []

question_url = "https://ca.ixl.com/math/grade-5/multiply-fractions-and-whole-numbers-sorting"
json = {}
scrape_question(question_url, json)
print(json)