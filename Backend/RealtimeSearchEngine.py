from googlesearch import search
from groq import Groq #improting the groq library to use its API.
from json import load, dump # importing functions to read and write JSON files.
import datetime #importing the datetime module for real-time date and time information.
from dotenv import dotenv_values # importing dotenv_values to read environment variables from a .env files.

#load environment variables from the .env files.
env_vars = dotenv_values(".env")

# Retrieve environment varriable for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client with the provided API Key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try :
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load (f)
except :
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to perform a google search and format the results.
def Googlesearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for'{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

# Predefined Chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can i help you?"}
]

# Function to get real-time information like the current date and time.
def information():
    date = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minutes = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    date += f"Use This Real-time Information if needed:\n"
    date += f"Day: {day}\n"
    date += f"Date: {date}\n"
    date += f"Month: {month}\n"
    date += f"Year: {year}\n"
    date += f"Time: {hour} hours, {minutes} minutes, {second} seconds.\n"
    return date

#function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # load the chat log from the JSON file.
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role": "system", "content": Googlesearch(prompt)})

    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model= "llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer =""

    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # clean up the response.
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log back to the JSON file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
    
    # Remove the most recent message from the chatbot conversation.
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# Main entry point of the program for interactive quering.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))