import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
import pandas as pd
import torch
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

model_index=20
batch_size=4096*4

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_dir=os.path.join('..','model')
model = BertForSequenceClassification.from_pretrained(os.path.join(model_dir,'finetune_title',f'epoch{model_index}'))
tokenizer = BertTokenizer.from_pretrained(os.path.join(model_dir,'finetune_title',f'epoch{model_index}'))
model.to(device)
model.eval()


if os.path.exists(os.path.join('..','result_alltime','Dict_ClassifyWork_Title_Raw')):
    ClassifyWork_Title_Raw=pickle.load(open(os.path.join('..','result_alltime','Dict_ClassifyWork_Title_Raw'),'rb'))
else:
    ClassifyWork_Title_Raw=dict()

title_batch=list()
id_batch=list()
data_dir=os.path.join('..','openalex','csv-files')
works=pd.read_csv(os.path.join(data_dir,'works.csv'),chunksize=100000,usecols=['id','title'])

chunk_count=0
for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        id=int(line['id'].strip('https://openalex.org/W'))
        if id in ClassifyWork_Title_Raw:
            continue
        if id not in Set_SelectWork:
            continue

        title=line['title'].lower()
        title_batch.append(title)
        id_batch.append(id)

        if len(title_batch)==batch_size:
            with torch.no_grad():
                tokenized_title = tokenizer(title_batch, max_length=32, truncation=True, padding=True, return_tensors="pt")
                tokenized_title = tokenized_title.to(device)
                output = model(**tokenized_title)[0].cpu().tolist()

            for j in range(batch_size):
                ClassifyWork_Title_Raw[id_batch[j]]=output[j]

            title_batch=list()
            id_batch=list()
    
    chunk_count+=1
    if chunk_count%50==0:
        pickle.dump(ClassifyWork_Title_Raw,open(os.path.join('..','result_alltime','Dict_ClassifyWork_Title_Raw'),'wb'))

with torch.no_grad():
    tokenized_title = tokenizer(title_batch, max_length=32, truncation=True, padding=True, return_tensors="pt")
    tokenized_title = tokenized_title.to(device)
    output = model(**tokenized_title)[0].cpu().tolist()

for j in range(len(output)):
    ClassifyWork_Title_Raw[id_batch[j]]=output[j]

pickle.dump(ClassifyWork_Title_Raw,open(os.path.join('..','result_alltime','Dict_ClassifyWork_Title_Raw'),'wb'))