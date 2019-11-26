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


import collections
import wx

from timelinelib.wxgui.components.mainpanel import MainPanel
from timelinelib.wxgui.components.statusbaradapter import StatusBarAdapter
from timelinelib.wxgui.frames.mainframe.menus.filemenu import FileMenu
from timelinelib.wxgui.frames.mainframe.menus.editmenu import EditMenu
from timelinelib.wxgui.frames.mainframe.menus.viewmenu import ViewMenu
from timelinelib.wxgui.frames.mainframe.menus.timelinemenu import TimelineMenu
from timelinelib.wxgui.frames.mainframe.menus.navigatemenu import NavigateMenu
from timelinelib.wxgui.frames.mainframe.menus.helpmenu import HelpMenu
# The following imports are used by the shortcut module
from timelinelib.wxgui.frames.mainframe.menus.timelinemenu import ID_CREATE_EVENT, ID_EDIT_EVENT, ID_DUPLICATE_EVENT, ID_SET_CATEGORY_ON_SELECTED, ID_MOVE_EVENT_UP, ID_MOVE_EVENT_DOWN, ID_CREATE_MILESTONE, ID_COMPRESS, ID_MEASURE_DISTANCE, ID_SET_CATEGORY_ON_WITHOUT, ID_EDIT_ERAS, ID_SET_READONLY, ID_UNDO, ID_REDO
from timelinelib.wxgui.frames.mainframe.menus.navigatemenu import ID_FIND_FIRST, ID_FIND_LAST, ID_FIT_ALL, ID_RESTORE_TIME_PERIOD

NONE = 0
CHECKBOX = 1
CHECKED_RB = 2
UNCHECKED_RB = 3
ID_NAVIGATE = wx.NewId() + 100


class GuiCreator:

    def _create_gui(self):
        self.shortcut_items = {}
        from timelinelib.config.shortcut import ShortcutController
        self.shortcut_controller = ShortcutController(self.config, self.shortcut_items)
        self._create_status_bar()
        self._create_main_panel()
        self._create_main_menu_bar()
        self._bind_frame_events()

    def _create_status_bar(self):
        self.CreateStatusBar()
        self.status_bar_adapter = StatusBarAdapter(self.GetStatusBar())

    def _create_main_panel(self):
        self.main_panel = MainPanel(self, self.config, self)

    def _create_main_menu_bar(self):
        main_menu_bar = wx.MenuBar()
        main_menu_bar.Append(FileMenu(self).create(), _("&File"))
        main_menu_bar.Append(EditMenu(self).create(), _("&Edit"))
        main_menu_bar.Append(ViewMenu(self).create(), _("&View"))
        self._timeline_menu = TimelineMenu(self).create()
        main_menu_bar.Append(self._timeline_menu, _("&Timeline"))
        self._navigation_menu_items = []
        self._navigation_functions_by_menu_item_id = {}
        self._navigate_menu = NavigateMenu(self).create()
        main_menu_bar.Append(self._navigate_menu, _("&Navigate"))
        main_menu_bar.Append(HelpMenu(self).create(), _("&Help"))
        self.shortcut_controller.load_config_settings()
        self.SetMenuBar(main_menu_bar)
        self.update_navigation_menu_items()
        self.enable_disable_menus()

    def _bind_frame_events(self):
        self.Bind(wx.EVT_CLOSE, self._window_on_close)

    def _create_menu(self, items_spec):
        menu = wx.Menu()
        for item in items_spec:
            if item is not None:
                self._create_menu_item(menu, item)
            else:
                menu.AppendSeparator()
        return menu

    def _create_menu_item(self, menu, item_spec):
        if isinstance(item_spec, collections.Callable):
            item_spec(menu)
        else:
            item_id, handler, label, checkbox = item_spec
            if label is not None:
                if checkbox == CHECKBOX:
                    item = menu.Append(item_id, label, kind=wx.ITEM_CHECK)
                elif checkbox == CHECKED_RB:
                    item = menu.Append(item_id, label, kind=wx.ITEM_RADIO)
                    item.Check(True)
                elif checkbox == UNCHECKED_RB:
                    item = menu.Append(item_id, label, kind=wx.ITEM_RADIO)
                else:
                    if label is not None:
                        item = menu.Append(item_id, label)
                    else:
                        item = menu.Append(item_id)
            else:
                item = menu.Append(item_id)
            self.shortcut_items[item_id] = menu.FindItemById(item_id)
            self.Bind(wx.EVT_MENU, handler, item)
