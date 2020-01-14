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
from timelinelib.calendar.num.timetype.timetype import NumTimeType
from timelinelib.calendar.num.time import NumTime
from timelinelib.dataimport.tutorial import NumericTutorialTimelineCreator


class EventDurationDialogTestCase(UnitTestCase):

    def test_can_initialixe(self):
        controller = self.a_controller(self.a_view())
        controller.on_init(self.a_db(), self.a_config(), None)
        self.assertEqual(controller.view.SetDurationResult.call_count, 1)
        controller.view.SetDurationResult.assert_called_with("0.0")

    def test_calculation_one_event(self):
        controller = self.a_num_view_controller(event_list=[(10, 22)])
        controller.on_ok_clicked()
        controller.view.SetDurationResult.assert_called_with("12")

    def test_calculation_two_events(self):
        controller = self.a_num_view_controller(event_list=[(10, 22), (25, 30)])
        controller.on_ok_clicked()
        controller.view.SetDurationResult.assert_called_with("17")

    def test_calculation_for_one_partial_event(self):
        controller = self.a_num_view_controller(event_list=[(10, 22)], start=11, end=14)
        controller.on_ok_clicked()
        controller.view.SetDurationResult.assert_called_with("3")

    def test_calculation_for_two_partial_events(self):
        controller = self.a_num_view_controller(event_list=[(10, 22), (25, 30)], start=20, end=27)
        controller.on_ok_clicked()
        controller.view.SetDurationResult.assert_called_with("4")

    @staticmethod
    def a_controller(view):
        return EventsDurationController(view)

    def a_num_view_controller(self, event_list=[], start=0, end=100):
        controller = self.a_controller(self.a_num_view())
        controller.on_init(self.a_num_db(event_list), self.a_config(), None)
        controller.view.GetStartTime.return_value = NumTime(start)
        controller.view.GetEndTime.return_value = NumTime(end)
        return controller

    @staticmethod
    def a_config(workday_length=8):
        config = Mock(Config)
        config.workday_length = workday_length
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

    @staticmethod
    def a_num_view(category=None, start=0, end=100, duration_type=NumTimeType.DURATION_TYPE_1):
        view = Mock(EventDurationDialog)
        view.GetCategory.return_value = category
        view.GetStartTime.return_value = NumTime(start)
        view.GetEndTime.return_value = NumTime(end)
        view.GetDurationType.return_value = duration_type
        view.GetPrecision.return_value = 0
        view.GetCopyToClipboard.return_value = None
        return view

    @staticmethod
    def a_num_db(event_list):
        creator = NumericTutorialTimelineCreator()
        for inx, period in enumerate(event_list):
            start, end = period
            creator.add_event(f"Event-{inx + 1}", "", start, end)
        return creator.get_db()
