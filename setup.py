from setuptools import find_packages, setup

setup(
    name='pjlink',
    version='1.0',
    author='Peter Ward',
    author_email='peteraward@gmail.com',
    url='http://hg.flowblok.id.au/pjlink',
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
            'pjlink = pjlink.cli:main',
        ],
    }
)
