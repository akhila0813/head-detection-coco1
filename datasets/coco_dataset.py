import torch
from torch.utils.data import Dataset
import cv2
import json

class CocoDataset(Dataset):
    def __init__(self, json_file, image_dir, transform=None):
        with open(json_file) as f:
            coco = json.load(f)
        self.images = {img['id']: img for img in coco['images']}
        self.annotations = {}
        for ann in coco['annotations']:
            self.annotations.setdefault(ann['image_id'], []).append(ann)
        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_id = list(self.images.keys())[idx]
        img_info = self.images[img_id]
        path = f"{self.image_dir}/{img_info['file_name']}"
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        anns = self.annotations.get(img_id, [])
        boxes = [ann['bbox'] for ann in anns]
        return img, boxes
