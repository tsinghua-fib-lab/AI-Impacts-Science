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

works_authorships=pd.read_csv(os.path.join(data_dir,'works_authorships.csv'),chunksize=100000,usecols=['work_id','author_position','author_id'])

Work_Author_Dict=dict()
Work_FirstAuthor_Dict=dict()
Work_LastAuthor_Dict=dict()
Author_Work_Dict=dict()

for chunk in tqdm(works_authorships):
    for _,line in chunk.iterrows():
        work_id=int(line['work_id'].strip('https://openalex.org/W'))
        if work_id in SelectWork_Year_TitleAbstract_Language and work_id in SelectWork_Journal:
            author_id=int(line['author_id'].strip('https://openalex.org/A'))
            author_position=line['author_position']
            
            if work_id not in Work_Author_Dict:
                Work_Author_Dict[work_id]=[]
            Work_Author_Dict[work_id].append(author_id)

            if author_position == 'first':
                Work_FirstAuthor_Dict[work_id]=author_id

            if author_position == 'last':
                Work_LastAuthor_Dict[work_id]=author_id

            if author_id not in Author_Work_Dict:
                Author_Work_Dict[author_id]=[]
            Author_Work_Dict[author_id].append(work_id)

print(len(Work_Author_Dict))
print(len(Work_FirstAuthor_Dict))
print(len(Work_LastAuthor_Dict))
print(len(Author_Work_Dict))

pickle.dump(Work_Author_Dict,open(os.path.join('..','result_alltime','Dict_Work_Author'),'wb'))
pickle.dump(Work_FirstAuthor_Dict,open(os.path.join('..','result_alltime','Dict_Work_FirstAuthor'),'wb'))
pickle.dump(Work_LastAuthor_Dict,open(os.path.join('..','result_alltime','Dict_Work_LastAuthor'),'wb'))
pickle.dump(Author_Work_Dict,open(os.path.join('..','result_alltime','Dict_Author_Work'),'wb'))