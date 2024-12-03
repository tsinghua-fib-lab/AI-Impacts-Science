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

with open(os.path.join('..','result_alltime','Dict_Work_Field'),'rb') as f:
    work_field_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_OpenalexFieldID_MAGFieldName'),'rb') as f:
    fieldid_fieldname_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Union'),'rb') as f:
    classify_dict=pickle.load(f)

target_fields=['Biology','Chemistry','Geology','Materials Science','Medicine','Physics']
target_field_ids={}

for target_field_name in target_fields:
    ids=list()
    for field_paper_id,field_name in fieldid_fieldname_dict.items():
        if field_name==target_field_name:
            ids.append(field_paper_id)
    target_field_ids[target_field_name]=set(ids)

target_field_ids['Total']=set().union(*target_field_ids.values())


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

results_field=dict()
for target_field_name,field_ids in target_field_ids.items():
    print(target_field_name)

    field_AI_index=list()
    field_NonAI_index=list()
    for work_id,work_index in tqdm(id_index_map.items()):
        try:
            if len(field_ids.intersection(set(work_field_dict[work_id])))>0:
                if classify_dict[work_id]==1:
                    field_AI_index.append(work_index)
                else:
                    field_NonAI_index.append(work_index)
        except:
            continue

    # args_list = [(field_AI_index, field_NonAI_index, sample_N, seed) for seed in range(sample_time)]
    # with mp.Pool(processes=8) as pool:
    #     sample_results = list(tqdm(pool.map(compute_extent, args_list), total=sample_time))

    sample_results = list()
    for t in tqdm(range(sample_time)):
        sample_results.append(compute_extent((field_AI_index, field_NonAI_index, sample_N, t)))

    AI_extent_mean = [sample_result[0] for sample_result in sample_results]
    NonAI_extent_mean = [sample_result[1] for sample_result in sample_results]
    AI_extent_median = [sample_result[2] for sample_result in sample_results]
    NonAI_extent_median = [sample_result[3] for sample_result in sample_results]
    AI_extent_max = [sample_result[4] for sample_result in sample_results]
    NonAI_extent_max = [sample_result[5] for sample_result in sample_results]

    results_field[target_field_name]=(AI_extent_mean, NonAI_extent_mean, AI_extent_median, NonAI_extent_median, AI_extent_max, NonAI_extent_max)
    
with open(os.path.join('..',f'result_alltime','Dict_Space_WorkField'),'wb') as f:
    pickle.dump(results_field,f)