
# cython
import Cython
import Cython.Plex.Errors
from Cython.Utils import detect_opened_file_encoding as cython_detect_opened_file_encoding
from Cython.Compiler.Main import Context as CythonContext
from Cython.Compiler.CythonScope import CythonScope
from Cython.Compiler.Scanning import (
    PyrexScanner as CythonTokenizer,
    StringSourceDescriptor as CythonStringSourceDescriptor
)
# pyperf
import pyperf
# woosh
import woosh
import _woosh_cpytoken
# python
import io
import os
import pathlib
import tokenize

import gc

runner = pyperf.Runner()

DATA = pathlib.Path(__file__).parent.absolute() / 'sample'
DATA_FILES = os.listdir(DATA)

for data_file in DATA_FILES:
    if data_file != 'codeop.py':
        continue
    with open(DATA / data_file, 'rb') as f:
        source = f.read()
        data = io.BytesIO(source)
        
    def test_woosh():
        data.seek(0)
        for token in woosh.tokenize(source):
            pass
    runner.bench_func(f'woosh-{data_file}', test_woosh)
    '''
    def test_tokenize():
        data.seek(0)
        for token in tokenize.tokenize(data.readline):
            pass
    runner.bench_func(f'tokenize-{data_file}', test_tokenize)
    
    def test_cython():
        data.seek(0)
        encoding = cython_detect_opened_file_encoding(data)
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
        l = []
        while True:
            token = tokenizer.read()
            l.append(token)
            if token == ('EOF', ''):
                break
    runner.bench_func(f'cython-{data_file}', test_cython)
    '''
    def test_cpython():
        data.seek(0)
        for token in _woosh_cpytoken.tokenize(source):
            pass
    runner.bench_func(f'cpython-{data_file}', test_cpython)

