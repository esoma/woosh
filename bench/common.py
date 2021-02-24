
# pyperf
import pyperf
# python
import io
import os
import pathlib

DATA = pathlib.Path(__file__).parent.absolute() / '../sample'
DATA_FILES = os.listdir(DATA)

runner = pyperf.Runner()

def bench(func):
    for data_file in DATA_FILES:
        if data_file != 'abc.py':
            continue
        with open(DATA / data_file, 'rb') as f:
            source = f.read()
            # this is for the Cython tokenizer, which chokes if it encounters
            # \r
            source = source.replace(b'\r\n', b'\n')
            source_file = io.BytesIO(source)
        def _():
            source_file.seek(0)
            func(source, source_file)
        runner.bench_func(data_file, _)
