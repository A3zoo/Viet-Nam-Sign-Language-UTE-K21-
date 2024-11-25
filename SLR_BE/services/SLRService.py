# import torch
# import pickle
# import numpy as np
# import os
# from model.ai.LSTM_ATTENTION_RESIDUAL import LSTMModel, MultiHeadAttention
# # from services.LSTM_ATTENTION_RESIDUAL import LSTMModel, MultiHeadAttention

# TOTAL_POSE_LANDMARKS = 25
# TOTAL_HAND_LANDMARKS = 21
# TOTAL_HANDS = 2
# NUM_FRAME_PROCESS = 32
# TOTAL_COORDINATES = TOTAL_POSE_LANDMARKS * 3 + TOTAL_HAND_LANDMARKS * 3 * TOTAL_HANDS
# fixed_size = (256, 256)
# NOSE_POSITION=0

# # Load model and label encoder
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(CURRENT_DIR, "./LSTM_model_resedual.pth")

# model = LSTMModel(input_size=67*3, hidden_size=128, num_layers=3, num_classes=100,)
# model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
# model.eval()

# with open('../model/ai/label_encoder.pkl', 'rb') as f:
#     label_encoder = pickle.load(f)

# def predict(lm_list):
#     lm_list_detect = np.array(lm_list, dtype=np.float32)  # Đảm bảo dtype là float32
#     lm_list_detect = np.expand_dims(lm_list_detect, axis=0)

#     V = TOTAL_POSE_LANDMARKS + TOTAL_HAND_LANDMARKS * TOTAL_HANDS
#     C = 3

#     lm_list_detect = lm_list_detect.reshape((lm_list_detect.shape[0], lm_list_detect.shape[1], V, C))
#     lm_tensor = torch.tensor(lm_list_detect)  # Chuyển sang Tensor

#     model.eval()
#     with torch.no_grad():
#         outputs = model(lm_tensor)  # Truyền dữ liệu qua mô hình
#         _, predicted_idx = torch.max(outputs, 1)  # Lấy nhãn có xác suất cao nhất
#         label = label_encoder.inverse_transform([predicted_idx.item()])[0]
#         print('nhan dien::', label)
#         return label

