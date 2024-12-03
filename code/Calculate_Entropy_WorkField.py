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


def compute_entropy(args):
    local_AI_index,local_NonAI_index,local_sample_N,seed=args
    np.random.seed(seed)
    grid_size = 2

    AI_sample_index = np.random.choice(local_AI_index, min(local_sample_N,len(local_AI_index)), replace=False)
    AI_embeddings = embed_list[AI_sample_index, :10]
    
    AI_min_values = AI_embeddings.min(axis=0)
    AI_max_values = AI_embeddings.max(axis=0)

    AI_steps = (AI_max_values - AI_min_values) / grid_size

    AI_grid_indices = np.floor((AI_embeddings - AI_min_values) / AI_steps).astype(int)
    AI_grid_indices = np.clip(AI_grid_indices, 0, grid_size - 1)

    AI_grid_counts = {}
    for idx in AI_grid_indices:
        AI_grid_tuple = tuple(idx)
        if AI_grid_tuple not in AI_grid_counts:
            AI_grid_counts[AI_grid_tuple] = 0
        AI_grid_counts[AI_grid_tuple] += 1

    AI_total_points = len(AI_embeddings)
    AI_probabilities = np.array(list(AI_grid_counts.values())) / AI_total_points

    AI_entropy = -np.sum(AI_probabilities * np.log(AI_probabilities))


    NonAI_sample_index = np.random.choice(local_NonAI_index, min(local_sample_N,len(local_NonAI_index)), replace=False)
    NonAI_embeddings = embed_list[NonAI_sample_index, :10]
    
    NonAI_min_values = NonAI_embeddings.min(axis=0)
    NonAI_max_values = NonAI_embeddings.max(axis=0)

    NonAI_steps = (NonAI_max_values - NonAI_min_values) / grid_size

    NonAI_grid_indices = np.floor((NonAI_embeddings - NonAI_min_values) / NonAI_steps).astype(int)
    NonAI_grid_indices = np.clip(NonAI_grid_indices, 0, grid_size - 1)

    NonAI_grid_counts = {}
    for idx in NonAI_grid_indices:
        NonAI_grid_tuple = tuple(idx)
        if NonAI_grid_tuple not in NonAI_grid_counts:
            NonAI_grid_counts[NonAI_grid_tuple] = 0
        NonAI_grid_counts[NonAI_grid_tuple] += 1

    NonAI_total_points = len(NonAI_embeddings)
    NonAI_probabilities = np.array(list(NonAI_grid_counts.values())) / NonAI_total_points

    NonAI_entropy = -np.sum(NonAI_probabilities * np.log(NonAI_probabilities))
    
    return AI_entropy, NonAI_entropy


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
        sample_results.append(compute_entropy((field_AI_index, field_NonAI_index, sample_N, t)))

    AI_entropy = [sample_result[0] for sample_result in sample_results]
    NonAI_entropy = [sample_result[1] for sample_result in sample_results]

    results_field[target_field_name]=(AI_entropy, NonAI_entropy)
    
with open(os.path.join('..',f'result_alltime','Dict_Entropy_WorkField'),'wb') as f:
    pickle.dump(results_field,f)