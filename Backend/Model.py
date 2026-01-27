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
    # Heuristic: If it looks like a question, treat it as general query immediately.
    # This prevents the LLM from trying to "play" or "open" things for simple questions.
    lower_prompt = prompt.lower().strip()

    # Special Heuristic for Image Generation (Bypass LLM for speed/reliability)
    # PRIORITIZE THIS: Check for image keywords BEFORE checking if it's a question.
    if "generate" in lower_prompt and ("image" in lower_prompt or "picture" in lower_prompt or "photo" in lower_prompt):
        return [f"generate image {lower_prompt}"]
    if "create" in lower_prompt and ("image" in lower_prompt or "picture" in lower_prompt):
        return [f"generate image {lower_prompt}"]
    if "make" in lower_prompt and ("image" in lower_prompt or "picture" in lower_prompt):
        return [f"generate image {lower_prompt}"]

    question_starters = ["what", "who", "how", "why", "where", "when", "tell me", "explain", "hey", "hi", "hello"]

    for starter in question_starters:
        if lower_prompt.startswith(starter):
            return [f"general {lower_prompt}"]



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

    # Valid command prefixes
    command_prefixes = [
        "open ", "close ", "play ", "system ", 
        "content ", "google search ", "youtube search ", 
        "generate image ", "general ", "exit"
    ]
    
    # Filter/Validate tasks
    final_tasks = []
    for task in tasks:
        # Check if the LLM output is exactly one of the strict formats
        is_valid = False
        for prefix in command_prefixes:
            if task.startswith(prefix):
                final_tasks.append(task)
                is_valid = True
                break
        if not is_valid:
            # If prompt was "exit", model might just say "exit" (which is in prefixes but strict format)
            if task == "exit":
                final_tasks.append(task)

    # Fallback Mechanism:
    # If no valid COMMANDS were found (model outputted garbage or just keywords),
    # assume it's a GENERAL conversation using the ORIGINAL prompt.
    if not final_tasks:
        final_tasks.append(f"general {prompt}")

    return final_tasks


#entry point for the script.
if __name__ == "__main__":
    #continuously prompt the user for the input and process it.
    while True:
        print(FirstLayerDMM(input(">>>  "))) # Print the categorized response.