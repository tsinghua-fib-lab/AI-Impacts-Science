import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','openalex','csv-files')

SelectWork_Year_TitleAbstract_Language=list()
works=pd.read_csv(os.path.join(data_dir,'works.csv'),chunksize=100000,usecols=['id','publication_year','title','abstract_inverted_index','language'])

year_start=1980
year_end=2011

os.makedirs(os.path.join('..',f'result_{year_start}-{year_end}'),exist_ok=True)
os.makedirs(os.path.join('..',f'figure_{year_start}-{year_end}'),exist_ok=True)
os.makedirs(os.path.join('..',f'figure_{year_start}-{year_end}','oldfigure'),exist_ok=True)

for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        if pd.isna(line['abstract_inverted_index']):
            continue
        if pd.isna(line['title']):
            continue

        year=line['publication_year']
        if not (year>=year_start and year<=year_end):
            continue

        if line['language']!='en':
            continue

        if len(line['abstract_inverted_index'])<=2:
            continue

        id=int(line['id'].strip('https://openalex.org/W'))
        
        SelectWork_Year_TitleAbstract_Language.append(id)

print(len(SelectWork_Year_TitleAbstract_Language))
pickle.dump(SelectWork_Year_TitleAbstract_Language,open(os.path.join('..','result_alltime',f'List_SelectWork_Year{year_start}-{year_end}_TitleAbstract_Language'),'wb'))