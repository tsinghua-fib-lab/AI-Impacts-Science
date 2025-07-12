import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm

with open(os.path.join('..','result_alltime','List_SelectWork_Year1980-2025_TitleAbstract_Language'),'rb') as f:
    SelectWork_Year_TitleAbstract_Language=set(pickle.load(f))
with open(os.path.join('..','result_alltime','List_SelectWork_JournalConference'),'rb') as f:
    SelectWork_JournalConference=set(pickle.load(f))


translator=str.maketrans('','','!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~\xa0')
nano_feature_words={'nano','nanoscale','nano-scale','nanosized','nano-sized'}

data_dir=os.path.join('..','openalex','csv-files')
works=pd.read_csv(os.path.join(data_dir,'works.csv'),chunksize=100000,usecols=['id','title'])

Work_IsNanoSci_Dict=dict()
for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        id=int(line['id'].strip('https://openalex.org/W'))
        if id in SelectWork_Year_TitleAbstract_Language and id in SelectWork_JournalConference:
            title=line['title']
            title_words=set(title.lower().translate(translator).split(' '))

            common_words=title_words&nano_feature_words
            if len(common_words)!=0:
                Work_IsNanoSci_Dict[id]=title
            else:
                Work_IsNanoSci_Dict[id]=None

with open(os.path.join('..','result_alltime',f'Dict_Work_IsNanoSci'),'wb') as f:
    pickle.dump(Work_IsNanoSci_Dict,f)