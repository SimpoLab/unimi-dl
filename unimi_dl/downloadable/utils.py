from __future__ import annotations
from typing import Any
import logging
import unicodedata
import re
from unimi_dl.platform.session_manager.unimi import UnimiSessionManager


def download_by_ydl(url: str, path: str) -> bool:
    import youtube_dl

    logger = logging.getLogger("youtube-dl")
    ydl_opts = {
        "v": "true",
        "nocheckcertificate": "true",
        "restrictfilenames": "true",
        "logger": logger,
        "quiet": logger.level != logging.INFO
    }

    #ydl_opts["outtmpl"] = path + ".%(ext)s"
    ydl_opts["outtmpl"] = path
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return True


def download_by_requests(url: str, path: str) -> bool:

    session = UnimiSessionManager.getSession()
    r = session.get(url)

    with(open(path, "wb") as file):
        file.write(r.content)

    return True


def sanitize(value: Any) -> str:
    """
    Removes trailing underscores and hyphens, whitespaces, parentheses and %
    """
    value = str(value)
    value = unicodedata.normalize('NFKC', value)
    return re.sub(r'[\s()%]+', '', value).strip('-_')
