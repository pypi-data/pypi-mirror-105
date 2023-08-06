from distutils.core import setup, Extension
setup(name = 'searches', version = '0.1',author="4gboframram", url="", description="search functions for Pyubiomes",
   ext_modules = [Extension('searches', ['wrap.c'])])