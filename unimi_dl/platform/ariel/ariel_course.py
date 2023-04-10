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
        self.has_subsections = (
            False  # indicates if it already retrieved the available subsections
        )
        self.has_attachments = False

    def getAllAttachments(self) -> list[Attachment]:
        attachments = []
        for child in self.subsections:
            attachments = attachments + child.getAttachments()
        return self.getAttachments() + attachments

    def getAttachments(self) -> list[Attachment]:
        if not self.has_attachments:
            html = utils.getPageHtml(self.url)
            threads = utils.findAllArielThreadList(html)  # get threads
            for thread in threads:
                if isinstance(thread, Tag):
                    trs = utils.findAllRows(thread)
                    for tr in trs:
                        self.attachments = self.attachments + utils.findAllAttachments(
                            tr, self.url
                        )

            self.has_attachments = True
        return self.attachments.copy()

    def getSubsections(self) -> list[Section]:
        # not sure which edge case was handling this
        html = utils.getPageHtml(self.url)
        print('html', html)
        self.sections = parseSections(html, self.url)
        # if not self.has_subsections:
        #     html = utils.getPageHtml(self.url)
        #     rooms = utils.findAllArielRoomsList(html)  # get subsections

        #     for thread in rooms:
        #         if isinstance(thread, Tag):
        #             trs = utils.findAllRows(thread)
        #             for tr in trs:
        #                 a_tags = utils.findAllATags(tr)
        #                 for a in a_tags:
        #                     href = a.get("href")
        #                     if isinstance(href, str):
        #                         self.addSection(name=a.get_text(), url=href)

        #     self.has_subsections = True
        return self.subsections

    def addSection(self, name: str, url: str):
        self.subsections.append(
            ArielSection(
                name=name, url=url
            )
        )
        return True


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
        test: list[ArielSection] | None = None
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
        print('html', html)
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
