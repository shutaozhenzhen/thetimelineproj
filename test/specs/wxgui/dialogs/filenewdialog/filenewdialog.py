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

from timelinelib.wxgui.dialogs.filenewdialog.filenewdialog import FileNewDialog
from timelinelib.wxgui.dialogs.filenewdialog.filenewdialogcontroller import FileNewDialogController
from timelinetest import UnitTestCase
from timelinetest import WxDialogTestCase


class describe_file_new_dialog(WxDialogTestCase):

    HALT_FOR_MANUAL_INSPECTION = False

    def test_it_can_be_created(self):
        self.open_dialog(self.create_dialog)

    def create_dialog(self):
        items = [
            {
                "text": "hello",
                "description": "hello is a standard phrase",
            },
            {
                "text": "there",
                "description": "there can be used after hello. but this is a "
                               "long label\n\nand some newlines",
            },
        ]
        return FileNewDialog(None, items)

    def on_closing(self, dialog):
        print(dialog.GetSelection())


class describe_file_new_dialog_controller(UnitTestCase):

    def setUp(self):
        self.view = Mock(FileNewDialog)
        self.controller = FileNewDialogController(self.view)

    def test_it_selects_the_first_item(self):
        self.controller.on_init([])
        self.view.SelectItem.assert_called_with(0)
