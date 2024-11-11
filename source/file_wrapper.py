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