import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))
from crawl import crawl
crawl("./fake")