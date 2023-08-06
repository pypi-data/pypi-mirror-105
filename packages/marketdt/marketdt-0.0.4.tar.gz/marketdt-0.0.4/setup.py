from setuptools import setup

setup(
  name='marketdt',
  version='0.0.4',
  description='Market-oriented datetime functions (currently only NYSE)',
  py_modules=["mktdt"],
  package_dir={'':'src'},
)