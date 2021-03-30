#!/usr/bin/env python3

from setuptools import setup
import pathlib
from unimi_dl.__init__ import __version__ as udlv
from unimi_dl.__init__ import __license__ as udll

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="unimi-dl",
    version=udlv,
    description="Script per scaricare videolezioni dai portali Unimi",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aclerici-unimi/unimi-dl",
    author="Alessandro Clerici and Zhifan Chen",
    license=udll,
    classifiers=[],  # to be completed
    packages=["unimi_dl", "unimi_dl.downloader", "unimi_dl.ariel"],
    include_package_data=True,  # ?
    install_requires=["requests", "youtube-dl"],
    entry_points={
        "console_scripts": [
            "unimi-dl=unimi_dl.__main__:main"
        ]
    }
)
