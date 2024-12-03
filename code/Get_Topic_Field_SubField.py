import os
import setproctitle
setproctitle.setproctitle('AI Impact@haoqianyue')

import pickle
import pandas as pd
from tqdm import tqdm

data_dir=os.path.join('..','openalex','csv-files')

topics=pd.read_csv(os.path.join(data_dir,'topics.csv'),chunksize=100000)

topicname_topicid_dict=dict()
for chunk in tqdm(topics):
    for _,line in chunk.iterrows():
        topicid=int(line['id'].strip('https://openalex.org/T'))
        topicname=line['display_name']
        topicname_topicid_dict[topicname]=topicid
pickle.dump(topicname_topicid_dict,open(os.path.join('..','result_alltime','Dict_TopicName_TopicID'),'wb'))


# Topic_Field_Dict=dict()
# for chunk in tqdm(topics):
#     for _,line in chunk.iterrows():
#         topicid=int(line['id'].strip('https://openalex.org/T'))
#         fieldid=int(line['field_id'].strip('https://openalex.org/fields/'))
#         Topic_Field_Dict[topicid]=fieldid

# pickle.dump(Topic_Field_Dict,open(os.path.join('..','result_alltime','Dict_Topic_Field'),'wb'))

# Topic_SubField_Dict=dict()
# subfieldname_subfieldid_dict=dict()
# for chunk in tqdm(topics):
#     for _,line in chunk.iterrows():
#         subfieldid=int(line['subfield_id'].strip('https://openalex.org/subfields/'))
#         subfieldname=line['subfield_display_name']
        
#         Topic_SubField_Dict[int(line['id'].strip('https://openalex.org/T'))]=subfieldid
        
#         if subfieldid not in set(subfieldname_subfieldid_dict.values()):
#             if subfieldname not in subfieldname_subfieldid_dict:
#                 subfieldname_subfieldid_dict[subfieldname]=subfieldid
#             else:
#                 subfieldname_subfieldid_dict[subfieldname+'-1']=subfieldid

# pickle.dump(Topic_SubField_Dict,open(os.path.join('..','result_alltime','Dict_Topic_SubField'),'wb'))
# pickle.dump(subfieldname_subfieldid_dict,open(os.path.join('..','result_alltime','Dict_SubFieldName_SubFieldID'),'wb'))