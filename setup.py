#!/usr/bin/env python3

# Copyright 2018 Facundo Batista
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://github.com/facundobatista/infoauth

"""Build tar.gz for infoauth."""

from distutils.core import setup

setup(
    name='infoauth',
    version=open('version.txt', 'rt', encoding='ascii').read().strip(),
    license='GPL-3',
    author='Facundo Batista',
    author_email='facundo@taniquetil.com.ar',
    description='A small but handy module and script to load/save tokens from/to disk.',
    long_description=open('README.rst', 'rt', encoding='utf8').read(),
    url='https://github.com/facundobatista/infoauth',
    packages=["infoauth"],
    scripts=["bin/infoauth"],
    keywords="info auth tokens",  # Keywords to get found easily on PyPI results,etc.
    install_requires=['setuptools'],
    tests_require=['nose', 'flake8', 'pep257', 'rst2html5'],  # What unittests require.
    python_requires='>=3.3',  # Minimum Python version supported.
    #extras_require={
    #    'setuptools': 'setuptools',
    #},

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Natural Language :: English',
        'Natural Language :: Spanish',

        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
