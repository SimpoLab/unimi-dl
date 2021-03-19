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


from os import listdir
import re


def filename_number(prefix):
    ls = listdir("unimi-dl_output")
    file_regex = re.compile(prefix + r'_\d\d\d\.', re.IGNORECASE)
    number_regex = re.compile(r'\d+')
    retval = 1
    for file in ls:
        match = file_regex.match(file)
        if match:
            num = int(number_regex.search(match.group(0)).group(0))
            if num >= retval:
                retval = num+1
    return '%03d' % retval
