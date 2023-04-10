import os
from unittest import TestCase
from unittest import mock
from unimi_dl.downloadable.attachment import Attachment


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
                # parse all courses
                myof.read(),
                # select main page
                course_main_page.read(),
                # click on main page link
                course_subsection1_page.read(),
                # clink on subsection 1 link
                course_subsection2_page.read(),
            ]

            self.ariel = Ariel(self.email, self.password)
            courses = self.ariel.getCourses()

            test_course = next(filter(lambda course: course.name ==
                                      "Architettura degli elaboratori II Edizione 1",
                                      courses))

            print('test_course', test_course)
            self.assertIsInstance(test_course, ArielCourse)
            test_section = next(filter(
                lambda section: section.name == "Laboratorio 2021/2022 (VECCHIO)",
                test_course.getSections()))
            print('test_section', test_section)
            self.assertIsInstance(test_section, ArielSection)
            test_subsection = next(filter(
                lambda subsection: subsection.name == "Turno B - Rivolta",
                test_section.getSubsections()))
            print('test_subsection', test_subsection.getAttachments())
            self.assertIsInstance(test_subsection, ArielSection)
            for attachment in test_subsection.getAttachments():
                self.assertIsInstance(attachment, Attachment)
                print(attachment, '\n\n')
