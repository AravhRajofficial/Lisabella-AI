import os  #import the OS library 
from rich import print #import the Rich library to ehance terminal outputs.
from llama_cpp import Llama

MODEL_PATH = os.path.join("Models", "LLM", "phi-2.Q4_K_M.gguf")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_gpu_layers=20, #GPU offload 
    verbose=False
)

#Define a list of recognized function keyword for task categorization.
funcs =[
    "exit", "general", "realtime", "open", "close", "play", "generate image", "system", "content", "google search", "youtube search", "reminder"
]

def FirstLayerDMM(prompt: str):
    system_prompt = """
    You are a decision-making model.
    Classify the user query into tasks with STRICT prefixes.
    
    Valid STRICT formats:
    - open [app/website]
    - close [app/website]
    - play [song name]
    - google search [query]
    - youtube search [query]
    - system [command]
    - content [topic]
    - generate image [prompt]
    - general [query]
    - exit

    Example:
    Query: "open youtube"
    Output: open youtube

    Query: "play song hello"
    Output: play hello

    Rules:
    - ALWAYS start with one of the prefixes above.
    - Do NOT just obtain the noun (e.g. do not return "youtube", return "open youtube").
    - Return ONLY comma-separated tasks.
    """

    full_prompt = f"{system_prompt}\nUser: {prompt}\nAssistant:"

    output = llm(
        full_prompt,
        max_tokens=50,
        stop=["\n", "User:"]
    )

    text = output["choices"][0]["text"].strip().lower()


    # split & clean
    tasks = [t.strip() for t in text.split(",") if t.strip()]

    return tasks


#entry point for the script.
if __name__ == "__main__":
    #continuously prompt the user for the input and process it.
    while True:
        print(FirstLayerDMM(input(">>>  "))) # Print the categorized response.