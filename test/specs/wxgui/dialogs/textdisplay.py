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

from timelinelib.wxgui.dialogs.textdisplay.textdisplaydialogcontroller import TextDisplayDialogController
from timelinelib.wxgui.dialogs.textdisplay.view import TextDisplayDialog
from timelinetest import UnitTestCase
from timelinetest.utils import create_dialog


class describe_text_display_dialog(UnitTestCase):

    def setUp(self):
        self.view = Mock(TextDisplayDialog)
        self.controller = TextDisplayDialogController(self.view)

    def test_it_can_be_created(self):
        with create_dialog(TextDisplayDialog, "title", "text", None) as dialog:
            if self.HALT_GUI:
                dialog.ShowModal()

    def test_set_text_on_init(self):
        self.controller.on_init("hello world")
        self.view.SetText.assert_called_with("hello world")
