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


import wx

from unittest.mock import Mock

from timelinelib.calendar.gregorian.time import GregorianDelta
from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from canvas.data.memorydb.db import MemoryDB
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import an_event
from timelinelib.wxgui.frames.mainframe.mainframe import AlertController


class describe_alert_controller(UnitTestCase):

    def test_display_events_alerts(self):

        def assert_prequisites():
            self.assertFalse(self.event.get_data("alert") is None)

        def assert_dialog_calls(dlg):
            expected_text = "Trigger time: %s\n\nEvent: %s\n\nTime to go" % (
                self.now, self.event.get_label(GregorianTimeType()))
            dlg.SetText.assert_called_with(expected_text)
            dlg.SetWindowStyleFlag.assert_called_with(wx.STAY_ON_TOP)
            dlg.ShowModal.assert_called_with()
            dlg.Destroy.assert_called_with()

        def assert_event_data():
            self.assertTrue(self.event.get_data("alert") is None)

        dlg = self.a_dialog_mock()
        assert_prequisites()
        self.controller.display_events_alerts(
            [self.event, an_event()],
            GregorianTimeType(),
            dialog=dlg
        )
        assert_dialog_calls(dlg)
        assert_event_data()

    def test_pytime_has_expired(self):
        self.given_early_pytimes()
        self.given_controller_time_type(GregorianTimeType())
        expired = self.controller._time_has_expired(self.tm)
        self.assertTrue(expired)

    def test_pytime_has_not_expired(self):
        self.given_late_pytimes()
        expired = self.controller._time_has_expired(self.tm)
        self.assertFalse(expired)

    def a_dialog_mock(self):
        dlg = Mock()
        dlg.GetWindowStyleFlag.return_value = 0
        return dlg

    def given_early_pytimes(self):
        self.given_pytime_now()
        self.given_pytime_earlier()
        self.given_controller_time_type(GregorianTimeType())
        self.alert = (self.now, "Time to go")

    def given_late_pytimes(self):
        self.given_pytime_now()
        self.given_pytime_later()
        self.given_controller_time_type(GregorianTimeType())
        self.alert = (self.now, "Time to go")

    def given_pytime_now(self):
        self.now = GregorianTimeType().now()

    def given_pytime_later(self):
        self.tm = self.now + GregorianDelta.from_days(1)

    def given_pytime_earlier(self):
        self.tm = self.now + GregorianDelta.from_days(-1)

    def given_controller_time_type(self, time_type):
        self.controller.time_type = time_type

    def setUp(self):
        self.now = GregorianTimeType().now()
        self.alert = (self.now, "Time to go")
        self.db = MemoryDB()
        self.event = an_event()
        self.event.set_data('alert', self.alert)
        self.event.db = self.db
        self.main_frame = Mock()
        self.controller = AlertController(self.main_frame)
