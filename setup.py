#!/usr/bin/env python
from setuptools import setup, find_packages
from distutils.command.build import build
import os
import sys
import subprocess

root_dir = os.path.dirname(__file__)
resource_file = os.path.join(root_dir, 'resources', 'ui', 'resource.qrc')
resource_file_dest = os.path.join(
    root_dir,
    'ade',
    'ui',
    'resource.py'
)


class Build(build):
    def run(self):
        pyside_rcc_command = 'pyside-rcc'
        if sys.platform == 'win32':
            import PySide
            pyside_rcc_command = os.path.join(
                os.path.dirname(PySide.__file__),
                'pyside-rcc.exe'
            )

        try:
            subprocess.check_call([
                pyside_rcc_command,
                '-os',
                resource_file_dest,
                resource_file
            ])
        except:
            print 'pyside-rcc command unavailable. Skipping resources.'

        build.run(self)

setup(
    version='0.3.0',
    description='Ade, a templated file system manager',
    author='Lorenzo Angeli',
    name='ade',
    author_email='lorenzo.angeli@gmail.com',
    packages=find_packages(exclude=["test"]),
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
    cmdclass={
        'build': Build,
    },
)
