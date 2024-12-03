import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','openalex','csv-files')

SelectSource_Journal=list()
sources=pd.read_csv(os.path.join(data_dir,'sources.csv'))

for _,line in tqdm(sources.iterrows()):
    count=line['works_count']
    if pd.isna(line['issn']):
        continue
    id=int(line['id'].strip('https://openalex.org/S'))
    
    SelectSource_Journal.append(id)

print(len(SelectSource_Journal))
pickle.dump(SelectSource_Journal,open(os.path.join('..','result_alltime','List_SelectSource_Journal'),'wb'))


SelectSource_Journal=set(SelectSource_Journal)
SelectWork_Journal=list()
works=pd.read_csv(os.path.join(data_dir,'works_primary_locations.csv'),chunksize=100000,usecols=['work_id','source_id'])

for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        work_id=int(line['work_id'].strip('https://openalex.org/W'))
        source_id=int(line['source_id'].strip('https://openalex.org/S'))
        if source_id not in SelectSource_Journal:
            continue

        SelectWork_Journal.append(work_id)

print(len(SelectWork_Journal))
pickle.dump(SelectWork_Journal,open(os.path.join('..','result_alltime','List_SelectWork_Journal'),'wb'))