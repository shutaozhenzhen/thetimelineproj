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


import wx

from mock import Mock
from mock import sentinel

from timelinelib.config.dotfile import Config
from timelinelib.wxgui.dialogs.preferencesdialog.preferencesdialogcontroller import PreferencesDialogController
from timelinelib.wxgui.dialogs.preferencesdialog.preferencesdialog import PreferencesDialog
from timelinetest import UnitTestCase
from timelinetest.utils import create_dialog


class describe_preferences_dialog(UnitTestCase):

    def setUp(self):
        self.view = Mock(PreferencesDialog)
        self.controller = PreferencesDialogController(self.view)
        self.config = Mock(Config)
        self.config.get_week_start.return_value = "monday"
        self.config.get_open_recent_at_startup.return_value = True
        self.config.get_use_inertial_scrolling.return_value = False
        self.config.get_never_show_period_events_as_point_events.return_value = True
        self.config.get_center_event_texts.return_value = True

    def test_it_can_be_created(self):
        with create_dialog(PreferencesDialog, None, self.config) as dialog:
            if self.HALT_GUI:
                dialog.ShowModal()

    def test_sets_open_recent_on_init(self):
        self.config.get_open_recent_at_startup.return_value = sentinel.OPEN_RECENT
        self.controller.on_init(self.config)
        self.view.SetCheckboxOpenRecent.assert_called_with(sentinel.OPEN_RECENT)

    def test_sets_open_recent_on_change(self):
        self.controller.on_init(self.config)
        self.controller.on_open_recent_change(event_is_checked(sentinel.OPEN_RECENT))
        self.config.set_open_recent_at_startup.assert_called_with(sentinel.OPEN_RECENT)

    def test_sets_inertial_scrolling_on_init(self):
        self.config.get_use_inertial_scrolling.return_value = sentinel.INERTIAL_SCROLLING
        self.controller.on_init(self.config)
        self.view.SetCheckboxInertialScrolling.assert_called_with(sentinel.INERTIAL_SCROLLING)

    def test_sets_inertial_scrolling_on_change(self):
        self.controller.on_init(self.config)
        self.controller.on_inertial_scrolling_changed(event_is_checked(sentinel.INERTIAL_SCROLLING))
        self.config.set_use_inertial_scrolling.assert_called_with(sentinel.INERTIAL_SCROLLING)

    def test_sets_period_point_on_init(self):
        self.config.get_never_show_period_events_as_point_events.return_value = sentinel.PERIOD_POINT
        self.controller.on_init(self.config)
        self.view.SetCheckboxPeriodPoint.assert_called_with(sentinel.PERIOD_POINT)

    def test_sets_period_point_on_change(self):
        self.controller.on_init(self.config)
        self.controller.on_period_point_changed(event_is_checked(sentinel.PERIOD_POINT))
        self.config.set_never_show_period_events_as_point_events.assert_called_with(sentinel.PERIOD_POINT)

    def test_sets_center_text_on_init(self):
        self.config.get_center_event_texts.return_value = sentinel.CENTER_TEXT
        self.controller.on_init(self.config)
        self.view.SetCheckboxCenterText.assert_called_with(sentinel.CENTER_TEXT)

    def test_sets_center_text_on_change(self):
        self.controller.on_init(self.config)
        self.controller.on_center_changed(event_is_checked(sentinel.CENTER_TEXT))
        self.config.set_center_event_texts.assert_called_with(sentinel.CENTER_TEXT)

    def test_sets_week_start_on_init(self):
        self.config.get_week_start.return_value = "sunday"
        self.controller.on_init(self.config)
        self.view.SetWeekStart.assert_called_with(1)

    def test_sets_week_start_on_change(self):
        self.controller.on_init(self.config)
        self.controller.on_week_start_changed(event_selection(1))
        self.config.set_week_start.assert_called_with("sunday")


def event_is_checked(value):
    event = Mock(wx.CommandEvent)
    event.IsChecked.return_value = value
    return event


def event_selection(value):
    event = Mock(wx.CommandEvent)
    event.GetSelection.return_value = value
    return event
