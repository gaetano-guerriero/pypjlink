from setuptools import find_packages, setup

setup(
    name='pypjlink',
    version='1.0',
    author=('Peter Ward <peteraward@gmail.com>, '
            'Gaetano Guerriero <gaetano.guerriero@spacespa.it>'),
    url='https://github.com/gaetano-guerriero/pypjlink',
    description='PJLink is a standard for controlling data projectors.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: Apache v2',
        'Natural Language :: English',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Utilities',
    ],

    install_requires=['appdirs'],
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'pjlink = pypjlink.cli:main',
        ],
    }
)
