import os
import sys
import json
from file_collection import File_Collection
from file_wrapper import File_Wrapper

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))
from crawl import crawl


INPUT_LOCATION = "./input"
META_LOCATION = "input_metadata.json"

def check_differences(c1):
   file_test = crawl(INPUT_LOCATION)
   if file_test == c1:
      print("File metadata is current.")
   else:
      print("Database updates are possible.")

c1 = None
try:
   c1 = File_Collection.deserialize(META_LOCATION)
   check_differences(c1)
except FileNotFoundError as F:
   crawl(INPUT_LOCATION)



