import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm


with open(os.path.join('..','result_alltime','Dict_Author_Work'),'rb') as f:
    Dict_Author_Work=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_FirstAuthor'),'rb') as f:
    Dict_Work_FirstAuthor=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_LastAuthor'),'rb') as f:
    Dict_Work_LastAuthor=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_Year'),'rb') as f:
    Dict_Work_Year=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Union'),'rb') as f:
    Dict_Work_Classify=pickle.load(f)

Author_Career_Dict=dict()

for author_id,work_ids in tqdm(Dict_Author_Work.items()):
    author_career=[len(work_ids),9999,9999,9999,9999,0,-1,-1]#[paper数量，第一次发paper，第一次第一作者，第一次最后作者，第一次搞AI，最后一次发paper，第一次第一作者是否AI，第一次最后作者是否AI]
    for work_id in work_ids:
        try:
            year=Dict_Work_Year[work_id]
            classify=Dict_Work_Classify[work_id]
            
            first_author=Dict_Work_FirstAuthor[work_id]
            last_author=Dict_Work_LastAuthor[work_id]
        except:
            continue

        if year<author_career[1]:
            author_career[1]=year
        if year>author_career[5]:
            author_career[5]=year
        if classify==1 and year<author_career[4]:
            author_career[4]=year

        if author_id==first_author:
            if year<author_career[2]:
                author_career[2]=year
                author_career[6]=classify

        if author_id==last_author:
            if year<author_career[3]:
                author_career[3]=year
                author_career[7]=classify

    Author_Career_Dict[author_id]=author_career

print(len(Author_Career_Dict))
pickle.dump(Author_Career_Dict,open(os.path.join('..','result_alltime','Dict_Author_Career'),'wb'))