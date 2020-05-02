import os
import random
import shutil

split_ratio = 73

in_dir = 'data/allTrainingReadable'
out_dir = 'data/Original5'
matrix_out_dir = out_dir + '_Matrix'
all_java_filepath = []
all_matrix_filepath = []
for root, dirs, files in os.walk(in_dir):
    for f in files:
        file_path = os.path.join(root, f)
        if file_path.endswith(".java"):
        #print(file_path)
            all_java_filepath.append(file_path)
        if file_path.endswith(".matrix"):
            all_matrix_filepath.append(file_path)

n = len(all_java_filepath) * split_ratio / 100
split_list = random.sample(all_java_filepath, int(n))
split_list2 = list(set(all_java_filepath) - set(split_list))
print(split_list2)

if not os.path.exists(out_dir):
    os.makedirs(out_dir)
if not os.path.exists(matrix_out_dir):
    os.makedirs(matrix_out_dir)

os.makedirs(os.path.join(out_dir, str(split_ratio)))
os.makedirs(os.path.join(out_dir, str(100 - split_ratio)))
out_subdir1 = os.path.join(out_dir, str(split_ratio))
out_subdir2 = os.path.join(out_dir, str(100 - split_ratio))
os.makedirs(os.path.join(matrix_out_dir, str(split_ratio)))
os.makedirs(os.path.join(matrix_out_dir, str(100 - split_ratio)))
matrix_out_subdir1 = os.path.join(matrix_out_dir, str(split_ratio))
matrix_out_subdir2 = os.path.join(matrix_out_dir, str(100 - split_ratio))
for file_path in split_list:
    matrix_file_path = file_path + '.matrix'
    file_name = os.path.split(file_path)[1]
    matrix_file_name = os.path.split(matrix_file_path)[1]
    shutil.copyfile(file_path, os.path.join(out_subdir1, file_name))
    if os.path.exists(matrix_file_path):
        shutil.copyfile(matrix_file_path, os.path.join(matrix_out_subdir1, matrix_file_name))

for file_path in split_list2:
    matrix_file_path = file_path + '.matrix'
    file_name = os.path.split(file_path)[1]
    matrix_file_name = os.path.split(matrix_file_path)[1]
    shutil.copyfile(file_path, os.path.join(out_subdir2, file_name))
    if os.path.exists(matrix_file_path):
        shutil.copyfile(matrix_file_path, os.path.join(matrix_out_subdir2, matrix_file_name))

