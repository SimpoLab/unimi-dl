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
    `self.attachments` is a list of the attachments of the node. At the first call of getAttachments Section will try to retrieve all the attachments of the ArielNode and the children
    `self.subsections` is a dictionary with the name and the Section associated with it
    """

    def __init__(self, name: str, url: str, base_url: str, parent_section=None) -> None:
        if url.startswith("ThreadList.aspx"):
            url = base_url + utils.API + url
        super().__init__(
            name=name, url=url, base_url=base_url, parent_section=parent_section
        )
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
                            tr, self.base_url
                        )

            self.has_attachments = True
        return self.attachments.copy()

    def getSubsections(self) -> list[Section]:
        if not self.has_subsections:
            html = utils.getPageHtml(self.url)
            rooms = utils.findAllArielRoomsList(html)  # get subsections

            for thread in rooms:
                if isinstance(thread, Tag):
                    trs = utils.findAllRows(thread)
                    for tr in trs:
                        a_tags = utils.findAllATags(tr)
                        for a in a_tags:
                            href = a.get("href")
                            if isinstance(href, str):
                                self.addSection(name=a.get_text(), url=href)

            self.has_subsections = True
        return self.subsections

    def addSection(self, name: str, url: str):
        self.subsections.append(
            ArielSection(
                name=name, url=url, base_url=self.base_url, parent_section=self
            )
        )
        return True


class ArielCourse(Course):
    def __init__(self, name: str, teachers: list[str], url: str, edition: str) -> None:
        super().__init__(name=name, teachers=teachers, url=url, edition=edition)
        self.sections = []  # type: list[Section]

    def getSections(self) -> list[Section]:
        if not self.sections:
            self.sections = utils.findAllSections(self.base_url)

        return self.sections
