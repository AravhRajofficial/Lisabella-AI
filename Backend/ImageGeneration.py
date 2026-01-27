import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
import platform

# Function to open and display images based on a given prompt.
def open_images(prompt):
    folder_path = r"Data"  # Folder where the images are stored.
    prompt = prompt.replace(" ", "_") # Replace spaces within prompt with underscores.

    # Generate the file name for the image.
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            print(f"Opening image: {image_path}")
            # Use os.startfile on Windows for a more reliable opening behavior
            if platform.system() == "Windows":
                os.startfile(image_path)
            else:
                img = Image.open(image_path)
                img.show()
            sleep(1)  # pause for 1 second before showing the next image.

        except (IOError, FileNotFoundError):
            print(f"Unable to open or find {image_path}")

# List of API URLs (Fallback Strategy)
# If the first one fails (410 Gone), the code will automatically try the next one.
API_URLS = [
    "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
    "https://router.huggingface.co/hf-inference/models/prompthero/openjourney-v4",
    "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-2-1",
    "https://router.huggingface.co/hf-inference/models/runwayml/stable-diffusion-v1-5",
    "https://router.huggingface.co/hf-inference/models/CompVis/stable-diffusion-v1-4"
]

# Get the API key, with a fallback to empty string if not found
huggingface_api_key = get_key('.env', 'HuggingFaceAPIKey')
if not huggingface_api_key:
    print("Warning: HuggingFaceAPIKey not found in .env file. Image generation will not work.")
    print("Please add your HuggingFaceAPIKey to the .env file.")
    huggingface_api_key = ""

headers = {"Authorization": f"Bearer {huggingface_api_key}"}

# Async function to send a query to the Hugging Face API
# Now supports retrying with different models
async def query(payload):
    if not huggingface_api_key:
        print("Error: Cannot query Hugging Face API without an API key.")
        return None
        
    for url in API_URLS:
        try:
            print(f"Attempting with model: {url.split('/')[-2]}/{url.split('/')[-1]}")
            response = await asyncio.to_thread(requests.post, url, headers=headers, json=payload)
            
            # If successful, return the content immediately
            if response.status_code == 200:
                print("Success!")
                return response.content
            
            # If error is 410 (Gone) or 503 (Loading), print and try next
            print(f"Failed with status {response.status_code}: {response.text}") # Print FULL error
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            
    print("All models failed.")
    return None

# Async function to generate image based on the given prompt
async def generate_images(prompt: str):
    if not huggingface_api_key:
        print("Error: Cannot generate images without a Hugging Face API key.")
        print("Please add your HuggingFaceAPIKey to the .env file.")
        return False
        
    tasks = []
    print(f"Starting generation for: '{prompt}'")
    
    # We will generate 4 images. 
    # Since we have a fallback loop inside 'query', each task will independently find a working model.
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, 4k, sharp, high quality, realistic, seed={randint(0, 100000)}"
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Then, gather them all at once
    print("Generating 4 images concurrently (with auto-fallback)...")
    image_bytes_list = await asyncio.gather(*tasks)
    print("Image data received. Saving files...")

    # Check if any images were generated
    if not any(image_bytes_list):
        print("No images were generated. API request may have failed.")
        return False

    # Ensure the 'Data' directory exists before saving files
    os.makedirs("Data", exist_ok=True)

    # Then, save all the files
    saved_files = []
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            file_path = os.path.join("Data", f"{prompt.replace(' ', '_')}{i+1}.jpg")
            try:
                with open(file_path, "wb") as f:
                    f.write(image_bytes)
                print(f"Saved image {i+1} to {file_path}")
                saved_files.append(os.path.abspath(file_path))
            except IOError as e:
                print(f"Failed to save image {i+1}: {e}")
    
    return saved_files 

# Wrapper function to generate and open images
def GenerateImages(prompt:str):
    generated_files = asyncio.run(generate_images(prompt))  # Run the async image generation
    if generated_files:
        # open_images(prompt) # DISABLED: We now show in GUI
        return generated_files # Return paths to Main
    else:
        print("Image generation failed.")
        return []

# Main loop to monitor for image generation requests
if __name__ == "__main__":
    print("Image Generation script started. Monitoring for requests...")
    while True:
        try:
            # Read the status and prompt from the data file
            with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
                data = f.read().strip()
            
            if not data:
                sleep(2)
                continue

            prompt, status = data.split(",", 1)

            # if the status indicates an image generation request
            if status.lower() == "true":
                print(f"Request received. Generating images for prompt: '{prompt}'")
                files = GenerateImages(prompt=prompt)

                # Reset the status in the file after generating images
                if files:
                    print("Processing complete. Resetting status and exiting.")
                else:
                    print("Image generation failed. Resetting status and exiting.")
                    
                with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                    f.write("False,False")
                break # exit the loop after processing the request
            else:
                sleep(2) # Wait before checking the file again

        except FileNotFoundError:
            print("Waiting for Frontend\Files\ImageGeneration.data to be created...")
            sleep(5)
        except ValueError as e:
            print(f"Error parsing data file: {e}")
            print("Resetting status and continuing...")
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            sleep(2)
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            print("Resetting status and exiting to prevent error loop.")
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break