import time
import os
import sys
import asyncio
from pathlib import Path
import socket

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from Backend.SpeechToText import SpeechRecognition
from Backend.Model import FirstLayerDMM
from Backend.TextToSpeech import TextToSpeech
from Backend.Automation import Automation
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.ImageGeneration import GenerateImages
from Backend.SentimentAnalysis.Heart import EmotionalCore # Import Heart

PRIORITY = [
    "exit",
    "open",
    "close",
    "play",
    "generate image",
    "system",
    "content",
    "google search",
    "youtube search",
    "general"
]

def pick_primary_task(tasks):
    for priority in PRIORITY:
        for task in tasks:
            if task.startswith(priority):
                return task
    return None


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

# ... existing imports ...

RESPOND_FILE_PATH = os.path.join("Frontend", "Files", "Responses.data")
STATUS_FILE_PATH = os.path.join("Frontend", "Files", "Status.data")
TEXT_INPUT_PATH = os.path.join("Frontend", "Files", "TextInput.data")

# Singleton Socket to prevent double execution
SINGLE_INSTANCE_SOCKET = None

def check_single_instance():
    global SINGLE_INSTANCE_SOCKET
    SINGLE_INSTANCE_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Try to bind to a specific port. If it fails, another instance is using it.
        SINGLE_INSTANCE_SOCKET.bind(('127.0.0.1', 65432))
        print("Singleton check passed. Instance locked.")
    except OSError:
        print("\n" + "!"*50)
        print("ERROR: Another instance of Lisabella AI is already running!")
        print("Please close the existing window before starting a new one.")
        print("!"*50 + "\n")
        sys.exit(1)

def ShowTextToScreen(text):
    with open(RESPOND_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(text)

def SetAssistantStatus(status):
    with open(STATUS_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(status)

def main():
    """ Main function to run the Lisabella AI assistant."""
    check_single_instance() # <--- VERIFY SINGLE INSTANCE
    print("Lisabella AI started. Listening for commands...")
    
    # Initialize Heart
    heart = EmotionalCore()
    
    # WAKE WORD STATE
    ConversationMode = False
    LastInteractionTime = 0
    CONVERSATION_TIMEOUT = 60 # Seconds
    MIC_OFF_TIMEOUT = 240 # 4 Minutes (Auto-Sleep)
    PreviousMicStatus = "False"

    while True:
        # Check for Text Input first
        query = None
        IsTextInput = False

        if os.path.exists(TEXT_INPUT_PATH):
            try:
                with open(TEXT_INPUT_PATH, "r", encoding="utf-8") as f:
                    query = f.read().strip()
                os.remove(TEXT_INPUT_PATH)
                IsTextInput = True # Text input always bypasses wake word
            except Exception as e:
                print(f"Error reading text input: {e}")
        
        # If no text input, check Mic
        if not query:
            mic_status = get_mic_status()
            
            # STATE TRANSITION: If Mic just turned ON (or startup), Wake Up immediately!
            if mic_status == "True" and PreviousMicStatus == "False":
                print("Mic Activated: Conversation Mode ON (10s)")
                ConversationMode = True
                LastInteractionTime = time.time()
            
            PreviousMicStatus = mic_status

            # IDLE STATE
            if mic_status != "True":
                ConversationMode = False # Reset if mic is turned off
                time.sleep(0.2)
                continue
            
            # AUTO-SLEEP LOGIC (4 Mins Inactivity)
            if (time.time() - LastInteractionTime) > MIC_OFF_TIMEOUT:
                print("Auto-Sleep: 4 minutes of inactivity. Turning Mic OFF.")
                set_mic_status("False")
                # TextToSpeech("Microphone off due to inactivity.") # Optional Feedback (Commented out to be silent)
                ConversationMode = False
                continue
            
            # listen once
            print("Mic on, Listening...")
            SetAssistantStatus("Listening...")
            query = SpeechRecognition()
        
        # If we have a query (from Text OR Voice)
        if not query:
            # If Mic is ON but heard nothing (silence), just loop. 
            # Don't turn off Mic, just go back to listening.
            if get_mic_status() == "True":
                 continue
            else:
                 pass # Mic off, loop continues at top
            continue
            
        print(f"Recognized command: {query}")
        
        # --- WAKE WORD LOGIC (Voice Only) ---
        if not IsTextInput:
            CurrentTime = time.time()
            CleanQuery = query.lower()
            
            # If in active conversation
            if ConversationMode and (CurrentTime - LastInteractionTime < CONVERSATION_TIMEOUT):
                print("Conversation Mode Active. Processing...")
                LastInteractionTime = CurrentTime # Reset timer
                
            # If calling her name (Trigger)
            # 'nisha', 'liza', 'niza' are common transcriptions of 'Lisa' when speaking English names in Hindi mode.
            elif any(w in CleanQuery for w in ["lisa", "lisabella", "nisha", "liza", "niza", "leesa", "misha"]):
                print("Wake Word Detected!")
                ConversationMode = True
                LastInteractionTime = CurrentTime
                
            # Else: Ignore
            else:
                print(f"Ignored: '{query}' (No Wake Word)")
                continue

        SetAssistantStatus(f"Processing: {query}")
        if not IsTextInput:
             ShowTextToScreen(f"User: {query}")

        # Clean query for classification (Remove Wake Word)
        # This prevents "Lisa generate image" from being seen as "General" because of the name.
        cleaned_query_for_model = query.lower().replace("lisa", "").replace("lisabella", "").strip(" .,")
        
        # Decision making
        tasks = FirstLayerDMM(cleaned_query_for_model)

        # Route & Execute
        if tasks:
            primary_task = pick_primary_task(tasks)

            if not primary_task:
                print("No valid tasks found.")
                SetAssistantStatus("No Task Found")
                # return # <--- BUG: This kills the app. Changed to continue.
                continue
            
            # ------GENERAL QUERY-----
            if primary_task.startswith("general"):
                print(f"General query: {primary_task}")
                # Use Realtime Search Engine
                query_text = primary_task.replace("general", "").strip()
                
                # CRITICAL FIX: If query is empty (e.g. just "Lisa"), ignore it.
                if not query_text:
                    continue
                
                # Update Heart
                heart.analyze_input(query_text)
                emotion_prompt = heart.get_system_instructions()

                response_text = RealtimeSearchEngine(query_text, heart_instruction=emotion_prompt)
                
                # Display and Speak
                SetAssistantStatus("Replying...")
                ShowTextToScreen(f"Lisabella: {response_text}")
                
                # --- DYNAMIC VOICE TEMPERING ---
                # Calculate Rate and Pitch based on emotional state
                voice_rate_val = 0
                voice_pitch_val = 0
                
                # Energy affects Speed
                if heart.state["energy"] > 0.8: voice_rate_val = 15 # Fast
                elif heart.state["energy"] < 0.4: voice_rate_val = -10 # Slow
                
                # Happiness affects Pitch
                if heart.state["happiness"] > 0.8: voice_pitch_val = 5 # Higher
                elif heart.state["happiness"] < 0.4: voice_pitch_val = -5 # Lower
                
                voice_rate = f"{'+' if voice_rate_val >= 0 else ''}{voice_rate_val}%"
                voice_pitch = f"{'+' if voice_pitch_val >= 0 else ''}{voice_pitch_val}Hz"
                
                TextToSpeech(response_text, rate=voice_rate, pitch=voice_pitch)

            # -----IMAGE GENERATION-----
            elif primary_task.startswith("generate image"):
                prompt = primary_task.replace("generate image", "").strip()
                print(f"Generating image for prompt: {prompt}")
                ShowTextToScreen(f"Lisabella: Generating image for {prompt}...")
                image_files = GenerateImages(prompt)
                
                if image_files:
                    # Capture the first image path and send it to the GUI
                    primary_image_path = image_files[0]
                    with open(os.path.join("Frontend", "Files", "Image.data"), "w") as f:
                        f.write(primary_image_path)
                        
                    ShowTextToScreen(f"Lisabella: Image generated.")
                    TextToSpeech("Here is the image you asked for.")
                else:    
                    ShowTextToScreen(f"Lisabella: Failed to generate images.")
                    TextToSpeech("Sorry, I could not generate the images.")
            
            # ----AUTOMATION TASKS-----
            elif primary_task.startswith(("open", "close", "play", "system", "content", "google search", "youtube search")):
                print(f"Executing primary automation : {primary_task}")
                asyncio.run(Automation(tasks))
                ShowTextToScreen(f"Lisabella: Executed {primary_task}")


        # optional voice feedback
        # TextToSpeech("Done.")   
        SetAssistantStatus("Idle")

        # Update Timer to keep conversation alive
        LastInteractionTime = time.time()
        
        # Reset Mic -> back to idle
        # set_mic_status("False") # <--- DISABLED for Hands-Free
        time.sleep(0.2)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
