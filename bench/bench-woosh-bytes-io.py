
# bench
from common import bench
# woosh
from woosh import tokenize

def _(source, source_file):
    for token in tokenize(source_file):
        pass
    
bench(_)
