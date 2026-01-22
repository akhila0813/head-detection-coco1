import sys
import os
import cv2

# Add project root to sys.path so we can import datasets
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datasets.coco_dataset import CocoDataset

# Load the training dataset
dataset = CocoDataset(
    json_file="data/coco/annotations/scut_head_partB_train.json",
    image_dir="data/coco/images/train2017"
)

# Pick the first sample
img, boxes = dataset[0]

# Draw bounding boxes
for box in boxes:
    x, y, w, h = [int(i) for i in box]
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Show the image
cv2.imshow("Sample", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
