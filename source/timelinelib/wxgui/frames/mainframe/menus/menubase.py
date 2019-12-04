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


class MenuBase(wx.Menu):

    def __init__(self, parent, event_handlers, shortcuts, requiring_timeline, requiring_visible_timeline_view=[],
                 requiring_writeable_timeline=[]):
        wx.Menu.__init__(self)
        self._parent = parent
        self._event_handlers = event_handlers
        self._shortcuts = shortcuts
        self._requiring_timeline = requiring_timeline
        self._requiring_visible_timeline_view = requiring_visible_timeline_view
        self._requiring_writeable_timeline = requiring_writeable_timeline

    def _bind_event_handlers(self):
        for wxid in self._event_handlers:
            self._parent.Bind(wx.EVT_MENU, self._event_handlers[wxid], id=wxid)

    def _register_shortcuts(self, menu):
        for wxid in self._shortcuts:
            self._parent.shortcut_items[wxid] = menu.FindItemById(wxid)

    def _register_menus_requiring_timeline(self, menu):
        for wxid in self._requiring_timeline:
            self._parent.menu_controller.add_menu_requiring_timeline(menu.FindItemById(wxid))
        for wxid in self._requiring_visible_timeline_view:
            self._parent.menu_controller.add_menu_requiring_visible_timeline_view(menu.FindItemById(wxid))
        for wxid in self._requiring_writeable_timeline:
            self._parent.menu_controller.add_menu_requiring_writable_timeline(menu.FindItemById(wxid))
