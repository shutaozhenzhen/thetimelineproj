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


from unittest.mock import Mock

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.wxgui.dialogs.categoryfinder.controller import CategoryFinderDialogController
from timelinelib.wxgui.dialogs.categoryfinder.view import CategoryFinderDialog
from timelinelib.wxgui.frames.mainframe.mainframe import MainFrame
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_category_with
from timelinelib.proxies.sidebar import SidebarProxy


A_CATEGORIES = [a_category_with("Aaaa"),
                a_category_with("Abc"), ]

CATEGORIES = A_CATEGORIES + [a_category_with("xxx")]


class describe_category_finder_dialog_controller(UnitTestCase):

    def setUp(self):
        self.mainframe = Mock(MainFrame)
        self.db = Mock(MemoryDB)
        self.db.get_categories.return_value = CATEGORIES
        self.view = Mock(CategoryFinderDialog)
        self.view.GetTarget.return_value = "A"
        self.controller = CategoryFinderDialogController(self.view)
        self.controller.on_init(self.db, None)
        self.proxy = Mock(SidebarProxy)
        self.controller.set_sidebar_proxy(self.proxy)

    def test_handles_char_entries(self):
        self.controller.on_char(None)
        self.view.SetCategories.assert_called_with([category.name for category in A_CATEGORIES])

    def test_categories_can_be_checked(self):
        self.controller.on_check(None)
        self.proxy.check_categories.assert_called_with(A_CATEGORIES)

    def test_categories_can_be_unchecked(self):
        self.controller.on_uncheck(None)
        self.proxy.uncheck_categories.assert_called_with(A_CATEGORIES)
