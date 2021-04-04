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

from __future__ import annotations

class Downloader:
    def __init__(self, email: str, password: str) -> None:
        self.email    = email
        self.password = password

    def get_videos(self, url: str) -> list[str]:
        """ Returns a list of links, which corresponds to the videos available for download, from the {url}
        {url} must be the root page where the videos are published"""
        raise NotImplementedError

    def download(self, url: str, dst: str):
        """ Downloads file from the provided {url} and saves it in {dst}
        Note that the path should include the name to be assigned to the downloaded file"""
        raise NotImplementedError
