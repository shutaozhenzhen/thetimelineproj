# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018  Rickard Lindberg, Roger Lindberg
#
# This file is part of Timeline.
#
# Timeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Timeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Timeline.  If not, see <http://www.gnu.org/licenses/>.


from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.help.helppagerepository import HelpPageRepository
from timelinelib.help.helppagerepository import HelpPage


HOME_PAGE_ID = "contents"
HELP_RESOURCES_ROOT_DIR = "root_dir"
PAGE_PREFIX = "page:"
PAGE_ID = "id"
PAGE_HEADER = "header"
PAGE_BODY = "body"


class HelpPageRepositoryUnitTestCase(UnitTestCase):

    def setUp(self):
        UnitTestCase.setUp(self)
        self.repository = HelpPageRepository(HOME_PAGE_ID, HELP_RESOURCES_ROOT_DIR, PAGE_PREFIX)


class describe_help_page_repoistory_instansiation(HelpPageRepositoryUnitTestCase):

    def test_has_an_empty_page_dictionary_when_instatiated(self):
        self.assertEqual({}, self.repository.help_pages)

    def test_is_given_a_home_page_id_when_instatiated(self):
        self.assertEqual(HOME_PAGE_ID, self.repository.home_page)

    def test_is_given_a_help_resources_root_dir_when_instatiated(self):
        self.assertEqual(HELP_RESOURCES_ROOT_DIR, self.repository.help_resources_root_dir)

    def test_is_given_a_page_prefix_when_instatiated(self):
        self.assertEqual(PAGE_PREFIX, self.repository.page_prefix)


class describe_help_page_repoistory_page_creation(HelpPageRepositoryUnitTestCase):

    def test_a_page_can_be_created_and_saved(self):
        self.repository.install_page(None, None, None, None)
        self.assertEqual(1, len(self.repository.help_pages))

    def test_created_pages_are_of_correct_type(self):
        self.repository.install_page(None, None, None, None)
        keys = self.repository.help_pages.keys()
        page = self.repository.help_pages[next(iter(keys))]
        self.assertTrue(isinstance(page, HelpPage))

    def test_pages_are_defined_by_id_header_body_and_related_pages(self):
        self.repository.install_page(PAGE_ID, PAGE_HEADER, PAGE_BODY, [])

    def test_related_pages_has_default_value(self):
        self.repository.install_page(PAGE_ID, PAGE_HEADER, PAGE_BODY)
        page = self.repository.get_page(PAGE_ID)
        self.assertEqual([], page.related_pages)

    def test_pages_has_id_header_body_and_related_pages(self):
        self.repository.install_page(PAGE_ID, PAGE_HEADER, PAGE_BODY, [])
        page = self.repository.get_page(PAGE_ID)
        self.assertEqual(PAGE_ID, page.page_id)
        self.assertEqual(PAGE_HEADER, page.header)
        self.assertEqual(PAGE_BODY, page.body)
        self.assertEqual([], page.related_pages)


class describe_help_page_repoistory_page_retrieval(HelpPageRepositoryUnitTestCase):

    def test_pages_can_be_retrieved_by_page_id(self):
        self.repository.install_page(PAGE_ID, PAGE_HEADER, PAGE_BODY, [])
        page = self.repository.get_page(PAGE_ID)
        self.assertTrue(page)

    def test_pages_not_crated_cannot_be_retrieved(self):
        page = self.repository.get_page(PAGE_ID)
        self.assertFalse(page)

    def test_pages_can_be_found_by_text_search_in_header(self):
        self.repository.install_page(PAGE_ID, PAGE_HEADER, PAGE_BODY, [])
        pages = self.repository._find_pages(PAGE_HEADER)
        self.assertEqual(1, len(pages))
        self.assertEqual(PAGE_HEADER, pages[0].header)


class describe_help_page_repoistory_page_search(HelpPageRepositoryUnitTestCase):

    def test_pages_can_be_found_by_text_search_in_body(self):
        self.repository.install_page(PAGE_ID, PAGE_HEADER, PAGE_BODY, [])
        pages = self.repository._find_pages("body")
        self.assertEqual(1, len(pages))
        self.assertEqual(PAGE_HEADER, pages[0].header)

    def test_serach_result_page_rendered_when_no_matches_found(self):
        serach_result_page = self.repository.get_search_results_page("body")
        self.assertEqual(
            u"<h1>⟪Search results for 'body'⟫</h1><ul></ul>",
            serach_result_page
        )

    def test_serach_result_page_rendered_when_matches_found(self):
        self.repository.install_page(PAGE_ID, PAGE_HEADER, PAGE_BODY, [])
        serach_result_page = self.repository.get_search_results_page("body")
        self.assertEqual(
            u'<h1>⟪Search results for \'body\'⟫</h1><ul><li><a href="page:id">header</a></li></ul>',
            serach_result_page
        )


class HelpPageUnitTestCase(UnitTestCase):

    def setUp(self):
        UnitTestCase.setUp(self)
        self.repository = HelpPageRepository(HOME_PAGE_ID, HELP_RESOURCES_ROOT_DIR, PAGE_PREFIX)
        self.help_page = HelpPage(self.repository, PAGE_ID, PAGE_HEADER, PAGE_BODY, [])


class describe_help_page(HelpPageUnitTestCase):

    def test_has_ref_to_repository(self):
        self.assertEqual(self.repository, self.help_page.help_page_repository)

    def test_has_id_header_body_and_related_pages(self):
        self.assertEqual(PAGE_ID, self.help_page.page_id)
        self.assertEqual(PAGE_HEADER, self.help_page.header)
        self.assertEqual(PAGE_BODY, self.help_page.body)
        self.assertEqual([], self.help_page.related_pages)

    def test_can_be_rendered_to_html(self):
        self.assertEqual("<h1>%s</h1><p>%s</p>" % (PAGE_HEADER, PAGE_BODY), self.help_page.render_to_html())

    def test_can_be_rendered_to_html_with_related_pages(self):
        self.repository.install_page("foo", PAGE_HEADER, PAGE_BODY, [])
        self.repository.install_page("bar", PAGE_HEADER, PAGE_BODY, [])
        self.help_page = HelpPage(self.repository, PAGE_ID, PAGE_HEADER, PAGE_BODY, ["foo", "bar"])
        self.assertEqual(
            u'<h1>header</h1><p>body</p><h2>⟪Related pages⟫</h2><ul><li><a href="page:foo">header</a></li><li><a href="page:bar">header</a></li></ul>',
            self.help_page.render_to_html()
        )

    def test_can_be_rendered_to_html_with_related_pages_not_found(self):
        self.help_page = HelpPage(self.repository, PAGE_ID, PAGE_HEADER, PAGE_BODY, ["foo", "bar"])
        self.assertEqual(
            u'<h1>%s</h1><p>%s</p><h2>⟪Related pages⟫</h2><ul></ul>' % (PAGE_HEADER, PAGE_BODY),
            self.help_page.render_to_html()
        )
