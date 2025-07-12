import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import json
import pickle
import pandas as pd
from tqdm import tqdm

with open(os.path.join('..','result_alltime','List_SelectWork_Year1980-2025_TitleAbstract_Language'),'rb') as f:
    SelectWork_Year_TitleAbstract_Language=set(pickle.load(f))
with open(os.path.join('..','result_alltime','List_SelectWork_JournalConference'),'rb') as f:
    SelectWork_JournalConference=set(pickle.load(f))


translator=str.maketrans('','','!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~\xa0')

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

data_feature_words={'data','dataset'}

data_dir=os.path.join('..','openalex','csv-files')
works=pd.read_csv(os.path.join(data_dir,'works.csv'),chunksize=100000,usecols=['id','title','abstract_inverted_index'])

Work_IsData_Dict=dict()
for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        id=int(line['id'].strip('https://openalex.org/W'))
        if id in SelectWork_Year_TitleAbstract_Language and id in SelectWork_JournalConference:
            title=line['title']
            title_words=set(title.lower().translate(translator).split(' '))
            title_common_words=title_words&data_feature_words

            abstract=restore_abstract(json.loads(line['abstract_inverted_index']))
            abstract_words=set(abstract.lower().translate(translator).split(' '))
            abstract_common_words=abstract_words&data_feature_words

            Work_IsData_Dict[id]=(len(title_common_words),len(abstract_common_words))


with open(os.path.join('..','result_alltime',f'Dict_Work_IsData'),'wb') as f:
    pickle.dump(Work_IsData_Dict,f)