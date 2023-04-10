import logging
import re

from bs4 import BeautifulSoup, Tag
from unimi_dl.downloadable import Attachment
from unimi_dl.course import Course
import urllib.parse
from functools import reduce
import unimi_dl.platform.ariel.utils as utils
import unimi_dl.platform.ariel.ariel_course as ariel_course

from ..platform import Platform
from ..session_manager.unimi import UnimiSessionManager


class Ariel(Platform):
    courses: list[Course] = []

    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)
        self.session = UnimiSessionManager.getSession(
            email=email, password=password)

        self.courses = self.__parseCourses()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging in")

    def getCourses(self) -> list[Course]:
        """Returns a list of `Course` of the accessible courses"""
        return self.courses

    def getAttachments(self, url: str) -> list[Attachment]:
        parsed_url = urllib.parse.urlparse(url)
        attachments_url = parsed_url.geturl()
        html = utils.getPageHtml(attachments_url)
        threads = utils.findAllArielThreadList(html)  # get threads
        # create base url with only scheme and netloc
        base_url = urllib.parse.urlunparse(
            (parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
        attachments = []
        for thread in threads:
            if not isinstance(thread, Tag):
                pass

            trs = utils.findAllRows(thread)
            for tr in trs:
                attachments = attachments + utils.findAllAttachments(
                    tr, base_url
                )

        return attachments

    def get_manifests(self, url: str) -> dict[str, str]:  # TODO: remove this
        self.logger.info("Getting video page")
        video_page = self.session.get(url).text
        self.logger.info("Collecting manifests and video names")
        res = {}
        manifest_re = re.compile(
            r"https://.*?/mp4:.*?([^/]*?)\.mp4/manifest.m3u8")
        for i, manifest in enumerate(manifest_re.finditer(video_page)):
            title = (
                urllib.parse.unquote(manifest[1])
                if manifest[1]
                else urllib.parse.urlparse(url)[1] + str(i)
            )
            while title in res:
                title += "_other"
            res[title] = manifest[0]
        return res

    def __parseCourses(self):
        html = utils.getPageHtml(utils.OFFERTA_FORMATIVA)
        page = BeautifulSoup(html, "html.parser")
        courses_tr_tags = page.select(
            'table.table:nth-child(1) > tbody:nth-child(1) > tr')
        courses: list[Course] = reduce(parseCourseReducer, courses_tr_tags, [])
        return courses


def parseCourseReducer(courses: list[Course], course_tr: Tag) -> list[Course]:
    a_tag = course_tr.select_one(
        'tr > td:nth-child(2) > table:nth-child(2) > tbody:nth-child(1) > \
        tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > h5:nth-child(1) > \
        span:nth-child(1) > span:nth-child(1) > a:nth-child(2)')
    if a_tag is None:
        return courses

    # TODO: filter duplicates
    teacher_list = course_tr.select(
        'tr td.col-md-11 ul.list-user a')

    edition_tag = course_tr.select_one(
        'td:nth-child(2) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > \
        td:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(1) > \
        small:nth-child(1) > span:nth-child(2)'
    )

    edition_txt = edition_tag.get_text() if edition_tag else ""

    course_name = a_tag.get_text()
    course_url = a_tag.attrs['href']
    course = ariel_course.ArielCourse(
        name=course_name,
        url=course_url, teachers=list(
            map(lambda x: x.get_text(), teacher_list)),
        edition=edition_txt)
    courses.append(course)
    return courses
