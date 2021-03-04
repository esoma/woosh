
# python
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
    
cpytoken = Extension(
    '_woosh_cpytoken',
    sources=[
        'cpytoken.c',
        'token.c',
        'tokenizer.c',
    ],
    language='c',
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


setup(
    name='woosh-cpytoken',
    ext_modules=[cpytoken],
    cmdclass={
        'build_ext': BuildExtCommand,
    },
)
