#import required Libraries
from AppOpener import close, open as open  # import function to open and close app.
from webbrowser import open as webopen  #import the brwoser functionality.
from pywhatkit import search, playonyt  # Import function for google search and Youtube playback.
from dotenv import dotenv_values  # Import dotenv to manage environmental variables.
from bs4 import BeautifulSoup  # Importing BeautifulSoup for prasing HTML content.
from rich import print  # Import rich for styled consule output
from groq import Groq  # Import Groq for AI chat functionalities.
import webbrowser # Import webbrowser for opening URLs.
import subprocess # Import subprocess for interacting with the system.
import requests # Import requests for making HTP requests.
import keyboard  # Import keyboard for keyboard related actions.
import asyncio  # import asyncio for asynchronous programming.
import os # Import os for operating system functionalities.

# Load environmental variable from .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API Key

# Define CSS class for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWsb Ywphnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfke", "WQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = ""

# Initialize the Groq client with API Key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user innteractions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with."
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask."
]

# List to store Chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am{os.environ['Username']}, You're a content writer. You have to write content like letter"}]

# Function to perform a Google Search
def GoogleSearch(Topic):
    search(Topic) # Use pywhatkit's search function to perform a google search.
    return True # Indicate success.

# Function to generate content usinng AI and save it to a file.
def Content(Topic):
    # Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = "notepad.exe"  # Default text editor.
        subprocess.Popen([default_text_editor, File]) # Open the file in Notepad.

    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) # Add the user's prompt to messages.

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Specify the AI model.
            messages=SystemChatBot + messages, # Include system instructions and chat history.
            max_tokens=2048, # Limit the maximum tokens in the response.
            temperature=0.7, # Adjust response randomness.
            top_p=1, # Use nucleus sampling for response diversity.
            stream=True,  # Enable streaming respoonse.
            stop=None  # Allow the model to determine stopping conditions.
        )

        Answer = ""  # Initialize an empty string for the response.

        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for the content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.
            
        Answer = Answer.replace("<s>", "") # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer}) # Add the AI's response to message.
        return Answer
    
    Topic: str = Topic.replace("Content ", "")  # Remove "Content " from the topic.
    ContentByAI = ContentWriterAI(Topic)  # Generate content using AI.

    # Save the generated content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write the content to the file.
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")  # Open the file in Notepad.
    return True # Indicate sucess.

# Function to search for a topic on Youtube.
# def