import torch
import torch.nn as nn
import os
import numpy as np
from model.ai.LSTM_ATTENTION import LSTMModel, MultiHeadAttention
# from model.ai import MultiHeadAttention, LSTMModel
from utils.utils.LabelMapping import load_label_mappings
from utils.utils.FixNumberFrame import fixed_num_frame
from dotenv import load_dotenv
from model.STGCN.STGCN import Model
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
scaler = StandardScaler()
NUM_CLASS = 57
TOTAL_POSE_LANDMARKS = 25
TOTAL_HAND_LANDMARKS = 21
TOTAL_HANDS = 2
NUM_FRAME_PROCESS = 30
TOTAL_COORDINATES = TOTAL_POSE_LANDMARKS * 3 + TOTAL_HAND_LANDMARKS * 3 * TOTAL_HANDS
fixed_size = (256, 256)
NOSE_POSITION=0

load_dotenv()
NUM_FRAME_PROCESS = int(os.getenv("SLR_NUM_FRAME", 30))
PREDICT_NUMBER = int(os.getenv("SLR_PREDICT_NUMBER", 5))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "../model/STGCN/model5_best_in_all_data.pth")
# LABEL_PATH = os.path.join(BASE_DIR, "../model/STGCN/class_mapping.txt")

# # Khởi tạo model
# model = LSTMModel(input_size=67*3, hidden_size=128, num_layers=3, num_classes=NUM_CLASS)
# state_dict = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
# model.load_state_dict(state_dict)
# # model = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
# model.eval()

# # Sử dụng ánh xạ
# idx_to_label, label_to_idx = load_label_mappings(LABEL_PATH)

#STGCN
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../model/STGCN/model5_best_in_all_data.pth")
LABEL_PATH = os.path.join(BASE_DIR, "../model/STGCN/class_mapping.txt")
SCALE_PATH = os.path.join(BASE_DIR, "../model/STGCN/scaler.pkl")

loaded_scaler = joblib.load(SCALE_PATH)
detailed_body_connections = [(0, 1), (0, 4), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 7), (4, 0), (4, 5), (5, 6), (5, 4), (6, 8), (6, 5), (7, 3), (8, 6), (9, 10), (10, 9), (11, 12), (11, 13), (12, 11), (12, 14), (13, 11), (13, 15), (14, 12), (14, 16), (15, 13), (15, 17), (15, 21), (16, 14), (16, 18), (16, 22), (17, 15), (17, 19), (18, 16), (18, 20), (19, 15), (19, 17), (20, 16), (20, 18), (21, 15), (21, 19), (22, 16), (23, 24), (23, 11), (24, 12), (24, 23), (25, 26), (26, 25), (26, 27), (27, 26), (27, 28), (28, 27), (28, 29), (29, 28), (30, 25), (30, 31), (30, 34), (31, 30), (31, 32), (32, 31), (32, 33), (33, 32), (34, 30), (34, 38), (35, 34), (35, 36), (36, 35), (36, 37), (37, 36), (38, 34), (38, 42), (38, 39), (39, 38), (39, 40), (40, 39), (40, 41), (41, 40), (42, 38), (42, 43), (43, 42), (43, 44), (44, 43), (44, 45), (45, 44), (46, 47), (47, 46), (47, 48), (48, 47), (48, 49), (49, 48), (49, 50), (50, 49), (51, 46), (51, 52), (51, 55), (52, 51), (52, 53), (53, 52), (53, 54), (54, 53), (55, 51), (55, 59), (56, 55), (56, 57), (57, 56), (57, 58), (58, 57), (59, 55), (59, 63), (59, 60), (60, 59), (60, 61), (61, 60), (61, 62), (62, 61), (63, 59), (63, 64), (64, 63), (64, 65), (65, 64), (65, 66), (66, 65)]
# Khởi tạo model
model = Model(in_channels=3, num_nodes=67, inward_edges=detailed_body_connections, n_classes=NUM_CLASS, dropout_ratio = 0.1,batch_norm=True)
state_dict = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
model.load_state_dict(state_dict)
# model = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
model.eval()

# Sử dụng ánh xạ
idx_to_label, label_to_idx = load_label_mappings(LABEL_PATH)


# def predict(payload):
#     print('payload::', len(payload.lm_list))
#     lm_list_detect = np.array(payload.lm_list, dtype=np.float32)  # Đảm bảo dtype là float32
#     lstLabel = []
#     lm_list_detect_temp = lm_list_detect
#     max_confidence = 0
#     best_label = None

#     for i in range(PREDICT_NUMBER):
#         print(NUM_FRAME_PROCESS)
#         lm_list_detect = fixed_num_frame(lm_list_detect_temp, NUM_FRAME_PROCESS)
#         lm_list_detect = np.expand_dims(lm_list_detect, axis=0)

#         V = TOTAL_POSE_LANDMARKS + TOTAL_HAND_LANDMARKS * TOTAL_HANDS
#         C = 3

#         lm_list_detect = lm_list_detect.reshape((lm_list_detect.shape[0], lm_list_detect.shape[1], V, C))
#         lm_tensor = torch.tensor(lm_list_detect)  # Chuyển sang Tensor

#         model.eval()
#         with torch.no_grad():
#             outputs = model(lm_tensor)  # Truyền dữ liệu qua mô hình
#            # Tính toán xác suất (probabilities)
#             probabilities = torch.softmax(outputs, dim=1)  # Chuyển đổi thành xác suất
#             _, predicted_idx = torch.max(probabilities, 1)
#              # Xác suất của nhãn dự đoán
#             confidence = probabilities[0, predicted_idx].item() * 100

#             label = idx_to_label[predicted_idx.item()]  # Truy cập ánh xạ nhãn
#             print(f'Nhãn: {label} - {confidence:.2f}%')
#             # lstLabel.append(label)
#             if confidence > max_confidence:
#                 max_confidence = confidence
#                 best_label = label
#     return best_label


def predict_with_STGCN(payload):
    print('payload::', len(payload.lm_list))
    lm_list_detect = np.array(payload.lm_list, dtype=np.float32)  # Đảm bảo dtype là float32
    lstLabel = []
    lm_list_detect_temp = lm_list_detect
    max_confidence = 0
    best_label = None
    lm_list_detect = fixed_num_frame(lm_list_detect_temp, NUM_FRAME_PROCESS)
    lm_list_detect = np.expand_dims(lm_list_detect, axis=0)

    V = TOTAL_POSE_LANDMARKS + TOTAL_HAND_LANDMARKS * TOTAL_HANDS
    C = 3

    lm_list_detect = lm_list_detect.reshape((lm_list_detect.shape[0], lm_list_detect.shape[1], V, C))
    lm_tensor = torch.tensor(lm_list_detect)  # Chuyển sang Tensor
    lm_tensor = lm_tensor.permute(0,3,1,2)
    lm_tensor = scale(lm_tensor)
    model.eval()
    with torch.no_grad():
        outputs = model(lm_tensor)  # Dự đoán từ mô hình
        predicted_classes = torch.argmax(outputs, dim=1)  # Lấy nhãn có xác suất cao nhất
            # Xác suất của nhãn dự đoán

        label = idx_to_label[predicted_classes.item()]  # Truy cập ánh xạ nhãn
        print(f'Nhãn: {label}')
            
    return label

def scale(lm_tensor):
    batch_data = lm_tensor[0]
    batch_x = batch_data[0].t()
    batch_y = batch_data[1].t()
    batch_s = batch_data[2]
    x_scaled_data = scaler.fit_transform(batch_x.numpy())
    y_scaled_data = scaler.fit_transform(batch_y.numpy())
    batch_x = torch.from_numpy(x_scaled_data).t()
    batch_y = torch.from_numpy(y_scaled_data).t()
    batch = torch.stack([batch_x, batch_y, batch_s])
    return batch.unsqueeze(0)



