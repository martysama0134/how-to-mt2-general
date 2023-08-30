import os

def delete_empty_folders(directory):
    # Get a list of all items (folders and files) in the current directory
    items = os.listdir(directory)

    for item in items:
        # Create the full path of the item
        item_path = os.path.join(directory, item)

        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Recursively call the function to check and delete empty folders
            delete_empty_folders(item_path)

            # After checking subdirectories, check if the current folder is empty
            if not os.listdir(item_path):
                print(f"Deleting empty folder: {item_path}")
                os.rmdir(item_path)

if __name__ == "__main__":
    current_directory = "."
    delete_empty_folders(current_directory)
