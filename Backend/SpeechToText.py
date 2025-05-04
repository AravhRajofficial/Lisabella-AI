from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import mtranslate as mt
from dotenv import dotenv_values
import time

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")

# Get current working directory
current_dir = os.getcwd()
html_file_path = os.path.join(current_dir, "Data", "Voice.html")
html_file_url = "file:///" + html_file_path.replace("\\", "/")

# Chrome options setup
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
# DO NOT use headless mode!

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Modify query format
def QueryModifier(Query):
    new_query = Query.lower().strip()
    if new_query and new_query[-1] not in [".", "?", "!"]:
        new_query += "."
    return new_query.capitalize()

# Translate to English
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Perform speech recognition
def SpeechRecognition():
    driver.get(html_file_url)
    time.sleep(2)
    driver.find_element(By.ID, "start").click()
    print("Listening... Speak. Click the Stop button in the browser to finish.\n")

    last_text = ""
    stable_count = 0

    while True:
        try:
            Text = driver.find_element(By.ID, "output").text.strip()

            if Text != last_text:
                last_text = Text
                stable_count = 0
                print("\rYou said: " + Text, end="")
            else:
                stable_count += 1

            # If the text has not changed for 5 loops (~5 seconds), assume stop clicked
            if stable_count >= 5:
                break

            time.sleep(1)

        except Exception:
            pass

    driver.find_element(By.ID, "end").click()

    if "en" in InputLanguage.lower():
        return QueryModifier(last_text)
    else:
        return QueryModifier(UniversalTranslator(last_text))


# Run the program
if __name__ == "__main__":
    while True:
        text = SpeechRecognition()
        print("You said:", text)
