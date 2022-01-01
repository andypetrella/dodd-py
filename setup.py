from setuptools import find_packages, setup

setup(
    name="dodd-py", 
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    
)