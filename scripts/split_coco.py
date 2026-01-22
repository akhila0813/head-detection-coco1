import os
import json
import shutil
import random

# ===== Paths =====
INPUT_JSON = "data/coco/scut_head_partB_coco.json"  # your original COCO JSON
IMAGE_SRC = "data/raw/SCUT_HEAD_Part_B/JPEGImages"  # source images
ANNOTATION_DEST = "data/coco/annotations"
IMAGE_DEST = "data/coco/images"

# Seed for reproducibility
random.seed(42)

# ===== Create folders =====
os.makedirs(ANNOTATION_DEST, exist_ok=True)
os.makedirs(os.path.join(IMAGE_DEST, "train2017"), exist_ok=True)
os.makedirs(os.path.join(IMAGE_DEST, "val2017"), exist_ok=True)

# ===== Load original COCO JSON =====
with open(INPUT_JSON) as f:
    coco = json.load(f)

images = coco['images']
random.shuffle(images)

# ===== Split 80% train / 20% val =====
split_idx = int(0.8 * len(images))
train_images = images[:split_idx]
val_images = images[split_idx:]

def save_split(images_split, split_name):
    image_ids = {img['id'] for img in images_split}
    split_annotations = [ann for ann in coco['annotations'] if ann['image_id'] in image_ids]

    # Save JSON
    split_json = {
        "images": images_split,
        "annotations": split_annotations,
        "categories": coco['categories']
    }
    with open(f"{ANNOTATION_DEST}/scut_head_partB_{split_name}.json", "w") as f:
        json.dump(split_json, f, indent=2)

    # Copy images
    for img in images_split:
        src_path = os.path.join(IMAGE_SRC, img['file_name'])
        dst_path = os.path.join(IMAGE_DEST, f"{split_name}2017", img['file_name'])
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
        else:
            print(f"⚠️  Image not found: {src_path}, skipping...")

# ===== Run splits =====
save_split(train_images, "train")
save_split(val_images, "val")

print("✅ Train/Val split completed successfully!")
