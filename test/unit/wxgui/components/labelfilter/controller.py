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


from timelinelib.test.cases.unit import UnitTestCase
from unittest.mock import Mock
from timelinelib.wxgui.components.labelfilter.controller import LabelFilterController


class describe_label_filtercontroller(UnitTestCase):

    def test_empty_filter_and_event_with_no_labels_is_visible(self):
        self.simulate_user_adding_labels_to_filter("")
        self.assertTrue(self.controller.visible(self.get_event_with_labels("")))

    def test_empty_filter_and_event_with_labels_is_visible(self):
        self.simulate_user_adding_labels_to_filter("")
        self.assertTrue(self.controller.visible(self.get_event_with_labels("foo bar")))

    def test_any_filter_and_event_with_no_labels_is_not_visible(self):
        self.simulate_user_adding_labels_to_filter("foo")
        self.simulate_user_selecting_radio_button_for_any_label()
        self.assertFalse(self.controller.visible(self.get_event_with_labels("")))

    def test_any_filter_and_event_with_labels_is_visible(self):
        self.simulate_user_adding_labels_to_filter("foo")
        self.simulate_user_selecting_radio_button_for_any_label()
        self.assertTrue(self.controller.visible(self.get_event_with_labels("foo bar")))

    def test_any_filter_and_event_with_mismatch_labels_is_not_visible(self):
        self.simulate_user_adding_labels_to_filter("zyxb")
        self.simulate_user_selecting_radio_button_for_any_label()
        self.assertFalse(self.controller.visible(self.get_event_with_labels("foo bar")))

    def test_all_filter_and_event_with_no_labels_is_not_visible(self):
        self.simulate_user_adding_labels_to_filter("foo")
        self.simulate_user_selecting_radio_button_for_all_labels()
        self.assertFalse(self.controller.visible(self.get_event_with_labels("")))

    def test_all_filter_and_event_with_labels_is_visible(self):
        self.simulate_user_adding_labels_to_filter("foo")
        self.simulate_user_selecting_radio_button_for_all_labels()
        self.assertTrue(self.controller.visible(self.get_event_with_labels("foo bar")))

    def test_all_filter_and_event_with_mismatch_labels_is_not_visible(self):
        self.simulate_user_adding_labels_to_filter("foo zyxb")
        self.simulate_user_selecting_radio_button_for_all_labels()
        self.assertFalse(self.controller.visible(self.get_event_with_labels("foo bar")))

    def test_all_filter_and_event_with_match_labels_is_visible(self):
        self.simulate_user_adding_labels_to_filter("foo zyxb")
        self.simulate_user_selecting_radio_button_for_all_labels()
        self.assertTrue(self.controller.visible(self.get_event_with_labels("foo zyxb")))

    def simulate_user_adding_labels_to_filter(self, labels):
        self.view.get_labels.return_value = labels.split()

    def simulate_user_selecting_radio_button_for_any_label(self):
        self.view.match_all.return_value = False

    def simulate_user_selecting_radio_button_for_all_labels(self):
        self.view.match_all.return_value = True

    @staticmethod
    def get_event_with_labels(labels):
        event = Mock()
        event.get_data.return_value = labels
        return event

    def setUp(self):
        self.view = Mock()
        self.controller = LabelFilterController(self.view)
