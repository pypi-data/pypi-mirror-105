"""Spiral dataset for binary classification."""

import numpy as np
import torch


def make_spiral(n_samples=500, noise=0.3):
    def get_samples(n, delta_t):
        points = []
        for i in range(n):
            r = i / n_samples * 5
            t = 1.75 * i / n * 2 * np.pi + delta_t
            x = r * np.sin(t) + np.random.rand(1) * noise
            y = r * np.cos(t) + np.random.rand(1) * noise
            points.append([x, y])
        return points

    n = n_samples // 2
    positive = get_samples(n=n, delta_t=0)
    negative = get_samples(n=n, delta_t=np.pi)
    x = np.concatenate(
        [np.array(positive).reshape(n, -1),
         np.array(negative).reshape(n, -1)],
        axis=0)
    y = np.concatenate([np.zeros(n), np.ones(n)])
    return x, y


class Spiral(torch.utils.data.TensorDataset):
    """Spiral dataset for binary classification."""
    def __init__(self, n_samples=500, noise=0.3):
        x, y = make_spiral(n_samples, noise)
        super().__init__(torch.Tensor(x), torch.LongTensor(y))
