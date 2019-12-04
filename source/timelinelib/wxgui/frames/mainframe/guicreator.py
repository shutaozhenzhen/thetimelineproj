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

"""
A base class for the mainframe window, responsible for creating the GUI.
"""

import os

import wx

from timelinelib.wxgui.components.mainpanel import MainPanel
from timelinelib.wxgui.components.statusbaradapter import StatusBarAdapter
from timelinelib.wxgui.frames.mainframe.menus.filemenu import FileMenu
from timelinelib.wxgui.frames.mainframe.menus.editmenu import EditMenu
from timelinelib.wxgui.frames.mainframe.menus.viewmenu import ViewMenu
from timelinelib.wxgui.frames.mainframe.menus.timelinemenu import TimelineMenu
from timelinelib.wxgui.frames.mainframe.menus.navigatemenu import NavigateMenu
from timelinelib.wxgui.frames.mainframe.menus.helpmenu import HelpMenu
import timelinelib.wxgui.frames.mainframe.menus as mid

NONE = 0
CHECKBOX = 1
CHECKED_RB = 2
UNCHECKED_RB = 3


class GuiCreator:

    def _create_gui(self):
        self.shortcut_items = {}
        from timelinelib.config.shortcut import ShortcutController
        self.shortcut_controller = ShortcutController(self.config, self.shortcut_items)
        self._create_status_bar()
        self._create_main_panel()
        self._create_main_menu_bar()

    def _create_status_bar(self):
        self.CreateStatusBar()
        self.status_bar_adapter = StatusBarAdapter(self.GetStatusBar())

    def _create_main_panel(self):
        self.main_panel = MainPanel(self, self.config, self)

    def _create_main_menu_bar(self):
        self.mnu_file_open_recent_submenu = wx.Menu()
        self.menu_controller.timeline_menu = TimelineMenu(self, self.main_panel.timeline_panel)
        main_menu_bar = wx.MenuBar()
        main_menu_bar.Append(FileMenu(self).create(), _("&File"))
        main_menu_bar.Append(EditMenu(self).create(), _("&Edit"))
        main_menu_bar.Append(ViewMenu(self).create(), _("&View"))
        self._timeline_menu = self.menu_controller.timeline_menu.create()
        main_menu_bar.Append(self._timeline_menu, _("&Timeline"))
        self._navigation_menu_items = []
        self._navigation_functions_by_menu_item_id = {}
        self._navigate_menu = NavigateMenu(self).create()
        main_menu_bar.Append(self._navigate_menu, _("&Navigate"))
        main_menu_bar.Append(HelpMenu(self).create(), _("&Help"))
        self.shortcut_controller.load_config_settings()
        self.SetMenuBar(main_menu_bar)
        self.menu_controller.set_menu_bar(main_menu_bar)
        self.update_navigation_menu_items()
        self.EnableDisableMenus()

    # Menu creation/destruction
    def _clear_navigation_menu_items(self):
        while self._navigation_menu_items:
            item = self._navigation_menu_items.pop()
            if item in self._navigate_menu.MenuItems:
                self._navigate_menu.Remove(item)
        self._navigation_functions_by_menu_item_id.clear()

    def _create_navigation_menu_items(self):
        item_data = self.timeline.get_time_type().get_navigation_functions()
        pos = 0
        id_offset = self.get_navigation_id_offset()
        for (itemstr, fn) in item_data:
            if itemstr == "SEP":
                item = self._navigate_menu.InsertSeparator(pos)
            else:
                wxid = mid.ID_NAVIGATE + id_offset
                item = self._navigate_menu.Insert(pos, wxid, itemstr)
                self._navigation_functions_by_menu_item_id[item.GetId()] = fn
                self.Bind(wx.EVT_MENU, self._navigation_menu_item_on_click, item)
                self.shortcut_items[wxid] = item
                id_offset += 1
            self._navigation_menu_items.append(item)
            pos += 1

    def get_navigation_id_offset(self):
        id_offset = 0
        if self.timeline.get_time_type().get_name() == "numtime":
            id_offset = 100
        return id_offset

    def _navigation_menu_item_on_click(self, evt):
        self.save_time_period()
        fn = self._navigation_functions_by_menu_item_id[evt.GetId()]
        time_period = self.main_panel.get_time_period()
        fn(self, time_period, self.main_panel.Navigate)

    def _create_recent_menu_items(self):
        self.open_recent_map = {}
        for path in self.config.get_recently_opened():
            self._map_path_to_recent_menu_item(path)

    def _map_path_to_recent_menu_item(self, path):
        name = "%s (%s)" % (
            os.path.basename(path),
            os.path.dirname(os.path.abspath(path)))
        item = self.mnu_file_open_recent_submenu.Append(wx.ID_ANY, name)
        self.open_recent_map[item.GetId()] = path
        self.Bind(wx.EVT_MENU, self._mnu_file_open_recent_item_on_click, item)
