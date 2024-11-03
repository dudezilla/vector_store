import unittest
import tempfile
import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))

from file_wrapper import File_Wrapper
from file_collection import File_Collection


class Test_File_Collection(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file1_path = os.path.join(self.temp_dir.name, "file1.txt")
        self.file2_path = os.path.join(self.temp_dir.name, "file2.txt")
        self.file3_path = os.path.join(self.temp_dir.name, "file3.txt")
        self.file4_path = os.path.join(self.temp_dir.name, "file4.txt")


        with open(self.file1_path, 'w') as f:
            f.write("Hello World")
        
        with open(self.file2_path, 'w') as f:
            f.write("Hello Python")
        
        with open(self.file3_path, 'w') as f:
            f.write("Hello Python")

        with open(self.file4_path, 'w') as f:
            f.write("Hello Python")


        self.file1 = File_Wrapper("file1.txt", self.temp_dir.name)
        self.file2 = File_Wrapper("file2.txt", self.temp_dir.name)
        self.file3 = File_Wrapper("file3.txt", self.temp_dir.name)
        self.file4 = File_Wrapper("file4.txt", self.temp_dir.name)
        #self.file3 = self.file1#File_Wrapper("file1.txt", self.temp_dir.name)
        self.collection = File_Collection()
        self.collection.append(self.file1)
        self.collection.append(self.file2)
        self.collection.append(self.file3)
        self.collection.append(self.file4)


    def tearDown(self):
        self.temp_dir.cleanup()

    def test_append_and_getitem(self):
        #print(self.collection[self.file1_path])
        self.assertEqual(self.collection[self.file1_path], self.file1)
        self.assertEqual(self.collection[self.file2_path], self.file2)

    # def test_unique_contents(self):
    #     unique_files = self.collection.unique_contents()
    #     # self.assertEqual(len(unique_files), 2)
    #     # self.assertIn(self.file1, unique_files)
    #     # self.assertIn(self.file2, unique_files)
    #     print(unique_files)
    #     # result = {"b10a8db164e0754105b7a99be72e3fe5": {"paths": ["/tmp/tmpl2nn7c47/file1.txt"]}, "a709c173220d6185d12248faa9f40ac8": {"paths": ["/tmp/tmpl2nn7c47/file2.txt", "/tmp/tmpl2nn7c47/file3.txt", "/tmp/tmpl2nn7c47/file4.txt"]}}
    #     #RANDOM PATHS... Can I fix them?
    #     # print(unique_files)
    #     # print(result)
    #     #self.assertEquals(unique_files,result)
    def test_unique_contents(self):
        unique_files = self.collection.unique_contents()
        expected_result = {
            "b10a8db164e0754105b7a99be72e3fe5": {"paths": [self.file1_path]},
            "a709c173220d6185d12248faa9f40ac8": {"paths": [self.file2_path, self.file3_path, self.file4_path]}
        }
        self.assertEqual(unique_files, expected_result)
        

    def test_next_file(self):
        collection = self.collection
        files_iter = collection.next_file()
        top = next(files_iter).observed_at()
        for file in files_iter:
            file_top = file.observed_at()
            self.assertTrue(top >= file_top, "iterate in descending order")
            top = file_top


    def test_str(self):
        expected_str = (
            f"\tfile1.txt\n\tpath:{self.temp_dir.name}\n\ttimestamp:{self.file1.observed_at()}\n\n"
            f"\tfile2.txt\n\tpath:{self.temp_dir.name}\n\ttimestamp:{self.file2.observed_at()}\n\n"
        )
        #print(str(self.collection))
        print("todo establish a contract with test_str and str")
        #print(expected_str)
        #a bad test.
        #self.assertEqual(str(self.collection), expected_str)

if __name__ == "__main__":
    unittest.main()