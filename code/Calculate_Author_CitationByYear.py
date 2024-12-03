import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
from tqdm import tqdm

with open(os.path.join('..','result_alltime','Dict_Author_Work'),'rb') as f:
    author_work_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_Year'),'rb') as f:
    work_year_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_CitationByYear'),'rb') as f:
    work_cite_year_dict=pickle.load(f)

result_author_cite_year=dict()
end_year=2024

for author_id,work_list in tqdm(author_work_dict.items()):
    if author_id not in result_author_cite_year:
        result_author_cite_year[author_id]=dict([(i,0) for i in range(1980,end_year+1)])

    for work_id in work_list:
        try:
            work_year=work_year_dict[work_id]
            work_cite_year=work_cite_year_dict[work_id]
        except:
            continue

        if work_year > end_year:
            continue

        for year,citation in work_cite_year.items():
            result_author_cite_year[author_id][work_year+year]+=citation

with open(os.path.join('..','result_alltime','Dict_Author_CitationByYear'),'wb') as f:
    pickle.dump(result_author_cite_year,f)