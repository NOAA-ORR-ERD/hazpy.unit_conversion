#!/usr/bin/env python

"""
unit_conversion package

All it really contains is the one unit_conversion module,
a data module, plus a module for lat-lon conversion.

All of unit_conversion is imported here for convenience

"""
__version__ = "2.2"

# to support the hazpy namespace packege
__import__('pkgutil').extend_path(__path__, __name__)

from unit_conversion import *


