#!/usr/local/bin/python2.7
#### @martysama0134 pack-cleaning scripts ####
import os
root_dir = "."
outp_dir = "d_"
indexfile = "Index"
read_indx = True # read from index, otherwise read all folders alphabetically
indx_newf = False # new index format

def ensure_dir(file_path):
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)

def read_index(newFormat=False):
	dirs = []
	with open(indexfile) as f1:
		f1.readline() # skip first line PACK
		fToggle = False # read only even lines
		for line in f1.readlines():
			# skip odd lines if old format
			if not newFormat:
				fToggle = not fToggle
				if fToggle:
					continue
			# skip duplicates
			line = line.strip()
			if line not in dirs:
				dirs.append(line.strip())
	return dirs

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
		dirs.append(fold_name)
	return dirs

def process_pack(name):
	pack_folder = name #os.path.join(root_dir, name)
	pack_prefix = os.path.join(pack_folder,"")
	for subdir, dirs, files in os.walk(pack_folder):
		for file in files:
			# print(os.path.join(subdir, file))
			real_path = os.path.join(subdir, file)
			virt_path = real_path[len(pack_prefix):]
			outp_path = os.path.join(outp_dir, virt_path)
			# print("%s -> %s" % (real_path, outp_path))
			# make dirs and move
			ensure_dir(outp_path)
			try:
				os.rename(real_path, outp_path)
			except OSError:#FileExistsError:
				raise Exception("file %s already existing or buggy korean name" % real_path)

def process_list(pack_list):
	for pack in pack_list:
		print("processing... %s" % pack)
		process_pack(pack)

if __name__ == "__main__":
	if read_indx:
		process_list(read_index(indx_newf))
	else:
		process_list(get_folder_list())

