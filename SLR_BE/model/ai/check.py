import torch
from LSTM_ATTENTION_RESIDUAL import LSTMModel, MultiHeadAttention
MODEL_PATH = "./model_checkpoint.pth"

# Tải nội dung file
data = torch.load(MODEL_PATH, map_location=torch.device("cpu"))

# Kiểm tra kiểu dữ liệu
if isinstance(data, dict):
    print("File chứa state_dict.")
    print("Các keys trong state_dict:", data.keys())  # In ra các keys của state_dict
else:
    print("File chứa toàn bộ model.")
    print("Loại dữ liệu lưu:", type(data))
