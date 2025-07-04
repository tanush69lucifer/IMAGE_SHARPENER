import torch
import torch.nn as nn
import torch.optim as optim
import os
from student_model import StudentCNN
from utils import load_image
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def simulate_teacher(img):
    kernel = torch.tensor([
        [[[-1, -1, -1],
          [-1,  9, -1],
          [-1, -1, -1]]]
    ], dtype=torch.float32).repeat(3, 1, 1, 1).to(img.device)
    return F.conv2d(img, kernel, padding=1, groups=3)

student = StudentCNN().to(device)
optimizer = optim.Adam(student.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

images = os.listdir("images")
for epoch in range(3):
    for name in images:
        img = load_image(f"images/{name}").to(device)
        with torch.no_grad():
            target = simulate_teacher(img)

        output = student(img)
        loss = loss_fn(output, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch+1}, Image: {name}, Loss: {loss.item():.6f}")

torch.save(student.state_dict(), "student_weights_rgb.pth")
print("Training complete. Weights saved to student_weights_rgb.pth")
