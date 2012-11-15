from setuptools import find_packages, setup

setup(
    name='pjlink',
    version='1.0',
    description='PJLink is a standard for controlling data projectors.',
    author='Peter Ward',
    author_email='peteraward@gmail.com',
    packages=find_packages(),
    install_requires=['appdirs'],
    entry_points = {
        'console_scripts': [
            'pjlink = pjlink.cli:main',
        ],
    }
)
