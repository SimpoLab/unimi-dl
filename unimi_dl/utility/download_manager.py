import logging

from pathlib import Path
from typing import Optional

from unimi_dl.downloadable import Attachment

from json import dumps as json_dumps, load as json_load
from json.decoder import JSONDecodeError

logger = logging.getLogger(__name__)

class Downloads:
    def __init__(self, ariel: Optional[list[str]] = [],
        panopto: Optional[list[str]] = [],
        msstream: Optional[list[str]] = []) -> None:

        if ariel is None:
            ariel = []

        if panopto is None:
            panopto = []

        if msstream is None:
            msstream = []

        self.ariel = ariel
        self.panopto = panopto
        self.msstream = msstream

class DownloadManager:
    """
    Manages the `downloaded.json`.
    If the `download.json` specified in `downloaded_path` doesn't exists, it will be created when `save()` will be called
    """
    def __init__(self, downloaded_path: str) -> None:
        self.path = Path(downloaded_path).expanduser()
        try:
            with(self.path.open("r") as downloaded_file):
                try:
                    downloaded_json = json_load(downloaded_file) # type: dict[str, list[str]]
                    # avoid KeyError
                    ariel = downloaded_json.get("ariel")
                    panopto = downloaded_json.get("panopto")
                    msstream = downloaded_json.get("msstream")
                    self.downloaded = Downloads(ariel, panopto, msstream)
                except JSONDecodeError:
                    logging.warning(f"Not valid JSON . Ignoring...")
                    self.downloaded = Downloads()
        except FileNotFoundError:
            logging.warning(f"{self.path} not found. It will be created")
            self.downloaded = Downloads()

    def doDownload(self, platform: str, attachment: Attachment, path: str, dry_run:bool = False, force:bool = False) -> None:
        """
        Downloads the `attachment` in the given `path` and saves it under `platform`.
        If `dry_run` is True then the `attachment` is only added to the downloaded list but not effectively downloaded
        If `force` is True then the `attachment` will be downloaded even if it's already in the downloaded list (by default is False)
        TODO: 
        - to change, need a better way to handle type hinting
        """
        l = getattr(self.downloaded, platform) # type: list[str]
        if not isinstance(attachment, Attachment):
            raise Exception(f"{attachment} is not an Attachment")
        if attachment.url not in l or force:
            if dry_run or attachment.download(path):
                l.append(attachment.url)
                setattr(self.downloaded, platform, l)
        else:
            logger.warning(f"{attachment} already downloaded")


    def save(self) -> None:
        """
        Writes the changes to the `self.path`
        """
        with(self.path.open("w") as downloaded_file):
            downloaded_file.write(json_dumps(self.downloaded.__dict__))

    def wipeDownloaded(self, platform: str, to_removed: list[str]) -> None:
        l = getattr(self.downloaded, platform) # type: list[str]
        for entry in to_removed:
            l.remove(entry)

        setattr(self.downloaded, platform, l)
        self.save()

    def getDownloadFrom(self, platform: str) -> list[str]:
        """
        Gets a list of url of downloaded attachments
        """
        return getattr(self.downloaded, platform) # list[str]
        

    def getDownloads(self) -> Downloads:
        return self.downloaded
