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
with open(os.path.join('..','result_alltime','Dict_Topic_Field'),'rb') as f:
    Topic_Field_Dict=pickle.load(f)

works_topics=pd.read_csv(os.path.join(data_dir,'works_topics.csv'),chunksize=100000)
Work_Field_Dict=dict()

for chunk in tqdm(works_topics):
    for _,line in chunk.iterrows():
        work_id=int(line['work_id'].strip('https://openalex.org/W'))
        if work_id in SelectWork_Year_TitleAbstract_Language and work_id in SelectWork_Journal:
            topic_id=int(line['topic_id'].strip('https://openalex.org/T'))
            # score=float(line['score'])
            topic_field_id=Topic_Field_Dict[topic_id]

            if work_id not in Work_Field_Dict:
                Work_Field_Dict[work_id]=set()
            Work_Field_Dict[work_id].add(topic_field_id)

print(len(Work_Field_Dict))
pickle.dump(Work_Field_Dict,open(os.path.join('..','result_alltime','Dict_Work_Field'),'wb'))