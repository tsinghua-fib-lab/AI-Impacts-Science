import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import os
import json
import pickle
import pandas as pd
from tqdm import tqdm

with open(os.path.join('..','result_alltime','Dict_ClassifyWork_Union'),'rb') as f:
    classify_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_Field'),'rb') as f:
    work_field_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_Work_Year'),'rb') as f:
    work_year_dict=pickle.load(f)
with open(os.path.join('..','result_alltime','Dict_OpenalexFieldID_MAGFieldName'),'rb') as f:
    fieldid_fieldname_dict=pickle.load(f)


target_fields=['Biology','Chemistry','Geology','Materials Science','Medicine','Physics']
start_year=1980
end_year=2025

phrase_field_year=dict()
for year in range(start_year,end_year+1):
    phrase_field_year[year]=[0,0,dict(),dict()]#number of non-AI papers,number of AI papers,non-AI count abstract,AI count abstract


translator=str.maketrans('','','!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~\xa0')

def restore_abstract(indexed_abstract):
    # Create a list with the length equal to the number of total words in the abstract
    total_length = max(max(indices) for indices in indexed_abstract.values()) + 1
    restored_abstract = [''] * total_length

    # Fill in the words at the correct positions
    for word, positions in indexed_abstract.items():
        for position in positions:
            restored_abstract[position] = word

    # Join the words into a single string
    return ' '.join(restored_abstract)


data_dir=os.path.join('..','openalex','csv-files')
works=pd.read_csv(os.path.join(data_dir,'works.csv'),chunksize=100000,usecols=['id','title','abstract_inverted_index'])

phrase_len=3
for chunk in tqdm(works):
    for _,line in chunk.iterrows():
        id=int(line['id'].strip('https://openalex.org/W'))
        try:
            paper_classify = classify_dict[id]
            field_ids=work_field_dict[id]
            year=work_year_dict[id]
        except:
            continue

        abstract=restore_abstract(json.loads(line['abstract_inverted_index'])).lower().translate(translator).split(' ')
        phrases=set([' '.join(abstract[i:i+phrase_len]) for i in range(len(abstract)-phrase_len+1)])

        for field_id in field_ids:
            field_name=fieldid_fieldname_dict[field_id]
            if field_name in target_fields:
                temp=phrase_field_year[year]
                if not paper_classify:
                    temp[0]+=1
                    for phrase in phrases:
                        temp[2][phrase] = temp[2].get(phrase, 0) + 1
                else:
                    temp[1]+=1
                    for phrase in phrases:
                        temp[3][phrase] = temp[3].get(phrase, 0) + 1

                break

with open(os.path.join('..','result_alltime',f'Dict_Work_PhraseLen{phrase_len}ByYear_allFields'),'wb') as f:
    pickle.dump(phrase_field_year,f)