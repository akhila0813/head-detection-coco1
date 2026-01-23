# Head Detection Dataset (SCUT-HEAD → COCO)
## Overview
This project converts the **SCUT-HEAD Part B** dataset from its original XML annotation format into the **COCO** object detection format.

The pipeline includes:
- Dataset organization
- XML → COCO conversion
- Train / validation split
- PyTorch-compatible dataset loader
- Visualization for sanity checking
## Dataset Source
**SCUT-HEAD Dataset**
The SCUT-HEAD dataset is a public head-detection dataset containing crowd images.
- Each image is annotated using Pascal VOC XML format.
- Annotations contain bounding boxes for human heads.
- [Scut-Head Dataset on Kaggle](https://www.kaggle.com/datasets/hoangxuanviet/scut-head)
> ⚠️ **Note**:Due to dataset size and licensing constraints, raw images are not included in this repository.
After downloading SCUT-HEAD Part-B, place it under data/raw/SCUT_HEAD_Part_B/ so that all scripts can locate the dataset automatically.
## Project Structure
```
head-detection-coco/
├── scripts/
│   ├── scut_to_coco.py        # XML → COCO conversion
│   ├── split_coco.py          # Train / validation split
│   └── visualize_sample.py    # Visualization & sanity check
│
├── datasets/
│   └── coco_dataset.py        # Reusable PyTorch Dataset class
│
├── data/
│   ├── raw/
│   │   └── SCUT_HEAD_Part_B/
│   │       ├── JPEGImages/
│   │       └── Annotations/
│   │
│   └── coco/
│       ├── scut_head_partB_coco.json
│       ├── annotations/
│       └── images/
│           ├── train2017/
│           └── val2017/
├── requirements.txt
├── .gitignore
└── README.md
```
## Environment Setup
Install Dependencies:
```bash
pip install -r requirements.txt
```
Dependencies include: `numpy`, `torch`, `torchvision`, `pycocotools`, `pillow`, `opencv-python`, `matplotlib`.
## Run
Follow these steps to reproduce the dataset preparation:
### 1. Dataset Placement
After downloading and extracting `SCUT_HEAD_Part_B`, place it as follows:
```
data/raw/SCUT_HEAD_Part_B/
├── JPEGImages/      # Contains .jpg files
└── Annotations/     # Contains .xml files
```
**Why?** This separation ensures raw data remains untouched (immutable infrastructure) and scripts remain reproducible across different machines.
### 2. Convert SCUT XML → COCO JSON
Run the conversion script:
```bash
python scripts/scut_to_coco.py
```
**Expected Output:**
```text
📸 Found 2405 images
✅ SCUT → COCO conversion completed
Images processed     : 2405
Annotations created  : ~44000
Images skipped       : 0
COCO file saved to   : data/coco/scut_head_partB_coco.json
```
**Critical Check:** Ensure `Images skipped` is 0. If not, check if XML files are missing for some images.
### 3. Train / Validation Split
Split the dataset into training (80%) and validation (20%) sets. This is crucial to prevent "data leakage" during model evaluation.
```bash
python scripts/split_coco.py
```
**Expected Output:**
```text
✅ Train/Val split completed successfully!
Files generated:
- data/coco/annotations/scut_head_partB_train.json
- data/coco/annotations/scut_head_partB_val.json
- data/coco/images/train2017/  (Contains ~1924 images)
- data/coco/images/val2017/    (Contains ~481 images)
```
### 4. Visualization & Sanity Check
**Always** verify your data is correct.
```bash
python scripts/visualize_sample.py
```
**Action:**
1. A window will open showing a image with annottaions.
2. Verify that **Green Boxes** accurately surround the heads in the image.
3. Press any key to close the window.




