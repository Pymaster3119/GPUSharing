import pickle
import zipfile
import re
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import concurrent.futures

class ImageDataset:
    def __init__(self):
        with open("ModelTransform", "rb") as txt:
            self.transform = pickle.load(txt)[0]
        with open("paths", "rb") as txt:
            self.paths = pickle.load(txt)
        self.imgs = []
        self.labels = []
        self.length = 0
        for i in range(len(self.paths)):
            with zipfile.ZipFile(self.paths[i]) as zip:
                for j in zip.namefile():
                    try:
                        img_data = zip.open(j)
                        img = Image.open(BytesIO(img_data))
                        img = img.convert("RGB")
                        self.labels.append(i)
                        self.imgs.append(j)
                        self.length += 1
                    except:
                        pass
    def __len__(self):
        return self.length
    
    def __getitem__(self, idx):
        return 