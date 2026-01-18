import time
import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from Backend.SpeechToText import SpeechRecognition
from Backend.Model import FirstLayerDMM
from Backend.TextToSpeech import TextToSpeech
from Backend.Automation import Automation

MIC_FILE_PATH = os.path.join("Frontend", "Files", "Mic.data")

def get_mic_status():
    try:
        with open(MIC_FILE_PATH, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "False"

def set_mic_status(value: str):
    with open(MIC_FILE_PATH, "w") as f:
        f.write(value)


def main():
    """ Main function to run the Lisabella AI assistant."""
    print("Lisabella AI started. Listening for commands...")
    while True:
        mic_status = get_mic_status()
        
        # IDLE STATE
        if mic_status != "True":
            time.sleep(0.2)
            continue
        
        # listen once
        print("Mic on, Listening...")
        query = SpeechRecognition()

        if not query:
            set_mic_status("False")
            continue
        print(f"Recognized command: {query}")

        # Decision making
        tasks = FirstLayerDMM(query)

        # Route & Execute
        if tasks:
            for task in tasks:
                if task.startswith("general"):
                    # Chat response handled elsewhere (text-only for now)
                    print(f"General query: {task}")
                
                elif task.startswith(("open", "close", "play", "system", "content", "google search", "youtube search")):
                    # Automation tasks
                    print(f"Executing automation: {task}")
                    Automation([task])

                elif task.startswith("generate image"):
                    prompt = task.replace("generate image", "").strip()
                    print(f"Generating image for: {prompt}")
                    with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "w") as f:
                        f.write(f"{prompt},True")

        # optional voice feedback
        TextToSpeech("Done.")   

        # Reset Mic -> back to idle
        set_mic_status("False")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
