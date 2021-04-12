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

import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from .ariel import get_ariel_session
from .platform import Platform


def get_panopto_session(email: str, password: str) -> requests.Session:
    s = get_ariel_session(email, password)
    auth_url = r"https://unimi.cloud.panopto.eu/Panopto/Pages/Auth/Login.aspx?instance=Labonline"
    disable_warnings(InsecureRequestWarning)
    s.get(auth_url, verify=False)
    return s


class Panopto(Platform):
    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging in")
        self.session = get_panopto_session(email, password)

    def get_manifests(self, url: str) -> list[tuple[str, str]]:
        self.logger.info("Getting video page")
        video_page = self.session.get(url).text

        iframe_re = re.compile(r"<iframe src=\"(.*?)\"")
        iframe_url = iframe_re.search(video_page)[1]
        self.logger.debug(f"iframe URL: {iframe_url}")
        manifest_page = self.session.get(iframe_url).text

        self.logger.info("Collecting manifests")
        manifest_re = re.compile(r"\"VideoUrl\":\"(https:.*?\.m3u8)\"")
        manifest = manifest_re.search(manifest_page)[1].replace("\\", "")

        self.logger.info("Fetching video names")
        title_re = re.compile(r"<title>(.*?)</title>")
        filename = title_re.search(manifest_page)[1]

        return [(filename, manifest)]
