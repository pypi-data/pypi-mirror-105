import torch
from torch import nn
import pytorch_lightning as pl
import numpy as np
import pickle
import itertools
from tqdm.notebook import tqdm
from fast_transformers.masking import TriangularCausalMask, LengthMask

from universal_translator.modules import EmbeddingLayer, HeadLayer, Encoder, utils


class Translator(pl.LightningModule):

    def __init__(self, config):
        super().__init__()

        self.config = config
        self.save_hyperparameters()

        self.eos_id = config['eos_id']
        self.criterion = nn.CrossEntropyLoss()

        self.embeddings = nn.ModuleDict([[src, EmbeddingLayer(**config['embedding'][src])] for src in config['embedding']])
        self.encoder = Encoder(config['encoder'])
        self.decoder = Encoder(config['decoder'])
        self.heads = nn.ModuleDict([[trg, HeadLayer(**config['head'][trg])] for trg in config['head']])

        if config['tie_embeddings_heads']:
            utils.tie_embeddings_and_heads(self.embeddings, self.heads)
        

    def configure_optimizers(self):
        opt = torch.optim.Adam(self.parameters(), lr=self.config['lr'])
        sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=self.config['max_epochs'], eta_min=0.)
        return [opt], [sch]

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def encode_decode(self, src, trg, src_inp, trg_inp, src_length_mask=None, trg_length_mask=None, cross_att_mask=None):
        enc_emb = self.embeddings[src](src_inp.long())
        enc = self.encoder(enc_emb, x_length_mask=src_length_mask)

        dec_emb = self.embeddings[trg](trg_inp.long())
        dec = self.decoder(x=dec_emb, 
                           x_length_mask=trg_length_mask, 
                           memory=enc, 
                           memory_mask=cross_att_mask, 
                           memory_length_mask=src_length_mask)

        logits = self.heads[trg](dec)
        return logits


    def forward(self, inputs):
        res = {}
        domains = list(inputs.keys())
        src_trg_pairs = [e for e in itertools.product(domains, domains) if e[0] != e[1]]
        for src, trg in src_trg_pairs:
            res[(src, trg)] = self.encode_decode(
                src=src, 
                trg=trg, 
                src_inp=inputs[src]['X'], 
                trg_inp=inputs[trg]['X'], 
                src_length_mask=inputs[src]['X_len'], 
                trg_length_mask=inputs[trg]['X_len']
            )
        return res


    def step(self, batch, mode='train'):
        res = self.forward(batch)
        losses = {}
        total_loss = 0
        for domain in res:
            logits = res[domain]
            labels = batch[domain[1]]['labels'].long()
            losses[domain] = self.criterion(logits.transpose(1,2), labels)
        
        total_loss = 0
        cnt = 0
        for domain in losses:
            cnt += 1
            total_loss += losses[domain]
            self.log(mode + '_' + str(domain), losses[domain].item())

        total_loss /= cnt
        self.log(mode + '_loss', total_loss.item())
        return total_loss

    def training_step(self, batch, batch_idx):
        return self.step(batch)

    def validation_step(self, batch, batch_idx):
        self.step(batch, mode='val')

    def translate(self, prompt, src, trg, max_len=1000, top_p=1., t=1.):
        self.eval()
        with torch.no_grad():
            res = []
            src_inp = torch.tensor(prompt).long().to(self.device).unsqueeze(0)

            for _ in tqdm(range(max_len)):
                trg_inp = torch.tensor(res).long().to(self.device). unsqueeze(0)
                logits = self.encode_decode(src, trg, src_inp, trg_inp)
                next_tok = utils.sample(logits[0], top_p, t)
                res += [next_tok]
                if next_tok == self.eos_id:
                    break
        return res