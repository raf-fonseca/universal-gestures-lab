import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

output_dim = 1 # binary classification for thumbs up or down
input_dim = 17 # 17 features

# Model
class FeedforwardNeuralNetModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(FeedforwardNeuralNetModel, self).__init__()
        # Linear function
        self.fc1 = nn.Linear(input_dim, hidden_dim) 
        # Non-linearity
        self.tanh = nn.Tanh()
        # Linear function (readout)
        self.fc2 = nn.Linear(hidden_dim, output_dim)  

    def forward(self, x):
        # Linear function
        out = self.fc1(x)
        # Non-linearity
        out = self.tanh(out)
        # Linear function (readout)
        out = self.fc2(out)
        return out

# Data set
def split_feature_label(data):
    X = data[:, :-1]
    Y = data[:, -1]
    return X, Y

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.X, self.Y = split_feature_label(data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]

# Loader fn
def load_data(dataset, batch_size=64):
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return loader

def main():
    train_path = "train_data/train_0.pt"
    test_path = "test_data/test_0.pt"
    train_data = torch.load(train_path)
    test_data = torch.load(test_path)
    train_loader = load_data(train_data)
    test_loader = load_data(test_data)
    
    batch_size = 64
    n_iters = len(train_loader) * 64 * 5 # 5 epochs
    num_epochs = int(n_iters / (len(train_data)/batch_size))
    
    model = FeedforwardNeuralNetModel(input_dim, 100, output_dim)
    criterion = nn.BCELoss()
    learning_rate = 0.01
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    
    # for iteration in num_epochs:
    for epoch in range(num_epochs):
       for i, (X, Y) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(X)
            loss = criterion(outputs, Y)
            loss.backward()
            optimizer.step()
            iter += 1
            
            if iter % 500 == 0:
                correct = 0
                total = 0
                for X, Y in test_loader:
                    outputs = model(X)
                    _, predicted = torch.max(outputs.data, 1)
                    total += y.size(0)
                    correct += (predicted == Y).sum()

                accuracy = 100 * correct / total
                print('Iteration: {}. Loss: {}. Accuracy: {}'.format(iter, loss.item(), accuracy))

if __name__ == "__main__":
    main()
