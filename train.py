import main
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
import pickle

class model(nn.Module):
    def __init__(self):
        super(model, self).__init__()
        with open("Model", "rb") as txt:
            self.layers = pickle.load(txt)

    def forward(self, x):
        for i in self.layers:
            x=i(x)
        return x
    
