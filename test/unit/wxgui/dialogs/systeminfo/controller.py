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


from sys import version as python_version
import platform
import locale

import wx

from unittest.mock import Mock

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.systeminfo.view import SystemInfoDialog
from timelinelib.wxgui.dialogs.systeminfo.controller import SystemInfoDialogController
from timelinelib.config.dotfile import Config


DATE_FORMAT = 'dd-mm-yyyy'
CONFIG_FILE_PATH = '\\foo\\bar\\_timeline.cfg'


class describe_system_info_dialog_controller(UnitTestCase):

    def test_initiation(self):
        self.controller.on_init(self.view)
        self.view.SetSystemVersion.assert_called_with(', '.join(platform.uname()))
        self.view.SetLocaleSetting.assert_called_with(" ".join(locale.getlocale(locale.LC_TIME)))
        self.view.SetPythonVersion.assert_called_with(python_version.replace("\n", ""))
        self.view.SetWxPythonVersion.assert_called_with(wx.version())
        self.view.SetDateFormat.assert_called_with(DATE_FORMAT)
        self.view.SetConfigFile.assert_called_with(CONFIG_FILE_PATH)

    def test_initiation_with_no_parent(self):
        self.controller.on_init(None)
        self.view.SetSystemVersion.assert_called_with(', '.join(platform.uname()))
        self.view.SetLocaleSetting.assert_called_with(" ".join(locale.getlocale(locale.LC_TIME)))
        self.view.SetPythonVersion.assert_called_with(python_version.replace("\n", ""))
        self.view.SetWxPythonVersion.assert_called_with(wx.version())
        self.view.SetDateFormat.assert_called_with('?')
        self.view.SetConfigFile.assert_called_with('?')

    def setUp(self):
        locale.setlocale(locale.LC_ALL, '')
        UnitTestCase.setUp(self)
        self.view = Mock(SystemInfoDialog)
        config = Mock(Config)
        config.path = CONFIG_FILE_PATH
        config.get_date_format.return_value = DATE_FORMAT
        self.view.config = config
        self.controller = SystemInfoDialogController(self.view)
