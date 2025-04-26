from groq import Groq # importing the Groq API to use its API.
from json import load, dump # importing functions to read and write json files.
import datetime # importing the datetime module for real-time date and timme information.
from dotenv import dotenv_values # importing dotenv_values to read environment variables from the .env file.
import os 

#load environmental variables from the .env file.
env_vars = dotenv_values(".env")

GroqAPIKey = env_vars.get("GroqAPIKey")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

print(f"GroqAPIKey: {GroqAPIKey}")
if not GroqAPIKey:
    raise ValueError("Missing GroqAPIKey in .env file.")

#Initialize the Groq client using the provided API Key.
client = Groq(api_key=GroqAPIKey)

#Initialize an empty list to state that messages'
messages = []

# Define a system message that provides context to the API Chatbot about its role and behaviour
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# A list of system instruction for its chatbot.
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load tje chat log from a JSON file.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f) # load existing message from the chat log.
except FileNotFoundError:
    #If the file doesn't exist, crate an empty JSOn file to store chat logs.
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to get real-time date and time information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now() # get the current date and time.
    day = current_date_time.strftime("%A") # Day of the week.
    date = current_date_time.strftime("%d") # Day of the month.
    month = current_date_time.strftime("%B") # Full month name.
    year = current_date_time.strftime("%Y") # Year
    hour = current_date_time.strftime("%H") # Hour in 24-hour format.
    minute = current_date_time.strftime("%M") # Minute.
    second = current_date_time.strftime("%S") # Second.

     # Format the information into a string.
    data = f"Please use this real-time information if needed,\n"
    data += f"Day:{day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes :{second} seconds.\n"
    return data

# Function tp modify the Chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split("\n") # splites the response into lines.
    non_empty_lines = [line for line in lines if line.strip()] # removes empty lines.
    modified_answer = "\n".join(non_empty_lines) # Join the element lines back together.
    return modified_answer

# Main chatbot functions to handel users queries.
def ChatBot(Query):
    """This function sends the user's query to the ChatBot and returns the AI's response."""

    try :
        # Load the existing chat log from the JSONN files.
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        
        # Append the user's query to the messages list.
        messages.append({"role": "user", "content": f"{Query}"})

        # Make a request to the Groq API for a response.
        completion = client.chat.completions.create(
            model = "llama3-70b-8192", # Specify the AI model to use.
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages, # Includes system instructions
            max_tokens=1024, # Limits the maximum tokens in the response.
            temperature = 0.7, # Adjust response randomness (higher means more random).
            top_p=1, # use necleus sampling to control diversity.
            stream = True, # Enable streaming response.
            stop=None # Allow the model to cetermine when to stop. 
        )

        Answer = "" # Initialize an empty string to store the AI's response.

        # Process the streamed response chunls.
        for chunk in completion :
            if chunk.choices[0].delta.content: # Check if there is content in the current chunk.
                Answer += chunk.choices[0].delta.content # Append the content to the answer.
        
        Answer = Answer.replace("</s>", "") # Clean up any unwanted tokens from the response.

        # Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log to the JSON file.
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        
        # Return the formatted response.
        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        # Handles the error by printing the exception and resetting the loop.
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query) # Retry the query after resetting the log.
    
# main program entry point.
if __name__=="__main__":
    while True:
        user_input = input("Enter Your Question:") # Prompt the user for a question
        print(ChatBot(user_input)) # Call the chatbot function and print it's response.