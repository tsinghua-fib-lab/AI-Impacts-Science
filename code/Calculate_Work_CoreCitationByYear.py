import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
from tqdm import tqdm

with open(os.path.join('..','result_alltime','Dict_Work_Year'),'rb') as f:
    work_year_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_CoreReference'),'rb') as f:
    work_core_reference_dict=pickle.load(f)

result_core_cite_year=dict()
end_year=2025

for work_id,core_reference_list in tqdm(work_core_reference_dict.items()):
    try:
        work_year=work_year_dict[work_id]
    except:
        continue

    if work_year > end_year:
        continue

    for core_reference_id in core_reference_list:
        try:
            core_reference_year=work_year_dict[core_reference_id]

            if core_reference_id not in result_core_cite_year:
                result_core_cite_year[core_reference_id]={key: 0 for key in range(end_year+1-work_year)}
            
            result_core_cite_year[core_reference_id][work_year-core_reference_year]+=1
        except:
            continue

with open(os.path.join('..','result_alltime','Dict_Work_CoreCitationByYear'),'wb') as f:
    pickle.dump(result_core_cite_year,f)