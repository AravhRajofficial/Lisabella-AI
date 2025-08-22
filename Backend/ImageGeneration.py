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

# API details for the Hugging Face stable diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Get the API key, with a fallback to empty string if not found
huggingface_api_key = get_key('.env', 'HuggingFaceAPIKey')
if not huggingface_api_key:
    print("Warning: HuggingFaceAPIKey not found in .env file. Image generation will not work.")
    print("Please add your HuggingFaceAPIKey to the .env file.")
    huggingface_api_key = ""

headers = {"Authorization": f"bearer {huggingface_api_key}"}

# Async function to send a query to the Hugging Face API
async def query(payload):
    if not huggingface_api_key:
        print("Error: Cannot query Hugging Face API without an API key.")
        return None
        
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

# Async function to generate image based on the given prompt
async def generate_images(prompt: str):
    if not huggingface_api_key:
        print("Error: Cannot generate images without a Hugging Face API key.")
        print("Please add your HuggingFaceAPIKey to the .env file.")
        return False
        
    tasks = []
    print("Creating 4 image generation tasks...")
    # First, create all the tasks
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, 4k, sharp, high quality, high resolution, seed={randint(0, 100000)}"
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Then, gather them all at once
    print("Generating 4 images concurrently...")
    image_bytes_list = await asyncio.gather(*tasks)
    print("Image data received. Saving files...")

    # Check if any images were generated
    if not any(image_bytes_list):
        print("No images were generated. API request may have failed.")
        return False

    # Ensure the 'Data' directory exists before saving files
    os.makedirs("Data", exist_ok=True)

    # Then, save all the files
    success_count = 0
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            file_path = os.path.join("Data", f"{prompt.replace(' ', '_')}{i+1}.jpg")
            try:
                with open(file_path, "wb") as f:
                    f.write(image_bytes)
                print(f"Saved image {i+1} to {file_path}")
                success_count += 1
            except IOError as e:
                print(f"Failed to save image {i+1}: {e}")
    
    return success_count > 0  # Return True if at least one image was saved

# Wrapper function to generate and open images
def GenerateImages(prompt:str):
    success = asyncio.run(generate_images(prompt))  # Run the async image generation
    if success:
        open_images(prompt) # open the generated images
        return True
    else:
        print("Image generation failed. Cannot open images.")
        return False

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
                success = GenerateImages(prompt=prompt)

                # Reset the status in the file after generating images
                if success:
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