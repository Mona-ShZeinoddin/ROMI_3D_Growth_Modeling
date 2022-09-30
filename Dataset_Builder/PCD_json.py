##Build .json file
# list to store txt files
import json
import os
Dict = {}
Dict["taxonomy_id"] = "00000001"
#Dict["taxonomy_name"] = "stem"
#Dict["taxonomy_name"] = "Pine"
Dict["taxonomy_name"] = "Arabidopsis"
#rootdir = '/home/mona/Documents/My_model_of_growth/PoinTr_data/Experiment_01/data'
#rootdir = '/home/mona/Documents/Plant_modeling_with_LPY/sampling_christophes_arabidopsis/data'
rootdir = '/home/mona/Documents/My_model_of_growth/Arabidopsis_samplr/data'
sub_dir = []
for it in os.scandir(rootdir):
    if it.is_dir():
        sub_dir.append(it.path)

for i in sub_dir:
    data_type = i.rsplit('/', 1)[-1]
    res = []
    # os.walk() returns subdirectories, file from current directory and 
    # And follow next directory from subdirectory list recursively until last directory
    for root, dirs, files in os.walk(i):
        for file in files:
            if file.endswith(".pcd") and file not in ['00.pcd','01.pcd','02.pcd']:
                res.append(file.split('.')[0]) 
    Dict[data_type] = res


json_object = json.dumps([Dict], indent = 4)
  
# Writing to sample.json
with open("/home/mona/Documents/My_model_of_growth/Arabidopsis_samplr/data/Arabidopsis.json", "w") as outfile:
    outfile.write(json_object)