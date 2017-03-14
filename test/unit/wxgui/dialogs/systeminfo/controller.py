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

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.systeminfo.view import SystemInfoDialog
from timelinelib.wxgui.dialogs.systeminfo.controller import SystemInfoDialogController


class describe_system_info_dialog_controller(UnitTestCase):

    def test_instantiation(self):
        pass

    def test_initiation(self):
        self.view.SetSystemVersion.assert_called()
        self.view.SetPythonVersion.assert_called()
        self.view.SetWxPythonVersion.assert_called()
        self.view.SetLocaleSetting.assert_called()
        self.view.SetDateFormat.assert_called()

    def setUp(self):
        UnitTestCase.setUp(self)
        self.view = Mock(SystemInfoDialog)
        self.controller = SystemInfoDialogController(self.view)
