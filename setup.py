# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages


if sys.version_info.major < 3:
    print("Python 3.x is required.")
    sys.exit(1)


def read_file(fname):
    """  Read file into string.

    Parameters
    ----------
    fname : str
        Full path to the file.

    Return
    ------
    str :
        File content as a string.
    """
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf8").read()


setup(
    name="covid19",
    version="0.1.0",
    author="Stefano Ubbiali",
    author_email="stefano.ubbiali@outlook.com",
    description=(
        "Data analysis of the COVID-19 pandemic."
    ),
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    keywords="",
    license="",
    packages=find_packages(),
    install_requires=read_file("requirements.txt").split("\n"),
    setup_requires=["setuptools_scm", "pytest-runner"],
    tests_require=["pytest"],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience:: Science / Research",
        # "License :: OSI Approved:: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ),
)
