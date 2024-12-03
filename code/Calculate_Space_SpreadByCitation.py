import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
import numpy as np
from tqdm import tqdm


index_list=list()
embed_list=list()

for file in tqdm([file for file in os.listdir(os.path.join('..','result_alltime')) if 'EmbedWork' in file]):
    with open(os.path.join('..','result_alltime',file),'rb') as f:
        data=pickle.load(f)
    index_list.append(np.array(list(data.keys())))
    embed_list.append(np.array(list(data.values())))

index_list=np.hstack(index_list)
embed_list=np.vstack(embed_list)

id_index_map=dict()
for i in range(len(index_list)):
    id_index_map[index_list[i]]=i


with open(os.path.join('..','result_alltime','Dict_Work_Year'),'rb') as f:
    work_year_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_RefenencedBy'),'rb') as f:
    work_referencedby_dict=pickle.load(f)


space_citation=dict()
for work_id,citation_list in tqdm(work_referencedby_dict.items()):
    try:
        work_year=work_year_dict[work_id]
    except:
        continue

    citation_year_dict=dict()
    for citation_id in citation_list:
        try:
            citation_year=work_year_dict[citation_id]
            if citation_year>=work_year:
                citation_year_dict[citation_id]=citation_year
        except:
            continue

    citation_sorted = sorted(citation_year_dict, key=citation_year_dict.get)

    index_list=[id_index_map[citation_id] for citation_id in citation_sorted]
    embeddings=embed_list[index_list]
    embeddings_center = embed_list[id_index_map[work_id]]
    
    extent_citation=[]
    max_extent=0
    for i in range(len(embeddings)):
        extent_new = np.linalg.norm(embeddings[i] - embeddings_center)
        if extent_new > max_extent:
            max_extent = extent_new
        extent_citation.append(max_extent)

    space_citation[work_id]=extent_citation

with open(os.path.join('..','result_alltime','Dict_Space_SpreadByCitation'),'wb') as f:
    pickle.dump(space_citation,f)