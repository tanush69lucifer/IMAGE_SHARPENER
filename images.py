import cv2
import os
from glob import glob

input_dir = 'DIV2K_train_HR'  # path to downloaded dataset
output_sharp = 'dataset/sharp'
output_blur = 'dataset/blurred'

os.makedirs(output_sharp, exist_ok=True)
os.makedirs(output_blur, exist_ok=True)

image_paths = glob(f'{input_dir}/*.png')[:8000]  # take first 8000

for i, path in enumerate(image_paths):
    img = cv2.imread(path)
    if img is None:
        continue
    
    img = cv2.resize(img, (256, 256))
    blurred = cv2.GaussianBlur(img, (7, 7), sigmaX=1.5)

    cv2.imwrite(f"{output_sharp}/img_{i+1:04d}.jpg", img)
    cv2.imwrite(f"{output_blur}/img_{i+1:04d}.jpg", blurred)
