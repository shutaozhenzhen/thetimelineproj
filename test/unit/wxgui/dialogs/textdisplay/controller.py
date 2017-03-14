# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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


import wx

from mock import Mock

from timelinelib.wxgui.dialogs.textdisplay.controller import TextDisplayDialogController
from timelinelib.wxgui.dialogs.textdisplay.view import TextDisplayDialog
from timelinelib.test.cases.unit import UnitTestCase


class describe_text_display_dialog_gui(UnitTestCase):

    def test_it_can_be_created(self):
        self.show_dialog(TextDisplayDialog, "title", "text", None)


class describe_text_display_dialog(UnitTestCase):

    def test_set_text_on_init(self):
        self.controller.on_init("hello world")
        self.view.SetText.assert_called_with("hello world")

    def test_cant_copy_to_clipboard_when_clipboard_open_fails(self):
        wx.TheClipboard.Open.return_value = False
        self.controller.on_copy_click(None)
        self.view.DisplayErrorMessage.assert_called_with(_("Unable to copy to clipboard."))

    def test_can_copy_to_clipboard_when_clipboard_opens(self):
        wx.TheClipboard.Open.return_value = True
        self.controller.on_copy_click(None)
        self.assertEqual(wx.TheClipboard.SetData.call_count, 1)
        self.assertEqual(wx.TheClipboard.Close.call_count, 1)

    def setUp(self):
        self.TheClipboard = wx.TheClipboard
        wx.TheClipboard = Mock()
        self.view = Mock(TextDisplayDialog)
        self.view.GetText.return_value = "Test text"
        self.controller = TextDisplayDialogController(self.view)

    def tearDown(self):
        wx.TheClipboard = self.TheClipboard
