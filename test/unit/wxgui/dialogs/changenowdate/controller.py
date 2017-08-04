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

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.changenowdate.controller import ChangeNowDateDialogController
from timelinelib.wxgui.dialogs.changenowdate.view import ChangeNowDateDialog


class describe_change_now_date_dialog_controller(UnitTestCase):

    def setUp(self):
        self.view = Mock(ChangeNowDateDialog)
        self.controller = ChangeNowDateDialogController(self.view)
        self.db = Mock()
        self.callback_function = Mock()
        self.controller.on_init(self.db, self.callback_function)
        self.app = wx.App(False)
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)

    def tearDown(self):
        self.app.Destroy()

    def test_can_check_show_time(self):
        self.view.IsShowTimeChecked.return_value = True
        self.controller.on_show_time_changed(None)
        self.view.ShowTime.assert_called_with(True)

    def test_can_uncheck_show_time(self):
        self.view.IsShowTimeChecked.return_value = False
        self.controller.on_show_time_changed(None)
        self.view.ShowTime.assert_called_with(False)

    def test_invalid_time_raises_value_error(self):
        self.view.GetNowValue.return_value = None
        self.controller.on_time_changed()
        self.assertEqual(self.callback_function.call_count, 1)
