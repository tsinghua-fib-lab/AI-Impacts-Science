import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','openalex','csv-files')
authors=pd.read_csv(os.path.join(data_dir,'authors.csv'),chunksize=100000,usecols=['id','last_known_institutions'])

Author_Institution_Dict=dict()
for chunk in tqdm(authors):
    for _,line in chunk.iterrows():
        try:
            author_id=int(line['id'].strip('https://openalex.org/A'))

            if line['last_known_institutions'] is not None:
                institution_id=int(line['last_known_institutions'].strip('https://openalex.org/I'))
                Author_Institution_Dict[author_id] = institution_id
        except:
            continue

print(len(Author_Institution_Dict))
pickle.dump(Author_Institution_Dict,open(os.path.join('..','result_alltime','Dict_Author_Institution'),'wb'))