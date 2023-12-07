import pandas as pd
import json

# JSON 파일로 저장
json_file_train = './annotations/deeplesion_train.json'
json_file_val = './annotations/deeplesion_val.json'
json_file_test = './annotations/deeplesion_test.json'

# CSV 파일 경로
csv_file_path = './DL_info.csv'

# CSV 데이터를 DataFrame으로 읽기
df = pd.read_csv(csv_file_path)

# 각 데이터셋에 대한 COCO 데이터 초기화
coco_data_train = {
    "images": [],
    "annotations": [],
    "categories": [{"id": 1, "name": "lesion"}]
}

coco_data_val = {
    "images": [],
    "annotations": [],
    "categories": [{"id": 1, "name": "lesion"}]
}

coco_data_test = {
    "images": [],
    "annotations": [],
    "categories": [{"id": 1, "name": "lesion"}]
}

# 이미지 ID 할당을 위한 사전(dictionary)
image_ids_train = {}
image_ids_val = {}
image_ids_test = {}
current_id_train = 1
current_id_val = 1
current_id_test = 1

# 어노테이션 ID
annotation_id_train = 1
annotation_id_val = 1
annotation_id_test = 1

# 데이터를 COCO 포맷으로 변환 및 분할
for idx, row in df.iterrows():
    file_name = row['File_name']
    width, height = map(int, row['Image_size'].split(', '))
    bbox = list(map(float, row['Bounding_boxes'].split(', ')))
    bbox_coco = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
    train_val_test = row['Train_Val_Test']

    # Train 데이터셋
    if train_val_test == 1:
        if file_name not in image_ids_train:
            image_ids_train[file_name] = current_id_train
            current_id_train += 1
            coco_data_train["images"].append({
                "id": image_ids_train[file_name],
                "file_name": file_name,
                "width": width,
                "height": height
            })

        coco_data_train["annotations"].append({
            "id": annotation_id_train,
            "image_id": image_ids_train[file_name],
            "category_id": 1,
            "bbox": bbox_coco,
            "area": bbox_coco[2] * bbox_coco[3],
            "iscrowd": 0
        })
        annotation_id_train += 1

    # Validation 데이터셋
    elif train_val_test == 2:
        if file_name not in image_ids_val:
            image_ids_val[file_name] = current_id_val
            current_id_val += 1
            coco_data_val["images"].append({
                "id": image_ids_val[file_name],
                "file_name": file_name,
                "width": width,
                "height": height
            })

        coco_data_val["annotations"].append({
            "id": annotation_id_val,
            "image_id": image_ids_val[file_name],
            "category_id": 1,
            "bbox": bbox_coco,
            "area": bbox_coco[2] * bbox_coco[3],
            "iscrowd": 0
        })
        annotation_id_val += 1

    # Test 데이터셋
    elif train_val_test == 3:
        if file_name not in image_ids_test:
            image_ids_test[file_name] = current_id_test
            current_id_test += 1
            coco_data_test["images"].append({
                "id": image_ids_test[file_name],
                "file_name": file_name,
                "width": width,
                "height": height
            })

        coco_data_test["annotations"].append({
            "id": annotation_id_test,
            "image_id": image_ids_test[file_name],
            "category_id": 1,
            "bbox": bbox_coco,
            "area": bbox_coco[2] * bbox_coco[3],
            "iscrowd": 0
        })
        annotation_id_test += 1

with open(json_file_train, 'w') as f:
    json.dump(coco_data_train, f, indent=4)
with open(json_file_val, 'w') as f:
    json.dump(coco_data_val, f, indent=4)
with open(json_file_test, 'w') as f:
    json.dump(coco_data_test, f, indent=4)
