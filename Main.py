
from Backend.SpeechToText import SpeechRecognition
import os

def main():
    """
    Main function to run the Lisabella AI assistant.
    """
    print("Lisabella AI started. Listening for commands...")
    while True:
        command = SpeechRecognition()
        if command:
            if "generate image" in command.lower() or "create a picture of" in command.lower():
                # Extract the prompt from the command
                prompt = command.lower().replace("generate image of", "").replace("generate image", "").replace("create a picture of", "").strip()
                if prompt:
                    print(f"Image generation prompt: {prompt}")
                    # Write the prompt to the data file to trigger image generation
                    try:
                        with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "w") as f:
                            f.write(f"{prompt},True")
                        print("Image generation request sent.")
                    except FileNotFoundError:
                        print("Error: Could not find ImageGeneration.data file.")
                else:
                    print("No prompt found for image generation.")
            else:
                # Here you can add other commands for the assistant
                print(f"Command received: {command}")


if __name__ == "__main__":
    main()
