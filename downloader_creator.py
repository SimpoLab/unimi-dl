from interface_downloader import Downloader
from ariel import ArielDownloader

def createDownloader(email: str, password: str, platform: str) -> Downloader:
    """ Factory method to create the appropriate downloader for the request platform
    Should always call this method and never the constructor"""
    if platform == 'ariel':
        downloader = ArielDownloader(email, password)
        return downloader

    raise NotImplementedError
