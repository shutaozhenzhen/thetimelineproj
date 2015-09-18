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

from timelinelib.wxgui.dialogs.timeeditordialog.timeeditordialog import TimeEditorDialog
from timelinelib.wxgui.dialogs.timeeditordialog.timeeditordialogcontroller import TimeEditorDialogController
from timelinetest import UnitTestCase
from timelinetest.utils import create_dialog
from timelinelib.data.db import MemoryDB
from timelinetest.utils import human_time_to_gregorian


class describe_TimeEditorDialog_for_gregorian_time(UnitTestCase):

    def setUp(self):
        self.db = MemoryDB()
        self.view = Mock(TimeEditorDialog)
        self.controller = TimeEditorDialogController(self.view)

    def test_it_can_be_created(self):
        tm = human_time_to_gregorian("31 Dec 2010 00:00")
        with create_dialog(TimeEditorDialog, None, None, self.db.get_time_type(), tm, "Go to Date") as dialog:
            if self.HALT_GUI:
                dialog.ShowModal()

    def test_hours_set_to_midday_if_not_given_by_user(self):
        self.given_time_not_shown_in_dialog("31 Dec 2010 00:00")
        self.when_ok_button_clikced()
        self.view.SetTime.assert_called_with(human_time_to_gregorian("31 Dec 2010 12:00"))

    def given_time_not_shown_in_dialog(self, human_time):
        tm = human_time_to_gregorian(human_time)
        self.controller.on_init(self.db.get_time_type(), tm)
        self.view.GetTime.return_value = tm
        self.view.ShowTimeIsChecked.return_value = False

    def when_ok_button_clikced(self):
        self.controller.ok_button_clicked(None)

