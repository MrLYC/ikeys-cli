# coding: utf-8

import os

from setuptools import setup

long_description = ""
if os.path.exists("README"):
    with open("README", "rt") as fp:
        long_description = fp.read()
elif os.path.exists("README.md"):
    with open("README.md", "rt") as fp:
        long_description = fp.read()


setup(
    name="ikeys-cli",
    packages=["ikeys_cli"],
    version="0.3.7",
    description="ikeystone python client",
    url="https://github.com/MrLYC/ikeys-cli",
    long_description=long_description,
    author="MrLYC",
    author_email="imyikong@gmail.com",
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords=["ikeystone"],
    install_requires=["requests>=2.7.0", "IFV>=0.1.4"],
)
