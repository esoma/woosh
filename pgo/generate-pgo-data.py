
# this script is used as the data set to generate the profile data for profile
# guided optimization of the c extension

# woosh
import woosh
# python
import io
import os
import pathlib

DATA = pathlib.Path(__file__).parent.absolute() / '../sample'
DATA_FILES = os.listdir(DATA)

for data_file in DATA_FILES:
    with open(DATA / data_file, 'rb') as f:
        source_bytes = f.read()
        source_file_like = io.BytesIO(source_bytes)
    print(data_file)
    list(woosh.tokenize(source_bytes))
    list(woosh.tokenize(source_file_like))
