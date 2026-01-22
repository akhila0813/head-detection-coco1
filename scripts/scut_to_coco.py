import os
import json
import xml.etree.ElementTree as ET
from PIL import Image

# =========================
# PATHS (relative paths)
# =========================
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

IMAGES_DIR = os.path.join(
    PROJECT_ROOT, "data", "raw", "SCUT_HEAD_Part_B", "JPEGImages"
)
ANNOTATIONS_DIR = os.path.join(
    PROJECT_ROOT, "data", "raw", "SCUT_HEAD_Part_B", "Annotations"
)
OUTPUT_JSON = os.path.join(
    PROJECT_ROOT, "data", "coco", "scut_head_partB_coco.json"
)

os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

def convert_scut_to_coco():
    if not os.path.exists(IMAGES_DIR):
        raise FileNotFoundError(f"Images folder not found: {IMAGES_DIR}")
    if not os.path.exists(ANNOTATIONS_DIR):
        raise FileNotFoundError(f"Annotations folder not found: {ANNOTATIONS_DIR}")

    coco = {
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, "name": "head"}]
    }

    img_id = 1
    ann_id = 1
    skipped = 0

    image_files = sorted(f for f in os.listdir(IMAGES_DIR) if f.endswith(".jpg"))
    print(f"📸 Found {len(image_files)} images")

    for img_file in image_files:
        img_path = os.path.join(IMAGES_DIR, img_file)

        try:
            w, h = Image.open(img_path).size
        except Exception as e:
            print(f"⚠️ Cannot open image {img_file}: {e}")
            skipped += 1
            continue

        coco["images"].append({
            "id": img_id,
            "file_name": img_file,
            "width": w,
            "height": h
        })

        xml_file = img_file.replace(".jpg", ".xml")
        xml_path = os.path.join(ANNOTATIONS_DIR, xml_file)

        if not os.path.exists(xml_path):
            skipped += 1
            img_id += 1
            continue

        tree = ET.parse(xml_path)
        root = tree.getroot()

        for obj in root.findall("object"):
            bbox = obj.find("bndbox")
            xmin = float(bbox.find("xmin").text)
            ymin = float(bbox.find("ymin").text)
            xmax = float(bbox.find("xmax").text)
            ymax = float(bbox.find("ymax").text)

            bw = xmax - xmin
            bh = ymax - ymin

            coco["annotations"].append({
                "id": ann_id,
                "image_id": img_id,
                "category_id": 1,
                "bbox": [xmin, ymin, bw, bh],
                "area": bw * bh,
                "iscrowd": 0
            })
            ann_id += 1

        img_id += 1

    with open(OUTPUT_JSON, "w") as f:
        json.dump(coco, f, indent=2)

    print("\n✅ SCUT → COCO conversion completed")
    print(f"Images processed     : {img_id - 1}")
    print(f"Annotations created  : {ann_id - 1}")
    print(f"Images skipped       : {skipped}")
    print(f"COCO file saved to   : {OUTPUT_JSON}")

# 🔴 THIS LINE IS CRITICAL
if __name__ == "__main__":
    convert_scut_to_coco()
