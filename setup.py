from setuptools import setup, find_packages
import codecs
import os
import re

with open("pytest_httpbin/version.py") as f:
    code = compile(f.read(), "pytest_httpbin/version.py", 'exec')
    exec(code)

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pytest-httpbin",

    # There are various approaches to referencing the version. For a discussion,
    # see http://packaging.python.org/en/latest/tutorial.html#version
    version=__version__,

    description="Easily test your HTTP library against a local copy of httpbin",
    long_description=long_description,

    # The project URL.
    url='https://github.com/kevin1024/pytest-httpbin',

    # Author details
    author='Kevin McCarthy',
    author_email='me@kevinmccarthy.org',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='pytest-httpbin testing pytest httpbin',
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data = True, # include files listed in MANIFEST.in
    install_requires = ['httpbin','six'],

    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'httpbin = pytest_httpbin.plugin',
        ]
    },
)
