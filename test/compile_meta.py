import os

def list_files(root_dir, meta_data):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            collect_folder_meta(dirname,dirpath,root_dir)
        for filename in filenames:
            collect_file_meta(filename,dirpath,root_dir)

def collect_folder_meta(dirname,dirpath,root_dir):
    rel_dir_path = os.path.relpath(os.path.join(dirpath, dirname), root_dir)
    print(rel_dir_path)

def collect_file_meta(filename,dirpath,root_dir):
    rel_file_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
    print(rel_file_path)

def split_filename(filename):
    parts = filename.rsplit('.', maxsplit=1)
    if len(parts) > 1:
        file_name, file_extension = parts[0], parts[1]
    else:
        file_name, file_extension = filename, ""
    return file_name, file_extension


test_data = ['new_file', 'new_file.txt', 'new_file_.tar.gz']


for value in test_data:
    filename = value
    file_name, file_extension = split_filename(filename)
    print(f"File name: {file_name}")
    print(f"File extension: {file_extension}")


