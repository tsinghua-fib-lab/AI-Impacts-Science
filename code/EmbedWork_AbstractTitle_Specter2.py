import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
import pandas as pd
import torch
import json
from tqdm import tqdm
from transformers import AutoTokenizer
from adapters import AutoAdapterModel

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

batch_size=4096

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(os.path.join('..','model','allenai','specter2_base'))
model = AutoAdapterModel.from_pretrained(os.path.join('..','model','allenai','specter2_base'))
model.load_adapter(os.path.join('..','model','allenai','adapter'), source="hf", load_as="specter2", set_active=True)
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


EmbedWork_AbstractTitle_Specter2=dict()
text_batch=list()
id_batch=list()
data_dir=os.path.join('..','openalex','csv-files')
works=pd.read_csv(os.path.join(data_dir,'works.csv'),chunksize=100000,usecols=['id','title','abstract_inverted_index'])

chunk_count=0
part_count=0
for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        id=int(line['id'].strip('https://openalex.org/W'))
        if id not in Set_SelectWork:
            continue

        abstract=restore_abstract(json.loads(line['abstract_inverted_index'])).lower()
        title=line['title'].lower()
        
        text_batch.append(title + tokenizer.sep_token + abstract)
        id_batch.append(id)

        if len(text_batch)==batch_size:
            with torch.no_grad():
                tokenized_text = tokenizer(text_batch, max_length=256+32, truncation=True, padding=True, return_tensors="pt")
                tokenized_text = tokenized_text.to(device)
                output = model(**tokenized_text)[0][:,0,:].cpu().numpy()

            for j in range(batch_size):
                EmbedWork_AbstractTitle_Specter2[id_batch[j]]=output[j,:]

            text_batch=list()
            id_batch=list()

    chunk_count+=1
    if chunk_count%50==0:
        pickle.dump(EmbedWork_AbstractTitle_Specter2,open(os.path.join('..','result_alltime',f'Dict_EmbedWork_AbstractTitle_Specter2_Part{part_count}'),'wb'))
        EmbedWork_AbstractTitle_Specter2=dict()
        part_count+=1

with torch.no_grad():
    tokenized_text = tokenizer(text_batch, max_length=256+32, truncation=True, padding=True, return_tensors="pt")
    tokenized_text = tokenized_text.to(device)
    output = model(**tokenized_text)[0][:,0,:].cpu().numpy()

for j in range(len(output)):
    EmbedWork_AbstractTitle_Specter2[id_batch[j]]=output[j,:]
pickle.dump(EmbedWork_AbstractTitle_Specter2,open(os.path.join('..','result_alltime',f'Dict_EmbedWork_AbstractTitle_Specter2_Part{part_count}'),'wb'))