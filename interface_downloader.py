from ariel import ArielDownloader
from __future__ import annotations


class Downloader:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        pass

    def download(self):
        pass

    @staticmethod
    def createDownloader(username: str, password: str, platform: str) -> Downloader:
        if platform == 'ariel':
            return ArielDownloader(username, password)
        
        
