#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from pypjlink import version

setup(
    name='pypjlink',
    version=version,
    author=('Peter Ward <peteraward@gmail.com>, '
            'Gaetano Guerriero <gaetano.guerriero@spacespa.it>'),
    author_email='gaetano.guerriero@spacespa.it',
    url='https://github.com/gaetano-guerriero/pypjlink',
    description='PJLink is a standard for controlling data projectors.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Utilities',
    ],

    install_requires=['appdirs'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pjlink = pypjlink.cli:main',
        ],
    },
    test_suite='pypjlink.tests',
)
