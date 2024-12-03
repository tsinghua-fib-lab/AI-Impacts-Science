import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','openalex','csv-files')
authors=pd.read_csv(os.path.join(data_dir,'authors.csv'),chunksize=100000,usecols=['id','display_name'])

Author_Name_Dict=dict()
for chunk in tqdm(authors):
    for _,line in chunk.iterrows():
        try:
            author_id=int(line['id'].strip('https://openalex.org/A'))
            author_name=line['display_name']

            if all(char.isascii() for char in author_name):
                Author_Name_Dict[author_id] = author_name
        except:
            continue

print(len(Author_Name_Dict))
pickle.dump(Author_Name_Dict,open(os.path.join('..','result_alltime','Dict_Author_Name'),'wb'))