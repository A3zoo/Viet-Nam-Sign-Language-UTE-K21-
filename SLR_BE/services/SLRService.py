import torch
import torch.nn as nn
import os
import numpy as np
from model.ai.LSTM_ATTENTION import LSTMModel, MultiHeadAttention
# from model.ai import MultiHeadAttention, LSTMModel
from utils.LabelMapping import load_label_mappings
from utils.FixNumberFrame import fixed_num_frame
from dotenv import load_dotenv

NUM_CLASS = 63
TOTAL_POSE_LANDMARKS = 25
TOTAL_HAND_LANDMARKS = 21
TOTAL_HANDS = 2
NUM_FRAME_PROCESS = 32
TOTAL_COORDINATES = TOTAL_POSE_LANDMARKS * 3 + TOTAL_HAND_LANDMARKS * 3 * TOTAL_HANDS
fixed_size = (256, 256)
NOSE_POSITION=0

load_dotenv()
NUM_FRAME_PROCESS = int(os.getenv("SLR_NUM_FRAME", 32))
PREDICT_NUMBER = int(os.getenv("SLR_PREDICT_NUMBER", 5))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../model/ai/best_model_lstm_attention2.pth")
LABEL_PATH = os.path.join(BASE_DIR, "../model/ai/class_list.txt")

# Khởi tạo model
model = LSTMModel(input_size=67*3, hidden_size=128, num_layers=3, num_classes=NUM_CLASS)
state_dict = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
model.load_state_dict(state_dict)
# model = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
model.eval()

# Sử dụng ánh xạ
idx_to_label, label_to_idx = load_label_mappings(LABEL_PATH)


def predict(payload):
    print('payload::', len(payload.lm_list))
    lm_list_detect = np.array(payload.lm_list, dtype=np.float32)  # Đảm bảo dtype là float32
    lstLabel = []
    lm_list_detect_temp = lm_list_detect
    max_confidence = 0
    best_label = None

    for i in range(PREDICT_NUMBER):
        print(NUM_FRAME_PROCESS)
        lm_list_detect = fixed_num_frame(lm_list_detect_temp, NUM_FRAME_PROCESS)
        lm_list_detect = np.expand_dims(lm_list_detect, axis=0)

        V = TOTAL_POSE_LANDMARKS + TOTAL_HAND_LANDMARKS * TOTAL_HANDS
        C = 3

        lm_list_detect = lm_list_detect.reshape((lm_list_detect.shape[0], lm_list_detect.shape[1], V, C))
        lm_tensor = torch.tensor(lm_list_detect)  # Chuyển sang Tensor

        model.eval()
        with torch.no_grad():
            outputs = model(lm_tensor)  # Truyền dữ liệu qua mô hình
           # Tính toán xác suất (probabilities)
            probabilities = torch.softmax(outputs, dim=1)  # Chuyển đổi thành xác suất
            _, predicted_idx = torch.max(probabilities, 1)
             # Xác suất của nhãn dự đoán
            confidence = probabilities[0, predicted_idx].item() * 100

            label = idx_to_label[predicted_idx.item()]  # Truy cập ánh xạ nhãn
            print(f'Nhãn: {label} - {confidence:.2f}%')
            # lstLabel.append(label)
            if confidence > max_confidence:
                max_confidence = confidence
                best_label = label
    return best_label



