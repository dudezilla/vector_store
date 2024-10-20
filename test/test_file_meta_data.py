import sys
import os
import tempfile
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))
from file_meta_data import crawl_directory,pascal_triangle_row
import unittest

class TestExample(unittest.TestCase):



    def setUp(self):

        pass

    def tearDown(self):
        pass

    def test_file_meta_data(self):
        

    def test_pascal_triangle_row(self):
        assert pascal_triangle_row(0) == [1], f"Test case {0} failed:{pascal_triangle_row(0)} != {0}"
        assert pascal_triangle_row(1) == [1,1], f"Test case {1} failed:{pascal_triangle_row(1)} != {1,1}"
        assert pascal_triangle_row(2) == [1,2,1], f"Test case {2} failed:{pascal_triangle_row(1)} != {1,2,1}"



if __name__ == '__main__':
    unittest.main()