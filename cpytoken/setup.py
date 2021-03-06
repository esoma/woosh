
# pgo
import pgo
# python
import sys
# setuptools
from setuptools import Extension, setup

    
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
    cmdclass={
        'build_ext': pgo.make_build_ext([sys.executable, 'profile.py']),
    },
)
