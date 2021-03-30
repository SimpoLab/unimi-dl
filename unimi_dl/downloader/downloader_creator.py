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


from unimi_dl.ariel.ariel import ArielDownloader
from unimi_dl.downloader.interface_downloader import Downloader


def createDownloader(email: str, password: str, platform: str, stdout_loglevel: int) -> Downloader:
    """ Factory method to create the appropriate downloader for the request platform
    Should always call this method and never the constructor"""
    if platform == 'ariel':
        downloader = ArielDownloader(email, password, stdout_loglevel)
        return downloader

    raise NotImplementedError
