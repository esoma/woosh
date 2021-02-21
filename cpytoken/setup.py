
# python
import pathlib
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

class BuildExtPgoCommand(build_ext):
   
    user_options = build_ext.user_options + [
        ('pgo-generate', None, 'build with profile guided instrumentation'),
        ('pgo-use', None, 'build using profile guided optimization'),
    ]
    
    def initialize_options(self):
        super().initialize_options()
        self.pgo_generate = None
        self.pgo_use = None
        
    def finalize_options(self):
        super().finalize_options()
        for extension in self.extensions:
            if self.pgo_generate:
                extension.extra_compile_args.append('/GL')
                extension.extra_link_args.append('/FASTGENPROFILE')
            if self.pgo_use:
                extension.extra_link_args.append('/USEPROFILE')

setup(
    name='woosh-cpytoken',
    ext_modules=[cpytoken],
    cmdclass={
        'build_ext': BuildExtPgoCommand,
    },
)
