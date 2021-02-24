
# cython
import Cython
import Cython.Plex.Errors
from Cython.Utils import (
    detect_opened_file_encoding as cython_detect_opened_file_encoding,
)
from Cython.Compiler.Main import Context as CythonContext
from Cython.Compiler.CythonScope import CythonScope
from Cython.Compiler.Scanning import (
    PyrexScanner as CythonTokenizer,
    StringSourceDescriptor as CythonStringSourceDescriptor
)
# bench
from common import bench
# python
import io

def _(source, source_file):
    encoding = cython_detect_opened_file_encoding(source_file)
    source_string = source.decode(encoding)
    context = CythonContext([], [], language_level=3)
    desc = CythonStringSourceDescriptor(b'__main__.py', source_string)
    scope = CythonScope(context)
    tokenizer = CythonTokenizer(
        io.StringIO(source_string),
        desc,
        source_encoding=encoding,
        scope=scope,
        context=context,
    )
    while True:
        token = tokenizer.read()
        if token == ('EOF', ''):
            break
    
bench(_)
