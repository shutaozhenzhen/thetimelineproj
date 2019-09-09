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


import unittest
from unittest.mock import Mock
from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.repositories.categories import CategoriesFacade


class describe_categories_repository(unittest.TestCase):
    
    def test_return_all_categories(self):
        self.assertEqual(self.all_categories, self.repo.get_all())

    def test_returns_visibility(self):
        category = Mock()
        for case in (True, False):
            self.set_visibility(case)
            self.assertEqual(case, self.repo.is_visible(category))

    def test_returns_event_visibility(self):
        category = Mock()
        for case in (True, False):
            self.set_event_visibility(case)
            self.assertEqual(case, self.repo.is_event_with_category_visible(category))

    def test_get_parents_returns_empty_list(self):
        self.assertEqual([], self.repo.get_parents(self.get_child_without_parents()))

    def test_get_parents_returns_list(self):
        parent, child = self.get_parent_and_child()
        self.assertEqual([parent], self.repo.get_parents(child))

    def test_get_parents_for_checked_childs_returns_list(self):
        self.set_visibility(True)
        parent, child = self.get_parent_and_child()
        self.db.get_categories.return_value = [child]
        parents = self.repo.get_parents_for_checked_childs()
        self.assertEqual([parent], parents)

    def setUp(self):
        self.db = Mock()
        self.all_categories = []
        self.db.get_categories.return_value = self.all_categories
        self.view_properties = Mock(ViewProperties)
        self.repo = CategoriesFacade(self.db, self.view_properties)
        
    def set_visibility(self, value):
        self.view_properties.is_category_visible.return_value = value

    def set_event_visibility(self, value):
        self.view_properties.is_event_with_category_visible.return_value = value

    def get_parent_and_child(self):
        child = Mock()
        parent = Mock()
        child._get_parent.return_value = parent
        parent._get_parent.return_value = None
        return parent, child

    def get_child_without_parents(self):
        child = Mock()
        child._get_parent.return_value = None
        return child
