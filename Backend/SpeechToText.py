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

# HTML file path
html_file_path = os.path.join(os.getcwd(), "Data", "Voice.html")
html_file_url = "file:///" + html_file_path.replace("\\", "/")

# Chrome options setup
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")  # Do NOT use headless!
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")

# Initialize driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

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
    driver.get(Data/Voice.html)
    time.sleep(2)
    driver.find_element(By.ID, "start").click()
    print("Listening... Speak something!")

    last_text = ""
    while True:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text.strip() and Text != last_text:
                last_text = Text
                driver.find_element(By.ID, "end").click()

                if "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            pass

# Run recognition loop
if __name__ == "__main__":
    while True:
        text = SpeechRecognition()
        print("You said:", text)
