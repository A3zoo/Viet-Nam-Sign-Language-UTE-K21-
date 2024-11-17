from .video_to_sequences import convert_list_video_to_mediapipe, read_video
import os
import shutil
import json
# Đường dẫn đến thư mục bạn muốn duyệt
parent_dir = 'D:\\SPKT\\HK1_n4\TLCN\\Sign_Language_Recognition\\Video_dataset'
out_put = 'D:\\SPKT\\HK1_n4\TLCN\\Sign_Language_Recognition\\data_set\\mediapipe_sequences'
# Duyệt qua tất cả các thư mục trong thư mục cha
for folder_name in os.listdir(parent_dir):
    input_folder = os.path.join(parent_dir, folder_name)
    out_put_path = os.path.join(out_put, folder_name)
    os.makedirs(out_put_path, exist_ok=True)
    # shutil.copy(os.path.join(input_folder, 'lable.txt'),out_put_path)
    convert_list_video_to_mediapipe(
        input_folder,
        folder_name,
        out_put_path
    )

