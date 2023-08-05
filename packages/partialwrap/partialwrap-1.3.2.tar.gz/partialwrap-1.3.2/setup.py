#!/usr/bin/env python
"""
partialwrap: A small Python library providing wrappers for external
             executables and Python functions so that they can easily be
             partialised with Python's functools.partial.
"""
from __future__ import division, absolute_import, print_function
import os
import codecs
import re
from setuptools import setup  # , find_packages


# find __version__

def _iread(*fparts):
    """ Read file data. """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *fparts), "r") as fp:
        return fp.read()


def _find_version(*file_paths):
    """Find version without importing module."""
    version_file = _iread(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# setup

package   = "partialwrap"
doclines  = "A small Python library providing wrappers for external"
doclines += " executables and Python functions so that they can easily"
doclines += " be partialised with Python's functools.partial"
readme   = open("README.md").read()

author = "Matthias Cuntz"
email  = "mc@macu.de"

version = _find_version(package, "version.py")

scripts = []

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Atmospheric Science",
    "Topic :: Scientific/Engineering :: Hydrology",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Software Development",
    "Topic :: Utilities",
]

setup(
    name                 = package,
    version              = version,
    maintainer           = author,
    maintainer_email     = email,
    description          = doclines,
    long_description     = readme,
    long_description_content_type = "text/markdown",
    author               = author,
    author_email         = email,
    url                  = "https://github.com/mcuntz/"+package,
    license              = "MIT",
    classifiers          = classifiers,
    platforms            = ["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    include_package_data = True,
    install_requires     = ["numpy"],
    extras_require       = {},
    packages             = [package], # find_packages(exclude=["tests*", "docs*"]),
    scripts              = scripts,
)
