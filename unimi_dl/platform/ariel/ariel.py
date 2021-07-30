import logging
import re
from unimi_dl.downloadable import Attachment
from unimi_dl.course import Course
import urllib.parse

import unimi_dl.platform.ariel.utils as utils
import unimi_dl.platform.ariel.ariel_course as ariel_course

from ..platform import Platform
from ..session_manager.unimi import UnimiSessionManager

class Ariel(Platform):
    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)
        self.session = UnimiSessionManager.getSession(email=email, password=password)

        self.courses = [] # type: list[Course]
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging in")

    def getCourses(self) -> list[Course]:
        """Returns a list of `Course` of the accessible courses"""
        if not self.courses:
            self.courses = []
            for course in utils.findAllCourses():
                name, teachers, url, edition = course
                self.courses.append(ariel_course.ArielCourse(name=name, teachers=teachers, url=url, edition=edition))
        return self.courses.copy() #it's a shallow copy, need a deep copy maybe?

    def getAttachments(self, url: str) -> list[Attachment]:
        return super().getAttachments(url)

    def get_manifests(self, url: str) -> dict[str, str]:# TODO: remove this
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
