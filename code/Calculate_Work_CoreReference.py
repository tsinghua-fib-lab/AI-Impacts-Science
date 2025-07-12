import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
from tqdm import tqdm

with open(os.path.join('..','result_alltime','Dict_Work_Reference'),'rb') as f:
    work_reference_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_ReferencedBy'),'rb') as f:
    work_referencedby_dict=pickle.load(f)

Work_CoreReference_Dict=dict()
end_year=2025

for work_id,childlist in tqdm(work_referencedby_dict.items()):
    try:
        fatherlist=work_reference_dict[work_id]
        childfatherset=set()   
        for childid in childlist:
            childfatherset.update(work_reference_dict[childid])

        fatherset=set(fatherlist)
        core_citations=childfatherset&fatherset
        Work_CoreReference_Dict[work_id]=core_citations
    except:
        continue

pickle.dump(Work_CoreReference_Dict,open(os.path.join('..','result_alltime','Dict_Work_CoreReference'),'wb'))