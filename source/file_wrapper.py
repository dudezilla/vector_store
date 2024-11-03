# import json
# import time
# import hashlib
# import os

# class File_Wrapper:
#     """
#     A class to represent a file and provide utilities for checksum calculation,
#     timestamping, and serialization.

#     Attributes:
#     ----------
#     file_name : str
#         The name of the file.
#     path : str
#         The path to the directory containing the file.
#     _checksum : str
#         The MD5 checksum of the file (cached after first calculation).
#     _timestamp : float
#         The timestamp when the File_Wrapper instance was created.

#     Methods:
#     -------
#     checksum:
#         Returns the MD5 checksum of the file.
#     get_checksum():
#         Calculates and returns the MD5 checksum of the file.
#     compare_checksum(checksum: str):
#         Compares the file's checksum with a given checksum.
#     compare(file_a, file_b):
#         Compares the checksums of two File_Wrapper instances.
#     __str__():
#         Returns the file name as a string representation of the object.
#     __eq__(other):
#         Checks equality based on file checksums.
#     observed_at():
#         Returns the human-readable timestamp when the instance was created.
#     serialize(file_path=None):
#         Serializes the object to a JSON string, optionally writing to a file.
#     """

#     def __init__(self, file_name: str, path: str):
#         """
#         Initializes the File_Wrapper with a file name and path.

#         Parameters:
#         ----------
#         file_name : str
#             The name of the file.
#         path : str
#             The path to the directory containing the file.
#         """
#         self.file_name = file_name
#         self.path = path
#         self._checksum = None
#         self._timestamp = time.time()

#     @property
#     def checksum(self):
#         """
#         Returns the MD5 checksum of the file, calculating it if necessary.

#         Returns:
#         -------
#         str
#             The MD5 checksum of the file.
#         """
#         if self._checksum is None:
#             self._checksum = self.get_checksum()
#         return self._checksum

#     def get_checksum(self):
#         """
#         Calculates and returns the MD5 checksum of the file.

#         Returns:
#         -------
#         str
#             The MD5 checksum of the file.
#         """
#         file_path = os.path.join(self.path, self.file_name)
#         hash_md5 = hashlib.md5()
#         with open(file_path, "rb") as f:
#             for chunk in iter(lambda: f.read(4096), b""):
#                 hash_md5.update(chunk)
#         return hash_md5.hexdigest()

#     def compare_checksum(self, checksum: str):
#         """
#         Compares the file's checksum with a given checksum.

#         Parameters:
#         ----------
#         checksum : str
#             The checksum to compare against.

#         Returns:
#         -------
#         bool
#             True if the checksums match, False otherwise.
#         """
#         return self.checksum == checksum

#     @staticmethod
#     def compare(file_a, file_b):
#         """
#         Compares the checksums of two File_Wrapper instances.

#         Parameters:
#         ----------
#         file_a : File_Wrapper
#             The first file to compare.
#         file_b : File_Wrapper
#             The second file to compare.

#         Returns:
#         -------
#         bool
#             True if the checksums match, False otherwise.
#         """
#         return file_a.checksum == file_b.checksum

#     def __str__(self):
#         """
#         Returns the file name as a string representation of the object.

#         Returns:
#         -------
#         str
#             The file name.
#         """
#         return str(self.file_name)
    
#     def name_with_path(self):
#         """
#         Returns the file name with path as a string representation of the object.

#         Returns:
#         -------
#         str
#             The file name, but with the path.
#         """
#         return str(os.path.join(self.path, self.file_name))


#     def __eq__(self, other):
#         """
#         Checks equality based on file checksums.

#         Parameters:
#         ----------
#         other : File_Wrapper
#             The other File_Wrapper instance to compare.

#         Returns:
#         -------
#         bool
#             True if the checksums match, False otherwise.
#         """
#         if not isinstance(other, File_Wrapper):
#             return NotImplemented
#         return self.checksum == other.checksum

#     def observed_at(self):
#         """
#         Returns the human-readable timestamp when the instance was created.

#         Returns:
#         -------
#         float
#             The creation timestamp in a human-readable format.
#         """
#         #return time.ctime(self._timestamp)
#         return self._timestamp

#     def serialize(self, file_path=None):
#         """
#         Serializes the object to a JSON string, optionally writing to a file.

#         Parameters:
#         ----------
#         file_path : str, optional
#             The path to the file where the JSON data should be written.

#         Returns:
#         -------
#         str
#             The JSON string representation of the object.
#         """
#         data = {
#             'file_name': self.file_name,
#             'path': self.path,
#             'checksum': self.checksum,
#             'timestamp': self.observed_at()
#         }
#         json_data = json.dumps(data, sort_keys=True, indent=4)
#         if file_path:
#             with open(file_path, 'w') as f:
#                 f.write(json_data)
#         return json_data
    


import json
import time
import hashlib
import os

class File_Wrapper:
    def __init__(self, file_name: str, path: str):
        self.file_name = str(file_name)
        self.path = str(path)
        self._checksum = None
        self._timestamp = time.perf_counter()

    @property
    def checksum(self):
        if self._checksum is None:
            self._checksum = self.get_checksum()
        return self._checksum

    def get_checksum(self):
        file_path = os.path.join(self.path, self.file_name)
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def compare_checksum(self, checksum: str):
        return self.checksum == checksum

    @staticmethod
    def compare(file_a, file_b):
        return file_a.checksum == file_b.checksum

    def __str__(self):
        return str(self.file_name)

    def __eq__(self, other):
        if not isinstance(other, File_Wrapper):
            return NotImplemented
        return self.checksum == other.checksum

    def observed_at(self):
        return self._timestamp

    def to_dict(self):
        """Convert instance to a dictionary representation."""
        return {
            'file_name': self.file_name,
            'path': self.path,
            'checksum': self.checksum,
            'timestamp': self.observed_at()
        }

    @classmethod
    def from_dict(cls, data):
        """Create an instance from a dictionary representation."""
        obj = cls(file_name=data['file_name'], path=data['path'])
        obj._checksum = data.get('checksum', None)
        obj._timestamp = data['timestamp']
        return obj

    def name_with_path(self):
        """
        Returns the file name with path as a string representation of the object.

        Returns:
        -------
        str
            The file name, but with the path.
        """
        return str(os.path.join(self.path, self.file_name))