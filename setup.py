from setuptools import setup, find_packages
import codecs
import os
import re

import pytest-httpbin

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open('DESCRIPTION.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pytest-httpbin",

    # There are various approaches to referencing the version. For a discussion,
    # see http://packaging.python.org/en/latest/tutorial.html#version
    version=pytest-httpbin.__version__,

    description="A pytest plugin for including a httpbin server in your tests",
    long_description=long_description,

    # The project URL.
    url='https://github.com/pypa/pytest-httpbinproject',

    # Author details
    author='Kevin McCarthy',
    author_email='me@kevinmccarthy.org',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],

    # What does your project relate to?
    keywords='pytest-httpbin testing pytest httpbin',
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires = ['httpbin'],
)
