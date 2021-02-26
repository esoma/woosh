
# python
import pathlib
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext

REPO = pathlib.Path(__file__).parent.absolute()
with open(REPO / 'README.md') as f:
    long_description = f.read()
    
tokenizer = Extension(
    '_woosh',
    include_dirs=['src', 'inc'],
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
    #undef_macros=['NDEBUG'],
    #library_dirs=['F:\programs\microprofiler'],
    #libraries=['micro-profiler_x64'],
    #extra_compile_args=['/GH', '/Gh', '/Zi'],
    #extra_link_args=['/INCREMENTAL:NO', '/DEBUG:FULL'],
    #extra_compile_args=['-fprofile-arcs', '-ftest-coverage'],
    #extra_link_args=['-fprofile-arcs'],
)

class BuildExtCommand(build_ext):
   
    user_options = build_ext.user_options + [
        ('pgo-generate', None, 'build with profile guided instrumentation'),
        ('pgo-use', None, 'build using profile guided optimization'),
        ('pgo-data=', None, 'the pgo data location/file'),
        ('gcov', None, 'build with gcov instrumentation'),
    ]
    
    def initialize_options(self):
        super().initialize_options()
        self.pgo_generate = None
        self.pgo_use = None
        self.pgo_data = None
        self.gcov = None
        
    def finalize_options(self):
        super().finalize_options()
        for extension in self.extensions:
            if self.gcov:
                extension.extra_compile_args.append('-fprofile-arcs')
                extension.extra_compile_args.append('-ftest-coverage')
                extension.extra_link_args.append('-fprofile-arcs')
            if self.pgo_generate:
                extension.extra_compile_args.append('/GL')
                extension.extra_link_args.append(
                    f'/FASTGENPROFILE:PGD={self.pgo_data}'
                    if self.pgo_data else 
                    '/FASTGENPROFILE'
                )
            if self.pgo_use:
                extension.extra_link_args.append(
                    f'/USEPROFILE:PGD={self.pgo_data}'
                    if self.pgo_data else 
                    '/USEPROFILE'
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
    cmdclass={
        'build_ext': BuildExtCommand,
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
