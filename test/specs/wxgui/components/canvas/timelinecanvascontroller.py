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
import wx

from timelinelib.canvas.data.db import MemoryDB
from timelinelib.canvas.data import Event
from timelinelib.canvas.data import TimeOutOfRangeLeftError
from timelinelib.canvas.data import TimeOutOfRangeRightError
from timelinelib.canvas.drawing.drawers.default import DefaultDrawingAlgorithm
from timelinelib.canvas import TimelineCanvas
from timelinelib.canvas.timelinecanvascontroller import TimelineCanvasController
from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.test.utils import gregorian_period
from timelinelib.test.utils import human_time_to_gregorian
from timelinelib.wxgui.components.timelinepanel import InputHandlerState


ANY_Y = 0


class TimelineViewSpec(UnitTestCase):

    def test_initializes_displayed_period_from_db(self):
        self.init_view_with_db_with_period("1 Aug 2010", "2 Aug 2010")
        self.assert_displays_period("1 Aug 2010", "2 Aug 2010")

    def test_disables_view_if_no_timeline_set(self):
        self.controller.set_timeline(None)
        self.timeline_canvas.Disable.assert_called_with()

    def setUp(self):
        self.mock_drawer = MockDrawer()
        self.app = wx.App()
        self.db = MemoryDB()
        self.timeline_canvas = Mock(TimelineCanvas)
        self.timeline_canvas.GetSize.return_value = (200, 100)
        self.timeline_canvas.GetEventAt.side_effect = lambda x, y, alt_down: self.mock_drawer.event_at(x, y, alt_down)
        self.timeline_canvas.GetEventWithHitInfoAt.return_value = None
        self.timeline_canvas.GetEventAt.side_effect = lambda x, y, alt_down: self.mock_drawer.event_at(x, y, alt_down)
        self.timeline_canvas.GetTimeAt.side_effect = lambda x: self.mock_drawer.get_time(x)
        self.timeline_canvas.Snap.side_effect = lambda x: self.mock_drawer.snap(x)
        self.timeline_canvas.IsEventSelected.side_effect = lambda x: self.controller.view_properties.is_selected(x)
        self.timeline_canvas.GetDb.return_value = self.db
        self.width = 10
        self.middle_x = self.width / 2
        self.timeline_canvas.GetSizeTuple.return_value = (self.width, 10)
        self.timeline_canvas.GetDividerPosition.return_value = 50
        self.timeline_canvas.GetSelectedEvents.return_value = []
        self.controller = TimelineCanvasController(
            self.timeline_canvas, drawer=self.mock_drawer)
        self.controller.post_hint_event = Mock()
        self.status_bar = Mock()
        state = InputHandlerState(
            self.timeline_canvas, self.status_bar, Mock(), Mock())

    def given_event_with(self, start="4 Aug 2010", end="10 Aug 2010",
                         text="Text", description=None,
                         pos=(0, 0), size=(0, 0)):
        event = Event().update(human_time_to_gregorian(start), human_time_to_gregorian(end), text)
        if description is not None:
            event.set_data("description", description)
        self.db.save_event(event)
        self.mock_drawer.events_and_rects.append((event, wx.Rect(pos[0], pos[1], size[0], size[1])))
        return event

    def given_time_at_x_is(self, x, time):
        self.mock_drawer.setup_get_time_call(x, human_time_to_gregorian(time))

    def init_view_with_db_with_period(self, start, end):
        self.db.set_displayed_period(gregorian_period(start, end))
        self.init_view_with_db()

    def init_view_with_db(self):
        self.controller.set_timeline(self.db)

    def start_shift_drag_at_x(self, x):
        ctrl_down = False
        shift_down = True
        self.controller.left_mouse_down(x, ANY_Y, ctrl_down, shift_down)

    def simulate_mouse_double_click(self, x, y):
        self.simulate_mouse_click(x, y)
        self.controller.left_mouse_dclick(x, y, ctrl_down=False)

    def simulate_mouse_click(self, x, y, ctrl_down=False):
        self.controller.left_mouse_down(x, y, ctrl_down=ctrl_down, shift_down=False)
        self.controller.left_mouse_up()

    def simulate_mouse_down_move_up(self, from_, to, ctrl_down=False, shift_down=False):
        x1, y1 = from_
        x2, y2 = to
        self.controller.left_mouse_down(x1, y1, ctrl_down, shift_down)
        self.controller.mouse_moved(x2, y2)
        self.controller.left_mouse_up()

    def simulate_mouse_move(self, x, y):
        self.controller.mouse_moved(x, y)

    def move_mouse_to_x(self, x):
        self.controller.mouse_moved(x, ANY_Y)

    def release_mouse(self):
        self.controller.left_mouse_up()

    def assert_event_has_period(self, event, start, end):
        self.assertEqual(gregorian_period(start, end), event.get_time_period())

    def assert_balloon_drawn_for_event(self, event):
        self.timeline_canvas.SetHoveredEvent.assert_called_with(event)

    def assert_highlights_region(self, start_end):
        if start_end is None:
            self.timeline_canvas.SetPeriodSelection.assert_called_with((None))
        else:
            (start, end) = start_end
            period = gregorian_period(start, end)
            self.timeline_canvas.SetPeriodSelection.assert_called_with(period)

    def assert_displays_period(self, start, end):
        view_properties = self.get_view_properties_used_when_drawing()
        self.assertEqual(
            gregorian_period(start, end), view_properties.displayed_period)

    def assert_timeline_redrawn(self):
        self.assertTrue(self.timeline_canvas.redraw_surface.called)

    def assert_created_event_with_period(self, start, end):
        self.timeline_canvas.open_create_event_editor.assert_called_with(
            human_time_to_gregorian(start), human_time_to_gregorian(end))

    def assert_is_selected(self, event):
        view_properties = self.get_view_properties_used_when_drawing()
        self.assertTrue(view_properties.is_selected(event))

    def assert_is_not_selected(self, event):
        view_properties = self.get_view_properties_used_when_drawing()
        self.assertFalse(view_properties.is_selected(event))

    def assert_has_posted_hint(self, text):
        self.controller.post_hint_event.assert_called_with(text)

    def get_view_properties_used_when_drawing(self):
        self.assertTrue(self.timeline_canvas.redraw_surface.called)
        draw_fn = self.timeline_canvas.redraw_surface.call_args[0][0]
        draw_fn(Mock())
        return self.mock_drawer.draw_view_properties


class MockDrawer(object):

    def __init__(self):
        self.events_and_rects = []
        self.snaps = []
        self.get_time_calls = {}
        self.hidden_event_count = 0
        self.set_event_box_drawer = Mock()
        self.set_background_drawer = Mock()

    def use_fast_draw(self, value):
        pass

    def setup_get_time_call(self, x, time):
        self.get_time_calls[x] = time

    def setup_snap(self, time, snap_to):
        self.snaps.append((human_time_to_gregorian(time), human_time_to_gregorian(snap_to)))

    def snap(self, time):
        for (time_inner, snap_to) in self.snaps:
            if time_inner == time:
                return snap_to
        return time

    def snap_selection(self, selection):
        return selection

    def event_at(self, x, y, alt_down=False):
        for (event, rect) in self.events_and_rects:
            if rect.Contains((x, y)):
                return event
        return None

    def event_rect(self, event):
        for (event_inner, rect) in self.events_and_rects:
            if event_inner == event:
                return rect
        raise Exception("Should not get here in tests.")

    def event_with_rect_at(self, x, y, alt_down=False):
        event = self.event_at(x, y)
        if event is None:
            return None
        return (event, self.event_rect(event))

    def get_time(self, x):
        any_time = human_time_to_gregorian("19 Sep 1999")
        return self.get_time_calls.get(x, any_time)

    def balloon_at(self, x, y):
        return None

    def get_hidden_event_count(self):
        return self.hidden_event_count

    def event_is_period(self, event):
        return False

    def draw(self, dc, timeline, view_properties, appearance, fast_draw=False):
        self.draw_dc = dc
        self.draw_timeline = timeline
        self.draw_view_properties = view_properties


class DrawingAreaSpec(UnitTestCase):

    def test_construction_works(self):
        self.timeline_canvas.SetBackgroundColour.assert_called_with(wx.WHITE)
        self.timeline_canvas.SetBackgroundStyle.assert_called_with(wx.BG_STYLE_CUSTOM)
        self.timeline_canvas.set_default_cursor.assert_called()
        self.timeline_canvas.Disable.assert_called()

    def test_get_timeline_returns_given_null_timeline(self):
        self.controller.set_timeline(None)
        self.assertEqual(None, self.controller.get_timeline())

    def test_get_timeline_returns_given_nonnull_timeline(self):
        db = MemoryDB()
        self.controller.set_timeline(db)
        self.assertEqual(db, self.controller.get_timeline())

    def setUp(self):
        self.app = wx.App()  # a stored app is needed to create fonts
        self.timeline_canvas = Mock(TimelineCanvas)
        self.timeline_canvas.GetDividerPosition.return_value = 1
        self.drawing_algorithm = DefaultDrawingAlgorithm()
        self.controller = TimelineCanvasController(
            self.timeline_canvas, drawer=self.drawing_algorithm)
