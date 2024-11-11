import os
import json
from file_wrapper import File_Wrapper


class File_Collection:
    """
    A collection class for managing and organizing a set of File_Wrapper instances.

    Attributes:
        files (dict): A dictionary to store files where keys are full file paths and values are File_Wrapper instances.
        unique (dict): A dictionary to store unique files based on their checksum where keys are checksums and values are lists of File_Wrapper instances.

    Methods:
        __getitem__(key): Get the File_Wrapper instance associated with the given key from the files dictionary.
        __setitem__(key, value): Set a File_Wrapper instance into the files dictionary with the given key.
        append(file_wrapper): Add a File_Wrapper instance to the collection, updating both files and unique dictionaries.
        unique_contents(): Retrieve a dictionary of unique content based on file checksums.
        next_file(): Generator that yields File_Wrapper instances sorted by timestamp in descending order.
        __str__(): Returns a string representation of the collection with details of each file.
    """

    def __init__(self):
        """Initialize the File_Collection with empty files and unique dictionaries."""
        self.files = {}
        self.unique = {}


    def __getitem__(self, key):
        """Return the File_Wrapper instance associated with the given key."""
        return self.files[key]

    def __setitem__(self, key, value):
        """
        Set a File_Wrapper instance into the files dictionary with the specified key.

        Raises:
            ValueError: If the value is not an instance of File_Wrapper.
        """
        if not isinstance(value, File_Wrapper):
            raise ValueError("Value must be a File_Wrapper instance")
        self.files[key] = value

    def append(self, file_wrapper):
        """
        Add a File_Wrapper instance to the collection.

        Updates both the files dictionary with the full file path as the key
        and the unique dictionary with the file's checksum as the key.

        Raises:
            ValueError: If the file_wrapper is not an instance of File_Wrapper.
        """
        if not isinstance(file_wrapper, File_Wrapper):
            raise ValueError("Value must be a File_Wrapper instance")

        full_name = str(os.path.join(file_wrapper.path, file_wrapper.file_name))
        self.files[full_name] = file_wrapper

        chksum = file_wrapper.checksum
        if chksum in self.unique:
            self.unique[chksum].append(file_wrapper)
        else:
            self.unique[chksum] = [file_wrapper]

    def unique_contents(self):
        """
        Retrieve a dictionary of unique content based on file checksums.

        Returns:
            dict: A dictionary where each key is a checksum and the value is a dictionary containing a list of paths.
        """
        unique_files = self.unique
        result = {}
        for key, value in unique_files.items():
            sub = []
            for v in value:
                sub.append(v.name_with_path())
            result[key] = {'paths': sub}
        return result

    def next_file(self):
        """
        Generator that yields File_Wrapper instances sorted by timestamp in descending order.
        
        Yields:
            File_Wrapper: Next file in the sorted order by timestamp.
        """
        for file in sorted(self.files.values(), key=lambda x: x._timestamp, reverse=True):
            yield file


    def __iter__(self):
        # Initialize the iterator with the sorted files
        self._iterator = iter(sorted(self.files.values(), key=lambda x: x._timestamp, reverse=True))
        return self

    def __next__(self):
        # Attempt to get the next item from the iterator
        try:
            return next(self._iterator)
        except StopIteration:
            # If there are no more elements, raise StopIteration
            raise StopIteration

    def __str__(self):
        """
        Return a string representation of the collection where duplicates are grouped by hashes.

        Returns:
            str: 
        """
        result = ""
        for file in self.files.values():
            result += f"\t{file.file_name}\n\tpath:{file.path}\n\ttimestamp:{file.observed_at()}\n"
        return result

    def to_dict(self):
        """Convert instance to a dictionary representation."""
        data = {
            'files': {path: file_wrapper.to_dict() for path, file_wrapper in self.files.items()},
            'unique': {checksum: [file_wrapper.to_dict() for file_wrapper in wrappers]
                       for checksum, wrappers in self.unique.items()}
        }
        return data

    @classmethod
    def from_dict(cls, data):
        """Create an instance from a dictionary representation."""
        manager = cls()
        manager.files = {path: File_Wrapper.from_dict(file_data) for path, file_data in data['files'].items()}
        manager.unique = {checksum: [File_Wrapper.from_dict(file_data) for file_data in wrapper_data]
                          for checksum, wrapper_data in data['unique'].items()}
        return manager

    def serialize(self, file_path):
        """Serialize the container to JSON and write to a file."""
        json_data = json.dumps(self.to_dict(), sort_keys=True, indent=4)
        with open(file_path, 'w') as f:
            f.write(json_data)

    @classmethod
    def deserialize(cls, file_path):
        """Deserialize a JSON file into a container instance."""
        with open(file_path, 'r') as f:
            data = json.load(f)
            return cls.from_dict(data)
        

    def __eq__(self, other):
        if not isinstance(other, File_Collection):
            return False
        return self._dicts_equal(self.files, other.files) and self._dicts_equal(self.unique, other.unique)

    def _dicts_equal(self, d1, d2):
        if d1.keys() != d2.keys():
            return False
        for key in d1:
            if d1[key] != d2[key]:
                return False
        return True
    
    def visit_unique_keys(self, callback):
        """
        Visit each unique key in the unique dictionary and perform a callback.

        Args:
            callback (function): A function that takes a key and the associated list of File_Wrapper instances.
        """
        for hash, file_locations in self.unique.items():
            callback(hash,file_locations)

    def len_unique(self):
        return len(self.unique)
    
    def len_files(self):
        return len(self.files)