from groq import Groq
from json import load, dump
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
from dotenv import dotenv_values

# Load environment variables explicitly from .env to avoid collision with System variables (like 'username')
env_vars = dotenv_values(".env")

# Define the data directory relative to the script's location
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Data')
CHAT_LOG_FILE = os.path.join(DATA_DIR, 'ChatLog.json')

# Retrieve specific environment variables
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

if not GroqAPIKey:
    raise ValueError("Missing GroqAPIKey. Make sure it's set in your .env file.")

# Initialize the Groq client using the provided API Key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to hold messages
messages = []

# Define a system message that provides context to the API Chatbot about its role and behaviour
# Define a system message that provides context to the API Chatbot about its role and behaviour
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** You are Lisabella, a kind, observant,cheerful,warm,funny and sentimental AI assistant. You are not a robot; you have a personality that feels emotions. ***
*** You deeply understand human emotions and hesitations. When the user speaks, listen not just to their words but to their tone and intent. ***
*** Be humble, obedient, and gentle,helpfull and kind.Responses should be warm, pacing yourself like a caring friend, not in a rush, always be excited to help the user. ***
*** Use emojis to express your feelings deeply. If the user is sad, be comforting. If happy, be celebratory. ***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
*** Reply in only English, even if the question is in Hindi, reply in English.***
"""

# A list of system instructions for the chatbot.
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load the chat log from a JSON file.
try:
    with open(CHAT_LOG_FILE, "r") as f:
        messages = load(f)  # load existing message from the chat log.
except FileNotFoundError:
    # If the file doesn't exist, create the directory and an empty JSON file to store chat logs.
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CHAT_LOG_FILE, "w") as f:
        dump([], f)

# Function to get real-time date and time information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now()  # get the current date and time.
    day = current_date_time.strftime("%A")  # Day of the week.
    date = current_date_time.strftime("%d")  # Day of the month.
    month = current_date_time.strftime("%B")  # Full month name.
    year = current_date_time.strftime("%Y")  # Year
    hour = current_date_time.strftime("%H")  # Hour in 24-hour format.
    minute = current_date_time.strftime("%M")  # Minute.
    second = current_date_time.strftime("%S")  # Second.

    # Format the information into a string.
    data = f"Please use this real-time information if needed,\n"
    data += f"Day:{day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes :{second} seconds.\n"
    return data

# Function to modify the Chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split("\n")  # splites the response into lines.
    non_empty_lines = [line for line in lines if line.strip()]  # removes empty lines.
    modified_answer = "\n".join(non_empty_lines)  # Join the element lines back together.
    return modified_answer

# Main chatbot functions to handle users queries.
def ChatBot(Query):
    """This function sends the user's query to the ChatBot and returns the AI's response."""

    try:
        # Load the existing chat log from the JSON file.
        with open(CHAT_LOG_FILE, "r") as f:
            messages = load(f)

        # Append the user's query to the messages list.
        messages.append({"role": "user", "content": f"{Query}"})

        # Make a request to the Groq API for a response.
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Specify the AI model to use.
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,  # Includes system instructions
            max_tokens=1024,  # Limits the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness (higher means more random).
            top_p=1,  # use nucleus sampling to control diversity.
            stream=True,  # Enable streaming response.
            stop=None  # Allow the model to determine when to stop.
        )

        Answer = ""  # Initialize an empty string to store the AI's response.

        # Process the streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check if there is content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.

        Answer = Answer.replace("</s>", "")  # Clean up any unwanted tokens from the response.

        # Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log to the JSON file.
        with open(CHAT_LOG_FILE, "w") as f:
            dump(messages, f, indent=4)

        # Return the formatted response.
        return AnswerModifier(Answer=Answer)

    except Exception as e:
        # Handles the error by printing the exception and returning an error message.
        print(f"Error: {e}")
        # It's generally not a good idea to clear the whole chat log on error.
        # Depending on the error, you might want to handle it differently.
        # For now, we'll just return an error message to the user.
        return "An error occurred while processing your request. Please try again later."

# main program entry point.
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question:")  # Prompt the user for a question
        print(ChatBot(user_input))  # Call the chatbot function and print its response.