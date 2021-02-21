
# this script is used as the data set to generate the profile data for profile
# guided optimization of the c extension

# woosh
import woosh
# python
import io
import os
import pathlib

DATA = pathlib.Path(__file__).parent.absolute() / 'sample'
DATA_FILES = os.listdir(DATA)

for data_file in DATA_FILES:
    with open(DATA / data_file, 'rb') as f:
        source = f.read()
        data = io.BytesIO(source)
    print(data_file)
    list(woosh.tokenize(data))
