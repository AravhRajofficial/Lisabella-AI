import speech_recognition as sr
import mtranslate as mt
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-IN")

# Simple query formatter
def QueryModifier(Query):
    new_query = Query.lower().strip()
    if new_query and new_query[-1] not in [".", "?", "!"]:
        new_query += "."
    return new_query.capitalize()

# Translate non-English input
def UniversalTranslator(Text):
    try:
        english_translation = mt.translate(Text, "en", "auto")
        return english_translation.capitalize()
    except Exception as e:
        print(f"Translation Error: {e}")
        return ""

# Recognize speech using the speech_recognition library
def SpeechRecognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak something!")
        r.pause_threshold = 1.0  # Wait sec before considering a phrase complete (was 1)
        r.energy_threshold = 300  # Minimum audio energy to consider as speech
        r.dynamic_energy_threshold = True 
        r.adjust_for_ambient_noise(source, duration=0.5) # Quick ambient check
        
        # Listen with timeouts
        # timeout: Max time to wait for speech to start
        # phrase_time_limit: Max time to listen once speech starts (prevents hanging)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language=InputLanguage)
        print(f"You said: {query}")

        if "en" in InputLanguage.lower():
            return QueryModifier(query)
        else:
            translated_query = UniversalTranslator(query)
            return QueryModifier(translated_query)

    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""

# Run recognition loop
if __name__ == "__main__":
    while True:
        text = SpeechRecognition()
        if text:
            print("Processed text:", text)