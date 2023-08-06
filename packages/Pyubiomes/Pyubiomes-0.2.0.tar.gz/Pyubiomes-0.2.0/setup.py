
long_desc='''
# Pyubiomes, a Simple (wip) Python Wrapper For [Cubiomes by Cubitect](https://github.com/Cubitect/cubiomes)
## Introduction
Pyubiomes is a (relatively) easy to use, easy to understand wrapper for the Cubiomes C library and a few more libraries. This project is still a wip, so please mention bugs/improvements. 

If you have any problems, look at the documentation, then ask on the discord server. Do not make a new issue. I will likely not see it.

This module requires [minecraft_nether_gen_rs](https://github.com/SeedFinding/minecraft_nether_generation_rs)'s Python binding for the nether utilities 

This project's [code documentation](https://www.youtube.com/watch?v=dQw4w9WgXcQ) can be found on 
its [github repository](https://github.com/4gboframram/Pyubiomes)
'''



from setuptools import setup, find_packages, Extension
setup(name = 'Pyubiomes', version = '0.2.0', description="a (probably bad wip) python wrapper for the C library Cubiomes", author="4gboframram", url="https://github.com/4gboframram/Pyubiomes",author_email="<zachawesomeness411@gmail.com>", long_description=long_desc, include_package_data=True,
long_description_content_type='text/markdown',
packages=find_packages(),
ext_modules = [Extension('Pyubiomes.overworld', sources=['./Pyubiomes/wrap.c'])],
#package_data={'': ['searches.so']}
)