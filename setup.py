
# python
import os.path
import pathlib
import platform
import shutil
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


REPO = pathlib.Path(__file__).parent.absolute()
with open(REPO / 'README.md', encoding='utf8') as f:
    long_description = f.read()
    

tokenizer = Extension(
    '_woosh',
    include_dirs=['src/_woosh', 'inc'],
    sources=[
        'src/_woosh/fifobuffer.c',
        'src/_woosh/lifobuffer.c',
        'src/_woosh/module.c',
        'src/_woosh/modulestate.c',
        'src/_woosh/tokenizerobject.c',
        'src/_woosh/tokenizerobject_encoding.c',
        'src/_woosh/tokenizerobject_group.c',
        'src/_woosh/tokenizerobject_indent.c',
        'src/_woosh/tokenizerobject_mechanics.c',
        'src/_woosh/tokenizerobject_number.c',
        'src/_woosh/tokenizerobject_operator.c',
        'src/_woosh/tokenizerobject_parse.c',
        'src/_woosh/tokenizerobject_sets.c',
        'src/_woosh/tokenizerobject_string.c',
        'src/_woosh/tokenobject.c',
        'src/_woosh/typeobject.c',
    ],
    language='c',
    extra_compile_args=['-fvisibility=hidden'] if platform.system() != 'Windows' else [],
    define_macros=[('WOOSH_EXPORT', None)],
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
        ('no-optimization', None, 'build without optimizations'),
    ]
    
    def initialize_options(self):
        super().initialize_options()
        self.pgo_generate = None
        self.pgo_use = None
        self.pgo_data = None
        self.gcov = None
        self.no_optimization = None
        
    def finalize_options(self):
        super().finalize_options()
        for extension in self.extensions:
            if self.no_optimization:
                extension.extra_compile_args.append('-O0')
            if self.gcov:
                extension.extra_compile_args.append('-fprofile-arcs')
                extension.extra_compile_args.append('-ftest-coverage')
                extension.extra_link_args.append('-fprofile-arcs')
                
    def build_extension(self, ext):
        is_msvc = self.compiler.__class__.__name__ == 'MSVCCompiler'
        if is_msvc:
            ext_path = self.get_ext_fullpath(ext.name)
            dll_name, dll_ext = os.path.splitext(os.path.basename(ext_path))
            output_dir = os.path.dirname(ext_path)
            implib = os.path.join(
                output_dir,
                self.compiler.library_filename(dll_name)
            )
            ext.extra_link_args.append(f'/IMPLIB:{implib}')
        if self.pgo_generate:
            if is_msvc:
                ext.extra_compile_args.append('/GL')
                ext.extra_link_args.append(
                    f'/FASTGENPROFILE:PGD={self.pgo_data}'
                    if self.pgo_data else 
                    '/FASTGENPROFILE'
                )
            else:
                flag = (
                    f'-fprofile-generate={self.pgo_data}'
                    if self.pgo_data else
                    '-fprofile-generate'
                )
                ext.extra_compile_args.append(flag)
                ext.extra_link_args.append(flag)
        if self.pgo_use:
            if is_msvc:
                ext.extra_link_args.append(
                    f'/USEPROFILE:PGD={self.pgo_data}'
                    if self.pgo_data else 
                    '/USEPROFILE'
                )
            else:
                flag = (
                    f'-fprofile-use={self.pgo_data}'
                    if self.pgo_data else
                    '-fprofile-use'
                )
                ext.extra_compile_args.append(flag)
                ext.extra_link_args.append(flag)
        super().build_extension(ext)
        

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
    packages=find_packages(where='src'),
    package_dir={"": 'src'},
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
