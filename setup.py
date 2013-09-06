#!/usr/bin/env python

"""
This setup is suitable for "python setup.py develop" if setuptools.
"""
from setuptools import setup, find_packages

from hazpy.unit_conversion import __version__

setup(
    name = "hazpy.unit_conversion",
    description='Physical Unit conversion utilties -- units useful for oil and chemical spill response',
    author='Christopher H. Barker',
    author_email='Chris.Barker@noaa.gov',
    url='http://www.response.restoration.noaa.gov/nucos',
    version = __version__,
    packages = find_packages(),
    namespace_packages = ["hazpy"],
    )
