import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
  name='quarkz',
  version='0.0.1',
  url='https://github.com/quarkz-encryption/Quarkz',
  author='tavivia',
  author_email='tavian@quarkz-encryption.com',
  packages=find_packages(exclude=("tests",)),
  platforms='any',
  license='MIT',
  ext_modules=[],
  description="An Encryption library",
  long_description='See https://github.com/quarkz-encryption/quarkz',
)
