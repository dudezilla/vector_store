from pathlib import Path
import os
import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))
from file_wrapper import File_Wrapper
from file_collection import File_Collection

def crawl(dir:str):
# Get the current directory path
    current_directory = Path(dir)
    file_collection = File_Collection()

    # Traverse through the directory and its subdirectories
    for path in current_directory.rglob('*'):  # rglob('*') will find all files and directories recursively
        if not path.is_dir():
            file_name = path.name
            dir_name = path.parent
            file_collection.append(File_Wrapper(file_name, dir_name))
            #print(f"Adding: path={path} file={file_name}")
            #print(str(file_collection))
            #print(file_collection.unique_contents())
            serialized = file_collection.serialize("input_metadata.json")
    return file_collection




