import logging
from urllib.parse import urlparse

import unimi_dl.downloadable.utils as utils

logger = logging.getLogger(__name__)


class Attachment:
    def __init__(self, name: str, filetype: str, url: str, section_name: str, description: str = "") -> None:
        self.section_name = section_name
        sane_name = utils.sanitize(name)
        self.name = sane_name
        self.url = urlparse(url).geturl()
        self.description = description
        self.filetype = filetype
        if self.filetype == "video":
            self._download = utils.download_by_ydl
        elif self.filetype == "document":
            self._download = utils.download_by_requests
        else:
            raise NotImplementedError(
                f"{self.filetype} filetype download not supported")

    def download(self, path_prefix: str) -> bool:
        import os
        path = os.path.join(path_prefix, self.name)
        msg = f"Downloading '{path}'"
        logger.info(msg)
        print(msg)
        result = self._download(self.url, path)

        if result:
            msg = f"Download {path} completed"
            print(msg)
            logger.info(msg)
        else:
            msg = f"Error occurred during {path} download. Please retry."
            print(msg)
            logger.info(msg)

        return result

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return f"{self.name}"
