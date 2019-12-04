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
            mid.ID_FIND_FIRST: lambda evt: parent.navigate_to_first_event(),
            mid.ID_FIND_LAST: lambda evt: parent.navigate_to_last_event(),
            mid.ID_FIT_ALL: lambda evt: parent.fit_all_events(),
            mid.ID_RESTORE_TIME_PERIOD: lambda evt: parent.restore_time_period(),
        }
        MenuBase.__init__(self, parent, event_handlers, SHORTCUTS, REQUIRING_TIMELINE)
        self._create_menu()
        self._bind_event_handlers()
        self._register_shortcuts()
        self._register_menus_requiring_timeline()

    def _create_menu(self):
        self.AppendSeparator()
        self.Append(mid.ID_FIND_FIRST, _("Find &First Event"))
        self.Append(mid.ID_FIND_LAST, _("Find &Last Event"))
        self.Append(mid.ID_FIT_ALL, _("Fit &All Events"))
        self.AppendSeparator()
        self.Append(mid.ID_RESTORE_TIME_PERIOD, _("Go to previous time period"))
