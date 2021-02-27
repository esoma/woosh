
# this script is used as the data set to generate the profile data for profile
# guided optimization of the c extension

# woosh
import woosh
# python
import io
import os
import pathlib

DATA = (pathlib.Path(__file__).parent.absolute() / '../sample').resolve()

for directory, _, files in os.walk(DATA):
    if directory.endswith('contrived'):
        continue
    directory = pathlib.Path(directory)
    for file in files:
        if not file.endswith('.py'):
            continue
        data_file = directory / file
        with open(data_file, 'rb') as f:
            source_bytes = f.read()
            source_file_like = io.BytesIO(source_bytes)
        print(data_file.relative_to(DATA))
        list(woosh.tokenize(source_bytes))
        list(woosh.tokenize(source_file_like))
