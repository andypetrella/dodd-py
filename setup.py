from setuptools import find_packages, setup
from os.path import splitext
from os.path import basename
from glob import glob

setup(
    name="dodd-py", 
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
)