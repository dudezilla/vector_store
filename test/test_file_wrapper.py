import unittest
import tempfile
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))

from file_wrapper import File_Wrapper

class TestFileWrapper(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.file_path_1 = os.path.join(self.test_dir.name, "test_file_1.txt")
        self.file_path_2 = os.path.join(self.test_dir.name, "test_file_2.txt")
        self.file_path_3 = os.path.join(self.test_dir.name, "test_file_3.txt")

        with open(self.file_path_1, 'w') as f:
            f.write("Hello World")

        with open(self.file_path_2, 'w') as f:
            f.write("Hello World")

        with open(self.file_path_3, 'w') as f:
            f.write("Different Content")

        self.wrapper_1 = File_Wrapper("test_file_1.txt", self.test_dir.name)
        self.wrapper_2 = File_Wrapper("test_file_2.txt", self.test_dir.name)
        self.wrapper_3 = File_Wrapper("test_file_3.txt", self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()
        pass

    def test_checksum(self):
        self.assertEqual(self.wrapper_1.checksum, self.wrapper_2.checksum)
        self.assertNotEqual(self.wrapper_1.checksum, self.wrapper_3.checksum)

    def test_compare_checksum(self):
        self.assertTrue(self.wrapper_1.compare_checksum(self.wrapper_2.checksum))
        self.assertFalse(self.wrapper_1.compare_checksum(self.wrapper_3.checksum))

    def test_compare(self):
        self.assertTrue(File_Wrapper.compare(self.wrapper_1, self.wrapper_2))
        self.assertFalse(File_Wrapper.compare(self.wrapper_1, self.wrapper_3))

    def test_equality(self):
        self.assertEqual(self.wrapper_1, self.wrapper_2)
        self.assertNotEqual(self.wrapper_1, self.wrapper_3)

    def test_str(self):
        expected_str = f"test_file_1.txt"
        self.assertEqual(str(self.wrapper_1), expected_str)

if __name__ == '__main__':
    unittest.main()