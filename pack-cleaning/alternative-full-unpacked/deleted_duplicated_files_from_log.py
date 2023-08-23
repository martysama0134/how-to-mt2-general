import os

log_file_path1 = "duplicated_files.log"
log_file_path2 = "repeated_files.log"
delete_log = False
delete_file = False
print_filename = True

def format_bytes(nBytes):
    # Formats bytes with periods as thousands separators
    return "{:,} bytes".format(nBytes).replace(",", ".")

def delete_files_from_log(log_file_path):
    # Check if the log file exists
    if not os.path.exists(log_file_path):
        print(f"The log file '{log_file_path}' does not exist.")
        return

    total_deleted_bytes = 0

    # Read the file paths from the log
    with open(log_file_path, 'r') as log_file:
        file_paths = log_file.read().splitlines()

    # Delete each file listed in the log
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                file_size = os.path.getsize(file_path)
                if delete_file:
                    os.remove(file_path)
                total_deleted_bytes += file_size
                if print_filename:
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {file_path}, Error: {str(e)}")
        else:
            print(f"File not found: {file_path}")

    # Remove the log file after processing
    if delete_log:
        os.remove(log_file_path)
        if print_filename:
            print(f"Log file '{log_file_path}' has been removed.")
    print(f"Total deleted bytes: {format_bytes(total_deleted_bytes)}")

if __name__ == "__main__":
    delete_files_from_log(log_file_path1)
    delete_files_from_log(log_file_path2)
