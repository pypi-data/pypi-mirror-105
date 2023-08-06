import torch
import numpy as np

from torch import nn
from torch.utils.data import Dataset, DataLoader
from pandas import DataFrame
from typing import Optional, List

from transformers import AutoTokenizer

#==================================================#
#--------------------CONSTANTS---------------------#
#==================================================#

class PreProcConst():
  def __init__(self):
    raise NotImplementedError

  SRC_ITM = 'src_item'        # source item
  INP_IDS = 'input_ids'       # input indeces
  ATT_MSK = 'attention_mask'  # attention mask
  TRG_ITM = 'trg_item'        # target item

class ModuleConst():
  def __init__(self):
    raise NotImplementedError

  # Nested modules
  INP2EMB = 'inp2emb' #       embedding layer name
  EMB2HID = 'emb2hid' #       aggregation / distribution layer name
  VEC2VEC = 'vec2vec' # _N_M  transition layer name (Mth module in Nth chain)
  DROPOUT = 'dropout' #       dropout layer name

  # Special
  VECSPLIT = '_'  # splitter in transition layer full name

  # Main modules
  EMBED = 'embedding'           # embedding module
  TRANS = 'transition'          # transition module
  AGGRG = 'aggregation'         # aggregation module
  DISTR = 'distribution'        # distribution module
  INTRA = 'internal_transition' # internal transition module
  INCON = 'internal_conversion' # internal conversion module

class EmbModeConst():
  def __init__(self):
    raise NotImplementedError
  
  DST_OUT = 0   # distributed output  - standard aggregation needed | no distribution
  AGG_OUT = 1   # aggregated output   - no aggregation              | standard distribution needed
  MIX_OUT = 2   # mixed output        - advanced aggregation needed | advanced distribution needed
  DEFAULT = -1  # default output

class PreAggModeConst():
  def __init__(self):
    raise NotImplementedError
  
  RSH_HID = 0 # reshape hidden vector to make it 3D-tensor
  EMPTY = -1  # no preprocessing

class PostAggModeConst():
  def __init__(self):
    raise NotImplementedError
  
  LST_HID = 0   # last hidden state (as a result of aggregation)
  ALL_LAY = 1   # concatenation of all hidden states (as a result of aggregation)
  LST_LAY = 2   # concatenation of all hidden states from the last layer (as a result of aggregation)
  ALL_AVG = 3   # average score of all hidden states (as a result of aggregation)
  LST_AVG = 4   # average score of all hidden states from the last layer (as a result of aggregation)
  EMPTY   = -1  # no postprocessing

class AggModeConst():
  def __init__(self):
    raise NotImplementedError

  INC = 0   # included                    (full aggregator)
  INR = 1   # included with restrictions  (functional aggregator)
  EXC = 2   # excluded                    (zero-aggregator)

class PreTransModeConst():
  def __init__(self):
    raise NotImplementedError
  
  RNN_STD = 0 # standard preprocessing before rnn
  EMPTY = -1  # no preprocessing

class PostTransModeConst():
  def __init__(self):
    raise NotImplementedError
  
  RNN_STD = 0 # standard postprocessing after rnn
  EMPTY = -1  # no postprocessing

#==================================================#
#---------------GLOBAL PREPROCESSING---------------#
#==================================================#

class TokenizedDataset(Dataset):
  def __init__(self, 
               src : np.ndarray, 
               trg : np.ndarray, 
               tokenizer : AutoTokenizer, 
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
      text=src_item, 
      add_special_tokens=True,
      max_length=self.max_len,
      return_token_type_ids=False,
      padding='max_length',
      return_attention_mask=True,
      return_tensors='pt'
    )

    return {
        PreProcConst.SRC_ITM: src_item, 
        PreProcConst.INP_IDS: encoder[PreProcConst.INP_IDS].flatten(), 
        PreProcConst.ATT_MSK: encoder[PreProcConst.ATT_MSK].flatten(), 
        PreProcConst.TRG_ITM: torch.tensor(trg_item, dtype=torch.long)
    }

class TokenizedDataLoaderFactory():
  @staticmethod
  def get_instance(data_frame : DataFrame, 
                   src_idx : str, 
                   trg_idx : str, 
                   tokenizer : AutoTokenizer, 
                   max_len : int, 
                   batch_size : int
    ) -> DataLoader:
    
    return DataLoader(
        TokenizedDataset(
            data_frame[src_idx].to_numpy(),
            data_frame[trg_idx].to_numpy(),
            tokenizer,
            max_len
        ),
        batch_size
    )

#==================================================#
#--------------------EMBEDDING---------------------#
#==================================================#

class EmbeddingModule(nn.Module):
  def __init__(self,
               basis : nn.Module,
               mode : Optional[int] = EmbModeConst.DEFAULT,
               dropout : Optional[float] = 0):
    
    super().__init__()
    self.add_module(ModuleConst.INP2EMB, basis)
    
    if dropout > 0:
      self.add_module(ModuleConst.DROPOUT, nn.Dropout(p=dropout))

    self.mode = mode
    self.act_dict = {ModuleConst.INP2EMB : self.act_inp2emb,
                     ModuleConst.DROPOUT : self.act_dropout}

  def act_inp2emb(self, module, inp):
    try:
      emb = module(*inp)
    except:
      emb = module(inp)

    if self.mode in [EmbModeConst.DST_OUT, EmbModeConst.AGG_OUT]:
      if isinstance(emb, torch.Tensor):
        self.mode = EmbModeConst.DEFAULT
      else:
        emb = emb[self.mode]
    return emb

  def act_dropout(self, module, emb):
    if self.mode in [EmbModeConst.MIX_OUT]:
      return (module(emb[0]), module(emb[1]))
    else:
      return module(emb)

  def forward(self, inp):
    emb = inp
    for name, module in self.named_children():
      emb = self.act_dict[name](module, emb)
    return emb

#==================================================#
#-------------------TRANSITION---------------------#
#==================================================#

class ModuleChain():
  def __init__(self,
               chain : List[nn.Module],
               pre = lambda hid : hid,
               post = lambda hid : hid):
    
    self._content = chain
    self._preprocess = pre
    self._postprocess = post

  @property
  def content(self):
    return self._content
  
  @property
  def preprocess(self):
    return self._preprocess
  
  @property
  def postprocess(self):
    return self._postprocess

class ModuleChainFactory():  
  @staticmethod
  def get_linear_chain(dim_desc : List[int],
                       bias_desc : Optional[List[bool]] = [True]
                       ) -> ModuleChain:
    chain = []
    for i in range(len(dim_desc) - 1):
      chain.append(nn.Linear(dim_desc[i], dim_desc[i + 1], bias_desc[i if i < len(bias_desc) else -1]))
    return ModuleChain(chain)
  
  RNN_PRE = {PreTransModeConst.RNN_STD : lambda hid : hid.unsqueeze(dim=1),
             PreTransModeConst.EMPTY   : lambda hid : hid}

  RNN_POST = {PostTransModeConst.RNN_STD : lambda hid : hid.squeeze(dim=1),
              PostTransModeConst.EMPTY   : lambda hid : hid}

  @staticmethod
  def get_rnn_chain(rnn_module_name,
                    dim_desc : List[int],
                    num_layers_desc : Optional[List[int]] = [1],
                    bidirectional_desc : Optional[List[bool]] = [False],
                    pre_mode : Optional[int] = PreTransModeConst.RNN_STD,
                    post_mode : Optional[int] = PostTransModeConst.RNN_STD,
                    pre = None,
                    post = None
                    ) -> ModuleChain:
    chain = []
    for i in range(len(dim_desc) - 1):
      chain.append(rnn_module_name(input_size = dim_desc[i] * (2 if (i > 0 and bidirectional_desc[i - 1 if i - 1 < len(bidirectional_desc) else -1]) else 1),
                                   hidden_size = dim_desc[i + 1],
                                   num_layers = num_layers_desc[i if i < len(num_layers_desc) else -1],
                                   bidirectional = bidirectional_desc[i if i < len(bidirectional_desc) else -1],
                                   batch_first = True
                                   )
      )

    return ModuleChain(chain, 
                       pre = pre if pre is not None else ModuleChainFactory.RNN_PRE[pre_mode], 
                       post = post if post is not None else ModuleChainFactory.RNN_POST[post_mode])
      
class TransitionModule(nn.Module):
  def __init__(self,
               chains : List[ModuleChain],
               dropout : Optional[float] = 0):
    
    super().__init__()
    self.chains = chains

    for i in range(len(chains)):
      for j in range(len(chains[i].content)):
        self.add_module(ModuleConst.VEC2VEC + str(i) + ModuleConst.VECSPLIT + str(j), chains[i].content[j])
    
    if dropout > 0:
      self.add_module(ModuleConst.DROPOUT, nn.Dropout(dropout))

    self.act_dict = {ModuleConst.VEC2VEC : self.act_vec2vec,
                     ModuleConst.DROPOUT : self.act_dropout}
  
  def act_vec2vec(self, module, vec, i, j):
    if j == 0:
      vec = self.chains[i].preprocess(vec)
    
    res = module(vec)
    if isinstance(res, torch.Tensor):
      vec = res
    else:
      vec = res[0]    

    if j == len(self.chains[i].content) - 1:
      vec = self.chains[i].postprocess(vec)
    
    return vec
  
  def act_dropout(self, module, vec):
    return module(vec)

  def forward(self, vec):
    for name, module in self.named_children():
      if name.startswith(ModuleConst.VEC2VEC):
        ids = name[len(ModuleConst.VEC2VEC):].split(ModuleConst.VECSPLIT)
        vec = self.act_dict[ModuleConst.VEC2VEC](module, vec, int(ids[0]), int(ids[1]))
      else:
        vec = self.act_dict[name](module, vec)

    return vec

#==================================================#
#-------------------AGGREGATION--------------------#
#==================================================#

class AggregationModule(nn.Module):
  def __init__(self,
               basis : Optional[nn.Module] = None,
               dropout : Optional[float] = 0,
               pre = lambda emb : emb,
               post = lambda hid : hid):
    
    super().__init__()
    if basis is not None:
      self.add_module(ModuleConst.EMB2HID, basis)
      self._mode = AggModeConst.INC
    else:
      self._mode = AggModeConst.INR

    if dropout > 0:
      self.add_module(ModuleConst.DROPOUT, nn.Dropout(dropout))

    self._perform = lambda emb : post(pre(emb))
    self.preprocess = pre
    self.postprocess = post
    self.act_dict = {ModuleConst.EMB2HID : self.act_emb2hid,
                     ModuleConst.DROPOUT : self.act_dropout}
  @property
  def mode(self):
    return self._mode

  @property
  def perform(self):
    return self._perform

  def act_emb2hid(self, module, emb):
    emb = self.preprocess(emb)
    try:
      hid, h0 = emb
      hid = module(hid, h0)
    except:
      hid = module(emb)
    hid = self.postprocess(hid)
    return hid
  
  def act_dropout(self, module, hid):
    return module(hid)

  def forward(self, emb):
    hid = emb
    if self.mode == AggModeConst.INR:
      hid = self.perform(hid)
    for name, module in self.named_children():
        hid = self.act_dict[name](module, hid)
    return hid

class AggregationModuleFactory():
  
  class Reshaper():
    def __init__(self, 
                 dim : Optional[int] = 2, 
                 div : Optional[int] = 0):
      self.dim = dim
      self.div = dim if div == 0 else div
    def __call__(self, hid):
      try:
        hid0, hid1 = hid 
      except:
        hid0, hid1 = None, hid
      hid1 = torch.reshape(hid1, (self.dim, hid1.size(0), hid1.size(1) // self.div))
      return (hid0, hid1) if hid0 is not None else hid1

  RNN_PRE = {
      PreAggModeConst.EMPTY : lambda emb : emb
  }

  RNN_POST = {
      PostAggModeConst.LST_HID : lambda hid : hid[1][-1],
      PostAggModeConst.ALL_LAY : lambda hid : torch.cat(([hid[1][i] for i in range(hid[1].size(0))]), dim=1),
      PostAggModeConst.ALL_AVG : lambda hid : torch.mean(hid[1], dim=0),
      PostAggModeConst.LST_LAY : lambda hid : torch.cat((hid[1][-2], hid[1][-1]), dim=1),
      PostAggModeConst.LST_AVG : lambda hid : torch.mean(hid[1][-2:], dim=0),
      PostAggModeConst.EMPTY   : lambda hid : hid,
  }

  @staticmethod
  def get_rnn_module(rnn_module_name,
                     input_size : int,
                     hidden_size : int,
                     num_layers : Optional[int] = 1,
                     bidirectional : Optional[bool] = False,
                     dropout : Optional[float] = 0,
                     pre_mode : Optional[int] = PreAggModeConst.EMPTY,
                     post_mode : Optional[int] = PostAggModeConst.LST_HID,
                     pre = None,
                     post = None
                     ) -> AggregationModule:

    # BEGIN CHECK PRE
    if pre is None:
      if pre_mode == PreAggModeConst.RSH_HID:
        pre = AggregationModuleFactory.Reshaper(num_layers * (2 if bidirectional else 1))
    # END CHECK PRE

    # BEGIN CHECK POST
    if post is None:
      if post_mode == PostAggModeConst.LST_AVG and bidirectional == False:
        post_mode = PostAggModeConst.LST_HID
      
      if post_mode == PostAggModeConst.LST_LAY and bidirectional == False:
        post_mode = PostAggModeConst.LST_HID
    # END CHECK POST

    return AggregationModule(basis = rnn_module_name(input_size = input_size,
                                                     hidden_size = hidden_size,
                                                     num_layers = num_layers,
                                                     bidirectional = bidirectional,
                                                     batch_first = True),
                             dropout = dropout,
                             pre = pre if pre is not None else AggregationModuleFactory.RNN_PRE[pre_mode],
                             post = post if post is not None else AggregationModuleFactory.RNN_POST[post_mode])

#==================================================#
#---------------SEMANTIC AGGREGATOR----------------#
#==================================================#

class SemanticAggregator(nn.Module):
  def __init__(self,
               embedding : EmbeddingModule,
               transition : TransitionModule,
               aggregation: Optional[AggregationModule] = None,
               internal_transition : Optional[TransitionModule] = None,
               internal_conversion : Optional[TransitionModule] = None,
               final_transformation = lambda hid : (hid, hid.max(dim=1)[1])):
    
    super().__init__()
    self.add_module(ModuleConst.EMBED, embedding)

    if internal_transition is not None:
      self.add_module(ModuleConst.INTRA, internal_transition)

    if internal_conversion is not None:
      self.add_module(ModuleConst.INCON, internal_conversion)

    if aggregation is not None:
      self.add_module(ModuleConst.AGGRG, aggregation)

    self.add_module(ModuleConst.TRANS, transition)
    self.final_transformation = final_transformation
  
    self.act_dict = {ModuleConst.EMBED : self.act_default,
                     ModuleConst.TRANS : self.act_default,
                     ModuleConst.AGGRG : self.act_default,
                     ModuleConst.INTRA : self.act_intra,
                     ModuleConst.INCON : self.act_incon}

  def act_default(self, module, data):
    return module(data)

  def act_intra(self, module, emb):
    try:
      res, inf = emb
    except:
      res, inf = emb, None
    res = module(res)
    return (res, inf) if inf is not None else res

  def act_incon(self, module, emb):
    try:
      inf, res = emb
    except:
      inf, res = None, emb
    res = module(res)
    return (inf, res) if inf is not None else res

  def forward(self, inp):
    out = inp
    for name, module in self.named_children():
      out = self.act_dict[name](module, out)

    return self.final_transformation(out)