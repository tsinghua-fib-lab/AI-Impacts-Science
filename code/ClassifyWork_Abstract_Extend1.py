import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
import pandas as pd
import torch
import json
from tqdm import tqdm
from transformers import BertForSequenceClassification,BertTokenizer

import warnings
warnings.filterwarnings('ignore')

with open(os.path.join('..','result_alltime','List_SelectWork_Journal'),'rb') as f:
    Set_SelectWork_Journal=set(pickle.load(f))
with open(os.path.join('..','result_alltime','List_SelectWork_Year1980-2024_TitleAbstract_Language'),'rb') as f:
    Set_SelectWork_Year_TitleAbstract_Language=set(pickle.load(f))

print(len(Set_SelectWork_Journal))
print(len(Set_SelectWork_Year_TitleAbstract_Language))

Set_SelectWork=Set_SelectWork_Journal.intersection(Set_SelectWork_Year_TitleAbstract_Language)
print(len(Set_SelectWork))

model_index=13
batch_size=2048

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_dir=os.path.join('..','model')
model = BertForSequenceClassification.from_pretrained(os.path.join(model_dir,'finetune_abstract_extend1',f'epoch{model_index}'))
tokenizer = BertTokenizer.from_pretrained(os.path.join(model_dir,'finetune_abstract_extend1',f'epoch{model_index}'))
model.to(device)
model.eval()


def restore_abstract(indexed_abstract):
    # Create a list with the length equal to the number of total words in the abstract
    total_length = max(max(indices) for indices in indexed_abstract.values()) + 1
    restored_abstract = [''] * total_length

    # Fill in the words at the correct positions
    for word, positions in indexed_abstract.items():
        for position in positions:
            restored_abstract[position] = word

    # Join the words into a single string
    return ' '.join(restored_abstract)


if os.path.exists(os.path.join('..','result_alltime','Dict_ClassifyWork_Abstract_Extend1')):
    ClassifyWork_Abstract_Extend1=pickle.load(open(os.path.join('..','result_alltime','Dict_ClassifyWork_Abstract_Extend1'),'rb'))
else:
    ClassifyWork_Abstract_Extend1=dict()

abstract_batch=list()
id_batch=list()
data_dir=os.path.join('..','openalex','csv-files')
works=pd.read_csv(os.path.join(data_dir,'works.csv'),chunksize=100000,usecols=['id','abstract_inverted_index'])

chunk_count=0
for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        id=int(line['id'].strip('https://openalex.org/W'))
        if id in ClassifyWork_Abstract_Extend1:
            continue
        if id not in Set_SelectWork:
            continue

        abstract=restore_abstract(json.loads(line['abstract_inverted_index'])).lower()
        abstract_batch.append(abstract)
        id_batch.append(id)

        if len(abstract_batch)==batch_size:
            with torch.no_grad():
                tokenized_abstract = tokenizer(abstract_batch, max_length=256, truncation=True, padding=True, return_tensors="pt")
                tokenized_abstract = tokenized_abstract.to(device)
                output = model(**tokenized_abstract)[0].cpu().tolist()

            for j in range(batch_size):
                ClassifyWork_Abstract_Extend1[id_batch[j]]=output[j]

            abstract_batch=list()
            id_batch=list()

    chunk_count+=1
    if chunk_count%50==0:
        pickle.dump(ClassifyWork_Abstract_Extend1,open(os.path.join('..','result_alltime','Dict_ClassifyWork_Abstract_Extend1'),'wb'))

with torch.no_grad():
    tokenized_abstract = tokenizer(abstract_batch, max_length=256, truncation=True, padding=True, return_tensors="pt")
    tokenized_abstract = tokenized_abstract.to(device)
    output = model(**tokenized_abstract)[0].cpu().tolist()

for j in range(len(output)):
    ClassifyWork_Abstract_Extend1[id_batch[j]]=output[j]

pickle.dump(ClassifyWork_Abstract_Extend1,open(os.path.join('..','result_alltime','Dict_ClassifyWork_Abstract_Extend1'),'wb'))