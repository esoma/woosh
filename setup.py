
# python
import pathlib
from setuptools import Extension, find_packages, setup

README_FILE_PATH = pathlib.Path(__file__).parent.absolute().joinpath(
    'README.md',
)
with open(README_FILE_PATH) as f:
    long_description = f.read()
    
tokenizer = Extension(
    '_woosh',
    include_dirs=['src'],
    sources=[
        'src/module.c',
        'src/modulestate.c',
        'src/tokenizerobject.c',
        'src/tokenizerobject_encoding.c',
        'src/tokenizerobject_group.c',
        'src/tokenizerobject_indent.c',
        'src/tokenizerobject_mechanics.c',
        'src/tokenizerobject_number.c',
        'src/tokenizerobject_operator.c',
        'src/tokenizerobject_parse.c',
        'src/tokenizerobject_sets.c',
        'src/tokenizerobject_string.c',
        'src/tokenobject.c',
        'src/typeobject.c',
    ],
    language='c',
)

setup(
    name='woosh',
    version='0.1.0',
    author='Erik Soma',
    author_email='stillusingirc@gmail.com',
    description='Fast Python Tokenizer',
    ext_modules=[tokenizer],
    long_description=long_description,
    long_description_content_type='text/markdown',
    tests_require=[
        'mypy',
        'pytest',
        'pytest-cov',
    ],
    url='https://github.com/esoma/woosh',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
