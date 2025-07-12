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

works_grant=pd.read_csv(os.path.join(data_dir,'works_grants.csv'),chunksize=100000)

Work_Grant_Dict=dict()

for chunk in tqdm(works_grant):
    for _,line in chunk.iterrows():
        work_id=int(line['work_id'].strip('https://openalex.org/W'))
        if work_id in SelectWork_Year_TitleAbstract_Language and work_id in SelectWork_JournalConference:
            funder_id=int(line['funder_id'].strip('https://openalex.org/F'))  
            if work_id not in Work_Grant_Dict:
                Work_Grant_Dict[work_id]=set()
            Work_Grant_Dict[work_id].add(funder_id)

print(len(Work_Grant_Dict))

pickle.dump(Work_Grant_Dict,open(os.path.join('..','result_alltime','Dict_Work_Grant'),'wb'))