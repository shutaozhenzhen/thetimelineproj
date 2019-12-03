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


class MenuController:

    def __init__(self):
        self.current_timeline = None
        self._has_timeline = False
        self.menus_requiring_timeline = []
        self.menus_requiring_writable_timeline = []
        self.menus_requiring_visible_timeline_view = []
        self._timeline_menu = None
        self._menu_bar = None

    def set_menu_bar(self, menu_bar):
        self._menu_bar = menu_bar

    def on_timeline_change(self, timeline):
        self.current_timeline = timeline
        self._has_timeline = self.current_timeline is not None

    def add_menu_requiring_writable_timeline(self, menu):
        self.menus_requiring_writable_timeline.append(menu)

    def add_menu_requiring_timeline(self, menu):
        self.menus_requiring_timeline.append(menu)

    def add_menu_requiring_visible_timeline_view(self, menu):
        self.menus_requiring_visible_timeline_view.append(menu)

    def enable_disable_menus(self, timeline_view_visible):
        for menu in self.menus_requiring_writable_timeline:
            self._enable_disable_menu_requiring_writable_timeline(menu)
        for menu in self.menus_requiring_timeline:
            self._enable_disable_menu_requiring_timeline(menu)
        for menu in self.menus_requiring_visible_timeline_view:
            self._enable_disable_menu_requiring_visible_timeline_view(menu, timeline_view_visible)

    def _enable_disable_menu_requiring_writable_timeline(self, menu):
        if not self._has_timeline:
            menu.Enable(False)
        elif self.current_timeline.is_read_only():
            menu.Enable(False)
        else:
            menu.Enable(True)

    def _enable_disable_menu_requiring_timeline(self, menu):
        menu.Enable(self._has_timeline)

    def _enable_disable_menu_requiring_visible_timeline_view(self, menu, timeline_view_visible):
        menu.Enable(self._has_timeline and timeline_view_visible)

    @property
    def timeline_menu(self):
        return self._timeline_menu

    @timeline_menu.setter
    def timeline_menu(self, value):
        self._timeline_menu = value

    def enable(self, menu_id, value):
        mnu = self._menu_bar.FindItemById(menu_id)
        mnu.Enable(value)
