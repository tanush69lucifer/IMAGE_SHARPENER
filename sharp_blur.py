import os
import urllib.request
from PIL import Image, ImageFilter
from io import BytesIO
import zipfile

# Settings
num_images = 500
image_size = (256, 256)
base_dir = "sharpen_dataset"
sharp_dir = os.path.join(base_dir, "sharp")
blurred_dir = os.path.join(base_dir, "blurred")

# Create folders
os.makedirs(sharp_dir, exist_ok=True)
os.makedirs(blurred_dir, exist_ok=True)

# Download and process images
for i in range(num_images):
    try:
        url = f"https://picsum.photos/seed/{i}/256/256"
        response = urllib.request.urlopen(url)
        img = Image.open(BytesIO(response.read())).convert("RGB")
        img = img.resize(image_size)

        # Save sharp
        sharp_path = os.path.join(sharp_dir, f"img_{i+1:03d}.jpg")
        img.save(sharp_path, "JPEG", quality=95)

        # Save blurred
        blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
        blurred_path = os.path.join(blurred_dir, f"img_{i+1:03d}.jpg")
        blurred.save(blurred_path, "JPEG", quality=95)

        print(f"Saved image {i+1}")
    except Exception as e:
        print(f"Error with image {i+1}: {e}")

# Optional: Zip the dataset
with zipfile.ZipFile("sharpen_dataset.zip", "w") as zipf:
    for folder in [sharp_dir, blurred_dir]:
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            zipf.write(path, arcname=os.path.relpath(path, base_dir))

print("\n✅ Done! Dataset ready and zipped.")
