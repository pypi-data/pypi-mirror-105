#!/usr/bin/env python

from setuptools import setup

exec(open('ykb/version.py').read())
setup(
    name='ykb',
    version=__version__
)
