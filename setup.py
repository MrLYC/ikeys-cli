# coding: utf-8

from setuptools import setup

setup(
    name="ikeys-cli",
    packages=["ikeys_cli"],
    version="0.3.3",
    description="ikeystone python client",
    url="https://github.com/MrLYC/ikeys-cli",
    author="MrLYC",
    author_email="imyikong@gmail.com",
    license="MIT",
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
    ],
    keywords=["ikeystone"],
    install_requires=["requests>=2.7.0", "IFV>=0.1.4"],
)
