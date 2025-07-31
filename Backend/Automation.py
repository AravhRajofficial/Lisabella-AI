#import required Libraries
from AppOpener import close, open as appopen  # import function to open and close app.
from webbrowser import open as webopen  #import the brwoser functionality.
from typing import List, AsyncGenerator, Any
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
Username = env_vars.get("Username")
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
SystemChatBot = [{"role": "system", "content": f"Hello, I am {Username}, You're a content writer. You have to write content like letter"}]

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
            
        Answer = Answer.replace("</s>", "") # Remove unwanted tokens from the response.
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
def YoutubeSearch(Topic):
    # construct the Youtube search URL. 
    Url4Search= f"https://www.youtube.com/results?search_query={Topic}"
    # Open the search URl in web browser.
    webbrowser.open(Url4Search) 
    return True

# Fuction to play a video in Youtube.
def PlayYoutube(query):
    # use pywhatkit's playonyt function to play the video.
    playonyt(query)
    return True

# Function to open an application or a relevant webpage.
def OpenApp(app, sess=requests.session):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True) # Attempt to oprn the app.
        return True
    
    except:
        # Nested function to extract links from HTMl content.
        def extract_link(html):
            if html is None:
                return[]
            soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
            links = soup.find_all('a', {'jsname':"UWckNb"})  # Find relevant links.
            return [link.get('href')for link in links] # Return the links.

        # Define function to perform a Google search and retrieve HTML.
        def search_google(query):
            url = f"https://www.google.com/search?q={query}" # Construct the Google search url.
            headers = {"User-Agent": useragent} # Use the predefined user-Agent.
            response = sess.get(url, headers=headers)  # Perform the GET request.

            if response.status_code == 200:
                return response.text # Return the HTML content.
            else:
                print("Failed to retrive search results.")
            return None
        
        html = search_google(app)  # Perform the google search.
        if html: 
            link = extract_link(html)[0] # Extract the first link from the search results.
            webopen(link)  # open the link in a web browser.

        return True
    
# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        pass 
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True) # Attempt to close the app.
            return True
        except:
            return False
        
# Function to execute system-level commands.
def System(command):
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute") # Stimulate the mute key press.

    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume unmute ") # Stimulate the unmute key press.    
    
    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up") # Stimulate the volume up key press.

    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down") # Stimulate the volume down key press.

    # Execute the command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True


# Asynchronous function to translate and execute user commands.
async def TrnslateAndExecute(commands: list{str}):
    funcs = [] # List to store asynchronous tasks.
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ").strip()) # Schedule app opening.
                funcs.append(fun)

        elif command.startswith("general "):
            pass  # Placeholder for general commands.
        elif command.startswith("realtime "):
             pass
        
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ").strip())
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play ").strip())
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content ").strip())
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ").strip())
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search ").strip())
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system ").strip())
            funcs.append(fun)

        else:
            print(f"No Function Found For: {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        yield result

# Asynchronous funnction to automate command execution.
async def Automation(commands: list(str)):
    async for result in TrnslateAndExecute(commands):
        pass

    return True

if __name__== "__main__":
    pass