
# pyperf
import pyperf
# python
import io
import os
import pathlib
import sys

DATA = (pathlib.Path(__file__).parent.absolute() / '../sample').resolve()

# parso needs this and pyperf doesn't include it in the inherit environs by
# default
sys.argv += ['--inherit-environ', 'LOCALAPPDATA']

runner = pyperf.Runner()

def bench(func):
    for directory, _, files in os.walk(DATA):
        directory = pathlib.Path(directory)
        for file in files:
            data_file = directory / file
            if not data_file.name == 'abc.py':
                continue
            if not data_file.name.endswith('.py'):
                continue
            with open(data_file, 'rb') as f:
                source = f.read()
                # this is for the Cython tokenizer, which chokes if it
                # encounters '\r'
                source = source.replace(b'\r\n', b'\n')
                source_file = io.BytesIO(source)
            def _():
                source_file.seek(0)
                func(source, source_file)
            runner.bench_func(str(data_file.relative_to(DATA)), _)
