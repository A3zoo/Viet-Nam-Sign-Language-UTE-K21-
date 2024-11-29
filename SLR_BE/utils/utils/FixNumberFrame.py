import random

def fixed_num_frame(lst_frame, num_frame=32):
    """
    Lấy ngẫu nhiên các frame từ video sao cho các frame được phân bố đều trong video,
    nhưng không làm thay đổi thứ tự của các frame trong video.
    """
    total_frame = len(lst_frame)

    if total_frame >= num_frame:
        # Tính tỷ lệ phân chia giữa các frame
        step = total_frame / num_frame  # Khoảng cách giữa các frame cần lấy

        # Chọn ngẫu nhiên frame trong các đoạn cách đều
        selected_frames = []
        for i in range(num_frame):
            # Tính chỉ số của frame cần lấy trong đoạn i
            random_index = int(i * step + random.uniform(0, step))  # Lấy chỉ số ngẫu nhiên trong đoạn
            selected_frames.append(lst_frame[min(random_index, total_frame - 1)])  # Đảm bảo không vượt quá total_frame

    else:
        # Nếu số lượng frame ít hơn num_frame, lặp lại các frame sao cho đủ
        repeat_count = (num_frame + total_frame - 1) // total_frame  # Tính số lần lặp
        extended_lst = lst_frame * repeat_count  # Lặp lại các frame
        selected_frames = extended_lst[:num_frame]  # Lấy đủ số frame cần thiết

    return selected_frames
