import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
from tqdm import tqdm

import itertools

with open(os.path.join('..','result_alltime','Dict_Work_RefenencedBy'),'rb') as f:
    work_referencedby_dict=pickle.load(f)

result_engage=dict()
for work_id,citation_list in tqdm(work_referencedby_dict.items()):
    n_citation=len(citation_list)
    n_engage=0

    citation_set=set(citation_list)
    for citation_id in citation_list:
        try:
            engage_set=set(work_referencedby_dict[citation_id])
        except:
            continue

        n_engage+=len(citation_set&engage_set)          

    result_engage[work_id]=(n_citation,n_engage)

with open(os.path.join('..','result_alltime','Dict_Work_Engage'),'wb') as f:
    pickle.dump(result_engage,f)
