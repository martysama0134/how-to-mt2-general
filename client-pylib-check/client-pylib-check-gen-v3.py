# martysama0134 & ChatGPT - 2023
import json
import os
import zlib

WORKING_DIR = r"C:\M2Clients\M2Client-v22"
PYLIB_FOLDER = ["lib"]#, "./miles"]
OUTPUT_FILENAME_CPP = "UserInterface-PyLibFilesTable-v3.cpp"
OUTPUT_FILENAME_JSON = "pylibfilestable.json"

WORKING_DIR = r"C:\Users\marty\Documents\M2Clients\S3llMetin2-v22.5.7.0"

# Function to calculate CRC32 checksum
def calculate_crc32(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        crc32_hash = zlib.crc32(data)
        return crc32_hash

if __name__ == "__main__":
    # Initialize an empty list to store file information
    file_info = []

    for folder_path in PYLIB_FOLDER:
        # Get a list of files in the folder_path directory
        file_list = os.listdir(os.path.join(WORKING_DIR, folder_path))

        # Iterate through the files and gather information
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            full_file_path = os.path.join(WORKING_DIR, file_path)
            if os.path.isfile(full_file_path):
                file_size = os.path.getsize(full_file_path)
                crc32 = calculate_crc32(full_file_path)
                file_info.append({
                    "fileName": file_path.replace("\\", "/"),
                    "stSize": file_size,
                    "dwCRC32": crc32
                })

    # Create and write the C++ style table to a file
    with open(OUTPUT_FILENAME_CPP, "w") as output_file:
        output_file.write("std::vector<PyLibFiles_t> PyLibFilesTable = {\n")
        for data in file_info:
            file_name = data["fileName"]
            file_size = data["stSize"]
            crc32 = data["dwCRC32"]
            output_file.write(f'    {{ "{file_name}", {file_size}, {crc32} }},\n')
        output_file.write("};\n")

    print(f"{OUTPUT_FILENAME_CPP} file has been created.")

    # Create and write the C++ style table to a file
    with open(OUTPUT_FILENAME_JSON, "w") as output_file:
        json.dump(file_info, output_file, indent=4)

    print(f"{OUTPUT_FILENAME_JSON} file has been created.")
