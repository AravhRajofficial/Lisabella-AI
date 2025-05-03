from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import mtranslate as mt
from dotenv import dotenv_values
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environmental variables from the .env file.
try:
    env_vars = dotenv_values(".env")
    InputLanguage = env_vars.get("InputLanguage", "en-US")
except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    InputLanguage = "en-US"  # Default to English if .env is not found

# Define the HTML code for the speech recognition interface.
HTMLCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecording()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById("output");
        let recognition;

        function startRecognition() {
            try {
                recognition = new webkitSpeechRecognition() || new SpeechRecognition();
                recognition.lang = '';
                recognition.continuous = true;
                recognition.interimResults = true;

                recognition.onresult = function(event){
                    const transcript = event.results[event.results.length - 1][0].transcript;
                    output.textContent = transcript;
                };

                recognition.onerror = function(event){
                    console.error('Speech recognition error:', event.error);
                };

                recognition.onend = function(){
                    console.log('Speech recognition ended');
                };
                
                recognition.start();
            } catch (error) {
                console.error('Error starting speech recognition:', error);
            }
        }

        function stopRecording() {
            if (recognition) {
                recognition.stop();
                output.innerHTML = "";
            }
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code
HTMLCode = str(HTMLCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Create Data directory if it doesn't exist
os.makedirs("Data", exist_ok=True)

# Write the modified HTML code to a file
try:
    with open(os.path.join("Data", "Voice.html"), "w", encoding='utf-8') as f:
        f.write(HTMLCode)
except Exception as e:
    logger.error(f"Error writing HTML file: {e}")

# Get the current working directory
current_dir = os.getcwd()
Link = os.path.join(current_dir, "Data", "Voice.html")

# Set chrome options for the WebDriver
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

# Initialize the Chrome WebDriver
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    logger.error(f"Error initializing Chrome WebDriver: {e}")
    raise

# Define the path for temporary files
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

def SetAssistantStatus(Status):
    try:
        with open(os.path.join(TempDirPath, "Status.data"), "w", encoding='utf-8') as file:
            file.write(Status)
    except Exception as e:
        logger.error(f"Error setting assistant status: {e}")

def QueryModifier(Query):
    try:
        new_query = Query.lower().strip()
        if not new_query:
            return ""
            
        query_words = new_query.split()
        question_words = ["how", "what", "who", "when", "where", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "will you"] 

        if any(word + " " in new_query for word in question_words):
            if query_words[-1][-1] in ['.', '?', "!"]:
                new_query = new_query[:-1] + "?"
            else:
                new_query += "?"
        else:
            if query_words[-1][-1] in [".", "?", "!"]:
                new_query = new_query[:-1] + "."
            else:
                new_query += "."
        return new_query.capitalize()
    except Exception as e:
        logger.error(f"Error modifying query: {e}")
        return Query

def UniversalTranslator(Text):
    try:
        english_translation = mt.translate(Text, "en", "auto")
        return english_translation.capitalize()
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        return Text

def SpeechRecognition():
    try:
        driver.get("file:///" + Link)
        time.sleep(2)  # wait for page to load
        
        start_button = driver.find_element(By.ID, "start")
        start_button.click()
        logger.info("Listening... Speak something!")

        last_text = ""
        max_attempts = 10
        attempts = 0

        while attempts < max_attempts:
            try:
                Text = driver.find_element(By.ID, "output").text
                if Text.strip() and Text != last_text:
                    last_text = Text
                    driver.find_element(By.ID, "end").click()

                    if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                        return QueryModifier(Text)
                    else:
                        SetAssistantStatus("Translating...")
                        return QueryModifier(UniversalTranslator(Text))
                
                time.sleep(0.5)
                attempts += 1
            except Exception as e:
                logger.error(f"Error during speech recognition: {e}")
                attempts += 1
                time.sleep(0.5)

        logger.warning("No speech detected after maximum attempts")
        return ""
    except Exception as e:
        logger.error(f"Error in SpeechRecognition: {e}")
        return ""

if __name__ == "__main__":
    try:
        while True:
            Text = SpeechRecognition()
            if Text:
                print(Text)
    except KeyboardInterrupt:
        logger.info("Speech recognition stopped by user")
    finally:
        driver.quit()