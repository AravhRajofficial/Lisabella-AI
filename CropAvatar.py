from PIL import Image
import os

# Source Image
source_path = r"C:/Users/ARVH/.gemini/antigravity/brain/f2169eb7-c5c0-4c78-8c99-7216c603c180/uploaded_image_1768988692500.jpg"
output_dir = r"Frontend/Graphics"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    img = Image.open(source_path)
    width, height = img.size
    
    # Grid dimensions (It's a 2 column x 3 row grid based on the visual, or 2x3?)
    # Looking at the image: It has 2 columns and 3 rows.
    # Total 6 faces.
    
    cell_width = width // 2
    cell_height = height // 3
    
    # 1. Idle (Top Left) - Row 0, Col 0
    idle_area = (0, 0, cell_width, cell_height)
    img_idle = img.crop(idle_area)
    img_idle.save(os.path.join(output_dir, "Avatar_Idle.png"))
    print("Saved Avatar_Idle.png")
    
    # 2. Blink/Happy (Top Right) - Row 0, Col 1
    # Closed eyes usually work for blinking
    blink_area = (cell_width, 0, width, cell_height)
    img_blink = img.crop(blink_area)
    img_blink.save(os.path.join(output_dir, "Avatar_Blink.png"))
    print("Saved Avatar_Blink.png")
    
    # 3. Talking (Middle Right) - Row 1, Col 1
    # This one has the music note and open mouth
    talk_area = (cell_width, cell_height, width, cell_height * 2)
    img_talk = img.crop(talk_area)
    img_talk.save(os.path.join(output_dir, "Avatar_Talking.png"))
    print("Saved Avatar_Talking.png")

except Exception as e:
    print(f"Error processing image: {e}")
