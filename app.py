import streamlit as st
import torch
from student_model import StudentCNN
from utils import load_image, save_image
import numpy as np
import cv2
import os

st.set_page_config(page_title="Image Sharpener", layout="centered")
st.title("🔧 AI Image Sharpener (StudentCNN)")

@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = StudentCNN().to(device)
    model.load_state_dict(torch.load("student_weights_rgb.pth", map_location=device))
    model.eval()
    return model, device

model, device = load_model()

uploaded = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])
if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(image, (256, 256))

    input_tensor = torch.from_numpy(resized.astype(np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor).squeeze(0).permute(1, 2, 0).cpu().numpy()

    output = np.clip(output, 0, 1)
    sharpened = (output * 255).astype(np.uint8)

    st.subheader("Original Image")
    st.image(resized, use_column_width=True)

    st.subheader("Sharpened Image")
    st.image(sharpened, use_column_width=True)

    result_path = "results/streamlit_output.jpg"
    os.makedirs("results", exist_ok=True)
    cv2.imwrite(result_path, cv2.cvtColor(sharpened, cv2.COLOR_RGB2BGR))

    with open(result_path, "rb") as file:
        st.download_button(label="📥 Download Sharpened Image",
                           data=file,
                           file_name="sharpened.jpg",
                           mime="image/jpeg")
