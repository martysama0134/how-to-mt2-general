#!/usr/local/bin/python2.7
#### @martysama0134 pack-cleaning scripts ####
import os
import shutil

def ensure_dir(file_path):
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)

def walklevel(some_dir, level=1):
	some_dir = some_dir.rstrip(os.path.sep)
	assert os.path.isdir(some_dir)
	num_sep = some_dir.count(os.path.sep)
	for root, dirs, files in os.walk(some_dir):
		yield root, dirs, files
		num_sep_this = root.count(os.path.sep)
		if num_sep + level <= num_sep_this:
			del dirs[:]

root_dir = os.path.join("d_", "")
outp_dir = "newpack"

def process_dirs(folder=root_dir, pack_prefix=""):
	folder_prefix = os.path.join(folder,"")
	dir_list = [i[0] for i in walklevel(folder)]
	for dir in dir_list:
		virt_path = dir[len(root_dir):]
		fold_name = dir[len(folder_prefix):]
		pack_name = pack_prefix+fold_name#os.path.basename(dir)
		if any([i in fold_name for i in ("guild_", "map_", "metin2_12zi_")]):
			pack_name = pack_prefix+"maps"
		outp_path = os.path.join(outp_dir, pack_name, virt_path)
		# print(virt_path)
		# skip base
		if fold_name=="":
			continue
		# recursing yw
		if fold_name=="ymir work":
			process_dirs(dir, "yw_")
			continue
		# print("%s -> %s" % (dir, outp_path))
		ensure_dir(outp_path)
		shutil.move(dir, outp_path)

if __name__ == "__main__":
	process_dirs()

