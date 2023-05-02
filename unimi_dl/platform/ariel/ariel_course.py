from typing import Optional
import urllib.parse
from bs4 import BeautifulSoup
from bs4.element import Tag

from unimi_dl.course import Course, Section
from unimi_dl.downloadable import Attachment

import unimi_dl.platform.ariel.utils as utils


class ArielSection(Section):
    """
    It's an implementation of a tree

    `self.root` is the root node of Section
    `self.parent` is the parent node of Section: if it's root then is None
    `self.name` is an identifier for the node
    `self.url` is the url associated to the node
    `self.base_url` is the base url of the node (the part till .it)
    `self.attachments` is a list of the attachments of the node. At the first
    call of getAttachments Section will try to retrieve all the attachments of
    the ArielNode and the children
    `self.subsections` is a dictionary with the name and the Section associated with it
    """

    def __init__(self, name: str, url: str) -> None:
        super().__init__(name=name, url=url)
        self.__attachments: list[Attachment] | None = None
        self.__subsections: list[ArielSection] | None = None

    def getAllAttachments(self) -> list[Attachment]:
        attachments = []
        for child in self.getSubsections():
            attachments = attachments + child.getAttachments()
        return self.getAttachments() + attachments

    def getAttachments(self) -> list[Attachment]:
        if self.__attachments is None:
            self.__attachments = []
            html = utils.getPageHtml(self.url)
            threads = utils.findAllArielThreadList(html)  # get threads
            for thread in threads:
                if isinstance(thread, Tag):
                    trs = utils.findAllRows(thread)
                    for tr in trs:
                        self.__attachments = self.__attachments +\
                            utils.findAllAttachments(
                                tr, self.url
                            )
        return self.__attachments

    def getSubsections(self):
        # not sure which edge case was handling this
        if self.__subsections is None:
            html = utils.getPageHtml(self.url)
            self.__subsections = []
            self.__subsections = parseSections(html, self.url)
        return self.__subsections


class ArielCourse(Course):
    def __init__(self, name: str, teachers: list[str], url: str, edition: str) -> None:
        parsed_url = urllib.parse.urlparse(url)
        self.__sections: Optional[list[ArielSection]] = None
        super().__init__(
            name=name,
            teachers=teachers,
            url=parsed_url.geturl(),
            edition=edition)

    def getSections(self) -> list[ArielSection]:
        if self.__sections is None:
            self.__sections = self.__retrieveSections()
        return self.__sections

    def __retrieveSections(self):
        """
        Finds all the sections of a given course specified in `base_url`.
        It looks up `CONTENUTI` endpoint and parses the html page
        """
        sections: list[ArielSection] = []
        parsed_url = urllib.parse.urlparse(self.url)
        if parsed_url.netloc == "labonline.ctu.unimi.it":
            return sections
        api_base_url = urllib.parse.urlunparse(
            (parsed_url.scheme, parsed_url.netloc, utils.API, '', '', ''))
        contents_url = urllib.parse.urljoin(
            api_base_url, utils.CONTENUTI)
        html = utils.getPageHtml(contents_url)
        sections = parseSections(html, contents_url)
        return sections


def parseSections(html: str, url: str) -> list[ArielSection]:
    """
    Parse the html page of the course and returns a list of ArielSection
    """
    sections: list[ArielSection] = []
    parsed_url = urllib.parse.urlparse(url)
    api_base_url = urllib.parse.urlunparse(
        (parsed_url.scheme, parsed_url.netloc, utils.API, '', '', ''))
    page = BeautifulSoup(html, "html.parser")
    a_tags = page.select("tbody.arielRoomList > tr > td > h2 > span > a")
    for a_tag in a_tags:
        href = a_tag.attrs['href']
        section_url = urllib.parse.urljoin(api_base_url, href)
        sections.append(
            ArielSection(
                name=a_tag.get_text(),
                url=section_url,
            )
        )
    return sections
