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


from unittest.mock import Mock
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.eventduration.controller import EventsDurationController
from timelinelib.db import db_open
from timelinelib.config.dotfile import Config
from timelinelib.wxgui.dialogs.eventduration.view import EventDurationDialog
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.calendar.gregorian.timetype.timetype import GregorianTimeType


class EventDurationDialogTestCase(UnitTestCase):

    def test_can_create(self):
        self.assertIsNotNone(self.a_controller())

    def test_can_initialixe(self):
        controller = self.a_controller()
        controller.on_init(self.a_db(), self.a_config(), None)
        # self.view.SetDurationResult(str(duration))
        self.assertEqual(controller.view.SetDurationResult.call_count, 1)
        controller.view.SetDurationResult.assert_called_with("0.0")

    def a_controller(self):
        return EventsDurationController(self.a_view())

    @staticmethod
    def a_config():
        config = Mock(Config)
        config.workday_length = 8
        return config

    @staticmethod
    def a_db():
        return db_open(":tutorial:")

    @staticmethod
    def a_view():
        view = Mock(EventDurationDialog)
        start = human_time_to_gregorian("1 Jan 2010")
        view.GetStartTime.return_value = start
        view.GetEndTime.return_value = start
        view.GetDurationType.return_value = GregorianTimeType.DURATION_TYPE_HOURS
        view.GetPrecision.return_value = 1
        view.GetCopyToClipboard.return_value = None
        return view
