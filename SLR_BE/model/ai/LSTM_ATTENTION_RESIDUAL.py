import torch
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, embed_size, num_heads):
        super(MultiHeadAttention, self).__init__()
        self.attention = nn.MultiheadAttention(embed_size, num_heads)

    def forward(self, x, mask=None):
        # Chuyển đổi đầu vào để phù hợp với yêu cầu của MultiHeadAttention trong PyTorch
        x = x.transpose(0, 1)  # Đổi thứ tự từ (N, T, E) sang (T, N, E)
        attn_output, _ = self.attention(x, x, x, attn_mask=mask)
        return attn_output.transpose(0, 1)  # Chuyển lại thứ tự từ (T, N, E) về (N, T, E)

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes, dropout=0.1, bidirectional=True, num_heads=8):
        super(LSTMModel, self).__init__()

        # Feature Augmentation Layer (FA)
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.bn1 = nn.BatchNorm1d(hidden_size)

        # LSTM Layers (Tăng số lớp LSTM hoặc tăng hidden size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True,
                            dropout=dropout, bidirectional=bidirectional)
        self.bn_lstm = nn.BatchNorm1d(hidden_size * 2 if bidirectional else hidden_size)

        # Multi-Head Attention Layer (Thêm số lượng đầu attention lớn hơn)
        self.attention = MultiHeadAttention(hidden_size * 2 if bidirectional else hidden_size, num_heads=num_heads)

        # Fully connected layer để phân loại từ
        self.fc_out = nn.Linear(hidden_size * 2, num_classes)  # Dự đoán 1 từ (hoặc lớp)

        # Dropout layers
        self.dropout = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(0.3)  # Thêm dropout mạnh mẽ hơn

        # Layer Normalization
        self.ln_lstm = nn.LayerNorm(hidden_size * 2 if bidirectional else hidden_size)
        self.ln_fc = nn.LayerNorm(num_classes)  # LayerNorm phải áp dụng cho số lớp đầu ra

    def forward(self, x):
        # Đầu vào có kích thước (N, T, V, C)
        N, T, V, C = x.size()

        # Gộp số lượng khớp (V) và số chiều tọa độ (C) để thành một vector đặc trưng duy nhất (N, T, V*C)
        x = x.view(N, T, V * C)  # (N, T, V*C)

        # Feature Augmentation (Tăng cường đặc trưng đầu vào)
        x = self.fc1(x)  # (N, T, hidden_size)
        x = self.bn1(x.transpose(1, 2)).transpose(1, 2)  # BatchNorm sau fully connected
        x = self.relu(x)
        x = self.dropout(x)

        # LSTM layer (Xử lý chuỗi thời gian)
        x, (hn, cn) = self.lstm(x)  # (N, T, 2*hidden_size)
        x = self.bn_lstm(x.transpose(1, 2)).transpose(1, 2)  # BatchNorm sau LSTM

        # LayerNorm sau LSTM
        x = self.ln_lstm(x)  # LayerNorm sau LSTM

        # Multi-Head Attention
        x = self.attention(x)

        # Dự đoán từ duy nhất cho toàn bộ video
        x_out = self.fc_out(x[:, -1, :])  # (N, num_classes), dùng output của bước cuối cùng trong chuỗi

        # LayerNorm sau Fully Connected layer
        x_out = self.ln_fc(x_out)  # LayerNorm trên đầu ra cuối cùng

        return x_out
