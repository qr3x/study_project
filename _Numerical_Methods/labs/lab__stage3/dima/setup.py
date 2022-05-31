import pybind11
from distutils.core import setup, Extension

ext_modules = [
    Extension(
        'iterMethods',
        ['main.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
    ),
]

setup(
    name='iterMethods',
    version='1.0.0',
    author='Debruine',
    description='IterMethods extension',
    ext_modules = ext_modules,
    requires=['pybind11']
)
