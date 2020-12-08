
# python
import pathlib
from setuptools import Extension, find_packages, setup

README_FILE_PATH = pathlib.Path(__file__).parent.absolute().joinpath(
    'README.md',
)
with open(README_FILE_PATH) as f:
    long_description = f.read()
    
tokenizer = Extension(
    'woosh._tokenizer',
    include_dirs=['src'],
    sources=['src/tokenizer.c'],
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
