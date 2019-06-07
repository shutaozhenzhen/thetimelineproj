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


from mock import Mock

from timelinelib.wxgui.components.searchbar.view import SearchBar
from timelinelib.wxgui.components.searchbar.controller import SearchBarController
from timelinelib.test.cases.unit import UnitTestCase


class describe_search_bar(UnitTestCase):

    def test_no_events_found_displays_nomatch_label(self):
        self.view.GetValue.return_value = ""
        self.view.GetPeriod.return_value = ""
        self.controller.search()
        self.view.UpdateNomatchLabels.assert_called_with(True)
        self.view.UpdateSinglematchLabel.assert_called_with(False)

    def test_no_events_found_no_navigation_call(self):
        self.view.GetValue.return_value = ""
        self.view.GetPeriod.return_value = ""
        self.controller.search()
        self.assertFalse(self.timeline_canvas.navigate)

    def test_on_event_found_displays_singlematch_label(self):
        self.view.GetValue.return_value = "one"
        self.view.GetPeriod.return_value = ""
        self.controller.search()
        self.view.UpdateNomatchLabels.assert_called_with(False)
        self.view.UpdateSinglematchLabel.assert_called_with(True)

    def test_on_event_found_navigation_called(self):
        self.view.GetValue.return_value = "one"
        self.view.GetPeriod.return_value = ""
        self.controller.search()
        self.assertTrue(self.timeline_canvas.navigate)

    def test_two_events_found_displays_no_label(self):
        self.view.GetValue.return_value = "two"
        self.view.GetPeriod.return_value = ""
        self.controller.search()
        self.view.UpdateNomatchLabels.assert_called_with(False)
        self.view.UpdateSinglematchLabel.assert_called_with(False)

    def test_three_events_makes_it_possible_to_move_to_next(self):
        self.view.GetValue.return_value = "three"
        self.view.GetPeriod.return_value = ""
        self.controller.search()
        self.assertTrue(self.controller._result_index == 0)
        self.controller.next()
        self.assertTrue(self.controller._result_index == 1)
        self.controller.next()
        self.assertTrue(self.controller._result_index == 2)
        self.controller.next()
        self.assertTrue(self.controller._result_index == 0)

    def test_three_events_makes_it_possible_to_move_to_prev(self):
        self.view.GetValue.return_value = "three"
        self.view.GetPeriod.return_value = ""
        self.controller.search()
        self.controller.next()
        self.controller.next()
        self.assertTrue(self.controller._result_index == 2)
        self.controller.prev()
        self.assertTrue(self.controller._result_index == 1)
        self.controller.prev()
        self.assertTrue(self.controller._result_index == 0)
        self.controller.prev()
        self.assertTrue(self.controller._result_index == 0)

    def test_searching_for_same_term_twice_goes_to_next_match(self):
        self.view.GetValue.return_value = "three"
        self.view.GetPeriod.return_value = ""
        self.controller.search()
        self.controller.search()
        self.assertEqual(self.controller._result_index, 1)

    def test_no_timeline_canvas_hides_search_bar(self):
        self.controller.set_timeline_canvas(None)
        self.view.Enable.assert_called_with(False)

    def setUp(self):
        self.view = Mock(SearchBar)
        self.timeline_canvas = TimelineCanvas()
        self.controller = SearchBarController(self.view)
        self.controller.set_timeline_canvas(self.timeline_canvas)


class TimelineCanvas():

    def __init__(self):
        self.navigate = False

    def GetFilteredEvents(self, search, period):
        if search == "":
            return []
        elif search == "one":
            return [1]
        elif search == "two":
            return [1, 2]
        elif search == "three":
            return [1, 2, 3]

    def GetPeriodChoices(self):
        return []
    
    def HighligtEvent(self, event, clear=False):
        pass

    def Navigate(self, fn):
        self.navigate = True
