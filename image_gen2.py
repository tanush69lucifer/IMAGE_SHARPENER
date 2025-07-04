import os
import random
from PIL import Image
import zipfile

# Settings
image_size = (256, 256)
num_images = 500
output_dir = "rgb_images"
zip_filename = "rgb_images_256x256.zip"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Generate images
for i in range(num_images):
    color = tuple(random.randint(0, 255) for _ in range(3))  # Random RGB color
    img = Image.new("RGB", image_size, color)
    filename = f"img_{i+1:03d}_{color[0]}_{color[1]}_{color[2]}.jpg"
    img.save(os.path.join(output_dir, filename), format="JPEG", quality=95)

# Zip the folder
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for file in os.listdir(output_dir):
        zipf.write(os.path.join(output_dir, file), arcname=file)

print(f"\n✅ Done! JPG images saved and zipped: {zip_filename}")
