try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
sys.path.insert(0, '.')
version = 0.1
long_description = 'Generates a documentation embaddable representation of a Voluptuous schema.'
description = long_description


setup(
    name='voluptuous-schema-parser',
    url='https://github.com/decbis/voluptuous-schema-parser',
    version=version,
    description=description,
    long_description=long_description,
    license='BSD',
    platforms=['any'],
    py_modules=['voluptuous-schema-parser'],
    author='Eugen Dinca',
    author_email='decostin@gmail.com',
    install_requires = [
        'setuptools >= 0.6b1',
    ],
)