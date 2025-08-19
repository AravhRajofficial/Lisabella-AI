from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import mtranslate as mt
from dotenv import dotenv_values
import time

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")

# HTML file path
html_file_path = os.path.join(os.getcwd(), "Data", "Voice.html")
html_file_url = "file:///" + html_file_path.replace("\\", "/")

# Chrome options setup
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--headless=new")  # As the comment suggests, headless mode can cause issues with media streams.
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")

# Initialize driver
driver = webdriver.Chrome(options=chrome_options)

# Simple query formatter
def QueryModifier(Query):
    new_query = Query.lower().strip()
    if new_query and new_query[-1] not in [".", "?", "!"]:
        new_query += "."
    return new_query.capitalize()

# Translate non-English input
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Recognize speech from browser
def SpeechRecognition():
    driver.get(html_file_url)
    time.sleep(2)
    driver.find_element(By.ID, "start").click()
    print("Listening... Speak something!")

    last_text = ""
    while True:
        try:
            text_from_browser = driver.find_element(By.ID, "output").text
            current_text = text_from_browser.strip()
            if current_text and current_text != last_text:
                last_text = current_text
                driver.find_element(By.ID, "end").click()

                if "en" in InputLanguage.lower():
                    return QueryModifier(current_text)
                else:
                    return QueryModifier(UniversalTranslator(current_text))
            time.sleep(0.2)  # Add a small delay to prevent high CPU usage
        except Exception as e:
            print(f"An error occurred during speech recognition: {e}")
            return ""  # Exit the function with an empty string on error

# Run recognition loop
if __name__ == "__main__":
    while True:
        text = SpeechRecognition()
        print("You said:", text)
