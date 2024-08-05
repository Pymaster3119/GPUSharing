import torch
import torch.nn as nn
import torch.optim as optim
class AILayer():
    def __init__(self, type, arg1, arg2):
        self.layer = eval("nn." + type + "(" + arg1 + "," + arg2 + ")")