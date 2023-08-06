import subprocess
subprocess.call(['pip', 'install', 'transformers'])

# Basic imports
import torch
from torch import nn
import numpy as np

from torch.utils.data import Dataset, DataLoader
from pandas import DataFrame

# External imports
from transformers import BertTokenizer

#==================================================#
# Dataset & DataLoaderFactory (Preprocessing)
#==================================================#

SRC_ITM = 'src_item'
INP_IDS = 'input_ids'
ATT_MSK = 'attention_mask'
TRG_ITM = 'trg_item'

class BertDataset(Dataset):
  def __init__(self, 
               src : np.ndarray, 
               trg : np.ndarray, 
               tokenizer : BertTokenizer, 
               max_len : int
    ):
    
    self.src = src
    self.trg = trg
    self.tokenizer = tokenizer
    self.max_len = max_len
  
  def __len__(self):
    return len(self.src)
  
  def __getitem__(self, idx : int):
    src_item = str(self.src[idx])
    trg_item = self.trg[idx]

    encoder = self.tokenizer.encode_plus(
      src_item, 
      add_special_tokens=True,
      max_length=self.max_len,
      return_token_type_ids=False,
      padding='max_length',
      return_attention_mask=True,
      return_tensors='pt'
    )

    return {
        SRC_ITM: src_item, 
        INP_IDS: encoder[INP_IDS].flatten(), 
        ATT_MSK: encoder[ATT_MSK].flatten(), 
        TRG_ITM: torch.tensor(trg_item, dtype=torch.long)
    }

class BertDataLoaderFactory():
  @staticmethod
  def get_instance(data_frame : DataFrame, 
                   src_idx : str, 
                   trg_idx : str, 
                   tokenizer : BertTokenizer, 
                   max_len : int, 
                   batch_size : int
    ) -> DataLoader:
    
    return DataLoader(
        BertDataset(
            data_frame[src_idx].to_numpy(),
            data_frame[trg_idx].to_numpy(),
            tokenizer,
            max_len
        ),
        batch_size
    )

#==================================================#
# Dataset & DataLoaderFactory
#==================================================#