# DeepLesion

> **This repository converts the DeepLesion dataset for use with mmdetection.**

 [DeepLesion](https://nihcc.app.box.com/v/DeepLesion) is a large-scale dataset for medical object detection. This dataset contains over 32,000 annotated CT images and is split into train, validation, and test sets. It coarsely defines eight types of lesions, including bone, abdomen, mediastinum, liver, lung, kidney, soft tissue, and pelvis. We have treated all lesions under the same 'lesion' category.


### 1️⃣ Preparing the Images

~~~bash
git clone https://github.com/anir16293/Deep-Lesion/tree/master
~~~

Modify the `download_directory` in `batch_download_zips.py`

~~~bash
# it takes a while, so using tmux is recommended
python batch_download_zips.py 
~~~

In `unzip_me.py`, set `base_dir` to the directory of the downloaded zip files and set a new `output_dir`

~~~bash
# it takes a while, so using tmux is recommended
python unzip_me.py
~~~

If cv2 is not installed, run `pip install opencv-python` to install it

Modify the path in `preprocess_me.py`. Set `csv_path` to the location of `DL_info.csv`

~~~bash
python preprocess_me.py
~~~

### 2️⃣ Preparing the Annotations

In `coconize_me.py`, insert the location of `DL_info.csv` into `csv_file_path`

~~~bash
python coconize_me.py
~~~

### 3️⃣ Inject noise using UNA

~~~bash
git clone https://github.com/Ryoo72/UNA.git
cd UNA
python una_inj.py --ratio 0.1 --class_type deeplesion --path {path_to_json} --target {target_path}
# EXAMPLE
# python una_inj.py --ratio 0.1 --class_type deeplesion --path ./DL_info.csv --target ./annotations
~~~

### 4️⃣ Setting Up MMDetection

~~~bash
git clone https://github.com/open-mmlab/mmdetection.git
~~~

Duplicate `configs/_base_/datasets/coco_detection.py` → `configs/_base_/datasets/coco_detection_dl.py` and change:
- data_root
- ann_file
- data_prefix

Duplicate `configs/_base_/models/fast-rcnn_r50_fpn.py` → `configs/_base_/models/fast-rcnn_r50_fpn_dl.py` and change `num_classes` to 1

Duplicate `configs/faster_rcnn/faster-rcnn_r50_fpn_1x_coco.py` and change to `'../_base_/models/faster-rcnn_r50_fpn_dl.py'`,`'../_base_/datasets/coco_detection_dl.py'`

Duplicate `mmdet/datasets/coco.py` → `mmdet/datasets/deeplesion.py`, rename the class to `DeepLesionDataset`.
Configure the class to only include 'lesion', and leave only one arbitrary palette, removing the rest.

If this step is not done correctly, a `ValueError: need at least one array to concatenate` will occur

Follow the instructions at [https://mmdetection.readthedocs.io/en/latest/get_started.html](https://mmdetection.readthedocs.io/en/latest/get_started.html)

> If you have reached this point without changing the default path, it is convenient to directly move the current `DeepLesion` directory to `mmdetection/data/` for use.

### 5️⃣ Run experiments

```bash
bash ./tools/dist_train.sh \
    {config_file_path} \
    16
```

> [!NOTE]  
> ✉️ kwangrok21@naver.com
