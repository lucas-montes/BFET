#!/usr/bin/env python

"""The setup script."""

from pathlib import Path
from setuptools import setup, find_packages

history = Path("HISTORY.rst").read_text()

requirements = [
    "Jinja2",
    "requests",
    "deepdiff[optimize]",
    "types-requests",
]

test_requirements = [
    "pytest",
    "django",
    "pydantic",
]

setup(
    author="Lucas Montes",
    author_email="lluc23@hotmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description=(
        "Better Faster Easier Testing. Create data models quickly and easly, create different"
        " data types for testing cases or create default tests files"
    ),
    entry_points={
        "console_scripts": [
            "bfet=bfet.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=Path("README.rst").read_text(),
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="bfet",
    name="bfet",
    packages=find_packages(include=["bfet", "bfet.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/lluc2397/bfet",
    version="0.1.11",
    zip_safe=False,
)
