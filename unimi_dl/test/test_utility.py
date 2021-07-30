from unimi_dl.course import Course, Section
from pathlib import Path
import unittest
from ..platform import Ariel
import os

class TestUtility(unittest.TestCase):
    def setUp(self) -> None:
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        if self.username == None:
            raise EnvironmentError("No Username provided")

        if self.password == None:
            raise EnvironmentError("No Password provided")

        self.ariel = Ariel(self.username, self.password)

        self.path_test = Path("./test/")
        self.path_test.mkdir(parents=True, exist_ok=True)
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_credential_manager(self):
        from unimi_dl.utility.credentials_manager import CredentialsManager
        credentials_manager = CredentialsManager("~/.local/share/unimi-dl/credentials.json")
        credentials = credentials_manager.getCredentials()
        assert(credentials.email == self.username)
        assert(credentials.password == self.password)

    def test_download_manager(self):
        from unimi_dl.utility.download_manager import DownloadManager
        download_manager = DownloadManager("./test/downloaded.json")

        ariel = self.ariel
        courses = ariel.getCourses()
        course = courses[0]
        video = None
        document = None
        for section in course.getSections():
            if video is not None and document is not None:
                download_manager.doDownload("ariel", document, str(self.path_test))
                assert(Path(str(self.path_test), document.name).exists())

                #download_manager.doDownload("ariel", video, str(self.path_test))
                #assert(Path(str(self.path_test), video.name).exists())

                download_manager.save()
                downloaded_json = read_from_json(str(download_manager.path))
                #assert(video.url in downloaded_json["ariel"])
                assert(document.url in downloaded_json["ariel"])
                break

            attachments = section.getAttachments()
            for attachment in attachments:
                
                if video is not None and document is not None:
                    break

                if video is None and attachment.filetype == "video":
                    video = attachment

                if document is None and attachment.filetype == "document":
                    document = attachment


def read_from_json(path: str):
    from json import dumps as json_dumps, load as json_load
    with(open(path, "r") as json_file):
        dict = json_load(json_file)
        return dict
    
if __name__ == '__main__':
    unittest.main()
