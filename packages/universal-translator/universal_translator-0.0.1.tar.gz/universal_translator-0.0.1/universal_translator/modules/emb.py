import numpy as np
import torch
from torch import nn
import math

class Embeddings(nn.Module):
    def __init__(self, n_vocab, d_emb):
        super(Embeddings, self).__init__()
        self.lut = nn.Embedding(n_vocab, d_emb)
        self.d_emb = d_emb

    def forward(self, x):
        return self.lut(x) * math.sqrt(self.d_emb)


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=512):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return self.pe[:, :x.size(1), :]


class EmbeddingLayer(nn.Module):
    def __init__(self, n_vocab, d_model, max_len=5000, dropout=0.1):
        super().__init__()
        
        self.embedding = Embeddings(n_vocab=n_vocab, d_emb=d_model)
        self.pos_emb = PositionalEncoding(d_model=d_model, max_len=max_len)
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x):
        x = self.embedding(x)
        pos_emb = self.pos_emb(x)
        return self.dropout(x + pos_emb)