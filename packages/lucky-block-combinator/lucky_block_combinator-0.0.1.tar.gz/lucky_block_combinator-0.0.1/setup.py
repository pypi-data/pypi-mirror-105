# -*- coding: utf-8 -*-
import os
import sys
from distutils.core import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("This version of Pydicttoxml requires Python {}.{},\
        but you're trying to install it on Python {}.{}.".format(
        *(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)
setup(
    name='lucky_block_combinator',
    version='0.0.1',
    description='Modifying Lucky Blocks to play them in multiple combinations, and Error fixing',
    author='LukeProducts',
    author_email='lukeproducts@gmx.net',
    url='https://github.com/LukeProducts',
    packages=['lucky_block_combinator'],
    keywords="lucky block Minecraft Mod combination error help",
    long_description=read('README.rst'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    license='BSD'
)