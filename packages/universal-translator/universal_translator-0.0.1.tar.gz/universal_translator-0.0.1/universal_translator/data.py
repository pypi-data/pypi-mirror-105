import numpy as np
import torch
import json
from tqdm import tqdm
from torch.utils.data import random_split, Dataset, DataLoader

def get_dataloaders(dataset,
                    n_jobs=2,
                    batch_size=64, 
                    val_frac=0.2):
    
    n = len(dataset)
    v = int(n*val_frac)
    train_dataset, val_dataset = random_split(dataset, [n - v, v])
    train_loader = DataLoader(
        dataset=train_dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=n_jobs, 
        collate_fn=dataset.collate_fn
    )
    val_loader = DataLoader(
        dataset=val_dataset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=n_jobs, 
        collate_fn=dataset.collate_fn
    )
    print('train dataset has {} samples and val dataset has {} samples.'.format(n-v, v))
    return train_loader, val_loader


def tokenize_and_filter(samples, tokenizers, max_len):
    res = []
    cnt = 0
    for s in tqdm(samples):
        add = True
        for k,v in s.items():
            s[k] = tokenizers[k].encode(v)
            if len(s[k]) > max_len:
                add = False
                cnt += 1
                break
        if add:
            res += [s]
    print(cnt, 'samples were filtered.')
    return res

class TranslationDataset(Dataset):
    def __init__(self, tokenizers : dict, manifest_path : str, max_len : int = 5000) -> None:
    
        super().__init__()
        self.tokenizers = tokenizers
        self.samples = tokenize_and_filter(
            samples=json.load(open(manifest_path)), 
            tokenizers=tokenizers, 
            max_len=max_len
        )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

    def collate_fn(self, batch):
        X = {}
        for b in batch:
            for k,v in b.items():
                if k not in X:
                    X[k] = []
                X[k] += [v]
                
        res = {}
        for k,v in X.items():
            x_len = torch.tensor([len(x) for x in v])
            M = max(x_len)
            res[k] = {
                'X': torch.tensor([
                    np.pad(
                        x[:-1], 
                        (0, M - len(x) + 1),
                        constant_values=self.tokenizers[k].pad_id
                    ) 
                    for x in v
                ]),
                'X_len': x_len,
                'labels': torch.tensor([
                    np.pad(
                        x[1:], 
                        (0, M - len(x) + 1),
                        constant_values=self.tokenizers[k].pad_id
                    )
                    for x in v
                ])
            }

        return res

        