from setuptools import setup

setup(
  name='marketdt',
  version='0.0.5',
  description='Market-oriented datetime functions (currently only NYSE)',
  long_description = 'documentation here: https://github.com/Cinglein/marketdt',
  py_modules=["mktdt"],
  package_dir={'':'src'},
)