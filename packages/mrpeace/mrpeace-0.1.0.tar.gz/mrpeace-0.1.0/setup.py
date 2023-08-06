#!/usr/bin/env python3

from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="mrpeace",
    version="0.1.0",
    description="Basic Cli",
    packages=find_packages(),
    include_package_date=True,
    author="Claudio Lau",
    author_email="claudio.lau12@gmail.com",
    license="Apache 2.0",
    classifiers=classifiers,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        mrpeace=mrpeace.cli:cli
    """,
)
