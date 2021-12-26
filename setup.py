"""Setup package"""

import os
import re
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext

# Packages to include in the distribution
packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

# Additional data required to install this package
package_data = {
    'streamdeck_manager': ['assets/*', 'assets/**/*']
}

# Files with that are data out of the package
# data_files=[('my_data', ['data/data_file'])],

# List of dependencies minimally needed by this project to run
with open('requirements.in') as f:
    install_requires = [x for x in f.read().splitlines() if not x.startswith(('--', '#'))]

# Trove classifiers
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Topic :: Software Development :: Tools',
    'License :: OSI Approved :: GNU General Public License v3',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy'
]

# Keywords to help users find this package on PyPi
keywords = ''

here = os.path.abspath(os.path.dirname(__file__))
meta = {}
readme = ''

# Read version and README files
with open(os.path.join(here, 'streamdeck_manager', '_meta.py'), 'r') as f:
    exec(f.read(), meta)
with open(os.path.join(here, 'README.md'), 'r') as f:
    readme = f.read()

setup(
    name=meta['__title__'],
    version=meta['__version__'],
    description=meta['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=meta['__url__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    license=meta['__license__'],
    classifiers=classifiers,
    keywords=keywords,
    platforms=['any'],
    packages=packages,
    install_requires=install_requires,
    package_data=package_data,
    include_package_data=True,
    python_requires=">=3.6.*, <4",
)
