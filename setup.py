"""Installer for dewbrick
"""

import os
from setuptools import setup, find_packages


setup(
    name='dewbrick',
    description='',
    long_description=open('README.rst').read(),
    version='1.0.0',
    author='Team Oh My Gourd',
    author_email='debrick@example.com',
    url='https://github.com/ohmygourd/debrick',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'console_scripts': [
            'dewbrick-app=dewbrick.app:main',
        ],
    },
    license='Apache'
)
