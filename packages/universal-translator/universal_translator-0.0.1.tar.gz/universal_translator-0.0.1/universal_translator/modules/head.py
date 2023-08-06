import numpy as np
import torch
from torch import nn
import math
from collections import OrderedDict


class HeadLayer(nn.Module):
    def __init__(self, n_vocab, d_model):
        super().__init__()
        self.head = nn.Linear(d_model, n_vocab)

    def forward(self, h):
        return self.head(h)