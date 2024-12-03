import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','openalex','csv-files')

with open(os.path.join('..','result_alltime','List_SelectWork_Year1980-2024_TitleAbstract_Language'),'rb') as f:
    SelectWork_Year_TitleAbstract_Language=set(pickle.load(f))
with open(os.path.join('..','result_alltime','List_SelectWork_Journal'),'rb') as f:
    SelectWork_Journal=set(pickle.load(f))

works_reference=pd.read_csv(os.path.join(data_dir,'works_referenced_works.csv'),chunksize=100000)

Work_Refenence_Dict=dict()
Work_RefenencedBy_Dict=dict()

for chunk in tqdm(works_reference):
    for _,line in chunk.iterrows():
        work_id=int(line['work_id'].strip('https://openalex.org/W'))
        if work_id in SelectWork_Year_TitleAbstract_Language and work_id in SelectWork_Journal:
            reference_id=int(line['referenced_work_id'].strip('https://openalex.org/W'))
            if reference_id in SelectWork_Year_TitleAbstract_Language and reference_id in SelectWork_Journal:    
                if work_id not in Work_Refenence_Dict:
                    Work_Refenence_Dict[work_id]=[]
                Work_Refenence_Dict[work_id].append(reference_id)

                if reference_id not in Work_RefenencedBy_Dict:
                    Work_RefenencedBy_Dict[reference_id]=[]
                Work_RefenencedBy_Dict[reference_id].append(work_id)

print(len(Work_Refenence_Dict))
print(len(Work_RefenencedBy_Dict))

pickle.dump(Work_Refenence_Dict,open(os.path.join('..','result_alltime','Dict_Work_Refenence'),'wb'))
pickle.dump(Work_RefenencedBy_Dict,open(os.path.join('..','result_alltime','Dict_Work_RefenencedBy'),'wb'))