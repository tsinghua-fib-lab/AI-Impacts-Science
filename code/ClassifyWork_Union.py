import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import pickle
from tqdm import tqdm
import numpy as np

with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Title_Raw'),'rb') as f:
    ClassifyWork_Title_Raw=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Abstract_Raw'),'rb') as f:
    ClassifyWork_Abstract_Raw=pickle.load(f)

with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Title_Extend1'),'rb') as f:
    ClassifyWork_Title_Extend1=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Abstract_Extend1'),'rb') as f:
    ClassifyWork_Abstract_Extend1=pickle.load(f)

ClassifyWork_Raw=dict()
for paper_id,title_value in tqdm(ClassifyWork_Title_Raw.items()):
    title_value_exp=np.exp(title_value)

    abstract_value=np.array(ClassifyWork_Abstract_Raw[paper_id])
    abstract_value_exp=np.exp(abstract_value)

    judge_value=0.5*(title_value_exp/np.sum(title_value_exp)+abstract_value_exp/np.sum(abstract_value_exp))
    ClassifyWork_Raw[paper_id]=judge_value[1]

ClassifyWork_Extend1=dict()
for paper_id,title_value in tqdm(ClassifyWork_Title_Extend1.items()):
    title_value_exp=np.exp(title_value)

    abstract_value=np.array(ClassifyWork_Abstract_Extend1[paper_id])
    abstract_value_exp=np.exp(abstract_value)

    judge_value=0.5*(title_value_exp/np.sum(title_value_exp)+abstract_value_exp/np.sum(abstract_value_exp))
    ClassifyWork_Extend1[paper_id]=judge_value[1]


ClassifyWork_UnionValue=dict()
ClassifyWork_Union=dict()
for paper_id,value in tqdm(ClassifyWork_Raw.items()):
    value_extend1=ClassifyWork_Extend1[paper_id]

    judge_value=0.5*(value+value_extend1)
    ClassifyWork_UnionValue[paper_id]=judge_value
    ClassifyWork_Union[paper_id]=int(judge_value>0.5)

pickle.dump(ClassifyWork_UnionValue,open(os.path.join('..','result_alltime','Dict_ClassifyWork_UnionValue'),'wb'))
pickle.dump(ClassifyWork_Union,open(os.path.join('..','result_alltime','Dict_ClassifyWork_Union'),'wb'))