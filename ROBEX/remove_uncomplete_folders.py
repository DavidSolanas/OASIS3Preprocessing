import os

def is_folder_empty(folder_path):
    # Check if a folder is empty (contains no files or subfolders)
    print(folder_path, len(os.listdir(folder_path)))
    return len(os.listdir(folder_path)) == 0

def remove_empty_subfolders(root_folder):
    for dirname in os.listdir(root_folder):
        current_folder = os.path.join(root_folder, dirname)
        t1w_folder = os.path.join(current_folder, "T1w")
        t2w_folder = os.path.join(current_folder, "T2w")

        # Check if both T1w and T2w subfolders are empty
        if is_folder_empty(t1w_folder) or is_folder_empty(t2w_folder):
            try:
                # Remove the subfolder if empty
                #os.rmdir(current_folder)
                print(f"Removed empty folder: {current_folder}")
            except OSError as e:
                print(f"Error while removing folder: {current_folder}, Error: {e}")

if __name__ == "__main__":
    root_folder_path = "/home/david/TFM/dataset/OASIS3_processed/OASIS3_processed"
    remove_empty_subfolders(root_folder_path)