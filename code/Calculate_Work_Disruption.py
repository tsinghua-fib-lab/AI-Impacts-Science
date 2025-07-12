import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
from tqdm import tqdm

with open(os.path.join('..','result_alltime','Dict_Work_Reference'),'rb') as f:
    work_reference_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_ReferencedBy'),'rb') as f:
    work_referencedby_dict=pickle.load(f)

Work_Disruption_Dict=dict()
end_year=2025

for work_id,fatherlist in tqdm(work_reference_dict.items()):
    try:
        childset=set(work_referencedby_dict[work_id])

        fatherchildset=set()
        for fatherid in fatherlist:
            fatherchildset.update(work_referencedby_dict[fatherid])
        fatherchildset.remove(work_id)

        set_j=childset.intersection(fatherchildset)
        n_j=len(set_j)
        n_i=len(childset) - n_j
        n_k=len(fatherchildset) - n_j
    
        disruption = (n_i - n_j) / (n_i + n_j + n_k)
        Work_Disruption_Dict[work_id] = disruption

    except:
        continue

pickle.dump(Work_Disruption_Dict,open(os.path.join('..','result_alltime','Dict_Work_Disruption'),'wb'))