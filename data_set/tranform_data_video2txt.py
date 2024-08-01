import cv2
import mediapipe as mp
import numpy as np
import json
from tqdm import tqdm

OUTPUT_FILE = "dataset.txt"
TOTAL_POSE_LANDMARKS = 23  # so diem lay tren pose 
TOTAL_HAND_LANDMARKS = 21  # so diem lay tren tay
TOTAL_HANDS = 2   
NUM_FRAME_PROCESS = 25 # So frame muon xu ly
NOSE_POSITION = 0

def make_landmark_timestep(pose_landmarks, right_hand_landmarks=None, left_hand_landmarks=None):
    c_lm = [0] * (TOTAL_POSE_LANDMARKS * 2 + TOTAL_HAND_LANDMARKS * 2 * TOTAL_HANDS)
    
    for i in range(TOTAL_POSE_LANDMARKS):
        c_lm[i * 2] = pose_landmarks.landmark[i].x
        c_lm[i * 2 + 1] = pose_landmarks.landmark[i].y
    
    if right_hand_landmarks:
        for i in range(TOTAL_HAND_LANDMARKS):
            c_lm[(TOTAL_POSE_LANDMARKS + i) * 2] = right_hand_landmarks.landmark[i].x
            c_lm[(TOTAL_POSE_LANDMARKS + i) * 2 + 1] = right_hand_landmarks.landmark[i].y
    
    if left_hand_landmarks:
        for i in range(TOTAL_HAND_LANDMARKS):
            c_lm[(TOTAL_POSE_LANDMARKS + TOTAL_HAND_LANDMARKS + i) * 2] = left_hand_landmarks.landmark[i].x
            c_lm[(TOTAL_POSE_LANDMARKS + TOTAL_HAND_LANDMARKS + i) * 2 + 1] = left_hand_landmarks.landmark[i].y

    c_lm = transform_to_nose_coordinate(c_lm, NOSE_POSITION)    
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
def read_vieo(video_path, label):
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
                    frame = draw_to_img(results, mp_drawing, frame)

                cv2.imshow('Pose Landmarks', frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        lm_list = fixed_num_frame(lm_list, NUM_FRAME_PROCESS)
        print('count frame:::', len(lm_list))
        lm_list.append(label)

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

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# lay data tu file json (vi lay data ASL)
"""
VD: 
    {
        "gloss": "book",
        "video_path": "C:/Users/ledin/Downloads/archive/wlasl-complete/videos/69241.mp4",
        "frame_start": 1,
        "frame_end": -1,
        "split": "train"
    }
"""
with open('WLASL_parsed_data.json', 'r') as json_file:
    all_data = json.load(json_file)
#file label chua nhan  VD: "book": "0"
with open('label.json', 'r') as json_file:
    dir_label = json.load(json_file)

# lay 1000 row  de train
train_data = all_data[:1000]
lst_data = []
try:
    for i in tqdm(range(len(train_data)), ncols=100):
        start = train_data[i]['frame_start']
        end = train_data[i]['frame_end']
        if (start == 1 and end == -1):
            video_path = train_data[i]['video_path']       
        
            try:
                data = read_vieo(video_path, dir_label[train_data[i]['gloss']])
                lst_data.append(data)
                
            except Exception as e:
                print(f"\nError encoding {video_path}\n{e}")
                continue   
except KeyboardInterrupt:
    print("\nLoading process interrupted by user.")                

# ghi du lieu ra file txt
with open(OUTPUT_FILE, 'a') as f:
    for data in lst_data:
            # moi dong 1 video (25 frame)
            f.write(','.join(map(str, data)) + '\n')

