import math
import random

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.flatten = nn.Flatten()
        self.network = nn.Sequential(
            nn.Linear(2, 10),
            nn.ReLU(),
            nn.Linear(10, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.network(x)


class CustomDataset(Dataset):
    def __init__(self):
        self.data = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
        self.labels = torch.tensor([0, 1, 1, 0], dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return 10000

    def __getitem__(self, idx):
        return self.data[idx % 4], self.labels[idx % 4]


model = Model().to(device)
loss_fn = nn.BCELoss()
LEARNING_RATE = 0.01
optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)
train_data = DataLoader(CustomDataset(), shuffle=True)
test_data = DataLoader(CustomDataset(), shuffle=True)


def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)
        # print(X, y, pred, loss)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test(dataloader, model: Model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += ((pred[0] > 0.5) == (y == 1.0)).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(
        f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n"
    )


if __name__ == "__main__":
    epochs = 1
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train(train_data, model, loss_fn, optimizer)
        test(test_data, model, loss_fn)
    model.eval()
    print((model(torch.tensor([0.0, 1.0]).to(device))))
    print("Done!")
