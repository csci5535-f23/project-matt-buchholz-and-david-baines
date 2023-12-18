from data_loader import load_dataset, PICKLE_DIR

import pandas as pd
#from transformers import BertTokenizer, BertForMaskedLM
from torch.utils.data import Dataset, DataLoader
from transformers import AdamW
import pickle
import os

import sentencepiece as spm
class CodeDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_length=128):
        self.data = dataframe['code'].tolist()
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        code = str(self.data[idx])
        inputs = self.tokenizer(
            code,
            truncation=True,
            max_length=self.max_length,
            padding='max_length',
            return_tensors='pt'
        )
        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze()
        }



def build_vocab_file(dataset, model_name) -> str:
    filename = f'{model_name}.vocab'
    if os.path.exists(filename):
        return filename

    with open('code_tmp.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(dataset['contents']))

    spm.SentencePieceTrainer.Train(f'--input=code_tmp.txt --model_prefix={model_name} --model_type=bpe --vocab_size=5000')


def finetune_baseline(model_name='bert-base-uncased', dataset_fraction=1, random_state=5535):

    train, test = load_dataset()
    train = train['contents']


if __name__ == '__main__':
    dataset, _ = load_dataset()
    build_vocab_file(dataset['contents'])


