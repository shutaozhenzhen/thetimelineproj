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


from timelinelib.canvas.data import Category
from timelinelib.canvas.data.category import EXPORTABLE_FIELDS
from timelinelib.canvas.data.category import sort_categories
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_category
from timelinelib.test.utils import a_category_with
from timelinelib.test.utils import CATEGORY_MODIFIERS


class describe_category(UnitTestCase):

    def test_can_get_values(self):
        category = Category().update("work", (50, 100, 150), (0, 0, 0))
        self.assertEqual(category.get_id(), None)
        self.assertEqual(category.get_name(), "work")
        self.assertEqual(category.get_color(), (50, 100, 150))
        self.assertEqual(category.get_font_color(), (0, 0, 0))
        self.assertEqual(category._get_parent(), None)

    def test_can_set_values(self):
        self.assertEqual(a_category().set_id(15).get_id(), 15)
        self.assertEqual(a_category().set_name("fun").get_name(), "fun")
        self.assertEqual(a_category().set_color((33, 66, 99)).get_color(), (33, 66, 99))
        self.assertEqual(a_category().set_progress_color((33, 66, 97)).get_progress_color(), (33, 66, 97))
        self.assertEqual(a_category().set_done_color((33, 66, 98)).get_done_color(), (33, 66, 98))
        self.assertEqual(a_category().set_font_color((11, 12, 13)).get_font_color(), (11, 12, 13))
        a_parent = a_category_with(name="parent")
        self.assertEqual(a_category().set_parent(a_parent)._get_parent(), a_parent)

    def test_has_exportable_fields(self):
        self.assertEqual(a_category().get_exportable_fields(), EXPORTABLE_FIELDS)

    def test_can_be_compared(self):
        self.assertEqNeImplementationIsCorrect(a_category, CATEGORY_MODIFIERS)


class describe_category_list_sorting(UnitTestCase):

    def test_sorts_categories_by_name(self):
        self.sort([
            a_category_with(name="b"),
            a_category_with(name="a")])
        self.assert_sorted_in_order(["a", "b"])

    def test_ignores_case(self):
        self.sort([
            a_category_with(name="Foo"),
            a_category_with(name="bar")])
        self.assert_sorted_in_order(["bar", "Foo"])

    def sort(self, categories):
        self.sorted_categories = sort_categories(categories)

    def assert_sorted_in_order(self, names):
        self.assertEqual(
            names,
            [category.get_name() for category in self.sorted_categories])
