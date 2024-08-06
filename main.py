import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
class AILayer():
    def __init__(self, type, arg1, arg2):
        if len(arg1.get() == 0):
            self.layer = eval("nn." + type.get() + "(" + ")")
        elif len(arg2.get() == 0):
            self.layer = eval("nn." + type.get() + "(" + arg1.get() + ")")
        else:
            self.layer = eval("nn." + type.get() + "(" + arg1.get() + "," + arg2.get() + ")")

class ImageTransform():
    def __init__(self, args):
        transformstring = "transforms.Compose(["
        for i in args.keys():
            transformstring+= "transforms." + i + "(" + args[i] + "),"
        transformstring += "])"
        self.transform = eval(transformstring)

transformlist = [
    "ToTensor", "Normalize", "Resize", "Scale", "CenterCrop", "Pad", "Lambda", "RandomApply",
    "RandomChoice", "RandomOrder", "RandomCrop", "RandomHorizontalFlip", "RandomVerticalFlip", "RandomResizedCrop","RandomRotation","RandomAffine",
    "Grayscale", "ColorJitter", "RandomErasing", "GaussianBlur", "RandomPerspective", "RandomInvert", "RandomPosterize", "RandomSolarize",
    "RandomAdjustSharpness", "RandomAutocontrast", "RandomEqualize", "FiveCrop", "TenCrop", "LinearTransformation", "ElasticTransform", "ToPILImage",
    "AutoAugment", "RandAugment", "TrivialAugmentWide", "AugMix"
]