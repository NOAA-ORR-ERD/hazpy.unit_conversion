#!/usr/bin/env python
"""
__init__.py for hazpy to support namespace package
"""

__import__('pkgutil').extend_path(__path__, __name__)
__import__('pkg_resources').declare_namespace(__name__)