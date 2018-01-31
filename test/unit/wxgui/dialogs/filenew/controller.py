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


from mock import Mock

from timelinelib.wxgui.dialogs.filenew.controller import FileNewDialogController
from timelinelib.wxgui.dialogs.filenew.view import FileNewDialog
from timelinelib.test.cases.unit import UnitTestCase


class describe_file_new_dialog_controller(UnitTestCase):

    def setUp(self):
        self.view = Mock(FileNewDialog)
        self.controller = FileNewDialogController(self.view)

    def test_it_selects_the_first_item(self):
        self.controller.on_init([])
        self.view.SelectItem.assert_called_with(0)
