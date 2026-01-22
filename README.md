Overview

This project converts the SCUT-HEAD Part B dataset from its original XML annotation format into the COCO object detection 
format.

The pipeline includes:

Dataset organization

XML → COCO conversion

Train / validation split

PyTorch-compatible dataset loader

Visualization for sanity checking

Dataset Source

SCUT-HEAD Dataset

The SCUT-HEAD dataset is a public head-detection dataset containing crowd images.

Each image is annotated using Pascal VOC XML format.

Annotations contain bounding boxes for human heads.

Scut-Head Dataset : https://www.kaggle.com/datasets/hoangxuanviet/scut-head

⚠️ Note:

Due to dataset size and licensing constraints, raw images are not pushed to GitHub.
Users must download the dataset separately and place it in the correct directory.

Project Structure

head-detection-coco/

├── scripts/

│   ├── scut_to_coco.py        # XML → COCO conversion

│   ├── split_coco.py          # Train / validation split

│   └── visualize_sample.py   # Visualization & sanity check

│

├── datasets/

│   └── coco_dataset.py       # Reusable PyTorch Dataset class

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

│
├── requirements.txt

├── .gitignore

└── README.md


Pipeline

--> Dataset Placement

After downloading and extracting SCUT_HEAD_Part_B, place it as follows:

data/raw/SCUT_HEAD_Part_B/

├── JPEGImages/

└── Annotations/


This separation ensures:

Raw data remains untouched

Processing scripts remain reproducible

--> Convert SCUT XML → COCO JSON

Script:

python scripts/scut_to_coco.py


What this script does:

Reads all images from JPEGImages/

Parses corresponding XML files from Annotations/

Converts bounding boxes to COCO format

Assigns category:

id: 1

name: "head"

Generates a single COCO annotation file

Output:

data/coco/scut_head_partB_coco.json


Example console output:

📸 Found 2405 images

✅ SCUT → COCO conversion completed

Images processed     : 2405

Annotations created  : ~43,930

Images skipped       : 0

--> Train / Validation Split

Script :

python scripts/split_coco.py


What this script does:

Reads the COCO annotation file

Randomly splits data into:

Train set

Validation set

Copies images into:

data/coco/images/train2017/

data/coco/images/val2017/


Writes corresponding annotation files into:

data/coco/annotations/



--> PyTorch Dataset Loader

File:

datasets/coco_dataset.py


Purpose:

Implements a reusable CocoDataset class

Loads:

Images

Bounding boxes

Labels

Returns data in PyTorch-friendly format


--> Visualization & Sanity Check

Script:

python scripts/visualize_sample.py


What this script does:

Loads the dataset using CocoDataset

Selects a random sample

Draws bounding boxes on the image

Displays the result

Why this is important:

Confirms annotation correctness

Verifies bounding box alignment

Detects data corruption early

This step ensures data quality before training.

Environment Setup

Install Dependencies

pip install -r requirements.txt


Dependencies include:

numpy

torch / torchvision

pycocotools

pillow

opencv-python

matplotlib


Each responsibility is isolated:

Conversion

Splitting

Loading

Visualization

--> Summary

Dataset: SCUT-HEAD Part B

Task: SCUT-HEAD Part B dataset from its original XML annotation format into the COCO format
 
Format: COCO

Images: 2405

Annotations: ~43k


