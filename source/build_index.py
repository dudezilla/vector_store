import os
import sys
import json
from file_collection import File_Collection
from file_wrapper import File_Wrapper

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))
from crawl import crawl


c1 = File_Collection.deserialize("input_metadata.json")

file_test = crawl("./input")
# for wrapper in c1:
#     print(str(wrapper))
#     print(wrapper.to_dict())
#     pass

# for key,list in c1.unique_contents().items():
#     print(f"md5:{key}")
#     for file in list['paths']:
#         print(file)
#c1.serialize("input_metadata.json")

if file_test == c1:
   print("File metadata is current.")
else:
   print("Database updates are possible.")
   
