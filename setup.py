from distutils.core import setup

setup(name='Stolat',
      version='0.1',
      description='A DSL for Information Extraction',
      author='Joe Geldart',
      author_email='joe@joegeldart.com',
      url = "http://github.com/jgeldart/stolat",
      long_description = """\
StoLat Insertion Parser Information Extraction DSL
==================================================

This library provides a DSL for information extraction using
the concept of insertion parsing. This allows for 'gapping' or
spurious elements allowing for more robust extraction.

The library leans heavily on generators, keeping only a fixed
window of the token stream in memory at any time.

The library is pure python, allowing it to be deployed in
restrictive environments such as Google App Engine.

Warnings
--------

This library is pre-alpha quality and the API may change at any
time. This was initially implemented in one evening as a challenge
to myself to express my idea for insertion parsing in as little
time as possible. It is intended that this will be developed in the
near future into a more full-featured and better architected library.

Installation
------------

See INSTALL.
      """,
      classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
      ], 
      package_dir={'': 'src'},
      packages=['stolat'])
