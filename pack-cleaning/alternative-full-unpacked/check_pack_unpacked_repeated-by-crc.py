import os
import zlib  # For CRC32 calculation

index_file_path = "../../bin/pack/Index"
root_pack_path = "./"
log_file_path = "repeated_files.log"  # Define the log file path

def calculate_crc32(file_path):
    crc32 = 0
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read the file in chunks to conserve memory
            if not data:
                break
            crc32 = zlib.crc32(data, crc32)
    return crc32 & 0xFFFFFFFF  # Ensure the CRC32 is a 32-bit unsigned integer

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
            crc32 = calculate_crc32(file_path)

            if rel_path in seen_files and seen_files[rel_path]['crc32'] == crc32:
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"{os.path.join(folder_name, rel_path)}\n")
            else:
                seen_files[rel_path] = {'crc32': crc32, 'folder': folder_name}

if __name__ == "__main__":
    # Delete the log file if it exists
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    pack_list = LoadIndex(index_file_path)
    seen_files = {}
    for folder_name in pack_list:
        see_all_files(os.path.join(root_pack_path, folder_name), seen_files)
