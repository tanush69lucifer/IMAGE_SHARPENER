import cv2
import numpy as np
import torch

def load_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (256, 256))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)  # [1, 3, 256, 256]
    return img

def save_image(tensor, path):
    img = tensor.squeeze(0).permute(1, 2, 0).detach().cpu().numpy()
    img = np.clip(img, 0, 1)
    img = (img * 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, img)
