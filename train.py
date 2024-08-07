import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image
from tqdm import tqdm
import ImageDataset
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
    
dataset = ImageDataset.ImageDataset()
print(f"Dataset initialized with {len(dataset)} samples")
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

batch_size = 16
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0, drop_last=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0, drop_last=True)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
model = model().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 100
train_losses = []
val_losses = []

for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs} started")
        model.train()
        running_loss = 0.0

        for images, labels in tqdm(train_loader, desc="Training"):
            images, labels = images.to(device, dtype=torch.float32), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)
        train_losses.append(train_loss)
        print("Training ended for epoch", epoch + 1)

        # Validation
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        print("Evaluation started")
        with torch.no_grad():
            for images, labels in tqdm(val_loader, desc="Evaluating"):
                images, labels = images.to(device, dtype=torch.float32), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print("Evaluation ended")

        val_loss /= len(val_loader)
        val_losses.append(val_loss)
        accuracy = 100 * correct / total

        print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Accuracy: {accuracy:.2f}%')
        torch.save(model.state_dict(), 'model' + str(epoch) + '.pth')