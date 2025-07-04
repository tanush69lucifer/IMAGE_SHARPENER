import torch
from student_model import StudentCNN
from utils import load_image, save_image
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = StudentCNN().to(device)
model.load_state_dict(torch.load("student_weights_rgb.pth", map_location=device))
model.eval()

os.makedirs("results", exist_ok=True)

img = load_image("images/test.jpg").to(device)

with torch.no_grad():
    out = model(img)

save_image(out, "results/sharpened.jpg")
print("Sharpened image saved to results/sharpened.jpg")
