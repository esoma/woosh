
# pyperf
import pyperf
# python
import io
import os
import pathlib

DATA = (pathlib.Path(__file__).parent.absolute() / '../sample').resolve()

runner = pyperf.Runner()

def bench(func):
    for directory, _, files in os.walk(DATA):
        directory = pathlib.Path(directory)
        for file in files:
            data_file = directory / file
            with open(data_file, 'rb') as f:
                source = f.read()
                # this is for the Cython tokenizer, which chokes if it encounters
                # \r
                source = source.replace(b'\r\n', b'\n')
                source_file = io.BytesIO(source)
            def _():
                source_file.seek(0)
                func(source, source_file)
            runner.bench_func(str(data_file.relative_to(DATA)), _)
