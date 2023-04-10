import os
from unittest import TestCase
from unittest import mock


from unimi_dl.platform.ariel.ariel import Ariel
from unimi_dl.platform.ariel.ariel_course import ArielCourse, ArielSection

from ..ariel import OFFERTA_MYOF_STUB_PATH

COURSE_MAIN_PAGE_STUB_PATH = os.path.join(
    os.path.dirname(__file__), 'course_main_page.html')

COURSE_SUBSECTION_1_STUB_PATH = os.path.join(
    os.path.dirname(__file__), 'subsection_1.html')

COURSE_SUBSECTION_2_STUB_PATH = os.path.join(
    os.path.dirname(__file__), 'subsection_2.html')


class ArielCourseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.email = "test@example.com"
        cls.password = "secret"

    def test_getCourses(self):
        with mock.patch('unimi_dl.platform.ariel.utils.getPageHtml') \
                as mock_getPageHtml,\
                open(OFFERTA_MYOF_STUB_PATH, 'r') as myof,\
                open(COURSE_MAIN_PAGE_STUB_PATH, 'r') as course_main_page,\
                open(COURSE_SUBSECTION_1_STUB_PATH, 'r') as course_subsection1_page,\
                open(COURSE_SUBSECTION_2_STUB_PATH, 'r') as course_subsection2_page:

            mock_getPageHtml.side_effect = [
                myof.read(),
                course_main_page.read(),
                course_subsection1_page.read(),
                course_subsection2_page.read(),
            ]

            self.ariel = Ariel(self.email, self.password)
            courses = self.ariel.getCourses()

            test_course = next(filter(lambda course: course.name ==
                                      "Architettura degli elaboratori II Edizione 1",
                                      courses))

            print('test_course', test_course)
            self.assertIsInstance(test_course, ArielCourse)
            for section in test_course.getSections():
                print('section', section)
                self.assertIsInstance(section, ArielSection)
