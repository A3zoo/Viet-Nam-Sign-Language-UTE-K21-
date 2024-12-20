import cv2
import mediapipe as mp
import numpy as np
import json
import os
import torch
import numpy as np


TOTAL_POSE_LANDMARKS = 25 
TOTAL_HAND_LANDMARKS = 42 
TOTAL_HANDS = 2
NUM_FRAME_PROCESS = 25
NOSE_POSITION = 0

LIST_BODY_LANDMARKS =  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

LIST_HAND_LANDMARKS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

def make_landmark_timestep(pose_landmarks, right_hand_landmarks=None, left_hand_landmarks=None):
    c_lm = []
    
    for i in LIST_BODY_LANDMARKS:
        c_lm.append([pose_landmarks.landmark[i].x, pose_landmarks.landmark[i].y, pose_landmarks.landmark[i].visibility])
    
    if right_hand_landmarks:
        for i in right_hand_landmarks.landmark:
            c_lm.append([i.x, i.y, i.visibility])
    else:
        c_lm.extend([[0,0,0]] * 21)
    
    if left_hand_landmarks:
        for i in left_hand_landmarks.landmark:
            c_lm.append([i.x, i.y, i.visibility])
    else:
        c_lm.extend([[0,0,0]] * 21)
    return c_lm

# Dua toa do ve cung 1 goc toa do (goc la diem 0: mui)
def transform_to_nose_coordinate(c_lm, nose_index=0):
    x, y = c_lm[nose_index * 2], c_lm[nose_index * 2 + 1]
    
    for i in range(0, len(c_lm), 2):
        if c_lm[i] != 0 or c_lm[i + 1] != 0:
            c_lm[i], c_lm[i + 1] = c_lm[i] - x, c_lm[i + 1] - y
    
    return c_lm

def draw_to_img(holistic_results, mp_drawing, image):
    small_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
    mp_drawing.draw_landmarks(
        image,
        holistic_results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
       landmark_drawing_spec=small_drawing_spec
    )
    mp_drawing.draw_landmarks(
        image,
        holistic_results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        landmark_drawing_spec=small_drawing_spec,
        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style()  
    )       

    mp_drawing.draw_landmarks(
        image,
        holistic_results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        landmark_drawing_spec=small_drawing_spec,
        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style()
    )

    return image

#  doc video va trich xuat du lieu
def read_video(video_path, label):
    cap = cv2.VideoCapture(video_path)
    lm_list = []

    with mp_holistic.Holistic(model_complexity=2) as holistic:
        while True:
            ret, frame = cap.read()
            if ret:
                # Tính toán đường chéo của khung hình gốc
                height, width = frame.shape[:2]
                diagonal = np.sqrt(height**2 + width**2)
                
                # Tính tỉ lệ co để đường chéo của khung hình mới là 256 pixel
                scale = 512 / diagonal
                
                # Thay đổi kích thước khung hình
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height))

                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = holistic.process(frameRGB)

                if results.pose_landmarks and (results.left_hand_landmarks or results.right_hand_landmarks):
                    lm = make_landmark_timestep(results.pose_landmarks, results.right_hand_landmarks, results.left_hand_landmarks)
                    #kiem tra co nhan dien du 25 frame k 
                    if len(lm) >= NUM_FRAME_PROCESS+1: #(25 frame + 1 label)
                        lm_list.append(lm)
                    else: 
                        print('Insufficient number of frames')
                if cv2.waitKey(1) == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        lm_list = fixed_num_frame(lm_list, NUM_FRAME_PROCESS)

        return lm_list

# co dinh so luong frame
def fixed_num_frame(lst_frame, num_frame):
    total_frame = len(lst_frame)
    
    num_step = max(total_frame // (num_frame - 1), 1)

    new_lst = []

    for i in range(num_frame):
        idx = min(i * num_step, total_frame - 1)
        new_lst.append(lst_frame[idx])

    return new_lst

def convert_list_video_to_mediapipe(input_folder_path, words, output_folder_path):
    
    for file_name in os.listdir(input_folder_path):
        # Tạo đường dẫn đầy đủ của file
        input_file = os.path.join(input_folder_path, file_name)
        # Kiểm tra nếu đó là file
        if not input_file.endswith('.txt'):
            print(f"Đang xử lý file: {file_name}")
            # Thực hiện hành động với file
            try:
                data = read_video(input_file, words)
                print(10*'10')
                tensor = torch.tensor(data, dtype=torch.float32)
                print(10*'9')
                output_file_path = os.path.join(output_folder_path, file_name + '.pt')
                print(10*'8')
                torch.save(tensor, output_file_path)
                
            except Exception as e:
                print(f"\nError encoding {input_file}\n{e}")
            





