
import os
from file_wrapper import File_Wrapper

class File_Collection:
    def __init__(self):
        self.files = {}
        self.unique = {}

    def __getitem__(self, key):
        return self.files[key]

    def __setitem__(self, key, value):
        if not isinstance(value, File_Wrapper):
            raise ValueError("Value must be a File_Wrapper instance")
        self.files[key] = value

    def append(self, file_wrapper):
        if not isinstance(file_wrapper, File_Wrapper):
            raise ValueError("Value must be a File_Wrapper instance")
        full_name= os.path.join(file_wrapper.path, file_wrapper.file_name)
        self.files[full_name] = file_wrapper
        chksum = file_wrapper.checksum
        if chksum in self.unique.keys():
            self.unique[chksum].append(file_wrapper)
        else:
            self.unique[chksum] = [file_wrapper]



    def unique_contents(self):
        unique_files = self.unique
        result = {}
        for key,value in unique_files.items():
            sub = []
            for v in value:
                sub.append(v.name_with_path())
            result[key]={'paths':sub}
        return result


    def next_file(self):
        #for file in sorted(self.files.values(), key=lambda x: x._timestamp):
        for file in sorted(self.files.values(), key=lambda x: x._timestamp, reverse=True):
            yield file

    def __str__(self):
        result = ""
        for file in self.files.values():
            result += f"\t{file.file_name}\n\tpath:{file.path}\n\ttimestamp:{file.observed_at()}\n"
        return result