from unimi_dl.course import Section, Course
import unittest
from ..platform import Ariel
import os


class TestAriel(unittest.TestCase):
    def setUp(self) -> None:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        if username is None:
            raise EnvironmentError("No Username provided")

        if password is None:
            raise EnvironmentError("No Password provided")

        self.courses = []
        self.instance = Ariel(email=username, password=password)
        return super().setUp()

    def tearDown(self) -> None:
        self.instance.session.close()
        return super().tearDown()

    def test_create(self):
        assert isinstance(self.instance, Ariel)

    def test_getcourses(self):
        ariel = self.instance

        self.courses = ariel.getCourses()
        for course in self.courses:
            assert isinstance(course, Course)

    def test_course_getAttachments_and_download(self):
        ariel = self.instance

        courses = ariel.getCourses()
        course = courses[0]
        for section in course.getSections():
            assert isinstance(section, Section)
            assert section != ""
            attachments = section.getAttachments()
            video = None
            document = None
            for attachment in attachments:
                if video is not None and document is not None:
                    break

                if video is None and attachment.filetype == "video":
                    video = attachment

                if document is None and attachment.filetype == "document":
                    document = attachment

            #            if video is not None:
            #                video.download("./output/")

            if document is not None:
                document.download("./output/")


if __name__ == "__main__":
    unittest.main()
