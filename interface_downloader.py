from __future__ import annotations

class Downloader:
    def __init__(self, email: str, password: str) -> None:
        self.email    = email
        self.password = password

    def get_videos(self, url: str) -> list[str]:
        """ Returns a list of links, which corresponds to the videos available for download, from the {url}
        {url} must be the root page where the videos are published"""
        raise NotImplementedError

    def download(self, url: str, dst: str):
        """ Downloads file from the provided {url} and saves it in {dst}
        Note that the path should include the name to be assigned to the downloaded file"""
        raise NotImplementedError
