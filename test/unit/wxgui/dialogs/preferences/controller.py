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
        config.uncheck_time_for_new_events = False
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
