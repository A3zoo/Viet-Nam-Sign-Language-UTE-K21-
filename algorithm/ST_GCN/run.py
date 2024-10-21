import torch

import os
parent_dir = 'D:\\Semester_7\\GraduationProject\\SLR\\Viet-Nam-Sign-Language-UTE-K21-\\data_set\\mediapipe_sequences'
a =[]
lable_decode = []
for lable in os.listdir(parent_dir):
    video_dir = os.path.join(parent_dir, lable)
    for file_name in os.listdir(video_dir):
        lable_decode.append(lable)
        input_file = os.path.join(video_dir, file_name)
        tensor = torch.load(input_file)
        tensor = torch.einsum('xyz->zxy', tensor)
        a.append(tensor)

batch = torch.stack(a)

batch.shape
len(lable_decode)
tensortest = batch[1]
tensor_reshaped = tensortest.unsqueeze(0)
tensor_reshaped.shape

import torch.nn.functional as F

# Danh sách cần one-hot encode
lst = lable_decode

# Tạo từ điển ánh xạ chuỗi sang số nguyên
unique_labels = list(set(lst))  # Lấy các giá trị duy nhất
label_to_index = {label: index for index, label in enumerate(unique_labels)}

# Chuyển đổi danh sách chuỗi thành danh sách chỉ số
indices = [label_to_index[label] for label in lst]

# Chuyển danh sách chỉ số thành tensor
tensor_indices = torch.tensor(indices)

# Sử dụng one-hot encoding (num_classes = len(unique_labels))
one_hot_encoded = F.one_hot(tensor_indices, num_classes=len(unique_labels))

# In kết quả
print("Unique Labels:", unique_labels)
print("One-Hot Encoded:\n", one_hot_encoded)
print(one_hot_encoded[1:10])
# Kết nối khớp cơ thể (Pose Estimation)
body_connections = [
    (0, 6),  # Mũi <-> Vai trái
    (0, 7),  # Mũi <-> Vai phải
    (6, 8),  # Vai trái <-> Khủy tay trái
    (8, 10), # Khủy tay trái <-> Cổ tay trái
    (7, 9),  # Vai phải <-> Khủy tay phải
    (9, 11), # Khủy tay phải <-> Cổ tay phải
    (6, 12), # Vai trái <-> Ngực
    (7, 12), # Vai phải <-> Ngực
    (12, 13),# Ngực <-> Hông trái
    (12, 14),# Ngực <-> Hông phải
    (13, 15),# Hông trái <-> Đầu gối trái
    (15, 17),# Đầu gối trái <-> Mắt cá chân trái
    (14, 16),# Hông phải <-> Đầu gối phải
    (16, 18),# Đầu gối phải <-> Mắt cá chân phải
    (17, 19),# Mắt cá chân trái <-> Gót chân trái
    (18, 20) # Mắt cá chân phải <-> Gót chân phải
]

# Kết nối khớp bàn tay (Hand Tracking)
hand_connections = [
    (0, 1),  # Cổ tay <-> Khớp ngón cái 1
    (1, 2),  # Khớp ngón cái 1 <-> Khớp ngón cái 2
    (2, 3),  # Khớp ngón cái 2 <-> Đầu ngón cái
    (0, 4),  # Cổ tay <-> Khớp ngón trỏ 1
    (4, 5),  # Khớp ngón trỏ 1 <-> Khớp ngón trỏ 2
    (5, 6),  # Khớp ngón trỏ 2 <-> Đầu ngón trỏ
    (0, 7),  # Cổ tay <-> Khớp ngón giữa 1
    (7, 8),  # Khớp ngón giữa 1 <-> Khớp ngón giữa 2
    (8, 9),  # Khớp ngón giữa 2 <-> Đầu ngón giữa
    (0, 10), # Cổ tay <-> Khớp ngón áp út 1
    (10, 11),# Khớp ngón áp út 1 <-> Khớp ngón áp út 2
    (11, 12),# Khớp ngón áp út 2 <-> Đầu ngón áp út
    (0, 13), # Cổ tay <-> Khớp ngón út 1
    (13, 14),# Khớp ngón út 1 <-> Khớp ngón út 2
    (14, 15),# Khớp ngón út 2 <-> Đầu ngón út
]

# Gộp cả hai danh sách lại thành một danh sách
all_connections = {
    "body_connections": body_connections,
    "hand_connections": hand_connections
}

print(all_connections)

from STGCN import Model
model = Model(in_channels=3, num_nodes=65, inward_edges=body_connections, n_classes=20)
results = model(tensor_reshaped)


print(results.shape)