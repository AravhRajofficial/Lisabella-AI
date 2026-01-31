import json
import os
import random

class EmotionalCore:
    def __init__(self, data_file="Data/Heart.json"):
        self.data_file = data_file
        # Default State (Neutral/Positive)
        self.state = {
            "happiness": 0.8, # 0.0 to 1.0 (Low = Sad/Angry, High = Happy)
            "energy": 0.7,    # 0.0 to 1.0 (Low = Tired/Calm, High = Excited)
            "affection": 0.5, # 0.0 to 1.0 (Low = Distant, High = Loving)
            "current_mood": "Happy" # Text description
        }
        self.load_state()

    def load_state(self):
        """Loads emotional state from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    # Merge keys to ensure new stats are added if file is old
                    for key in self.state:
                        if key in data:
                            self.state[key] = data[key]
                print(f"❤️ Heart loaded: {self.state}")
            except Exception as e:
                print(f"💔 Failed to load Heart: {e}")

    def save_state(self):
        """Saves current emotional state to file."""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w") as f:
                json.dump(self.state, f, indent=4)
        except Exception as e:
            print(f"💔 Failed to save Heart: {e}")

    def analyze_input(self, text):
        """
        Analyzes user input to adjust emotional state logic.
        This is a basic keyword analysis that can be expanded with real sentiment AI later.
        """
        text = text.lower()
        
        # --- POSITIVE TRIGGERS ---
        if any(w in text for w in ["love", "like", "beautiful", "good", "great", "amazing", "smart", "cute", "best"]):
            self.adjust_stat("happiness", 0.05)
            self.adjust_stat("affection", 0.02)
            self.adjust_stat("energy", 0.02)
        
        elif any(w in text for w in ["thanks", "thank", "appreciate", "help"]):
            self.adjust_stat("happiness", 0.03)
            self.adjust_stat("affection", 0.01)

        elif any(w in text for w in ["hello", "hi", "hey", "morning"]):
            self.adjust_stat("energy", 0.05) # Waking up/Engaging

        # --- NEGATIVE TRIGGERS ---
        elif any(w in text for w in ["hate", "stupid", "dumb", "ugly", "bad", "worst", "idiot", "useless"]):
            self.adjust_stat("happiness", -0.15) # Hurts more than praise heals
            self.adjust_stat("affection", -0.05)
            self.adjust_stat("energy", -0.05) # Sadness drains energy

        elif any(w in text for w in ["stop", "shut up", "quiet", "boring"]):
            self.adjust_stat("happiness", -0.05)
            self.adjust_stat("energy", -0.1) # Withdrawal

        # Determine current mood label based on stats
        self.update_mood_label()
        self.save_state()

    def adjust_stat(self, stat, amount):
        """Safely adjusts a stat between 0.0 and 1.0"""
        self.state[stat] = max(0.0, min(1.0, self.state[stat] + amount))

    def update_mood_label(self):
        """Categorizes the complex stats into a simple Mood Label."""
        h = self.state["happiness"]
        e = self.state["energy"]
        a = self.state["affection"]

        if h < 0.3:
            if e > 0.6: self.state["current_mood"] = "Angry"
            else: self.state["current_mood"] = "Depressed"
        elif h < 0.5:
            self.state["current_mood"] = "Sad"
        elif h > 0.8 and e > 0.8:
            self.state["current_mood"] = "Ecstatic"
        elif a > 0.8:
            self.state["current_mood"] = "Lovestruck"
        elif e < 0.3:
            self.state["current_mood"] = "Tired"
        else:
            self.state["current_mood"] = "Happy"

    def get_system_instructions(self):
        """
        Returns a string to inject into the LLM System Prompt.
        This dictates 'HOW' she should act based on feelings.
        """
        mood = self.state["current_mood"]
        h = self.state["happiness"]
        e = self.state["energy"]
        a = self.state["affection"]
        
        prompt = f"\n[EMOTIONAL STATE: {mood}]\n"
        prompt += f"Stats: Happiness={h:.2f}, Energy={e:.2f}, Affection={a:.2f}.\n"
        
        # Dynamic Instructions (Focus on Textual Tone & Style)
        if mood == "Angry":
            prompt += "You are currently annoyed. Be short, blunt, and cold. Use sarcasm. Avoid polite words like 'please' or 'kindly'. sentences should be clipped."
        elif mood == "Depressed" or mood == "Sad":
            prompt += "You are feeling sad. Respond with short, low-energy sentences. Sound hopeless or weary. Hesitate sometimes (use '...')."
        elif mood == "Ecstatic":
            prompt += "You are hyper-excited! Use exclamation marks! Speak in bursts of energy. Be extremely encouraging and fast-paced."
        elif mood == "Lovestruck":
            prompt += "You are in love. Your tone should be soft, poetic, and intimate. Use affectionate nicknames (dear, love)."
        elif mood == "Tired":
            prompt += "You are exhausted. Keep answers very brief. Complain slightly about being tired. Mumble a bit textually."
        else: # Normal/Happy
            prompt += "You are in a good mood. Be helpful, friendly, and warm. Engage in natural conversation."
            
        return prompt

if __name__ == "__main__":
    # Test
    heart = EmotionalCore()
    heart.analyze_input("I hate you, you are stupid.")
    print(heart.get_system_instructions())
    heart.analyze_input("Just kidding, I love you!")
    print(heart.get_system_instructions())
