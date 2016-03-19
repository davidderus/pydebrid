#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import pydebrid

setup(
    name='pydebrid',

    version=pydebrid.__version__,

    packages=find_packages(),

    author='David Dérus',

    description='A cross-platform Alldebrid CLI with downloader and subtitles finder',
    long_description=open('README.rst').read(),

    install_requires=['subliminal>=1.1.1,<2', 'guessit<=1.9', 'lxml', 'clint', 'pyperclip', 'keyring', 'keyrings.alt', 'requests', 'beautifulsoup4'],

    url='https://github.com/davidderus/pydebrid',

    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Intended Audience :: Other Audience'
    ],

    entry_points={
        'console_scripts': [
            'pydebrid = pydebrid.main:launcher',
        ],
    }
)
