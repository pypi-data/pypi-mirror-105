from setuptools import setup

setup(
  name='marketdt',
  version='0.0.3',
  description='Market-oriented datetime functions (currently only NYSE)',
  py_modules=["mktdt"],
  package_dir={'':'src'},
)