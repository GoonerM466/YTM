import os

def delete_m3u8_files(directory):
    for root, dirs, files in os.walk(directory, topdown=True):
        # Exclude the .github/workflows directory
        if '.github' in dirs and 'workflows' in dirs:
            dirs.remove('workflows')

        for file in files:
            if file.endswith(".m3u8"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

        # Check if there are no more files in the current directory
        if not os.listdir(root):
            os.rmdir(root)
            print(f"Deleted directory: {root}")

if __name__ == "__main__":
    target_directory = input("Enter the target directory path: ")

    if os.path.exists(target_directory):
        delete_m3u8_files(target_directory)
        print("Script executed successfully.")
    else:
        print(f"Error: The specified directory '{target_directory}' does not exist.")
