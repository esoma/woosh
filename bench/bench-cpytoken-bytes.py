
# bench
from common import bench
# woosh
from _woosh_cpytoken import tokenize

def _(source, source_file):
    for token in tokenize(source):
        pass
    
bench(_)
