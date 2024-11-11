from torch import Tensor, nn


class NeuralNetwork(nn.Module):
    # 3 seconds
    def __init__(self, waveform_size: int = 133062):
        super().__init__()
        self.network = nn.Sequential(
            nn.Flatten(),
            # I'm currently just spamming random
            # Non linear layers to see what happens
            nn.Linear(waveform_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Sigmoid(),
            nn.Linear(64, 64),
            nn.ReLU(),
            # Yes/no "categories"
            nn.Linear(64, 2),
            # Like sure I could just have one output neuron but no.
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.network(x)
