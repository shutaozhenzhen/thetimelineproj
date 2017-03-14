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


from mock import Mock
from mock import sentinel

from timelinelib.config.dotfile import Config
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.dateformat.view import DateFormatDialog
from timelinelib.wxgui.dialogs.dateformat.controller import DateFormatDialogController


class describe_date_format_dialog_controller(UnitTestCase):

    def test_instantiation(self):
        pass

    def test_initiation(self):
        self.view.SetDateFormat.assert_called_with(sentinel.DATE_TEXT)
        self.assertTrue(self.view.SetLocaleDateFormat.called)

    def test_closing_ok(self):
        self._simulate_user_entry("yyyy-mm-dd")
        self._simulate_ok_clicked()
        self.assertTrue(self.view.GetDateFormat.called)
        self.config.set_date_format.assert_called_with("yyyy-mm-dd")
        self.assertTrue(self.view.EndModalOk.called)

    def test_closing_error(self):
        self._simulate_user_entry("-mm-dd")
        self._simulate_ok_clicked()
        self.assertTrue(self.view.GetDateFormat.called)
        self.assertFalse(self.view.EndModalOk.called)
        self.assertTrue(self.view.DisplayErrorMessage.called)

    def _simulate_user_entry(self, date_format):
        self.view.GetDateFormat.return_value = date_format

    def _simulate_ok_clicked(self):
        self.controller.on_ok(None)

    def setUp(self):
        UnitTestCase.setUp(self)
        self.view = Mock(DateFormatDialog)
        self.config = Mock(Config)
        self.config.get_date_format.return_value = sentinel.DATE_TEXT
        self.controller = DateFormatDialogController(self.view)
        self.controller.on_init(self.config)
