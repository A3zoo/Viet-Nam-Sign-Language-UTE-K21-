import cv2
import mediapipe as mp

import csv
import os
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)


OUTPUT_DIR_SKELETON_XY = "skeleton_dataset/Skeletons/skeleton_data_xy_fix50frame"
OUTPUT_DIR_SKELETON_XYZ = "skeleton_dataset/Skeletons/skeleton_data_xyz_fix50frame"
OUTPUT_DIR_SKELETON = "skeleton_dataset/Skeletons/skeleton_data_xys_fix50frame"
OUTPUT_DIR_SKELETON_NO_SCALE = "skeleton_dataset/Skeletons_without_scale"

os.makedirs(OUTPUT_DIR_SKELETON_XY, exist_ok=True)
os.makedirs(OUTPUT_DIR_SKELETON_XYZ, exist_ok=True)
os.makedirs(OUTPUT_DIR_SKELETON, exist_ok=True)
os.makedirs(OUTPUT_DIR_SKELETON_NO_SCALE, exist_ok=True)

VIDEO_DATASET_PATH = './video_dataset/done'
NUM_FRAME_PROCESS = 50  # Số khung hình cố định xử lý cho mỗi video

TOTAL_POSE_LANDMARKS = 25   # Số khớp trong MediaPipe Pose
TOTAL_HAND_LANDMARKS = 21   # Số khớp trong mỗi bàn tay
TOTAL_HANDS = 2             # Tổng số bàn tay (trái và phải)
NOSE_POSITION = 0  

# Khởi tạo MediaPipe Holistic
mpHolistic = mp.solutions.holistic
holistic = mpHolistic.Holistic(
    static_image_mode=False,   #  xử lý video
    model_complexity=2,        # Tăng độ phức tạp để có độ chính xác cao hơn
    smooth_landmarks=True,
    enable_segmentation=True,  #phân đoạn nền
    )
mpDraw = mp.solutions.drawing_utils


# Hàm chuẩn hóa khung hình theo vị trí mũi (khớp 0)
def transform_to_nose_coordinate(c_lm, nose_index=0):
    x, y, z = c_lm[nose_index * 3], c_lm[nose_index * 3 + 1], c_lm[nose_index * 3 + 2]
    for i in range(0, len(c_lm), 3):
        c_lm[i], c_lm[i + 1], c_lm[i + 2] = c_lm[i] - x, c_lm[i + 1] - y, c_lm[i + 2]
    return c_lm

# Hàm chuẩn hóa khung hình theo vị trí mũi (khớp 0)
def transform_to_nose_coordinate_xyz(c_lm, nose_index=0):
    x, y, z = c_lm[nose_index * 3], c_lm[nose_index * 3 + 1], c_lm[nose_index * 3 + 2]
    for i in range(0, len(c_lm), 3):
        c_lm[i], c_lm[i + 1], c_lm[i + 2] = c_lm[i] - x, c_lm[i + 1] - y, c_lm[i + 2]-z
    return c_lm

# Hàm chuẩn hóa khung hình theo vị trí mũi (khớp 0)
def transform_to_nose_coordinate_xy(c_lm, nose_index=0):
    x, y = c_lm[nose_index * 2], c_lm[nose_index * 2 + 1]
    for i in range(0, len(c_lm), 2):
        c_lm[i], c_lm[i + 1]= c_lm[i] - x, c_lm[i + 1] - y
    return c_lm

# Hàm tạo dữ liệu khung xương từ holistic (Pose và Hand landmarks, không bao gồm Face)
def make_landmark_timestep(holistic_results, frame_width, frame_height, visibility_threshold=0.5):
    # Tạo mảng cho khớp của Pose và Hand (x, y, visibility)
    c_lm = [0] * (TOTAL_POSE_LANDMARKS * 3 + TOTAL_HAND_LANDMARKS * 3 * TOTAL_HANDS)
    c_lm_xyz = [0] * (TOTAL_POSE_LANDMARKS * 3 + TOTAL_HAND_LANDMARKS * 3 * TOTAL_HANDS)
    c_lm_xy = [0] * (TOTAL_POSE_LANDMARKS * 2 + TOTAL_HAND_LANDMARKS * 2 * TOTAL_HANDS)

    raw_lm = [0] * (TOTAL_POSE_LANDMARKS * 3 + TOTAL_HAND_LANDMARKS * 3 * TOTAL_HANDS)

    # Xử lý Pose landmarks
    if holistic_results.pose_landmarks:
        for idx, lm in enumerate(holistic_results.pose_landmarks.landmark):
            raw_lm[idx * 3:(idx + 1) * 3] = [lm.x * frame_width, lm.y * frame_height, lm.visibility]  # Lưu x, y, visibility
            c_lm[idx * 3:(idx + 1) * 3] = [lm.x, lm.y, lm.visibility]  # Lưu x, y, visibility
            c_lm_xyz[idx * 3:(idx + 1) * 3] = [lm.x, lm.y, lm.z]  # Lưu x, y, z
            c_lm_xy[idx * 2:(idx + 1) * 2] = [lm.x, lm.y]  # Lưu x, y

    # Xử lý Hand landmarks
    for hand_idx, hand_landmarks in enumerate([holistic_results.left_hand_landmarks, holistic_results.right_hand_landmarks]):
        if hand_landmarks:
            for idx, lm in enumerate(hand_landmarks.landmark):
                base_idx = TOTAL_POSE_LANDMARKS * 3 + (hand_idx * TOTAL_HAND_LANDMARKS * 3) + (idx * 3)
                raw_lm[base_idx:base_idx + 3] = [lm.x * frame_width, lm.y * frame_height, lm.visibility]  # Lưu x, y, visibility
                c_lm[base_idx:base_idx + 3] = [lm.x, lm.y, lm.visibility]  # Lưu x, y, visibility
                c_lm_xyz[base_idx:base_idx + 3] = [lm.x, lm.y, lm.z]  # Lưu x, y, z
                c_lm_xy[base_idx:base_idx + 2] = [lm.x, lm.y]  # Lưu x, y
    
    # Chuẩn hóa tọa độ c_lm theo vị trí mũi (khớp 0)
    raw_lm = transform_to_nose_coordinate(raw_lm, NOSE_POSITION)
    c_lm = transform_to_nose_coordinate(c_lm, NOSE_POSITION)
    c_lm_xyz = transform_to_nose_coordinate_xyz(c_lm_xyz, NOSE_POSITION)
    c_lm_xy = transform_to_nose_coordinate_xy(c_lm_xy, NOSE_POSITION)

    return raw_lm, c_lm, c_lm_xyz, c_lm_xy
# Hàm cố định số khung hình cho mỗi video
def fixed_num_frame(lst_frame, num_frame):
    total_frame = len(lst_frame)
    num_step = max(total_frame // (num_frame - 1), 1)
    new_lst = [lst_frame[min(i * num_step, total_frame - 1)] for i in range(num_frame)]
    return new_lst

# Hàm lưu dữ liệu khung xương vào file CSV
def save_skeleton_to_csv(lm_list, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Tiêu đề các cột: frame, 33 điểm từ Pose và 42 điểm từ tay
        headers = ['frame']
        for i in range(TOTAL_POSE_LANDMARKS):
            headers += [f'joint_{i}_x', f'joint_{i}_y', f'joint_{i}_visibility']
        for hand in range(TOTAL_HANDS):
            for i in range(TOTAL_HAND_LANDMARKS):
                headers += [f'hand_{hand}_joint_{i}_x', f'hand_{hand}_joint_{i}_y', f'hand_{hand}_joint_{i}_visibility']
        writer.writerow(headers)
        
        # Ghi dữ liệu khung xương cho mỗi khung hình
        for frame_idx, lm in enumerate(lm_list):
            writer.writerow([frame_idx] + lm)

def save_skeleton_xyz_to_csv(lm_list, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Tiêu đề các cột: frame, 33 điểm từ Pose và 42 điểm từ tay
        headers = ['frame']
        for i in range(TOTAL_POSE_LANDMARKS):
            headers += [f'joint_{i}_x', f'joint_{i}_y', f'joint_{i}_z']
        for hand in range(TOTAL_HANDS):
            for i in range(TOTAL_HAND_LANDMARKS):
                headers += [f'hand_{hand}_joint_{i}_x', f'hand_{hand}_joint_{i}_y', f'hand_{hand}_joint_{i}_z']
        writer.writerow(headers)
        
        # Ghi dữ liệu khung xương cho mỗi khung hình
        for frame_idx, lm in enumerate(lm_list):
            writer.writerow([frame_idx] + lm)
def save_skeleton_xy_to_csv(lm_list, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Tiêu đề các cột: frame, 33 điểm từ Pose và 42 điểm từ tay
        headers = ['frame']
        for i in range(TOTAL_POSE_LANDMARKS):
            headers += [f'joint_{i}_x', f'joint_{i}_y']
        for hand in range(TOTAL_HANDS):
            for i in range(TOTAL_HAND_LANDMARKS):
                headers += [f'hand_{hand}_joint_{i}_x', f'hand_{hand}_joint_{i}_y']
        writer.writerow(headers)
        
        # Ghi dữ liệu khung xương cho mỗi khung hình
        for frame_idx, lm in enumerate(lm_list):
            writer.writerow([frame_idx] + lm)


# Hàm lưu dữ liệu tọa độ gốc chưa chuẩn hóa vào file CSV
def save_skeleton_without_scale_to_csv(raw_lm_list, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = ['frame']
        for i in range(TOTAL_POSE_LANDMARKS):
            headers += [f'joint_{i}_x', f'joint_{i}_y', f'joint_{i}_visibility']
        for hand in range(TOTAL_HANDS):
            for i in range(TOTAL_HAND_LANDMARKS):
                headers += [f'hand_{hand}_joint_{i}_x', f'hand_{hand}_joint_{i}_y', f'hand_{hand}_joint_{i}_visibility']
        writer.writerow(headers)
        
        for frame_idx, raw_lm in enumerate(raw_lm_list):
            writer.writerow([frame_idx] + raw_lm)

def read_video(video_path, label, start, end):
    cap = cv2.VideoCapture(video_path)
    lm_list = []
    lm_xyz_list = []
    lm_xy_list = []
    raw_lm_list = []

    # Kích thước cố định cho khung hình
    fixed_size = (256, 256)
    num_frame = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Kích thước khung hình gốc
        height, width = frame.shape[:2]

        # Tính toán tỷ lệ thu nhỏ để đảm bảo giữ tỷ lệ gốc
        scale = min(fixed_size[0] / width, fixed_size[1] / height)
        new_width = int(width * scale)
        new_height = int(height * scale)

        # Thay đổi kích thước khung hình nhưng giữ nguyên tỷ lệ
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # Tạo viền (padding) để khung hình có kích thước cố định
        top = (fixed_size[1] - new_height) // 2
        bottom = fixed_size[1] - new_height - top
        left = (fixed_size[0] - new_width) // 2
        right = fixed_size[0] - new_width - left

        # Thêm viền (padding) vào khung hình
        padded_frame = cv2.copyMakeBorder(resized_frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # Chuyển đổi khung hình thành RGB để xử lý bằng MediaPipe
        frameRGB = cv2.cvtColor(padded_frame, cv2.COLOR_BGR2RGB)
        holistic_results = holistic.process(frameRGB)

        # Nếu phát hiện Pose hoặc Hand landmarks
        if holistic_results.pose_landmarks or holistic_results.left_hand_landmarks or holistic_results.right_hand_landmarks:
            # Gọi hàm make_landmark_timestep với thông tin kích thước khung hình
            raw_lm, lm, lm_xyz, lm_xy = make_landmark_timestep(holistic_results, fixed_size[0], fixed_size[1])
            lm_list.append(lm)
            raw_lm_list.append(raw_lm)
            lm_xy_list.append(lm_xy)
            lm_xyz_list.append(lm_xyz)

            # Vẽ Pose và Hand landmarks
            mpDraw.draw_landmarks(padded_frame, holistic_results.pose_landmarks, mpHolistic.POSE_CONNECTIONS)
            if holistic_results.left_hand_landmarks:
                mpDraw.draw_landmarks(padded_frame, holistic_results.left_hand_landmarks, mpHolistic.HAND_CONNECTIONS)
            if holistic_results.right_hand_landmarks:
                mpDraw.draw_landmarks(padded_frame, holistic_results.right_hand_landmarks, mpHolistic.HAND_CONNECTIONS)

        # Hiển thị khung hình (nếu cần)
        cv2.imshow("Skeleton Extraction", padded_frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    raw_lm_list = fixed_num_frame(raw_lm_list, NUM_FRAME_PROCESS)
    lm_list = fixed_num_frame(lm_list, NUM_FRAME_PROCESS)
    lm_xyz_list = fixed_num_frame(lm_xyz_list, NUM_FRAME_PROCESS)
    lm_xy_list = fixed_num_frame(lm_xy_list, NUM_FRAME_PROCESS)

    return raw_lm_list, lm_list, lm_xyz_list, lm_xy_list

# Hàm chính để xử lý và lưu dữ liệu
def process_and_save_data(video_path, label, start=1, end=-1):
    raw_lm_list, lm_list, lm_xyz_list, lm_xy_list = read_video(video_path, label, start, end)

    label_folder = os.path.join(OUTPUT_DIR_SKELETON, label)
    label_folder_xyz = os.path.join(OUTPUT_DIR_SKELETON_XYZ, label)
    label_folder_xy = os.path.join(OUTPUT_DIR_SKELETON_XY, label)
    label_folder_raw = os.path.join(OUTPUT_DIR_SKELETON_NO_SCALE, label)
    os.makedirs(label_folder, exist_ok=True)
    os.makedirs(label_folder_xyz, exist_ok=True)
    os.makedirs(label_folder_xy, exist_ok=True)
    os.makedirs(label_folder_raw, exist_ok=True)

    video_name = os.path.basename(video_path).split('.')[0]

     # Đường dẫn lưu file CSV cho skeleton
    skeleton_file_path = os.path.join(label_folder, f"{video_name}_skeleton_xys.csv")
    skeleton_without_scale_file_path = os.path.join(label_folder_raw, f"{video_name}_skeleton_without_scale.csv")
    skeleton_xyz_file_path = os.path.join(label_folder_xyz, f"{video_name}_skeleton_xyz.csv")
    skeleton_xy_file_path = os.path.join(label_folder_xy, f"{video_name}_skeleton_xy.csv")


    save_skeleton_to_csv(lm_list, skeleton_file_path)
    save_skeleton_without_scale_to_csv(raw_lm_list, skeleton_without_scale_file_path)
    save_skeleton_xy_to_csv(lm_xy_list, skeleton_xy_file_path)
    save_skeleton_xyz_to_csv(lm_xyz_list, skeleton_xyz_file_path)

video_dataset_path = VIDEO_DATASET_PATH
lst_data = []            

d=0

processed_videos_file = 'processed_videos.txt'

# Tải danh sách video đã xử lý từ file nếu có
if os.path.exists(processed_videos_file):
    with open(processed_videos_file, 'r') as f:
        processed_videos = set(line.strip() for line in f)
else:
    processed_videos = set()

for idx_label, subdir in enumerate(os.listdir(video_dataset_path)):
    subdir_path = os.path.join(video_dataset_path, subdir)
    if os.path.isdir(subdir_path):
        for file in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file)
            if os.path.isfile(file_path) and file_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                d+=1
                # Nếu video đã xử lý, bỏ qua
                if file in processed_videos:
                    continue

                # Kiểm tra độ dài video
                cap = cv2.VideoCapture(file_path)
                fps = cap.get(cv2.CAP_PROP_FPS)               # Lấy số khung hình trên giây
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Lấy tổng số khung hình
                duration = frame_count / fps                  # Tính thời gian video (giây)
                cap.release()  # Đóng video sau khi kiểm tra

                if duration >= 1:
                    process_and_save_data(file_path, label=subdir)
                    
                    # Thêm video vào danh sách đã xử lý và ghi vào file
                    processed_videos.add(file)
                    print(file, d)
                    with open(processed_videos_file, 'a') as f:
                        f.write(f"{file}\n")


