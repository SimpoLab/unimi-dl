#!/usr/bin/env python3

# Copyright (C) 2021 Alessandro Clerici Lorenzini and Zhifan Chen.
#
# This file is part of unimi-dl.
#
# unimi-dl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# unimi-dl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unimi-dl.  If not, see <https://www.gnu.org/licenses/>.


from setuptools import setup
import pathlib

from unimi_dl.__init__ import __license__ as udll
from unimi_dl.__init__ import __version__ as udlv

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="unimi-dl",
    version=udlv,
    description="Script per scaricare videolezioni dai portali Unimi",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SimpoLab/unimi-dl",
    author="Alessandro Clerici and Zhifan Chen",
    license=udll,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Education",
        "Topic :: Multimedia"
    ],
    packages=["unimi_dl", "unimi_dl.downloader", "unimi_dl.ariel"],
    python_requires=">=3",
    install_requires=["requests", "youtube-dl"],
    entry_points={
        "console_scripts": [
            "unimi-dl=unimi_dl.__main__:main"
        ]
    }
)
