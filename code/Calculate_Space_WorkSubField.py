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

with open(os.path.join('..','result_alltime','Dict_Work_SubField'),'rb') as f:
    work_subfield_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Union'),'rb') as f:
    classify_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_OpenalexSubFieldName_OpenalexSubFieldID'),'rb') as f:
    target_subfield_ids=pickle.load(f)

def compute_extent(args):
    local_AI_index,local_NonAI_index,local_sample_N,seed=args
    np.random.seed(seed)

    AI_sample_index = np.random.choice(local_AI_index, min(local_sample_N,len(local_AI_index)), replace=False)
    AI_embeddings = embed_list[AI_sample_index, :]
    
    AI_embeddings_center = np.mean(AI_embeddings, axis=0)
    AI_extent = np.linalg.norm(AI_embeddings - AI_embeddings_center, axis=1)
    AI_extent_mean = np.mean(AI_extent)
    AI_extent_median = np.median(AI_extent)
    AI_extent_max = np.max(AI_extent)

    
    NonAI_sample_index = np.random.choice(local_NonAI_index, min(local_sample_N,len(local_AI_index)), replace=False)
    NonAI_embeddings = embed_list[NonAI_sample_index, :]
    
    NonAI_embeddings_center = np.mean(NonAI_embeddings, axis=0)
    NonAI_extent = np.linalg.norm(NonAI_embeddings - NonAI_embeddings_center, axis=1)
    NonAI_extent_mean = np.mean(NonAI_extent)
    NonAI_extent_median = np.median(NonAI_extent)
    NonAI_extent_max = np.max(NonAI_extent)
    
    return AI_extent_mean, NonAI_extent_mean, AI_extent_median, NonAI_extent_median, AI_extent_max, NonAI_extent_max


sample_time = 1000
sample_N = 1000

results_subfield=dict()
for target_subfield_name,subfield_id in target_subfield_ids.items():
    print(target_subfield_name)

    subfield_AI_index=list()
    subfield_NonAI_index=list()
    for work_id,work_index in tqdm(id_index_map.items()):
        try:
            if subfield_id in set(work_subfield_dict[work_id]):
                if classify_dict[work_id]==1:
                    subfield_AI_index.append(work_index)
                else:
                    subfield_NonAI_index.append(work_index)
        except:
            continue

    min_len=min(len(subfield_AI_index),len(subfield_NonAI_index))

    if min_len<10:
        results_subfield[target_subfield_name]=None
        continue

    sample_results = list()
    for t in tqdm(range(sample_time)):
        sample_results.append(compute_extent((subfield_AI_index, subfield_NonAI_index, min(sample_N,min_len), t)))

    AI_extent_mean = [sample_result[0] for sample_result in sample_results]
    NonAI_extent_mean = [sample_result[1] for sample_result in sample_results]
    AI_extent_median = [sample_result[2] for sample_result in sample_results]
    NonAI_extent_median = [sample_result[3] for sample_result in sample_results]
    AI_extent_max = [sample_result[4] for sample_result in sample_results]
    NonAI_extent_max = [sample_result[5] for sample_result in sample_results]

    results_subfield[target_subfield_name]=(AI_extent_mean, NonAI_extent_mean, AI_extent_median, NonAI_extent_median, AI_extent_max, NonAI_extent_max)
    
with open(os.path.join('..',f'result_alltime','Dict_Space_WorkSubField'),'wb') as f:
    pickle.dump(results_subfield,f)