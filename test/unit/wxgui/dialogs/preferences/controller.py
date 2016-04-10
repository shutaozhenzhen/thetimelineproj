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

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.wxgui.dialogs.preferences.view import PreferencesDialog
from timelinelib.wxgui.dialogs.preferences.controller import PreferencesDialogController
from timelinelib.config.dotfile import Config
from timelinelib.features.experimental.experimentalfeatures import ExperimentalFeatures
from timelinelib.test.utils import ANY

CONFIG_FUZZY_ICON_NAME = "fuzzy.png"
CONFIG_LOCKED_ICON_NAME = "locked.png"
CONFIG_HYPERINK_ICON_NAME = "hyperlink.png"


class describe_preferences_dialog_controller(UnitTestCase):

    def test_construction(self):
        self.assertTrue(self.controller is not None)

    def test_choices_are_set_by_controller(self):
        self.view.SetIconsChoices.assert_called_with(ANY)

    def test_icon_names_are_set_from_config_data(self):
        self.view.SetFuzzyIcon.assert_called_once_with(CONFIG_FUZZY_ICON_NAME)
        self.view.SetLockedIcon.assert_called_once_with(CONFIG_LOCKED_ICON_NAME)
        self.view.SetHyperlinkIcon.assert_called_once_with(CONFIG_HYPERINK_ICON_NAME)

    def setUp(self):
        UnitTestCase.setUp(self)
        self.view = Mock(PreferencesDialog)
        self.controller = PreferencesDialogController(self.view)
        self.config = self._mock_config()
        self.features = self._mock_features()
        self.controller.on_init(self.config, self.features)

    def _mock_config(self):
        config = Mock(Config)
        config.get_open_recent_at_startup.return_value = ""
        config.get_use_inertial_scrolling.return_value = False
        config.get_never_show_period_events_as_point_events.return_value = False
        config.get_center_event_texts.return_value = False
        config.get_week_start.return_value = "monday"
        config.get_uncheck_time_for_new_events.return_value = False
        config.minor_strip_divider_line_colour = (100, 100, 100)
        config.major_strip_divider_line_colour = (100, 100, 100)
        config.now_line_colour = (100, 100, 100)
        config.weekend_colour = (255, 255, 255)
        config.get_fuzzy_icon.return_value = CONFIG_FUZZY_ICON_NAME
        config.get_locked_icon.return_value = CONFIG_LOCKED_ICON_NAME
        config.get_hyperlink_icon.return_value = CONFIG_HYPERINK_ICON_NAME
        return config

    def _mock_features(self):
        features = Mock(ExperimentalFeatures)
        features.get_all_features.return_Value = ()
        return features


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
        self.config.get_uncheck_time_for_new_events.return_value = False
        self.config.minor_strip_divider_line_colour = (100, 100, 100)
        self.config.major_strip_divider_line_colour = (100, 100, 100)
        self.config.now_line_colour = (200, 0, 0)
        self.config.weekend_colour = (255, 255, 255)
        self.config.get_fuzzy_icon.return_value = "fuzzy.png"
        self.config.get_locked_icon.return_value = "locked.png"
        self.config.get_hyperlink_icon.return_value = "hyperlink.png"
        self.config.get_vertical_space_between_events.return_value = 5
        self.config.get_colorize_weekends.return_value = False
        self.config.get_skip_s_in_decade_text.return_value = False
        self.experimental_features = Mock(ExperimentalFeatures)

    def test_it_can_be_created(self):
        self.show_dialog(PreferencesDialog, None, self.config)

    def test_sets_open_recent_on_init(self):
        self.config.get_open_recent_at_startup.return_value = sentinel.OPEN_RECENT
        self.simulate_dialog_opens()
        self.view.SetOpenRecentCheckboxValue.assert_called_with(sentinel.OPEN_RECENT)

    def test_sets_open_recent_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_open_recent_change(event_is_checked(sentinel.OPEN_RECENT))
        self.config.set_open_recent_at_startup.assert_called_with(sentinel.OPEN_RECENT)

    def test_sets_inertial_scrolling_on_init(self):
        self.config.get_use_inertial_scrolling.return_value = sentinel.INERTIAL_SCROLLING
        self.simulate_dialog_opens()
        self.view.SetInertialScrollingCheckboxValue.assert_called_with(sentinel.INERTIAL_SCROLLING)

    def test_sets_inertial_scrolling_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_inertial_scrolling_changed(event_is_checked(sentinel.INERTIAL_SCROLLING))
        self.config.set_use_inertial_scrolling.assert_called_with(sentinel.INERTIAL_SCROLLING)

    def test_sets_period_point_on_init(self):
        self.config.get_never_show_period_events_as_point_events.return_value = sentinel.PERIOD_POINT
        self.simulate_dialog_opens()
        self.view.SetNeverPeriodPointCheckboxValue.assert_called_with(sentinel.PERIOD_POINT)

    def test_sets_period_point_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_never_period_point_changed(event_is_checked(sentinel.PERIOD_POINT))
        self.config.set_never_show_period_events_as_point_events.assert_called_with(sentinel.PERIOD_POINT)

    def test_sets_center_text_on_init(self):
        self.config.get_center_event_texts.return_value = sentinel.CENTER_TEXT
        self.simulate_dialog_opens()
        self.view.SetCenterTextCheckboxValue.assert_called_with(sentinel.CENTER_TEXT)

    def test_sets_center_text_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_center_text_changed(event_is_checked(sentinel.CENTER_TEXT))
        self.config.set_center_event_texts.assert_called_with(sentinel.CENTER_TEXT)

    def test_sets_week_start_on_init_sunday(self):
        self.config.get_week_start.return_value = "sunday"
        self.simulate_dialog_opens()
        self.view.SetWeekStartSelection.assert_called_with(1)

    def test_sets_week_start_on_init_monday(self):
        self.config.get_week_start.return_value = "monday"
        self.simulate_dialog_opens()
        self.view.SetWeekStartSelection.assert_called_with(0)

    def test_sets_week_start_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_week_start_changed(event_selection(1))
        self.config.set_week_start.assert_called_with("sunday")

    def test_set_experimental_features_on_init(self):
        self.experimental_features.get_all_features.return_value = sentinel.FEATURES
        self.simulate_dialog_opens()
        self.view.AddExperimentalFeatures.assert_called_with(sentinel.FEATURES)

    def test_set_experimental_features_on_change(self):
        self.simulate_dialog_opens()
        event = Mock(wx.CommandEvent)
        mock_object = Mock()
        mock_object.GetLabel.return_value = sentinel.NAME
        event.GetEventObject.return_value = mock_object
        event.IsChecked.return_value = sentinel.VALUE
        self.controller.on_experimental_changed(event)
        self.experimental_features.set_active_state_on_feature_by_name.assert_called_with(sentinel.NAME, sentinel.VALUE)

    def test_opens_select_tab_order_dialog_on_click(self):
        self.simulate_dialog_opens()
        self.controller.on_tab_order_click(None)
        self.view.ShowSelectTabOrderDialog.assert_called_with(self.config)

    def simulate_dialog_opens(self):
        self.controller.on_init(self.config, self.experimental_features)


def event_is_checked(value):
    event = Mock(wx.CommandEvent)
    event.IsChecked.return_value = value
    return event


def event_selection(value):
    event = Mock(wx.CommandEvent)
    event.GetSelection.return_value = value
    return event
