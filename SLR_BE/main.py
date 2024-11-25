from fastapi import FastAPI
# from api.routes import router as api_router
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from model.ai.LSTM_ATTENTION_RESIDUAL import LSTMModel, MultiHeadAttention
import torch
import numpy as np
from model.dto.LandmarkPayload import LandmarkPayload
from model.dto.TestDTO import TestDTO

TOTAL_POSE_LANDMARKS = 25
TOTAL_HAND_LANDMARKS = 21
TOTAL_HANDS = 2
NUM_FRAME_PROCESS = 32
TOTAL_COORDINATES = TOTAL_POSE_LANDMARKS * 3 + TOTAL_HAND_LANDMARKS * 3 * TOTAL_HANDS
fixed_size = (256, 256)
NOSE_POSITION=0

load_dotenv()
HOST = os.getenv("SLR_HOST", "127.0.0.1") 
PORT = int(os.getenv("SLR_PORT", 8000)) 
middleware_url = os.getenv("SLR_ALLOW_URL")

app = FastAPI(title='SLR', version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=middleware_url, 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

import torch
import torch.nn as nn


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model/ai/best_model.pth")
LABEL_PATH = os.path.join(BASE_DIR, "model/ai/wlasl_class_list.txt")

# Khởi tạo model
model = LSTMModel(input_size=67*3, hidden_size=128, num_layers=3, num_classes=100)
state_dict = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
model.load_state_dict(state_dict)
# model = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
model.eval()

# Tạo hai ánh xạ từ file
def load_label_mappings(label_path):
    idx_to_label = {}
    label_to_idx = {}

    with open(label_path, 'r') as file:
        for line in file:
            idx, label = line.strip().split('\t')  # Dòng được phân tách bằng tab (\t)
            idx = int(idx)  # Chuyển số thành integer
            idx_to_label[idx] = label
            label_to_idx[label] = idx

    return idx_to_label, label_to_idx

# Sử dụng ánh xạ
idx_to_label, label_to_idx = load_label_mappings(LABEL_PATH)

@app.post("/predict")
async def predict(payload: LandmarkPayload):
    print('payload::', payload)
    lm_list_detect = np.array(payload.lm_list, dtype=np.float32)  # Đảm bảo dtype là float32
    print("Landmark list received:", lm_list_detect)
    lm_list_detect = np.expand_dims(lm_list_detect, axis=0)

    V = TOTAL_POSE_LANDMARKS + TOTAL_HAND_LANDMARKS * TOTAL_HANDS
    C = 3

    lm_list_detect = lm_list_detect.reshape((lm_list_detect.shape[0], lm_list_detect.shape[1], V, C))
    lm_tensor = torch.tensor(lm_list_detect)  # Chuyển sang Tensor

    model.eval()
    with torch.no_grad():
        outputs = model(lm_tensor)  # Truyền dữ liệu qua mô hình
        _, predicted_idx = torch.max(outputs, 1)  # Lấy nhãn có xác suất cao nhất
        label = idx_to_label[predicted_idx.item()]  # Truy cập ánh xạ nhãn
        print('nhan dien::', label)
        return {"label": label}
    
@app.post("/test")
async def test(payload: TestDTO):
    return {"age": payload.age, "name": payload.name}

# app.include_router(api_router, prefix="/api/v1")

@app.get('/')
async def home():
    return "Home"

if __name__ == '__main__':
    uvicorn.run("main:app",host=HOST, port=PORT)
