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

with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Union'),'rb') as f:
    classify_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_Year'),'rb') as f:
    work_year_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_OpenalexFieldID_MAGFieldName'),'rb') as f:
    fieldid_fieldname_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Author_Work'),'rb') as f:
    author_work_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Author_Career'),'rb') as f:
    author_career_dict=pickle.load(f)


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


sample_time = 100

results_author_AIvsNonAI=dict()
results_author_BeforeAIvsAfterAI=dict()
for author_id,author_work_ids in tqdm(author_work_dict.items()):
    try:
        if author_career_dict[author_id][4] == 9999:
            continue
    except:
        continue

    author_AI_index=list()
    author_NonAI_index=list()
    for work_id in author_work_ids:
        try:
            if classify_dict[work_id]==1:
                author_AI_index.append(id_index_map[work_id])
            else:
                author_NonAI_index.append(id_index_map[work_id])
        except:
            continue

    author_BeforeAI_index=list()
    author_AfterAI_index=list()
    for work_id in author_work_ids:
        try:
            if work_year_dict[work_id]<author_career_dict[author_id][4]:
                author_BeforeAI_index.append(id_index_map[work_id])
            else:
                author_AfterAI_index.append(id_index_map[work_id])
        except:
            continue

    if len(author_AI_index) < 10 or len(author_NonAI_index) < 10 or len(author_BeforeAI_index) < 10 or len(author_AfterAI_index) < 10:
        continue

    sample_N_AIvsNonAI=int(min(len(author_AI_index),len(author_NonAI_index))/2)
    sample_results_AIvsNonAI = list()
    for t in range(sample_time):
        sample_results_AIvsNonAI.append(compute_extent((author_AI_index, author_NonAI_index, sample_N_AIvsNonAI, t)))

    AI_extent_mean = [sample_result[0] for sample_result in sample_results_AIvsNonAI]
    NonAI_extent_mean = [sample_result[1] for sample_result in sample_results_AIvsNonAI]
    AI_extent_median = [sample_result[2] for sample_result in sample_results_AIvsNonAI]
    NonAI_extent_median = [sample_result[3] for sample_result in sample_results_AIvsNonAI]
    AI_extent_max = [sample_result[4] for sample_result in sample_results_AIvsNonAI]
    NonAI_extent_max = [sample_result[5] for sample_result in sample_results_AIvsNonAI]

    results_author_AIvsNonAI[author_id]=(AI_extent_mean,NonAI_extent_mean,AI_extent_median,NonAI_extent_median,AI_extent_max,NonAI_extent_max)

    
    sample_N_BeforeAIvsAfterAI=int(min(len(author_BeforeAI_index),len(author_AfterAI_index))/2)
    sample_results_BeforeAIvsAfterAI = list()
    for t in range(sample_time):
        sample_results_BeforeAIvsAfterAI.append(compute_extent((author_BeforeAI_index, author_AfterAI_index, sample_N_BeforeAIvsAfterAI, t)))

    BeforeAI_extent_mean = [sample_result[0] for sample_result in sample_results_BeforeAIvsAfterAI]
    AfterAI_extent_mean = [sample_result[1] for sample_result in sample_results_BeforeAIvsAfterAI]
    BeforeAI_extent_median = [sample_result[2] for sample_result in sample_results_BeforeAIvsAfterAI]
    AfterAI_extent_median = [sample_result[3] for sample_result in sample_results_BeforeAIvsAfterAI]
    BeforeAI_extent_max = [sample_result[4] for sample_result in sample_results_BeforeAIvsAfterAI]
    AfterAI_extent_max = [sample_result[5] for sample_result in sample_results_BeforeAIvsAfterAI]

    results_author_BeforeAIvsAfterAI[author_id]=(BeforeAI_extent_mean,AfterAI_extent_mean,BeforeAI_extent_median,AfterAI_extent_median,BeforeAI_extent_max,AfterAI_extent_max)

with open(os.path.join('..','result_alltime','Dict_Space_Author_AIvsNonAI'),'wb') as f:
    pickle.dump(results_author_AIvsNonAI,f)
with open(os.path.join('..','result_alltime','Dict_Space_Author_BeforeAIvsAfterAI'),'wb') as f:
    pickle.dump(results_author_BeforeAIvsAfterAI,f)