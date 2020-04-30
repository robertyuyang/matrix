import os
import random
import shutil

split_ratio = 70

in_dir = 'data/allUnreadable'
out_dir = 'data/70-1/'
allfilepath = []
for root, dirs, files in os.walk(in_dir):
    for f in files:
        file_path = os.path.join(root, f)
        if not file_path.endswith(".java"):
            continue
        #print(file_path)
        allfilepath.append(file_path)
n = len(allfilepath) * split_ratio / 100
split_list = random.sample(allfilepath, int(n))
split_list2 = list(set(allfilepath) - set(split_list))
print(split_list2)

if not os.path.exists(out_dir):
    os.makedirs(out_dir)
os.makedirs(os.path.join(out_dir, str(split_ratio)))
os.makedirs(os.path.join(out_dir, str(100 - split_ratio)))
out_subdir1 = os.path.join(out_dir, str(split_ratio))
out_subdir2 = os.path.join(out_dir, str(100 - split_ratio))
for filepath in split_list:
    file_name = os.path.split(filepath)[1]
    shutil.copyfile(file_path, os.path.join(out_subdir1, file_name))
for filepath in split_list2:
    file_name = os.path.split(filepath)[1]
    shutil.copyfile(file_path, os.path.join(out_subdir2, file_name))

