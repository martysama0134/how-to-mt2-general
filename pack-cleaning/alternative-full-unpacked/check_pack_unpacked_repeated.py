import os

index_file_path = "../../bin/pack/Index"
root_pack_path = "./"
log_file_path = "repeated_files.log"  # Define the log file path

def LoadIndex(filepath):
    # Read the content of the Index file
    index_packs = []
    with open(filepath, 'r') as index_file:
        lines = index_file.read().splitlines()
        # Loop through the lines in the Index file
        for line in reversed(lines):  # Reverse the order
            line = line.strip()
            # Skip lines that start with "PACK", "*", or are empty
            if line.startswith("PACK") or line.startswith("*") or not line:
                continue
            # Skip duplicated packs
            if line in index_packs:
                continue
            index_packs.append(line)
    return index_packs

def see_all_files(folder_name, seen_files):
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, folder_name)
            file_size = os.path.getsize(file_path)

            if rel_path in seen_files and seen_files[rel_path]['size'] == file_size:
                with open("repeated_files.log", "a") as log_file:
                    # log_file.write(f"Repeated: Original: {seen_files[rel_path]['folder']}/{rel_path}, Found in: {os.path.join(folder_name, rel_path)}\n")
                    log_file.write(f"{os.path.join(folder_name, rel_path)}\n")
            else:
                seen_files[rel_path] = {'size': file_size, 'folder': folder_name}

if __name__ == "__main__":
    # Delete the log file if it exists
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    pack_list = LoadIndex(index_file_path)
    seen_files = {}
    for folder_name in pack_list:
        see_all_files(os.path.join(root_pack_path, folder_name), seen_files)
