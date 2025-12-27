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






