import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
from tqdm import tqdm

with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Union'),'rb') as f:
    classify_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_Field'),'rb') as f:
    work_field_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_Year'),'rb') as f:
    work_year_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_OpenalexFieldID_MAGFieldName'),'rb') as f:
    fieldid_fieldname_dict=pickle.load(f)

with open(os.path.join('..','result_alltime','Dict_Work_RefenencedBy'),'rb') as f:
    work_referencedby_dict=pickle.load(f)

result_cite_year=dict()
end_year=2024

for work_id,citation_list in tqdm(work_referencedby_dict.items()):
    try:
        work_year=work_year_dict[work_id]
    except:
        continue

    if work_year > end_year:
        continue

    result_cite_year[work_id]={key: 0 for key in range(end_year+1-work_year)}

    for citation_id in citation_list:
        try:
            citation_year=work_year_dict[citation_id]
            result_cite_year[work_id][citation_year-work_year]+=1
        except:
            continue

with open(os.path.join('..','result_alltime','Dict_Work_CitationByYear'),'wb') as f:
    pickle.dump(result_cite_year,f)