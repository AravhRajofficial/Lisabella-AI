import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import mtranslate as mt

# Load language setting from .env
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")

# Generate HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head><title>Speech Recognition</title></head>
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
                    transcript += event.results[i][0].transcript + ' ';
                }}
                output.textContent += transcript;
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

# Write HTML
data_dir = os.path.join(os.getcwd(), "Data")
os.makedirs(data_dir, exist_ok=True)
html_path = os.path.join(data_dir, "Voice.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Chrome options
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/MyChromeProfile")  # Use pre-authorized profile
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
# ⚠️ Do NOT use --headless or fake media stream

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def QueryModifier(text):
    if not text: return ""
    text = text.strip().lower()
    if not text.endswith("."):
        text += "."
    return text.capitalize()

def UniversalTranslator(text):
    return mt.translate(text, "en", "auto").capitalize()

def SpeechRecognition():
    driver.get(f"file:///{html_path.replace(os.sep, '/')}")
    time.sleep(2)
    driver.find_element(By.ID, "start").click()
    print("🎙️ Listening...")

    last_text = ""
    while True:
        try:
            text = driver.find_element(By.ID, "output").text.strip()
            if text and text != last_text:
                print("🗣️ Heard:", text)
                last_text = text
            time.sleep(1)
        except:
            pass

if __name__ == "__main__":
    SpeechRecognition()
