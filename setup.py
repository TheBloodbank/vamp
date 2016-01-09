#!/usr/bin/env python

import os
import re
from setuptools import setup, find_packages

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('vamp/__init__.py').read(),
    re.M
    ).group(1)

long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.rst'
    )
).read()

setup(
    name='vamp',
    author='Sam Hart',
    author_email='hartsn@gmail.com',
    version=version,
    license='LICENSE',
    url='https://github.com/TheBlookbank/vamp',
    description='A bleeding edge package manager.',
    long_description=long_description,

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ' + \
                'GNU General Public License v2 or later (GPLv2+)',
        'Topic :: Software Development :: Version Control',
        'Topic :: Utilities'
    ],
    keywords='git github development circle circleci',

    packages=find_packages('.'),
    install_requires=[
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'vamp = vamp.run:run',
        ]
    },
)
