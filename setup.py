
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
    include_dirs=['src', 'inc'],
    sources=[
        'src/fifobuffer.c',
        'src/lifobuffer.c',
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
        # the msvc .lib file isn't normally installed in the python package,
        # this will copy it from the temp build directory to the actual output
        # directory
        if is_msvc:
            ext_path = self.get_ext_fullpath(ext.name)
            output_dir = os.path.dirname(ext_path)
            # this is explicitly "allowed" despite being an underscore variable
            build_temp = os.path.dirname(self._built_objects[0])
            dll_name, dll_ext = os.path.splitext(os.path.basename(ext_path))
            temp_implib_file = os.path.join(
                build_temp,
                self.compiler.library_filename(dll_name)
            )
            build_implib_file = os.path.join(
                output_dir,
                self.compiler.library_filename(dll_name)
            )
            shutil.copy(temp_implib_file, build_implib_file)
        

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
