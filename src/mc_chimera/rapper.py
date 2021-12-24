
from pathlib import Path

from mc_chimera.normalize import normalize_text

MODEL_DIR = Path(__file__).parent.parent.parent / 'model'

import argparse
import glob
import os
import json
import time
import logging
import random
import re
from itertools import chain
from string import punctuation

import numpy as np
import torch

from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    )

# 乱数シードの設定
def set_seed(seed):
  random.seed(seed)
  np.random.seed(seed)
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

set_seed(42)

from transformers import T5ForConditionalGeneration, T5Tokenizer

# トークナイザー（SentencePiece）
tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR, is_fast=True)

# 学習済みモデル
trained_model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)

# GPUの利用有無
USE_GPU = torch.cuda.is_available()
if USE_GPU:
    trained_model.cuda()

# 推論モード設定
trained_model.eval()
 

MAX_SOURCE_LENGTH = 128
MAX_TARGET_LENGTH = 128

def preprocess_body(text):
    return normalize_text(text.replace("\n", " "))

class Rapper():
  def verse(self, text):
    # 前処理とトークナイズを行う
    inputs = [preprocess_body(text)]
    batch = tokenizer.batch_encode_plus(
        inputs, max_length=MAX_SOURCE_LENGTH, truncation=True,
        padding="longest", return_tensors="pt")
    
    input_ids = batch['input_ids']
    input_mask = batch['attention_mask']
    if USE_GPU:
        input_ids = input_ids.cuda()
        input_mask = input_mask.cuda()
    
    # 生成処理を行う
    outputs = trained_model.generate(
        input_ids=input_ids, attention_mask=input_mask,
        max_length=MAX_TARGET_LENGTH,
        temperature=1.0,          # 生成にランダム性を入れる温度パラメータ
        num_beams=10,             # ビームサーチの探索幅
        diversity_penalty=1.0,    # 生成結果の多様性を生み出すためのペナルティ
        num_beam_groups=10,       # ビームサーチのグループ数
        num_return_sequences=1,   # 生成する文の数
        repetition_penalty=3.0,   # 同じ文の繰り返し（モード崩壊）へのペナルティ
    )
    
    # 生成されたトークン列を文字列に変換する
    generated_verses = [tokenizer.decode(ids, skip_special_tokens=True,
      clean_up_tokenization_spaces=False)
      for ids in outputs]
    
    return generated_verses[0]

if __name__ == '__main__':
  rapper = Rapper()
  print(MODEL_DIR)
  body = 'この街の夕日が好きになる 見とれてる横顔が隙になる'
  print(rapper.verse(body))

