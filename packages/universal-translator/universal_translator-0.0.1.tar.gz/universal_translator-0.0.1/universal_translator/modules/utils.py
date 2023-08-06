import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from fast_transformers.masking import TriangularCausalMask, LengthMask

def tie_embeddings_and_heads(embeddings : nn.ModuleDict, heads : nn.ModuleDict):
    for src in embeddings:
        if src in heads:
            embeddings[src].embedding.weight = heads[src].head.weight


def sample(x, top_p=1., t=1.):
    probs = F.softmax(x/t).detach().cpu()
    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    cumsum_sorted_probs = torch.cumsum(sorted_probs, dim=0)
    threshold = cumsum_sorted_probs > top_p
    idx = probs.size(0) - sum(threshold) + 1
    cand_indices = sorted_indices[:idx]
    cand_probs = probs[cand_indices]
    cand_probs /= cand_probs.sum()
    return np.random.choice(cand_indices.numpy(), size=1, p=cand_probs.numpy())[0]