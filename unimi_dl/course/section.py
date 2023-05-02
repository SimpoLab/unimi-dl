from __future__ import annotations

from urllib.parse import urlparse
from unimi_dl.downloadable import Attachment


class Section:
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = urlparse(url).geturl()

    def getAllAttachments(self) -> list[Attachment]:
        """
        Get all attachments from `self` and `self.subsections`
        """
        raise NotImplementedError

    def getAttachments(self) -> list[Attachment]:
        raise NotImplementedError

    def getSubsections(self) -> list[Section]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.name
