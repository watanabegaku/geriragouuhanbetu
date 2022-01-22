#from django.forms import forms
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from torchvision.models import resnet18
import pytorch_lightning as pl

from PIL import Image
import numpy as np

def transform(img):
    _transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return _transform(img)

class Net(pl.LightningModule):
    def __init__(self):
        super().__init__()

        self.conv = resnet18(pretrained=False)
        self.fc = nn.Linear(1000,3)

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x