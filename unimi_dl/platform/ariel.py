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
import logging
import re
import urllib.parse

import requests

from .platform import Platform


def get_ariel_session(email: str, password: str) -> requests.Session:
    s = requests.Session()
    login_url = 'https://elearning.unimi.it/authentication/skin/portaleariel/login.aspx?url=https://ariel.unimi.it/'
    payload = {'hdnSilent': 'true',
               'tbLogin': email,
               'tbPassword': password}
    s.post(login_url, data=payload)
    return s


class Ariel(Platform):
    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging in")
        self.session = get_ariel_session(email, password)

    def get_manifests(self, url: str) -> dict[str, str]:
        self.logger.info("Getting video page")
        video_page = self.session.get(url).text

        self.logger.info("Collecting manifests and video names")
        res = {}
        manifest_re = re.compile(
            r"https://.*?/mp4:.*?([^/]*?)\.mp4/manifest.m3u8")
        for i, manifest in enumerate(manifest_re.finditer(video_page)):
            title = urllib.parse.unquote(
                manifest[1]) if manifest[1] else urllib.parse.urlparse(url)[1]+str(i)
            while title in res:
                title += "_other"
            res[title] = manifest[0]
        return res
