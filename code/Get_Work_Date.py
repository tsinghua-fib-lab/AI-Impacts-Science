import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','openalex','csv-files')

with open(os.path.join('..','result_alltime','List_SelectWork_Year1980-2025_TitleAbstract_Language'),'rb') as f:
    SelectWork_Year_TitleAbstract_Language=set(pickle.load(f))
with open(os.path.join('..','result_alltime','List_SelectWork_JournalConference'),'rb') as f:
    SelectWork_JournalConference=set(pickle.load(f))

works=pd.read_csv(os.path.join(data_dir,'works.csv'),chunksize=100000,usecols=['id','publication_date'])
Work_Date_Dict=dict()

for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        id=int(line['id'].strip('https://openalex.org/W'))
        if id in SelectWork_Year_TitleAbstract_Language and id in SelectWork_JournalConference:
            Work_Date_Dict[id]=line['publication_date']

print(len(Work_Date_Dict))
pickle.dump(Work_Date_Dict,open(os.path.join('..','result_alltime','Dict_Work_Date'),'wb'))