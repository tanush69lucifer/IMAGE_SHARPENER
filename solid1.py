import os
import random
from PIL import Image
import zipfile

# Settings
num_images = 5000
image_size = (256, 256)
output_folder = "solid_colors"
os.makedirs(output_folder, exist_ok=True)

# Create solid color images
for i in range(1, num_images + 1):
    rgb = tuple(random.randint(0, 255) for _ in range(3))
    img = Image.new("RGB", image_size, rgb)
    filename = f"img_{i:05d}_{rgb[0]}_{rgb[1]}_{rgb[2]}.jpg"
    img.save(os.path.join(output_folder, filename), "JPEG", quality=95)

# Optional: Create zip file
with zipfile.ZipFile("solid_colors_5000.zip", "w") as zipf:
    for file in os.listdir(output_folder):
        zipf.write(os.path.join(output_folder, file), arcname=file)

print("✅ Done! 5000 solid color JPG images created and zipped.")
