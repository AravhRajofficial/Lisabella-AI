import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import mtranslate as mt
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")

# Write HTML file
html_code_path = os.path.join("Data", "Voice.html")
if not os.path.exists("Data"):
    os.makedirs("Data")

with open(html_code_path, "w", encoding="utf-8") as f:
    with open("voice.html", "r", encoding="utf-8") as src:
        html_content = src.read().replace("recognition.lang = 'en-US';", f"recognition.lang = '{InputLanguage}';")
        f.write(html_content)

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")
# NOTE: Do NOT add headless or fake device options if using real mic

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

html_file_url = f"file:///{os.path.abspath(html_code_path)}"

def QueryModifier(query):
    new_query = query.strip().lower()
    question_words = ["how", "what", "who", "when", "where", "why", "which", "whose", "whom", "can you", "will you"]
    if any(new_query.startswith(q) for q in question_words):
        return new_query.capitalize() + "?"
    return new_query.capitalize() + "."

def UniversalTranslator(text):
    return mt.translate(text, "en", "auto").capitalize()

def SpeechRecognition():
    driver.get(html_file_url)
    time.sleep(2)
    driver.find_element(By.ID, "start").click()
    print("🎙️ Listening... (Click 'Stop Recognition' in the browser to end)\n")

    last_text = ""
    stable_count = 0

    while True:
        try:
            Text = driver.find_element(By.ID, "output").text.strip()

            if Text != last_text:
                last_text = Text
                stable_count = 0
                print("\rYou said: " + Text, end="", flush=True)
            else:
                stable_count += 1

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

if __name__ == "__main__":
    while True:
        text = SpeechRecognition()
        print("\nFinal recognized:", text)
