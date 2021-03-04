
# bench
from common import bench
# python
from tokenize import tokenize

def _(source, source_file):
    for token in tokenize(source_file.readline):
        pass
    
bench(_)
