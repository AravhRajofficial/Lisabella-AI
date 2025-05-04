import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import mtranslate as mt
from dotenv import dotenv_values

# Load input language from .env
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")

# Write voice.html content to a file dynamically
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>

    <script>
        const output = document.getElementById("output");
        let recognition;
        let isRunning = false;

        function startRecognition() {{
            window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = '{InputLanguage}';
            recognition.continuous = true;
            recognition.interimResults = false;
            isRunning = true;

            recognition.onresult = function(event) {{
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    transcript += event.results[i][0].transcript;
                }}
                output.textContent += transcript + ' ';
            }};

            recognition.onend = function() {{
                if (isRunning) recognition.start();
            }};

            recognition.start();
        }}

        function stopRecognition() {{
            if (recognition) {{
                isRunning = false;
                recognition.stop();
            }}
        }}
    </script>
</body>
</html>
"""

# Write HTML to file
data_dir = os.path.join(os.getcwd(), "Data")
os.makedirs(data_dir, exist_ok=True)
html_path = os.path.join(data_dir, "Voice.html")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")
# Do NOT use headless or fake media options if using real mic

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def QueryModifier(query):
    new_query = query.strip().lower()
    question_words = ["how", "what", "who", "when", "where", "why", "which", "whose", "whom", "can you", "will you"]
    if any(new_query.startswith(q) for q in question_words):
        return new_query.capitalize() + "?"
    return new_query.capitalize() + "."

def UniversalTranslator(text):
    return mt.translate(text, "en", "auto").capitalize()

def SpeechRecognition():
    driver.get(f"file:///{html_path.replace(os.sep, '/')}")
    time.sleep(2)
    driver.find_element(By.ID, "start").click()

    print("🎙️ Listening... Speak continuously (Click 'Stop Recognition' in browser when done)\n")

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
        result = SpeechRecognition()
        print("\nFinal recognized:", result)
