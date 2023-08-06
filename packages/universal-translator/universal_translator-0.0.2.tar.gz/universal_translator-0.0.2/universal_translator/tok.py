import numpy as np
import json
import sentencepiece as spm
import os
from tqdm import tqdm

class Tokenizer:
    def __init__(self, sp_file:str=None) -> None:
        self.pad_id = 0
        self.sos_id = 1
        self.eos_id = 2
        self.sp_model = spm.SentencePieceProcessor(model_file=sp_file)

    def encode(self, inp):
        return [self.sos_id] + self.sp_model.encode(inp) + [self.eos_id]

    def decode(self, ids):
        ids = np.array(ids)
        ids = ids[ids != self.pad_id]
        if ids[0] == self.sos:
            ids = ids[1:]
        if ids[-1] == self.eos_id:
            ids = ids[:-1]
        return self.sp_model.decode(ids)


def train_tokenizers(manifest_path, save_path, vocab_sizes:dict):
    os.makedirs(save_path + 'texts/', exist_ok=True)
    os.makedirs(save_path + 'tokenizers/', exist_ok=True)
    
    samples = json.load(open(manifest_path))
    data = {}
    for s in samples:
        for k,v in s.items():
            if os.path.exists(save_path + 'tokenizers/' + k + '.model'):
                continue
                
            if k not in data:
                data[k] = []
            data[k] += [v]

    for k in tqdm(data):
        with open(save_path + 'texts/' + k + '.txt', 'w') as writer:
            writer.write('\n'.join(data[k]))

        os.makedirs(save_path + 'tokenizers/' + k, exist_ok=True)
        spm.SentencePieceTrainer.train(
            input=save_path + 'texts/' + k + '.txt', 
            model_prefix=save_path + 'tokenizers/' + k + '/' + k, 
            vocab_size=vocab_sizes[k]
        )    

def load_tokenizers(path):
    res = {}
    for tok in os.listdir(path):
        res[tok] = Tokenizer(path + tok + '/' + tok + '.model')
    return res