import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
from tqdm import tqdm

with open(os.path.join('..','result_alltime','Dict_Work_Year'),'rb') as f:
    work_year=pickle.load(f)   
with open(os.path.join('..','result_alltime','Dict_Work_Author'),'rb') as f:
    work_author=pickle.load(f) 
with open(os.path.join('..','result_alltime','Dict_Work_LastAuthor'),'rb') as f:
    work_lastauthor=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Author_Career'),'rb') as f:
    author_career=pickle.load(f)

result_team_last=dict()
for work_id,authors in tqdm(work_author.items()):
    try:
        year=work_year[work_id]
        lastauthor=work_lastauthor[work_id]
    except:
        continue

    leading_num=1
    supporting_num=0
    for author in authors:
        if author == lastauthor:
            continue

        try:
            role=author_career[author]
        except:
            supporting_num+=1
            continue

        if year<role[3]:
            supporting_num+=1
        else:
            leading_num+=1
                                
    result_team_last[work_id]=(supporting_num,leading_num)

with open(os.path.join('..','result_alltime','Dict_Work_TeamLast'),'wb') as f:
    pickle.dump(result_team_last,f)