
# bench
from common import bench
# parso
from parso.utils import python_bytes_to_unicode
from parso.python.tokenize import tokenize, parse_version_string

def _(source, source_file):
    source_string = python_bytes_to_unicode(source)
    for token in tokenize(
        source_string,
        version_info=parse_version_string('3.10')
    ):
        pass
    
bench(_)
