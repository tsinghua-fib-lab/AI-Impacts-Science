import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
import numpy as np
from tqdm import tqdm
from scipy.spatial.distance import cdist

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


with open(os.path.join('..','result_alltime','Dict_Work_RefenencedBy'),'rb') as f:
    work_referencedby_dict=pickle.load(f)

result_distance=dict()
for work_id,citation_list in tqdm(work_referencedby_dict.items()):
    engage_list=list()
    non_engage_list=list()

    if len(citation_list)>100:
        citation_list=citation_list[:100]

    try:
        engage_sets = [set(work_referencedby_dict[citation_id]) for citation_id in citation_list]
    except:
        continue

    index_list=[id_index_map[citation_id] for citation_id in citation_list]
    embeddings=embed_list[index_list]
    distances = cdist(embeddings, embeddings)

    for x,citation_id_x in enumerate(citation_list):       
        for y in range(x+1,len(citation_list)):
            citation_id_y = citation_list[y]
            if citation_id_x in engage_sets[y] or citation_id_y in engage_sets[x]:
                engage_list.append(distances[x,y])
            else:
                non_engage_list.append(distances[x,y])

    result_distance[work_id] = (len(citation_list), engage_list, non_engage_list)

with open(os.path.join('..','result_alltime','Dict_Work_Distance_Engage_NoEngage_Pairwise'),'wb') as f:
    pickle.dump(result_distance,f)