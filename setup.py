#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    version='0.1.0',
    description='Ade, a templated file system manager',
    author='Lorenzo Angeli',
    name='ade',
    author_email='lorenzo.angeli@gmail.com',
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    test_suite="test",
    entry_points={
        'console_scripts': [
            'ade = ade.main:run',
        ],
    },
    install_requires=[
        'argparse',
        'sphinx',
        'sphinx_rtd_theme'
    ],
)
