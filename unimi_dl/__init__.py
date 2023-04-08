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


__version__ = "0.3.1"
__license__ = "GPL v.3"


from os.path import join
from pathlib import Path
import sys
import unimi_dl.cmd as cmd


def get_data_dir() -> Path:
    """Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming"""

    home = Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"
    else:
        raise NotImplementedError


LOCAL = join(get_data_dir(), "unimi-dl")
CREDENTIALS = join(LOCAL, "credentials.json")
DOWNLOADED = join(LOCAL, "downloaded.json")
LOG = join(LOCAL, "log.txt")
AVAILABLE_PLATFORMS = ["ariel", "panopto"]

__all__ = ["cmd", "LOCAL", "CREDENTIALS",
           "DOWNLOADED", "LOG", "AVAILABLE_PLATFORMS"]
