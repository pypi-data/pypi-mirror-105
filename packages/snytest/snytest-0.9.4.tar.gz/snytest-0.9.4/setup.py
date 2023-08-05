#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import pathlib

from setuptools import find_packages
from setuptools import setup
from version import __version__

here = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (here / "pypidesc.md").read_text(encoding="utf-8")
setup(
    version=__version__,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "click",
        "certifi",
        "delphixpy",
        "python-dateutil",
        "colorama",
        "tabulate",
        "cryptography",
        "pytz"
    ],
    # Format is mypkg.mymodule:the_function'
    entry_points="""
        [console_scripts]
        dxi=dxi.dxi:dxi
    """,
    author="sunny",
    keywords="automation",  # noqa
    license="Apache 2",
    description=("test"),
    dependency_links=[],
    name="snytest",  #
    long_description_content_type="text/markdown",
    long_description=long_description,
    include_package_data=True,
    project_urls={},  # Optional
)
