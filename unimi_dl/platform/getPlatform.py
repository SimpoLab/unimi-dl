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

from .ariel import Ariel
from .panopto import Panopto
from .platform import Platform


def getPlatform(email: str, password: str, platform: str) -> Platform:
    """ Factory method to create the appropriate Platform instance. """

    if platform == 'ariel':
        return Ariel(email, password)
    if platform == 'panopto':
        return Panopto(email, password)

    raise NotImplementedError
