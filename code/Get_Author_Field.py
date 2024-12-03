import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm


with open(os.path.join('..','result_alltime','Dict_Author_Work'),'rb') as f:
    Dict_Author_Work=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_Field'),'rb') as f:
    Dict_Work_Field=pickle.load(f)

Author_Field_Dict=dict()

for author_id,work_ids in tqdm(Dict_Author_Work.items()):
    field_counts=dict()
    for work_id in work_ids:
        try:
            fields=Dict_Work_Field[work_id]
            for field in fields:
                if field not in field_counts:
                    field_counts[field]=0
                field_counts[field]+=1
        except:
            continue

    if len(field_counts)>0:
        fields_counts=sorted(field_counts.items(),key=lambda x:x[1],reverse=True)
        Author_Field_Dict[author_id]=fields_counts[0][0]

print(len(Author_Field_Dict))
pickle.dump(Author_Field_Dict,open(os.path.join('..','result_alltime','Dict_Author_Field'),'wb'))