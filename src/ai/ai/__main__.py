"""The main CLI entry point."""

from collections import Counter
from pathlib import Path

import torch
from torch import nn
from torch.types import Tensor
from torch.utils.data import DataLoader, Dataset

from ai.data import TAGS, AudioDataset
from ai.network import NeuralNetwork


def train(dataloader, model: nn.Module, loss_fn, optimizer, device):
    size = len(dataloader.dataset)
    model.train()
    # prev_batch = None
    for batch, (X, y) in enumerate(dataloader):
        # if batch != prev_batch:
        #     prev_batch = batch
        #     print("\n")
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        loss, current = loss.item(), (batch + 1) * len(X)
        print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]\r")
    print("\n")


def test(dataloader, model, loss_fn, device):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += ((pred.argmax(1) == 1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(
        f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n"
    )


def main() -> None:
    """Run the app."""
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    print(f"Using {device} device")
    # Initializing neural network
    model = NeuralNetwork().to(device)

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters())

    EPOCHS = 2
    BATCHES = 20
    print("Loading data...")
    train_dataset = AudioDataset(Path(__file__).parent.parent / "data" / "train")
    eval_dataset = AudioDataset(Path(__file__).parent.parent / "data" / "eval")
    e = Counter([eval_dataset[x][0].shape for x in range(len(eval_dataset))])
    common_shape = e.most_common()[0][0]
    trimmed = len(eval_dataset) - e.most_common()[0][1]
    print(
        f"Trimming {trimmed} samples ({trimmed/len(eval_dataset)*100:.2f}%)"
        " from evaluation dataset",
    )
    e = Counter([train_dataset[x][0].shape for x in range(len(train_dataset))])
    trimmed = len(train_dataset) - e.most_common()[0][1]
    print(
        f"Trimming {trimmed} samples ({trimmed/len(train_dataset)*100:.2f}%)"
        " from evaluation dataset",
    )
    eval_dataset.trim_to(common_shape)
    train_dataset.trim_to(common_shape)

    train_dataloader = DataLoader(
        train_dataset,
        batch_size=len(train_dataset) // BATCHES,
        shuffle=True,
    )
    test_dataloader = DataLoader(
        eval_dataset,
        batch_size=len(eval_dataset) // BATCHES,
        shuffle=True,
    )
    epochs = EPOCHS
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train(train_dataloader, model, loss_fn, optimizer, device=device)
        test(test_dataloader, model, loss_fn, device=device)
    print("Done!")
    torch.save(model.state_dict(), "model.pth")
    # print(eval_dataset[0][0].shape, eval_dataset[1][0].shape)


if __name__ == "__main__":
    main()
