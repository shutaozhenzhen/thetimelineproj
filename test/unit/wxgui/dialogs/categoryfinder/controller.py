# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
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


from mock import Mock

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.wxgui.dialogs.categoryfinder.controller import CategoryFinderDialogController
from timelinelib.wxgui.dialogs.categoryfinder.view import CategoryFinderDialog
from timelinelib.wxgui.frames.mainframe.mainframe import MainFrame
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import a_category_with


class describe_category_finder_dialog(UnitTestCase):

    def setUp(self):
        self.mainframe = Mock(MainFrame)
        self.db = Mock(MemoryDB)
        self.db.get_categories.return_value = [a_category_with("Aaaa"),
                                               a_category_with("Abc"),
                                               a_category_with("xxx")]
        self.view = Mock(CategoryFinderDialog)
        self.controller = CategoryFinderDialogController(self.view)

    def test_it_can_be_created(self):
        self.show_dialog(CategoryFinderDialog, None, self.db)
