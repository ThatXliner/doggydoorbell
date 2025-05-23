import io
import itertools
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import torch
import torchaudio
from torch import Tensor, nn
from torch.utils.data import Dataset
from torchaudio import transforms

TAGS = {
    "dd00136": "Whimper (dog)",
    "dd00141": "Pant (dog)",
    "01z5f": "Canidae, wild dogs, wolves",
    "0bt9lr": "Dog",
}

N_FFT = 400  # default


class AudioDataset(Dataset):
    """Loads our custom audio dataset with our custom label format."""

    def __init__(self, audio_dir: Path, n_fft: int = N_FFT, sample_rate: int = 44100):
        self.audio_dir = audio_dir
        self.dataset = []
        failures = 0
        spectrogram = transforms.Spectrogram(n_fft)
        target_samples = sample_rate * 3  # 3 seconds worth of samples
        # XXX: Remove islice for actual training
        for file in audio_dir.glob("*.mp3"):
            try:
                waveform, rate = torchaudio.load(file, format="mp3")
                # Downmix to mono
                waveform = torch.mean(waveform, dim=0, keepdim=True)

                # Resample if necessary
                if rate != sample_rate:
                    waveform = torchaudio.transforms.Resample(
                        orig_freq=rate, new_freq=sample_rate
                    )(waveform)

                # Trim to the first 3 seconds
                waveform = waveform[:, :target_samples]

                # Generate spectrogram
                data = spectrogram(waveform)
                self.dataset.append((data, file))
            except RuntimeError:
                failures += 1
        print(
            f"Failed to load {failures} files: {failures / (len(self.dataset) + failures):.2%}%"
        )

    def __len__(self):
        return len(self.dataset)

    def trim_to(self, shape):
        self.dataset = [x for x in self.dataset if x[0].shape == shape]

    def __getitem__(self, idx: int) -> tuple[Tensor, bool]:
        data, file = self.dataset[idx]
        return (
            data,
            # For now, we will just go with a binary classification
            any(
                label in TAGS
                for label in file.stem.split("_segment_", maxsplit=1)[1].split("_")[1:]
            ),
        )
