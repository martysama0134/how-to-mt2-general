#!/usr/local/bin/python2.7
#### @martysama0134 pack-cleaning scripts ####
import os

pack_dir = "newpack" # "." otherwise
outp_idx = "newIndex"
indx_newf = False # new index format

def walklevel(some_dir, level=1):
	some_dir = some_dir.rstrip(os.path.sep)
	assert os.path.isdir(some_dir)
	num_sep = some_dir.count(os.path.sep)
	for root, dirs, files in os.walk(some_dir):
		yield root, dirs, files
		num_sep_this = root.count(os.path.sep)
		if num_sep + level <= num_sep_this:
			del dirs[:]

def get_folder_list(folder="."):
	dir_list = [i[0] for i in walklevel(folder)]
	folder_prefix = os.path.join(folder,"")
	dirs = []
	for dir in dir_list:
		fold_name = dir[len(folder_prefix):]
		if fold_name=="":
			continue
		if fold_name=="d_": # skip
			continue
		dirs.append(fold_name)
	return dirs

def process_list(pack_list):
	with open(outp_idx, "w") as f1:
		f1.write("PACK\n")
		if indx_newf:
			f1.write("\n".join(pack_list)) #new offy format
		else:
			f1.write("".join([("*\n%s\n" % i) for i in pack_list])) #old format

if __name__ == "__main__":
	process_list(get_folder_list(pack_dir))

