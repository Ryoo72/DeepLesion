import numpy as np
import sys
import pandas as pd
import cv2
import os
from tqdm import tqdm

download_path = './unzipfiles/Images_png'
save_path = './prepr_datasets'
csv_path = './DL_info.csv'

if not os.path.isdir(save_path):
    os.makedirs(save_path, 0o777)

def preprocess_me(image, window_min, window_max):
    windowed_image = np.clip((image - window_min) / (window_max - window_min) * 255, 0, 255).astype(np.uint8)
    
    return windowed_image

dl_info_csv = pd.read_csv(csv_path)
img_names = dl_info_csv.File_name.values
DICOM_windows = dl_info_csv.DICOM_windows.values
 
img_names_set = set()
for img_name, window in zip(tqdm(img_names), DICOM_windows):
    if img_name not in img_names_set:
        window_list = [float(value.strip()) for value in window.split(',')]
        img_names_set.add(img_name)

        image_number = img_name.split('_')[-1]
        folder_name = '_'.join(img_name.split('_')[0:-1])
        final_path = os.path.join(download_path, folder_name, image_number)
        
        if os.path.exists(final_path):
            image = cv2.imread(final_path, -1).astype(np.int32) - 32768
            windowed_image = preprocess_me(image, window_list[0], window_list[1])    
            out_name = os.path.join(save_path, img_name)
        else:
            print(f"can not find {final_path}")
            continue
    
        cv2.imwrite(out_name, windowed_image)