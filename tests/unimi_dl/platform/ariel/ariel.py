import os
from unittest import TestCase
from unittest import mock
from unittest.mock import MagicMock, patch

from unimi_dl.platform.ariel.ariel import Ariel
from unimi_dl.platform.ariel.ariel_course import ArielCourse

OFFERTA_MYOF_STUB_PATH = os.path.join(
    os.path.dirname(__file__), 'offerta_myof.html')


class ArielTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.email = "test@example.com"
        cls.password = "secret"

    def test_getCourses(self):
        with mock.patch('unimi_dl.platform.ariel.utils.getPageHtml') \
                as mock_getPageHtml, open(OFFERTA_MYOF_STUB_PATH, 'r') as myof:
            mock_getPageHtml.return_value = myof.read()
            self.ariel = Ariel(self.email, self.password)
            courses = self.ariel.getCourses()
            for course in courses:
                print('course', course)
                self.assertIsInstance(course, ArielCourse)
