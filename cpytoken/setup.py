
# pgo
import pgo
# python
import pathlib
import sys
# setuptools
from setuptools import Extension, setup


dir = pathlib.Path(__file__).parent.absolute()
    
cpytoken = Extension(
    '_woosh_cpytoken',
    sources=[
        'cpytoken.c',
        'token.c',
        'tokenizer.c',
    ],
    language='c',
)

setup(
    name='woosh-cpytoken',
    ext_modules=[cpytoken],
    pgo={
        "profile_command": [sys.executable, str(dir / 'profile.py')],
    },
)
