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

from timelinelib.canvas.appearance import Appearance
from timelinelib.canvas.backgrounddrawers.defaultbgdrawer import DefaultBackgroundDrawer
from timelinelib.canvas.drawing import get_drawer
from timelinelib.canvas.drawing.viewproperties import ViewProperties
from timelinelib.canvas.eventboxdrawers.defaulteventboxdrawer import DefaultEventBoxDrawer
from timelinelib.canvas.events import create_timeline_redrawn_event
from timelinelib import DEBUG_ENABLED
from timelinelib.monitoring import Monitoring
from timelinelib.wxgui.components.font import Font


CHOICE_WHOLE_PERIOD = _("Whole Timeline")
CHOICE_VISIBLE_PERIOD = _("Visible Period")
CHOICES = (CHOICE_WHOLE_PERIOD, CHOICE_VISIBLE_PERIOD)


class TimelineCanvasController:

    def __init__(self, view, drawer=None):
        """
        The purpose of the drawer argument is make testing easier. A test can
        mock a drawer and use the mock by sending it in the drawer argument.
        Normally the drawer is collected with the get_drawer() method.
        """
        self.appearance = None
        self.monitoring = Monitoring()
        self.view = view
        self._set_drawing_algorithm(drawer)
        self.timeline = None
        self.set_appearance(Appearance())
        self.set_event_box_drawer(DefaultEventBoxDrawer())
        self.set_background_drawer(DefaultBackgroundDrawer())
        self._fast_draw = False
        self._set_initial_values_to_member_variables()
        self._set_colors_and_styles()
        self._set_search_choises()

    @property
    def scene(self):
        return self.drawing_algorithm.scene

    def get_appearance(self):
        return self.appearance

    def set_appearance(self, appearance):
        if self.appearance is not None:
            self.appearance.unlisten(self._redraw_timeline)
        self.appearance = appearance
        self.appearance.listen_for_any(self._redraw_timeline)
        self.redraw_timeline()

    def set_event_box_drawer(self, event_box_drawer):
        self.drawing_algorithm.set_event_box_drawer(event_box_drawer)

    def set_background_drawer(self, drawer):
        self.drawing_algorithm.set_background_drawer(drawer)

    def get_timeline(self):
        return self.timeline

    def get_view_properties(self):
        return self.view_properties

    def set_timeline(self, timeline):
        """Inform what timeline to draw."""
        self._unregister_timeline(self.timeline)
        if timeline is None:
            self._set_null_timeline()
        else:
            self._set_non_null_timeline(timeline)

    def use_fast_draw(self, value):
        self._fast_draw = value

    def navigate(self, navigation_fn):
        old_period = self.view_properties.displayed_period
        new_period = navigation_fn(old_period)
        MIN_ZOOM_DELTA, min_zoom_error_text = self.time_type.get_min_zoom_delta()
        if new_period.delta() < MIN_ZOOM_DELTA:
            raise ValueError(min_zoom_error_text)
        min_time = self.time_type.get_min_time()
        if min_time is not None and new_period.start_time < min_time:
            raise ValueError(_("Can't scroll more to the left"))
        max_time = self.time_type.get_max_time()
        if max_time is not None and new_period.end_time > max_time:
            raise ValueError(_("Can't scroll more to the right"))
        self.view_properties.displayed_period = new_period
        self.redraw_timeline()

    def _set_null_timeline(self):
        self.timeline = None
        self.time_type = None
        self.view.Disable()

    def _set_non_null_timeline(self, timeline):
        self.timeline = timeline
        self.time_type = timeline.get_time_type()
        self.timeline.register(self._timeline_changed)
        self.view_properties.unlisten(self._redraw_timeline)
        properties_loaded = self._load_view_properties()
        if properties_loaded:
            self.view_properties.listen_for_any(self._redraw_timeline)
            self._redraw_timeline()
            self.view.Enable()
            self.view.SetFocus()

    def _load_view_properties(self):
        properties_loaded = True
        try:
            self.view_properties.clear_db_specific()
            self.timeline.load_view_properties(self.view_properties)
            if self.view_properties.displayed_period is None:
                default_tp = self.time_type.get_default_time_period()
                self.view_properties.displayed_period = default_tp
            self.view_properties.hscroll_amount = 0
        except Exception:
            properties_loaded = False
        return properties_loaded

    def _unregister_timeline(self, timeline):
        if timeline is not None:
            timeline.unregister(self._timeline_changed)

    def get_time_period(self):
        """Return currently displayed time period."""
        if self.timeline is None:
            raise Exception(_("No timeline set"))
        return self.view_properties.displayed_period

    def redraw_timeline(self):
        self._redraw_timeline()

    def window_resized(self):
        self._redraw_timeline()

    def _one_and_only_one_event_selected(self):
        selected_event_ids = self.view_properties.get_selected_event_ids()
        nbr_of_selected_event_ids = len(selected_event_ids)
        return nbr_of_selected_event_ids == 1

    def _get_first_selected_event(self):
        selected_event_ids = self.view_properties.get_selected_event_ids()
        if len(selected_event_ids) > 0:
            event_id = selected_event_ids[0]
            return self.timeline.find_event_with_id(event_id)
        return None

    def get_time(self, x):
        return self.drawing_algorithm.get_time(x)

    def event_with_rect_at(self, x, y, alt_down=False):
        return self.drawing_algorithm.event_with_rect_at(x, y, alt_down)

    def event_at(self, x, y, alt_down=False):
        return self.drawing_algorithm.event_at(x, y, alt_down)

    def set_selected(self, event, is_selected):
        self.view_properties.set_selected(event, is_selected)

    def clear_selected(self):
        self.view_properties.clear_selected()

    def select_all_events(self):
        self.view_properties.select_all_events()

    def is_selected(self, event):
        return self.view_properties.is_selected(event)

    def set_hovered_event(self, event):
        self.view_properties.change_hovered_event(event)

    def get_hovered_event(self):
        return self.view_properties.hovered_event

    def set_selection_rect(self, cursor):
        self.view_properties.set_selection_rect(cursor.rect)
        self._fast_draw = True
        self.redraw_timeline()

    def remove_selection_rect(self):
        self.view_properties.set_selection_rect(None)
        self._fast_draw = True
        self.redraw_timeline()

    def get_hscroll_amount(self):
        return self.view_properties.hscroll_amount

    def set_hscroll_amount(self, amount):
        self.view_properties.hscroll_amount = amount

    def set_period_selection(self, period):
        if period is None:
            self.view_properties.period_selection = None
        else:
            self.view_properties.period_selection = (period.start_time, period.end_time)
        self._redraw_timeline()

    def select_events_in_rect(self, rect):
        self.view_properties.set_all_selected(self.get_events_in_rect(rect))

    def event_has_sticky_balloon(self, event):
        return self.view_properties.event_has_sticky_balloon(event)

    def set_event_sticky_balloon(self, event, is_sticky):
        self.view_properties.set_event_has_sticky_balloon(event, is_sticky)
        self.redraw_timeline()

    def add_highlight(self, event, clear):
        self.view_properties.add_highlight(event, clear)

    def tick_highlights(self):
        self.view_properties.tick_highlights(limit=15)

    def has_higlights(self):
        return self.view_properties.has_higlights()

    def get_period_choices(self):
        return CHOICES
        
    def _set_search_choises(self):
        self._search_choice_functions = {
            CHOICE_WHOLE_PERIOD: self._choose_whole_period,
            CHOICE_VISIBLE_PERIOD: self._choose_visible_period 
        }

    def filter_events(self, events, search_period):
        return self._search_choice_functions[search_period](events)
    
    def _choose_whole_period(self, events):
        return self.view_properties.filter_events(events)
    
    def _choose_visible_period(self, events): 
        events = self.view_properties.filter_events(events)
        period = self.view_properties.displayed_period
        return [e for e in events if period.overlaps(e.get_time_period())]

    def event_is_period(self, event):
        return self.drawing_algorithm.event_is_period(event.get_time_period())

    def snap(self, time):
        return self.drawing_algorithm.snap(time)

    def get_selected_events(self):
        return self.timeline.find_event_with_ids(
            self.view_properties.get_selected_event_ids()
        )

    def get_events_in_rect(self, rect):
        return self.drawing_algorithm.get_events_in_rect(rect)

    def get_hidden_event_count(self):
        return self.drawing_algorithm.get_hidden_event_count()

    def increment_font_size(self):
        self.drawing_algorithm.increment_font_size()
        self._redraw_timeline()

    def decrement_font_size(self):
        self.drawing_algorithm.decrement_font_size()
        self._redraw_timeline()

    def get_closest_overlapping_event(self, event, up):
        return self.drawing_algorithm.get_closest_overlapping_event(event, up=up)

    def balloon_at(self, cursor):
        return self.drawing_algorithm.balloon_at(*cursor.pos)

    def _timeline_changed(self, state_change):
        self._redraw_timeline()

    def _set_initial_values_to_member_variables(self):
        self.timeline = None
        self.view_properties = ViewProperties()
        self.dragscroll_timer_running = False

    def _set_colors_and_styles(self):
        """Define the look and feel of the drawing area."""
        self.view.SetBackgroundColour(wx.WHITE)
        self.view.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.view.set_default_cursor()
        self.view.Disable()

    def _redraw_timeline(self):

        def display_monitor_result(dc):
            (width, height) = self.view.GetSize()
            redraw_time = self.monitoring.timer_elapsed_ms
            self.monitoring.count_timeline_redraw()
            dc.SetTextForeground((255, 0, 0))
            dc.SetFont(Font(12, weight=wx.FONTWEIGHT_BOLD))
            index, is_in_transaction, history = self.timeline.transactions_status()
            dc.DrawText("Undo buffer size: %d" % len(history), width - 300, height - 100)
            dc.DrawText("Undo buffer pos: %d" % index, width - 300, height - 80)
            dc.DrawText("Redraw count: %d" % self.monitoring.timeline_redraw_count, width - 300, height - 60)
            dc.DrawText("Last redraw time: %.3f ms" % redraw_time, width - 300, height - 40)

        def fn_draw(dc):
            self.monitoring.timer_start()
            self.drawing_algorithm.draw(dc, self.timeline, self.view_properties, self.appearance, fast_draw=self._fast_draw)
            self.monitoring.timer_end()
            if DEBUG_ENABLED:
                display_monitor_result(dc)
            self._fast_draw = False

        if self.timeline and self.view_properties.displayed_period:
            self.view_properties.divider_position = (float(self.view.GetDividerPosition()) / 100.0)
            self.view.RedrawSurface(fn_draw)
            self.view.PostEvent(create_timeline_redrawn_event())

    def _set_drawing_algorithm(self, drawer):
        """
        The drawer interface:
            methods:
                draw(d, t, p, a, f)
                set_event_box_drawer(d)
                set_background_drawer(d)
                get_time(x)
                event_with_rect_at(x, y, k)
                event_at(x, y, k)
                event_is_period(p)
                snap(t)
                get_events_in_rect(r)
                get_hidden_event_count()
                increment_font_size()
                decrement_font_size()
                get_closest_overlapping_event(...)
                balloon_at(c)
            properties:
                scene
        """
        if drawer is not None:
            self.drawing_algorithm = drawer
        else:
            self.drawing_algorithm = get_drawer()
