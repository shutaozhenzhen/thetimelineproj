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
import timelinelib.wxgui.frames.mainframe.menus as mid
from timelinelib.wxgui.frames.mainframe.menus.menubase import MenuBase


SHORTCUTS = list()
REQUIRING_TIMELINE = (mid.ID_FIND_FIRST, mid.ID_FIND_LAST, mid.ID_FIT_ALL, mid.ID_RESTORE_TIME_PERIOD)


class NavigateMenu(MenuBase):

    def __init__(self, parent):
        event_handlers = {
            mid.ID_FIND_FIRST: self._find_first,
            mid.ID_FIND_LAST: self._find_last,
            mid.ID_FIT_ALL: lambda evt: parent.fit_all_events(),
            mid.ID_RESTORE_TIME_PERIOD: self._restore_time_period,
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE)

    def create(self):
        menu = self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts(menu)
        self._register_menus_requiring_timeline(menu)
        return menu

    def _create_menu(self):
        menu = wx.Menu()
        menu.AppendSeparator()
        menu.Append(mid.ID_FIND_FIRST, _("Find &First Event"))
        menu.Append(mid.ID_FIND_LAST, _("Find &Last Event"))
        menu.Append(mid.ID_FIT_ALL, _("Fit &All Events"))
        menu.AppendSeparator()
        menu.Append(mid.ID_RESTORE_TIME_PERIOD, _("Go to previous time period"))
        return menu

    def _find_first(self, evt):
        event = self._parent.timeline.get_first_event()
        if event:
            start = event.get_start_time()
            delta = self._parent.main_panel.get_displayed_period_delta()
            end = start + delta
            margin_delta = delta / 24
            self._parent.main_panel.Navigate(lambda tp: tp.update(start, end, -margin_delta))

    def _find_last(self, evt):
        event = self._parent.timeline.get_last_event()
        if event:
            end = event.get_end_time()
            delta = self._parent.main_panel.get_displayed_period_delta()
            try:
                start = end - delta
            except ValueError:
                start = self._parent.timeline.get_time_type().get_min_time()
            margin_delta = delta / 24
            self._parent.main_panel.Navigate(lambda tp: tp.update(start, end, end_delta=margin_delta))

    def _restore_time_period(self, evt):
        if self._parent.prev_time_period:
            self._parent.main_panel.Navigate(lambda tp: self._parent.prev_time_period)
