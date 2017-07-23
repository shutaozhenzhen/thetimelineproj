# -*- coding: utf-8 -*-
#
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


import sys

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

if sys.platform == "win32":
    FONT = u"12:74:90:92:False:MS Shell Dlg 2:-1:(0, 0, 0, 255)"
else:
    FONT = u"12:70:90:92:False:MS Shell Dlg 2:43:(0, 0, 0, 255)"


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
        self.app = wx.App()
        self.view = Mock(PreferencesDialog)
        self.controller = PreferencesDialogController(self.view)
        self.config = self._mock_config()
        self.features = self._mock_features()
        self.controller.on_init(self.config, self.features)

    def _mock_config(self):
        config = Mock(Config)
        config.open_recent_at_startup = ""
        config.use_inertial_scrolling = False
        config.never_show_period_events_as_point_events = False
        config.center_event_texts = False
        config.get_week_start.return_value = "monday"
        config.uncheck_time_for_new_events = False
        config.minor_strip_divider_line_colour = (100, 100, 100)
        config.major_strip_divider_line_colour = (100, 100, 100)
        config.now_line_colour = (100, 100, 100)
        config.weekend_colour = (255, 255, 255)
        config.get_bg_color.return_value = (255, 255, 255)
        config.fuzzy_icon = CONFIG_FUZZY_ICON_NAME
        config.locked_icon = CONFIG_LOCKED_ICON_NAME
        config.get_hyperlink_icon.return_value = CONFIG_HYPERINK_ICON_NAME
        config.never_use_time = False
        config.get_major_strip_font.return_value = "10:74:90:90:False:Tahoma:33:(0, 0, 0, 255)"
        config.get_minor_strip_font.return_value = "10:74:90:90:False:Tahoma:33:(0, 0, 0, 255)"
        config.get_legend_font.return_value = "10:74:90:90:False:Tahoma:33:(0, 0, 0, 255)"
        config.legend_pos = 0
        return config

    def _mock_features(self):
        features = Mock(ExperimentalFeatures)
        features.get_all_features.return_Value = ()
        return features


class describe_preferences_dialog(UnitTestCase):

    def setUp(self):
        self.app = wx.App()
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)
        self.view = Mock(PreferencesDialog)
        self.controller = PreferencesDialogController(self.view)
        self.config = Mock(Config)
        self.config.get_week_start.return_value = "monday"
        self.config.open_recent_at_startup = True
        self.config.use_inertial_scrolling = False
        self.config.text_below_icon = False
        self.config.never_show_period_events_as_point_events = True
        self.config.center_event_texts = True
        self.config.display_checkmark_on_events_done = False
        self.config.uncheck_time_for_new_events = False
        self.config.minor_strip_divider_line_colour = (100, 100, 100)
        self.config.major_strip_divider_line_colour = (100, 100, 100)
        self.config.now_line_colour = (200, 0, 0)
        self.config.weekend_colour = (255, 255, 255)
        self.config.get_bg_color.return_value = (255, 255, 255)
        self.config.fuzzy_icon = "fuzzy.png"
        self.config.locked_icon = "locked.png"
        self.config.get_hyperlink_icon.return_value = "hyperlink.png"
        self.config.vertical_space_between_events = 5
        self.config.colorize_weekends = False
        self.config.skip_s_in_decade_text = False
        self.config.get_major_strip_font.return_value = "10:74:90:90:False:Tahoma:33:(0, 0, 0, 255)"
        self.config.get_minor_strip_font.return_value = "10:74:90:90:False:Tahoma:33:(0, 0, 0, 255)"
        self.config.get_legend_font.return_value = "10:74:90:90:False:Tahoma:33:(0, 0, 0, 255)"
        self.config.legend_pos = 0
        self.config.date_format = "yyyy-mm-dd"
        self.config.never_use_time = False
        self.experimental_features = Mock(ExperimentalFeatures)
        self.evt = Mock()

    def tearDown(self):
        self.app.Destroy()

    def test_it_can_be_created(self):
        self.show_dialog(PreferencesDialog, None, self.config)

    def test_sets_open_recent_on_init(self):
        self.config.open_recent_at_startup = sentinel.OPEN_RECENT
        self.simulate_dialog_opens()
        self.view.SetOpenRecentCheckboxValue.assert_called_with(sentinel.OPEN_RECENT)

    def test_sets_open_recent_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_open_recent_change(event_is_checked(sentinel.OPEN_RECENT))
        self.assertEqual(self.config.open_recent_at_startup, sentinel.OPEN_RECENT)

    def test_sets_inertial_scrolling_on_init(self):
        self.config.use_inertial_scrolling = sentinel.INERTIAL_SCROLLING
        self.simulate_dialog_opens()
        self.view.SetInertialScrollingCheckboxValue.assert_called_with(sentinel.INERTIAL_SCROLLING)

    def test_sets_inertial_scrolling_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_inertial_scrolling_changed(event_is_checked(sentinel.INERTIAL_SCROLLING))
        self.assertEqual(self.config.use_inertial_scrolling, sentinel.INERTIAL_SCROLLING)

    def test_sets_period_point_on_init(self):
        self.config.never_show_period_events_as_point_events = sentinel.PERIOD_POINT
        self.simulate_dialog_opens()
        self.view.SetNeverPeriodPointCheckboxValue.assert_called_with(sentinel.PERIOD_POINT)

    def test_sets_period_point_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_never_period_point_changed(event_is_checked(sentinel.PERIOD_POINT))
        self.assertEqual(self.config.never_show_period_events_as_point_events, sentinel.PERIOD_POINT)

    def test_sets_center_text_on_init(self):
        self.config.center_event_texts = sentinel.CENTER_TEXT
        self.simulate_dialog_opens()
        self.view.SetCenterTextCheckboxValue.assert_called_with(sentinel.CENTER_TEXT)

    def test_sets_center_text_on_change(self):
        self.simulate_dialog_opens()
        self.controller.on_center_text_changed(event_is_checked(sentinel.CENTER_TEXT))
        self.assertEqual(self.config.center_event_texts, sentinel.CENTER_TEXT)

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

    def test_opens_date_format_dialog_on_click(self):
        self.controller.config = self.config
        self.simulate_on_date_formatter_click()
        self.view.ShowSelectDateFormatDialog.assert_called_with(self.config)
        self.view.SetCurrentDateFormat.assert_called_with(
            u"⟪Current⟫: %s" % self.config.date_format
        )

    def test_uncheck_time_for_new_events(self):
        self.evt.IsChecked.return_value = True
        self.controller.config = self.config
        self.controller.on_uncheck_time_for_new_events(self.evt)
        self.assertEqual(self.config.uncheck_time_for_new_events, self.evt.IsChecked.return_value)

    def test_on_major_strip_click(self):
        font = Mock()
        font.serialize.return_value = FONT
        self.config.get_major_strip_font.return_value = FONT
        self.controller.config = self.config
        self.view.ShowEditFontDialog.return_value = True
        self.controller.on_major_strip_click(None)
        self.config.set_major_strip_font.assert_called_with(FONT)

    def test_on_major_minor_click(self):
        font = Mock()
        font.serialize.return_value = FONT
        self.config.get_minor_strip_font.return_value = FONT
        self.controller.config = self.config
        self.view.ShowEditFontDialog.return_value = True
        self.controller.on_minor_strip_click(None)
        self.config.set_minor_strip_font.assert_called_with(FONT)

    def test_on_fuzzy_icon_changed(self):
        self.evt.GetString.return_value = sentinel.STRING
        self.controller.config = self.config
        self.controller.on_fuzzy_icon_changed(self.evt)
        self.assertEqual(self.config.fuzzy_icon, sentinel.STRING)
        self.view.DisplayIcons.assert_called_with()

    def test_on_locked_icon_changed(self):
        self.evt.GetString.return_value = sentinel.STRING
        self.controller.config = self.config
        self.controller.on_locked_icon_changed(self.evt)
        self.assertEqual(self.config.locked_icon, sentinel.STRING)
        self.view.DisplayIcons.assert_called_with()

    def test_on_hyperlink_icon_changed(self):
        self.evt.GetString.return_value = sentinel.STRING
        self.controller.config = self.config
        self.controller.on_hyperlink_icon_changed(self.evt)
        self.config.set_hyperlink_icon.assert_called_with(sentinel.STRING)
        self.view.DisplayIcons.assert_called_with()

    def test_on_vertical_space_between_events_click(self):
        self.controller.config = self.config
        self.view.GetVerticalSpaceBetweenEvents.return_value = sentinel.SPACE
        self.controller.on_vertical_space_between_events_click(self.evt)
        self.assertEqual(self.config.vertical_space_between_events, sentinel.SPACE)

    def test_on_colorize_weekends(self):
        self.controller.config = self.config
        self.view.GetColorizeWeekends.return_value = sentinel.COLORICE_WEEKENDS
        self.controller.on_colorize_weekends(self.evt)
        self.assertEqual(self.config.colorize_weekends, sentinel.COLORICE_WEEKENDS)

    def test_on_skip_s_in_decade_text(self):
        self.controller.config = self.config
        self.view.GetSkipSInDecadeText.return_value = sentinel.SKIP_S
        self.controller.on_skip_s_in_decade_text(self.evt)
        self.assertEqual(self.config.skip_s_in_decade_text, sentinel.SKIP_S)

    def test_on_legend_click_ok(self):
        self.controller.config = self.config
        self.config.get_legend_font.return_value = FONT
        self.view.ShowEditFontDialog.return_value = True
        self.controller.on_legend_click(self.evt)
        self.config.set_legend_font.assert_called_with(FONT)

    def test_on_legend_click_cancel(self):
        evt = Mock()
        self.controller.config = self.config
        self.config.get_legend_font.return_value = FONT
        self.view.ShowEditFontDialog.return_value = False
        self.controller.on_legend_click(evt)
        self.assertEqual(self.config.set_legend_font.call_count, 0)

    def test_sets_never_use_time(self):
        self.config.never_use_time = sentinel.NEVER_USE_TIME
        self.simulate_dialog_opens()
        self.view.SetNeverUseTime.assert_called_with(sentinel.NEVER_USE_TIME)

    def test_on_never_use_time(self):
        evt = Mock()
        self.controller.config = self.config
        self.view.GetNeverUseTime.return_value = sentinel.NEVER_USE_TIME
        self.controller.on_never_use_time_change(evt)
        self.assertEqual(self.config.never_use_time, sentinel.NEVER_USE_TIME)

    def simulate_dialog_opens(self):
        self.controller.on_init(self.config, self.experimental_features)

    def simulate_on_date_formatter_click(self):
        self.controller.on_date_formatter_click(None)


def event_is_checked(value):
    event = Mock(wx.CommandEvent)
    event.IsChecked.return_value = value
    return event


def event_selection(value):
    event = Mock(wx.CommandEvent)
    event.GetSelection.return_value = value
    return event
